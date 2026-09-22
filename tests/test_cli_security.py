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
    monkeypatch.setenv("PYTRUENAS_SSLVERIFY", "/etc/pki/lab.pem")
    assert args()._sslverify_() == "/etc/pki/lab.pem"
    # An explicit flag still wins over the environment.
    assert args(sslverify=True)._sslverify_() is True
    assert args(insecure=True)._sslverify_() is False
    monkeypatch.delenv("PYTRUENAS_SSLVERIFY")
    (tmp_path / "pytruenas.yaml").write_text("sslverify: false\n")
    assert args()._sslverify_() is False


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
    assert client.sslverify is False
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
