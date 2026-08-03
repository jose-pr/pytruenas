"""``install_sshcreds`` -- keypair provisioning and SSH configuration.

This had no test coverage before step 5 of the hostctl migration, which is
precisely why it needed some *before* being changed: it is the one place that
mutated ``client.shell``, and the rename to ``.ssh_config`` is the migration's
single breaking change.

The middleware side (generate/reuse a keypair, install the public half on
root's ``authorized_keys``) is unchanged by that rename; only where the private
key is *stored afterwards* moves.
"""

from unittest.mock import MagicMock

import pytest

from pytruenas import TrueNASClient

PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\nfake\n-----END PRIVATE KEY-----"
PUBLIC_KEY = "ssh-ed25519 AAAAC3Nz fake"


@pytest.fixture
def client(monkeypatch):
    c = TrueNASClient(None, autologin=False)
    # Stub the derivation itself: PRIVATE_KEY is a placeholder, not a real key,
    # so any genuine parser (cryptography or asyncssh) would reject it. Only
    # this is faked; every middleware call stays real-shaped.
    monkeypatch.setattr("pytruenas.host._public_key", lambda _key: PUBLIC_KEY)
    monkeypatch.setattr(type(c), "api", MagicMock())
    return c


def _wire(client, *, existing_keypair=None, root_sshpubkey=""):
    api = client.api
    api.keychaincredential._get.return_value = existing_keypair
    # The real middleware returns BOTH halves here; returning only the private
    # one would understate what install_sshcreds has to work with, and is what
    # made the asyncssh derivation look unavoidable.
    api.keychaincredential.generate_ssh_key_pair.return_value = {
        "private_key": PRIVATE_KEY,
        "public_key": PUBLIC_KEY,
    }
    api.keychaincredential._upsert.return_value = {
        "attributes": {"private_key": PRIVATE_KEY, "public_key": PUBLIC_KEY}
    }
    api.user._get.return_value = {"username": "root", "sshpubkey": root_sshpubkey}
    return api


# -- middleware side (unchanged by the rename) -----------------------------


def test_generates_a_keypair_when_none_exists(client):
    api = _wire(client)
    client.install_sshcreds()
    api.keychaincredential.generate_ssh_key_pair.assert_called_once()


def test_reuses_an_existing_keypair(client):
    api = _wire(client, existing_keypair={"attributes": {"private_key": PRIVATE_KEY}})
    client.install_sshcreds()
    api.keychaincredential.generate_ssh_key_pair.assert_not_called()


def test_explicit_private_key_is_not_regenerated(client):
    api = _wire(client)
    client.install_sshcreds(private_key=PRIVATE_KEY)
    api.keychaincredential.generate_ssh_key_pair.assert_not_called()


def test_keypair_is_upserted_under_the_given_name(client):
    api = _wire(client)
    client.install_sshcreds(name="custom")
    kwargs = api.keychaincredential._upsert.call_args.kwargs
    assert kwargs["name"] == "custom"
    assert kwargs["type"] == "SSH_KEY_PAIR"
    assert kwargs["attributes"]["public_key"] == PUBLIC_KEY


def test_default_name_is_pytruenas(client):
    api = _wire(client)
    client.install_sshcreds()
    assert api.keychaincredential._upsert.call_args.kwargs["name"] == "pytruenas"


def test_public_key_is_appended_to_root_authorized_keys(client):
    api = _wire(client, root_sshpubkey="ssh-rsa EXISTING other@host")
    client.install_sshcreds()
    written = api.user._upsert.call_args.kwargs["sshpubkey"]
    assert "ssh-rsa EXISTING other@host" in written
    assert PUBLIC_KEY in written


def test_public_key_is_not_duplicated(client):
    api = _wire(client, root_sshpubkey=PUBLIC_KEY)
    client.install_sshcreds()
    api.user._upsert.assert_not_called()


def test_handles_root_with_no_sshpubkey(client):
    api = _wire(client, root_sshpubkey=None)
    client.install_sshcreds()
    assert api.user._upsert.call_args.kwargs["sshpubkey"] == PUBLIC_KEY


# -- the optional 'ssh' extra is not required to provision -----------------


@pytest.fixture
def no_derivation(monkeypatch):
    """A client that cannot derive a public key at all.

    Stubs `_public_key` rather than just the asyncssh import: derivation now
    prefers `cryptography` and only falls back to asyncssh, so blocking one
    library would leave the other doing the work and the test would pass
    without proving anything.
    """
    c = TrueNASClient(None, autologin=False)

    def _boom(_private_key):
        raise ImportError("SSH/SFTP support requires the 'ssh' extra")

    monkeypatch.setattr("pytruenas.host._public_key", _boom)
    monkeypatch.setattr(type(c), "api", MagicMock())
    return c


def test_generating_a_keypair_needs_no_derivation(no_derivation):
    # Provisioning talks to the middleware and opens no SSH connection, so
    # requiring the extra here was a dependency on a library doing nothing.
    api = _wire(no_derivation)
    no_derivation.install_sshcreds()
    assert (
        api.keychaincredential._upsert.call_args.kwargs["attributes"]["public_key"]
        == PUBLIC_KEY
    )


def test_reusing_a_keypair_needs_no_derivation(no_derivation):
    # The stored credential carries the public half alongside the private one.
    api = _wire(
        no_derivation,
        existing_keypair={
            "attributes": {"private_key": PRIVATE_KEY, "public_key": PUBLIC_KEY}
        },
    )
    no_derivation.install_sshcreds()
    assert PUBLIC_KEY in api.user._upsert.call_args.kwargs["sshpubkey"]


def test_a_supplied_private_key_still_needs_the_extra(no_derivation):
    # The one genuine use: deriving the public half from a key the host does
    # not know. It fails loudly, pointing at the extra.
    _wire(no_derivation)
    with pytest.raises(ImportError, match="ssh"):
        no_derivation.install_sshcreds(private_key=PRIVATE_KEY)


def test_a_blank_stored_public_key_falls_back_to_deriving(no_derivation):
    # An empty/whitespace public_key is treated as absent rather than written
    # through as a blank authorized_keys line.
    _wire(
        no_derivation,
        existing_keypair={
            "attributes": {"private_key": PRIVATE_KEY, "public_key": " "}
        },
    )
    with pytest.raises(ImportError):
        no_derivation.install_sshcreds()


def test_root_is_selected_by_field_name_not_by_id(client):
    # `("username",)` is a one-item SEQUENCE, not the bare string "username".
    # DbAction.execute reads a bare `str` selector as a record *id*, so the
    # string form would ask the middleware to update the user whose id is
    # "username" rather than the one whose username is "root".
    api = _wire(client, root_sshpubkey="ssh-rsa EXISTING other@host")
    client.install_sshcreds()
    selector = api.user._upsert.call_args.args[0]
    assert selector == ("username",)
    assert not isinstance(selector, str)


# -- deriving a public key (cryptography, with asyncssh as the fallback) ----


def test_derivation_prefers_cryptography_over_asyncssh(monkeypatch):
    # asyncssh depends on cryptography, so the `ssh` extra already brings it --
    # and it is far lighter than a whole SSH protocol stack for pure key math.
    ser = pytest.importorskip("cryptography.hazmat.primitives.serialization")
    ed25519 = pytest.importorskip("cryptography.hazmat.primitives.asymmetric.ed25519")
    import pytruenas.host as host

    def _fail():
        raise AssertionError("asyncssh must not be used when cryptography works")

    monkeypatch.setattr(host, "_asyncssh", _fail)

    key = ed25519.Ed25519PrivateKey.generate()
    expected = (
        key.public_key()
        .public_bytes(ser.Encoding.OpenSSH, ser.PublicFormat.OpenSSH)
        .decode()
    )
    for fmt in (ser.PrivateFormat.OpenSSH, ser.PrivateFormat.PKCS8):
        pem = key.private_bytes(ser.Encoding.PEM, fmt, ser.NoEncryption()).decode()
        # Both encodings TrueNAS may hand back need a different loader.
        assert host._public_key(pem) == expected


def test_derivation_reports_an_unparseable_key(monkeypatch):
    pytest.importorskip("cryptography")
    import pytruenas.host as host

    with pytest.raises(ValueError, match="could not parse"):
        host._public_key("-----BEGIN PRIVATE KEY-----\nnot-a-key\n-----END-----")


def test_derivation_falls_back_to_asyncssh(monkeypatch):
    # An environment with asyncssh but no cryptography is unlikely (asyncssh
    # requires it) -- but the fallback must still work if it happens.
    import builtins

    import pytruenas.host as host

    real_import = builtins.__import__

    def _no_cryptography(name, *args, **kwargs):
        if name.startswith("cryptography"):
            raise ImportError("no cryptography")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", _no_cryptography)

    key = MagicMock()
    key.export_public_key.return_value = (PUBLIC_KEY + "\n").encode()
    fake_asyncssh = MagicMock()
    fake_asyncssh.import_private_key.return_value = key
    monkeypatch.setattr(host, "_asyncssh", lambda: fake_asyncssh)

    assert host._public_key(PRIVATE_KEY) == PUBLIC_KEY


# -- where the credential lands (this is what step 5 changes) --------------


def test_returns_the_installed_key(client):
    """The local fixture has no SSH leg to wire -- but still provisions."""
    _wire(client)
    assert client.install_sshcreds() == PRIVATE_KEY


def test_a_local_target_gets_no_ssh_leg(client):
    """There is no host to SSH *to*, and none is needed: commands run here.

    The keypair is still provisioned and installed on root's authorized_keys,
    so other machines can use it -- there is just no leg to attach it to.
    """
    _wire(client)
    client.install_sshcreds()
    assert client._config.is_local
    assert client._config.ssh is None


def test_a_remote_target_gets_the_key_wired_in(monkeypatch):
    """It lands on a real `SshConfig.client_keys` field.

    Not the `"client_keys|root"` string the pre-hostctl client packed into a
    username.
    """
    remote = TrueNASClient("wss://nas", autologin=False)
    monkeypatch.setattr("pytruenas.host._public_key", lambda _key: PUBLIC_KEY)
    monkeypatch.setattr(type(remote), "api", MagicMock())
    _wire(remote)

    assert remote.install_sshcreds() == PRIVATE_KEY
    assert remote._config.ssh.client_keys == [PRIVATE_KEY.encode()]


def test_does_not_overwrite_explicit_credentials(monkeypatch):
    """A caller who configured their own SSH auth keeps it."""
    from hostctl.host import SshConfig

    remote = TrueNASClient("wss://nas", autologin=False)
    monkeypatch.setattr("pytruenas.host._public_key", lambda _key: PUBLIC_KEY)
    monkeypatch.setattr(type(remote), "api", MagicMock())
    _wire(remote)

    remote._config.ssh = SshConfig(host="nas", password="hunter2")
    remote.install_sshcreds()
    assert remote._config.ssh.password == "hunter2"
    assert remote._config.ssh.client_keys is None
