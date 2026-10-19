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
from pytruenas.fs import LocalPath


def _posix_shell():
    for sh in ("/bin/sh", "/bin/bash"):
        if os.path.exists(sh):
            return sh
    return None


def _has_posix_shell():
    return _posix_shell() is not None


def test_local_construction_no_network():
    c = TrueNASClient(None, autologin=False)
    assert c._config.is_local
    assert c._target.scheme == "ws+unix"
    assert isinstance(c._config.credentials, LocalAuth)


def test_local_target_keeps_uri_syntax_in_the_socket_path():
    c = TrueNASClient("ws+unix:///run/a%3Fb/x.sock", autologin=False)
    assert c._target.path == "/run/a?b/x.sock"
    assert c._target.uri == "ws+unix:///run/a%3Fb/x.sock"


def test_creds_wired_from_target():
    c = TrueNASClient(None, credentials=("root", "secret"), autologin=False)
    assert isinstance(c._config.credentials, BasicAuth)


def test_api_key_creds():
    c = TrueNASClient(None, credentials="1-" + "a" * 64, autologin=False)
    assert isinstance(c._config.credentials, ApiKeyAuth)


def test_path_selection_local_vs_remote():
    """A local target gets real local paths; a remote one the websocket leg.

    Paths come back wrapped in hostctl's `CompositePosixPath` -- that wrapper
    is what lets a path fail over to the next provider -- so the provider list
    is what identifies the leg, not the returned class.
    """
    local = TrueNASClient(None, autologin=False)
    assert [p.name for p in local.path_providers] == ["local"]
    assert local.path("/etc/hosts").as_posix() == "/etc/hosts"

    remote = TrueNASClient("wss://nas", credentials="1-" + "a" * 64, autologin=False)
    assert [p.name for p in remote.path_providers] == ["tnasws"]


@pytest.mark.skipif(
    not _has_posix_shell(), reason="needs a POSIX shell (client.run execs via one)"
)
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

    def fake_request(method, url, headers=None, verify=None, files=None, timeout=None):
        captured.update(method=method, url=url, headers=headers, verify=verify)
        captured["timeout"] = timeout
        return MagicMock(json=lambda: {"job_id": 7})

    monkeypatch.setattr(
        "requests.Session.request", lambda self, *a, **k: fake_request(*a, **k)
    )
    # a pre-supplied token avoids the auth.generate_token API round trip
    c.api = MagicMock()
    c.upload(b"data", "config.upload", token="tok", wait=False)
    assert "/_upload" in captured["url"]
    assert captured["headers"]["Authorization"] == "Token tok"
    # Always passed per request -- see TrueNASClient._http_verify.
    assert captured["verify"] is True
    # A silent side channel blocked for good.
    assert captured["method"] == "POST" and all(captured["timeout"])


def test_upload_reports_a_refused_upload(monkeypatch):
    """A refused upload answers with an HTTP error and an HTML body, which
    surfaced as a bare KeyError naming neither the status nor the reason."""
    import requests

    from pytruenas.connection import ClientException

    c = TrueNASClient(None, autologin=False)
    c.api = MagicMock()

    resp = MagicMock(status_code=413, text="<html>Payload Too Large</html>")
    resp.raise_for_status.side_effect = requests.HTTPError("413 Client Error")
    monkeypatch.setattr("requests.Session.request", lambda self, *a, **k: resp)
    with pytest.raises(requests.HTTPError):
        c.upload(b"data", "config.upload", token="tok", wait=False)

    ok = MagicMock(status_code=200, text="not json")
    ok.raise_for_status.return_value = None
    ok.json.side_effect = ValueError("no json")
    monkeypatch.setattr("requests.Session.request", lambda self, *a, **k: ok)
    with pytest.raises(ClientException, match="no job id"):
        c.upload(b"data", "config.upload", token="tok", wait=False)
