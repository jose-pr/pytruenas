"""TrueNASClient construction + local paths (no network / no server).

Local targets skip the HTTP scheme-probe, so ``TrueNASClient(None)`` constructs
offline. Remote construction is exercised with the probe mocked.
"""

import os
import subprocess
from unittest.mock import MagicMock, patch

import pytest

from pytruenas import TrueNASClient
from pytruenas.auth import ApiKeyAuth, BasicAuth, LocalAuth
from pytruenas.fs import LocalPath, TruenasPath


def _posix_shell():
    for sh in ("/bin/sh", "/bin/bash"):
        if os.path.exists(sh):
            return sh
    return None


def _has_posix_shell():
    return _posix_shell() is not None


def test_local_construction_no_network():
    c = TrueNASClient(None, autologin=False)
    assert c._api.is_local
    assert c._api.scheme == "ws"
    assert isinstance(c._creds, LocalAuth)


def test_creds_wired_from_target():
    c = TrueNASClient(None, ("root", "secret"), autologin=False)
    assert isinstance(c._creds, BasicAuth)


def test_api_key_creds():
    c = TrueNASClient(None, "1-" + "a" * 64, autologin=False)
    assert isinstance(c._creds, ApiKeyAuth)


def test_path_selection_local_vs_remote():
    local = TrueNASClient(None, autologin=False)
    assert isinstance(local.path("/etc/hosts"), LocalPath)

    with patch.object(TrueNASClient, "_openwss", return_value=MagicMock()):
        with patch("requests.get") as rget:
            rget.return_value = MagicMock(url="https://nas/api/current", status_code=400)
            remote = TrueNASClient("nas.example.com", "1-" + "a" * 64,
                                   autologin=False, sslverify=False)
    assert isinstance(remote.path("/mnt/tank/x"), TruenasPath)


@pytest.mark.skipif(not _has_posix_shell(), reason="needs a POSIX shell (client.run execs via one)")
def test_run_local_subprocess():
    c = TrueNASClient(None, autologin=False)
    result = c.run("exit 0", executable=_posix_shell(), check=False)
    assert isinstance(result, subprocess.CompletedProcess)
    assert result.returncode == 0


def test_api_namespace_lazy():
    c = TrueNASClient(None, autologin=False)
    # .api is a cached Namespace; accessing an attribute builds a dotted method
    # name without any call.
    assert str(c.api.user) == "user"
    assert str(c.api.pool.dataset) == "pool.dataset"


def test_upload_builds_upload_target(monkeypatch):
    c = TrueNASClient(None, autologin=False)
    captured = {}

    def fake_post(url, headers=None, verify=None, files=None):
        captured["url"] = url
        captured["headers"] = headers
        return MagicMock(json=lambda: {"job_id": 7})

    monkeypatch.setattr("requests.post", fake_post)
    # a pre-supplied token avoids the auth.generate_token API round trip
    c.api = MagicMock()
    c.api.core.job_wait.return_value = None
    c.upload(b"data", "config.upload", token="tok", wait=False)
    assert "/_upload" in captured["url"]
    assert captured["headers"]["Authorization"] == "Token tok"
