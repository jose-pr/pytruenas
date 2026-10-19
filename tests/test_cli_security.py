"""What the CLI does about TLS and credentials.

It verified nothing by default -- `pytruenas call ... nas` sent its API key
over a connection whose certificate it never checked -- and had no credential
source but the target string, so a remote target with none connected
unauthenticated and every call failed on the far side.
"""

import os
import subprocess
import sys

import pytest

from pytruenas.utils.cmd import PyTrueNASArgs


@pytest.fixture
def args(monkeypatch, tmp_path):
    for name in ("SSLVERIFY", "INSECURE", "CA_BUNDLE"):
        monkeypatch.delenv("PYTRUENAS_" + name, raising=False)
    monkeypatch.delenv("PYTRUENAS_CREDENTIALS", raising=False)
    # `_config` names a file through the variable; until then, no config.
    monkeypatch.setenv("APPDATA", str(tmp_path / "appdata"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))
    monkeypatch.delenv("PYTRUENAS_CONFIG", raising=False)

    def build(**fields):
        parsed = PyTrueNASArgs()
        parsed.insecure = fields.get("insecure", False)
        parsed.ca_bundle = fields.get("ca_bundle")
        return parsed

    return build


@pytest.fixture
def bundle(tmp_path):
    path = tmp_path / "lab.pem"
    path.write_bytes(b"")
    return str(path)


def _config(tmp_path, text):
    """A YAML config file named by $PYTRUENAS_CONFIG (restored by `args`)."""
    pytest.importorskip("yaml")
    path = tmp_path / "pytruenas.cfg"
    path.write_text("#!yaml\n" + text)
    os.environ["PYTRUENAS_CONFIG"] = str(path)


def test_tls_is_verified_by_default(args):
    assert args()._verify_() is True


def test_each_layer_can_turn_verification_off(args, monkeypatch, tmp_path):
    assert args(insecure=True)._verify_() is False
    monkeypatch.setenv("PYTRUENAS_INSECURE", "1")
    assert args()._verify_() is False
    monkeypatch.delenv("PYTRUENAS_INSECURE")
    _config(tmp_path, "insecure: true")
    assert args()._verify_() is False


def test_each_layer_can_name_a_bundle(args, monkeypatch, tmp_path, bundle):
    assert args(ca_bundle=bundle)._verify_() == bundle
    monkeypatch.setenv("PYTRUENAS_CA_BUNDLE", bundle)
    assert args()._verify_() == bundle
    monkeypatch.delenv("PYTRUENAS_CA_BUNDLE")
    _config(tmp_path, f"ca_bundle: '{bundle}'")
    assert args()._verify_() == bundle


def test_a_flag_beats_the_environment_and_the_environment_the_config(
    args, monkeypatch, tmp_path, bundle
):
    _config(tmp_path, "insecure: true")
    monkeypatch.setenv("PYTRUENAS_CA_BUNDLE", bundle)
    assert args()._verify_() == bundle
    assert args(insecure=True)._verify_() is False


@pytest.mark.parametrize("value", ["", "   ", "0", "false"])
def test_an_empty_or_false_insecure_leaves_verification_on(args, monkeypatch, value):
    """`PYTRUENAS_SSLVERIFY=` (empty) turned verification off."""
    monkeypatch.setenv("PYTRUENAS_INSECURE", value)
    monkeypatch.setenv("PYTRUENAS_CA_BUNDLE", "")
    assert args()._verify_() is True


def test_a_bundle_that_does_not_exist_is_refused(args, monkeypatch):
    monkeypatch.setenv("PYTRUENAS_CA_BUNDLE", "/no/such/bundle.pem")
    with pytest.raises(ValueError, match="PYTRUENAS_CA_BUNDLE"):
        args()._verify_()
    with pytest.raises(ValueError, match="--ca-bundle"):
        args(ca_bundle="/no/such/bundle.pem")._verify_()


@pytest.mark.parametrize("value", ["0", "maybe", "[]"])
def test_a_config_insecure_that_is_not_a_boolean_is_refused(args, tmp_path, value):
    _config(tmp_path, "insecure: " + value)
    with pytest.raises(ValueError, match="insecure in"):
        args()._verify_()


def test_the_removed_settings_say_what_replaced_them(args, monkeypatch, tmp_path):
    monkeypatch.setenv("PYTRUENAS_SSLVERIFY", "false")
    with pytest.raises(ValueError, match="PYTRUENAS_INSECURE"):
        args()._verify_()
    monkeypatch.delenv("PYTRUENAS_SSLVERIFY")
    _config(tmp_path, "sslverify: false")
    with pytest.raises(ValueError, match="insecure and ca_bundle"):
        args()._verify_()


def test_credentials_come_from_the_environment_or_config(args, monkeypatch, tmp_path):
    pytest.importorskip("yaml")
    from pytruenas.auth import APIKeyAuth, BasicAuth

    assert args()._credentials_() is None
    _config(tmp_path, "credentials: root:hunter2")
    assert isinstance(args()._credentials_(), BasicAuth)
    monkeypatch.setenv("PYTRUENAS_CREDENTIALS", "1-" + "k" * 64)
    assert isinstance(args()._credentials_(), APIKeyAuth)  # env wins


def test_the_client_gets_them(args, monkeypatch):
    monkeypatch.setenv("PYTRUENAS_CREDENTIALS", "1-" + "k" * 64)
    client = args(insecure=True)._client_("nas")
    assert client.config.verify is False
    assert client.config.credentials.api_key.startswith("1-")


def test_a_target_that_carries_credentials_keeps_them(args, monkeypatch):
    """Passing both raises, so the fallback must stay out of the way."""
    monkeypatch.setenv("PYTRUENAS_CREDENTIALS", "1-" + "k" * 64)
    client = args()._client_("wss://root:hunter2@nas")
    assert client.config.credentials.password == "hunter2"


def test_the_flags_are_registered():
    """-k is curl's spelling; --ca-bundle names the trust; --sslverify is gone."""
    out = subprocess.run(
        [sys.executable, "-m", "pytruenas", "call", "--help"],
        capture_output=True,
        text=True,
    ).stdout
    assert "--insecure, -k" in out
    assert "--ca-bundle FILE" in out
    assert "sslverify" not in out
