"""Opening the web shell: every way it can fail closes the websocket it opened."""

import types

import pytest
from hostctl import OperationNotStartedError

from pytruenas import TrueNASClient
from pytruenas.connection import ClientException
import pytruenas.webshell as webshell
from pytruenas.webshell import WebShellSession


def _connect(monkeypatch, frames, generate_token=lambda *a, **k: "tok"):
    opened = []

    class _WS:
        def __init__(self, sslopt=None):
            self.frames = list(frames)
            self.closed = False
            opened.append(self)

        def connect(self, uri, **options):
            pass

        def send(self, payload):
            pass

        def settimeout(self, timeout):
            pass

        def recv(self):
            if self.frames:
                return self.frames.pop(0)
            raise TimeoutError

        def close(self):
            self.closed = True

    monkeypatch.setattr(webshell._websocket, "WebSocket", _WS)
    client = TrueNASClient("wss://nas", autologin=False)
    api = types.SimpleNamespace(
        auth=types.SimpleNamespace(generate_token=generate_token)
    )
    monkeypatch.setattr(type(client), "api", property(lambda self: api))
    session = WebShellSession(client)
    try:
        session.connect()
    except Exception as exc:
        assert len(opened) == 1
        return session, opened[0], exc
    assert len(opened) == 1
    return session, opened[0], None


def test_a_connected_session_is_kept(monkeypatch):
    session, ws, error = _connect(
        monkeypatch, ['{"msg": "connected", "id": "shell-1"}']
    )
    assert error is None and session.shell_id == "shell-1" and not ws.closed


@pytest.mark.parametrize(
    "frame, reason",
    [
        ('{"msg": "failed", "error": {"reason": "bad token"}}', "bad token"),
        # A refusal whose error is a string raised AttributeError.
        ('{"msg": "failed", "error": "bad token"}', "bad token"),
    ],
)
def test_a_refused_token_closes_the_websocket(monkeypatch, frame, reason):
    _, ws, error = _connect(monkeypatch, [frame])
    assert isinstance(error, OperationNotStartedError) and reason in str(error)
    assert ws.closed


def test_a_token_that_cannot_be_minted_closes_the_websocket(monkeypatch):
    """The opened websocket leaked: two per attempt, measured."""

    def refuse(*args, **kwargs):
        raise ClientException("denied")

    _, ws, error = _connect(monkeypatch, [], generate_token=refuse)
    assert isinstance(error, ClientException) and ws.closed


def test_silence_after_the_token_is_a_decline(monkeypatch):
    """It returned a session with no shell behind it."""
    _, ws, error = _connect(monkeypatch, [])
    assert isinstance(error, OperationNotStartedError)
    assert "no 'connected'" in str(error) and ws.closed
