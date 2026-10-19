"""What the CLI does about TLS and credentials.

It verified nothing by default -- `pytruenas call ... nas` sent its API key
over a connection whose certificate it never checked -- and had no credential
source but the target string, so a remote target with none connected
unauthenticated and every call failed on the far side.
"""

import subprocess
import sys

import pytest

from pytruenas.utils.cmd import PyTrueNASArgs


@pytest.fixture
def args(monkeypatch, tmp_path):
    monkeypatch.delenv("PYTRUENAS_SSLVERIFY", raising=False)
    monkeypatch.delenv("TN_CREDS", raising=False)
    monkeypatch.chdir(tmp_path)  # no stray ./pytruenas.yaml

    def build(**fields):
        parsed = PyTrueNASArgs()
        parsed.sslverify = fields.get("sslverify")
        parsed.insecure = fields.get("insecure", False)
        return parsed

    return build


def test_tls_is_verified_by_default(args):
    assert args()._sslverify_() is True


@pytest.mark.parametrize(
    "fields",
    [{"insecure": True}, {"sslverify": False}, {"sslverify": False, "insecure": True}],
)
def test_verification_can_be_turned_off(args, fields):
    assert args(**fields)._sslverify_() is False


def test_the_environment_and_config_are_honoured(args, monkeypatch, tmp_path):
    monkeypatch.setenv("PYTRUENAS_SSLVERIFY", "false")
    pytest.importorskip("yaml")  # only the config-file half needs the extra
    assert args()._sslverify_() is False
    # A path is a CA bundle, as it is for TrueNASClient(sslverify=...).
    bundle = tmp_path / "lab.pem"
    bundle.write_bytes(b"")
    monkeypatch.setenv("PYTRUENAS_SSLVERIFY", str(bundle))
    assert args()._sslverify_() == str(bundle)
    # An explicit flag still wins over the environment.
    assert args(sslverify=True)._sslverify_() is True
    assert args(insecure=True)._sslverify_() is False
    monkeypatch.delenv("PYTRUENAS_SSLVERIFY")
    (tmp_path / "pytruenas.yaml").write_text("sslverify: false\n")
    assert args()._sslverify_() is False


@pytest.mark.parametrize("value", ["", "   "])
def test_an_empty_environment_value_is_unset_not_off(args, monkeypatch, value):
    """`PYTRUENAS_SSLVERIFY=` turned verification off."""
    monkeypatch.setenv("PYTRUENAS_SSLVERIFY", value)
    assert args()._sslverify_() is True


@pytest.mark.parametrize("value", ["maybe", "/no/such/bundle.pem"])
def test_a_value_that_is_neither_a_boolean_nor_a_bundle_is_refused(
    args, monkeypatch, value
):
    """It was taken as a CA bundle path, which verifies nothing."""
    monkeypatch.setenv("PYTRUENAS_SSLVERIFY", value)
    with pytest.raises(ValueError, match="PYTRUENAS_SSLVERIFY"):
        args()._sslverify_()


@pytest.mark.parametrize("value", ["0", "''", "[]"])
def test_a_config_value_that_is_not_a_boolean_or_path_is_refused(args, tmp_path, value):
    pytest.importorskip("yaml")
    (tmp_path / "pytruenas.yaml").write_text("sslverify: " + value)
    with pytest.raises(ValueError, match="sslverify in"):
        args()._sslverify_()


def test_credentials_come_from_the_environment_or_config(args, monkeypatch, tmp_path):
    pytest.importorskip("yaml")
    from pytruenas.auth import ApiKeyAuth, BasicAuth

    assert args()._credentials_() is None
    (tmp_path / "pytruenas.yaml").write_text("credentials: root:hunter2\n")
    assert isinstance(args()._credentials_(), BasicAuth)
    monkeypatch.setenv("TN_CREDS", "1-" + "k" * 64)
    assert isinstance(args()._credentials_(), ApiKeyAuth)  # env wins


def test_the_client_gets_them(args, monkeypatch):
    monkeypatch.setenv("TN_CREDS", "1-" + "k" * 64)
    client = args(insecure=True)._client_("nas")
    assert client.config.verify is False
    assert client.config.credentials.api_key.startswith("1-")


def test_a_target_that_carries_credentials_keeps_them(args, monkeypatch):
    """Passing both raises, so the fallback must stay out of the way."""
    monkeypatch.setenv("TN_CREDS", "1-" + "k" * 64)
    client = args()._client_("wss://root:hunter2@nas")
    assert client.config.credentials.password == "hunter2"


def test_the_flags_are_registered():
    """-k is curl's spelling, and --sslverify/--no-sslverify is the pair."""
    out = subprocess.run(
        [sys.executable, "-m", "pytruenas", "call", "--help"],
        capture_output=True,
        text=True,
    ).stdout
    assert "--insecure, -k" in out
    assert "--sslverify, --no-sslverify" in out
