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

pytest.importorskip("asyncssh")

from pytruenas import TrueNASClient  # noqa: E402

PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\nfake\n-----END PRIVATE KEY-----"
PUBLIC_KEY = "ssh-ed25519 AAAAC3Nz fake"


@pytest.fixture
def client(monkeypatch):
    c = TrueNASClient(None, autologin=False)
    # Keep asyncssh out of it: importing a fake PEM would fail. Only the
    # public-key derivation is stubbed; every middleware call stays real-shaped.
    key = MagicMock()
    key.export_public_key.return_value = (PUBLIC_KEY + "\n").encode()
    fake_asyncssh = MagicMock()
    fake_asyncssh.import_private_key.return_value = key
    monkeypatch.setattr("pytruenas.host._asyncssh", lambda: fake_asyncssh)
    monkeypatch.setattr(type(c), "api", MagicMock())
    return c


def _wire(client, *, existing_keypair=None, root_sshpubkey=""):
    api = client.api
    api.keychaincredential._get.return_value = existing_keypair
    api.keychaincredential.generate_ssh_key_pair.return_value = {
        "private_key": PRIVATE_KEY
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
    key = MagicMock()
    key.export_public_key.return_value = (PUBLIC_KEY + "\n").encode()
    fake_asyncssh = MagicMock()
    fake_asyncssh.import_private_key.return_value = key
    monkeypatch.setattr("pytruenas.host._asyncssh", lambda: fake_asyncssh)
    monkeypatch.setattr(type(remote), "api", MagicMock())
    _wire(remote)

    assert remote.install_sshcreds() == PRIVATE_KEY
    assert remote._config.ssh.client_keys == [PRIVATE_KEY.encode()]


def test_does_not_overwrite_explicit_credentials(monkeypatch):
    """A caller who configured their own SSH auth keeps it."""
    from hostctl.host import SshConfig

    remote = TrueNASClient("wss://nas", autologin=False)
    key = MagicMock()
    key.export_public_key.return_value = (PUBLIC_KEY + "\n").encode()
    fake_asyncssh = MagicMock()
    fake_asyncssh.import_private_key.return_value = key
    monkeypatch.setattr("pytruenas.host._asyncssh", lambda: fake_asyncssh)
    monkeypatch.setattr(type(remote), "api", MagicMock())
    _wire(remote)

    remote._config.ssh = SshConfig(host="nas", password="hunter2")
    remote.install_sshcreds()
    assert remote._config.ssh.password == "hunter2"
    assert remote._config.ssh.client_keys is None
