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
    monkeypatch.setattr("pytruenas.client._asyncssh", lambda: fake_asyncssh)
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


def test_configures_ssh_credentials_for_later_use(client):
    """After installing, the client must be able to authenticate over SSH.

    Deliberately asserted through the *behaviour* rather than the storage
    layout, so this test survives the ``.shell`` -> ``.ssh_config`` rename and
    documents the contract that actually matters.
    """
    _wire(client)
    client.install_sshcreds()
    assert client._ssh_private_key() == PRIVATE_KEY


def test_does_not_overwrite_explicit_credentials(client):
    """A caller who configured their own SSH auth keeps it."""
    _wire(client)
    client.shell = client.shell._replace(username="root", password="hunter2")
    client.install_sshcreds()
    assert client._ssh_private_key() != PRIVATE_KEY
