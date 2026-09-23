"""Resources a client owns, and how far a credential's reach extends.

The theme is scope: a connection nobody closed, an SFTP backend rebuilt per
call, a token usable from anywhere, credentials on a plaintext socket.
"""

import gc
import logging
import threading
import weakref

import pytest

from pytruenas import TrueNASClient
from pytruenas.auth import ApiKeyAuth, BasicAuth, Credentials, LocalAuth


class _Conn:
    """Enough of a connection for the host's lifecycle handling."""

    closed = 0

    def __init__(self):
        self._closed = threading.Event()

    def close(self):
        type(self).closed += 1
        self._closed.set()


@pytest.fixture(autouse=True)
def _reset():
    _Conn.closed = 0


def _host(**kwargs):
    """A host whose connections are `_Conn`s.

    The attribute is set directly, not through monkeypatch: monkeypatch keeps a
    reference to the object it patched until teardown, which would keep the
    host alive and defeat the collection tests below.
    """
    host = TrueNASClient("wss://nas", autologin=False, **kwargs)
    host._openwss = _Conn  # type: ignore[method-assign]
    return host


# -- the connection -------------------------------------------------------


def test_a_dropped_client_closes_its_connection():
    """Without this the websocket and its reader thread stayed alive for the
    life of the process."""
    host = _host()
    host.conn  # open it
    reference = weakref.ref(host)
    del host
    gc.collect()
    assert reference() is None
    assert _Conn.closed == 1


def test_closing_explicitly_does_not_double_close():
    host = _host()
    host.conn
    host.close()
    assert _Conn.closed == 1
    del host
    gc.collect()
    assert _Conn.closed == 1  # the finalizer was detached


def test_reconnecting_tracks_the_new_connection():
    host = _host()
    first = host.conn
    first.close()  # the server dropped it
    second = host.conn
    assert second is not first
    del host
    gc.collect()
    # The first was closed above, the second by the finalizer.
    assert _Conn.closed == 2


# -- the SFTP backend -----------------------------------------------------


def test_the_sftp_backend_is_built_once_per_client():
    """pathlib_next keys its connection cache on the backend OBJECT, so a fresh
    backend per call never hit it: five readlink() calls opened five SSH
    sessions and closed none (measured live)."""
    pytest.importorskip("asyncssh")
    from pytruenas.fs.truenas import _sftp_backend

    host = TrueNASClient("wss://nas", shell="ssh://root@nas", autologin=False)
    ssh = host.config.ssh
    first = _sftp_backend(host, ssh)
    assert first is not None
    assert _sftp_backend(host, ssh) is first
    # A different client gets its own.
    other = TrueNASClient("wss://nas2", shell="ssh://root@nas2", autologin=False)
    assert _sftp_backend(other, other.config.ssh) is not first


def test_changing_the_ssh_settings_invalidates_the_backend():
    pytest.importorskip("asyncssh")
    from pytruenas.fs.truenas import _sftp_backend

    host = TrueNASClient("wss://nas", shell="ssh://root@nas", autologin=False)
    first = _sftp_backend(host, host.config.ssh)
    host.config.ssh.client_keys = [b"a new key"]
    assert _sftp_backend(host, host.config.ssh) is not first


# -- plaintext ------------------------------------------------------------


@pytest.mark.parametrize(
    "target,creds,warns",
    [
        # Credentials over plain ws to another machine: worth a line.
        ("ws://nas", ApiKeyAuth("1-" + "k" * 64), True),
        ("ws://nas", BasicAuth("root", "pw"), True),
        # Loopback, or no credential at all: nothing to warn about.
        ("ws://127.0.0.1:6000", BasicAuth("root", "pw"), False),
        ("ws://localhost:6000", BasicAuth("root", "pw"), False),
        ("ws://nas", LocalAuth(), False),
        # TLS: the point of the warning does not apply.
        ("wss://nas", BasicAuth("root", "pw"), False),
    ],
)
def test_credentials_on_a_plaintext_socket_are_reported(
    monkeypatch, caplog, target, creds, warns
):
    host = TrueNASClient(target, autologin=False)
    monkeypatch.setattr(host, "_openwss", _Conn)
    monkeypatch.setattr(
        type(host), "api", property(lambda self: _ApiOk()), raising=False
    )
    with caplog.at_level(logging.WARNING):
        host.login(creds)
    assert ("plaintext ws://" in caplog.text) is warns


def test_the_plaintext_warning_is_logged_once(monkeypatch, caplog):
    host = TrueNASClient("ws://nas", autologin=False)
    monkeypatch.setattr(host, "_openwss", _Conn)
    monkeypatch.setattr(
        type(host), "api", property(lambda self: _ApiOk()), raising=False
    )
    with caplog.at_level(logging.WARNING):
        host.login(BasicAuth("root", "pw"))
        host.login(BasicAuth("root", "pw"))
    assert caplog.text.count("plaintext ws://") == 1


class _ApiOk(dict):
    """`api.auth[...]` answering True, which is a successful legacy login."""

    def __init__(self):
        ok = lambda *a: True  # noqa: E731
        super().__init__(
            auth={
                "login": ok,
                "login_with_api_key": ok,
                "login_with_token": ok,
            }
        )

    def __getattr__(self, name):
        return self[name]


# -- credential strings ---------------------------------------------------


@pytest.mark.parametrize(
    "raw,otp",
    [
        ("root:hunter2", None),
        # The documented URI spelling, which was read as part of the token
        # itself (`otp_token="otp:123456"`) and rejected by the server.
        ("root:hunter2\notp:123456", "123456"),
        # The historical bare-token line still works.
        ("root:hunter2\n123456", "123456"),
    ],
)
def test_an_otp_is_split_the_documented_way(raw, otp):
    cred = Credentials(raw)
    assert isinstance(cred, BasicAuth)
    assert cred.password == "hunter2"
    assert cred.otp_token == otp


# -- the unix socket path -------------------------------------------------


@pytest.mark.parametrize(
    "path",
    [
        "/var/run/middleware/middlewared.sock",
        "/run/a?b/x.sock",
        "/run/w#h/x.sock",
        "/run/sp ace/x.sock",
    ],
)
def test_a_socket_path_survives_being_rendered(path):
    """`_target` interpolated it raw into a `ws+unix://` URI and `Target.parse`
    then unquoted what it read, so `/run/a?b/x.sock` rendered as `/run/a` --
    a property describing a different socket than the one in use."""
    from pytruenas.host import TrueNASConfig

    config = TrueNASConfig(socket_path=path, autologin=False)
    host = TrueNASClient(config)
    assert host.config.socket_path == path
    assert host._target.path == path


def test_a_socket_path_in_a_uri_is_percent_decoded():
    """A URI path is encoded by definition: `%3F` names a `?` in the file name,
    and connecting to the literal `%3F` spelling would open a different file."""
    host = TrueNASClient("unix:///run/a%3Fb/x.sock", autologin=False)
    assert host.config.socket_path == "/run/a?b/x.sock"
    # And it renders back to the form it came from.
    assert host._target.path == "/run/a?b/x.sock"


def test_the_default_socket_is_unchanged():
    from pytruenas.host import DEFAULT_SOCKET_PATH

    host = TrueNASClient(None, autologin=False)
    assert host.config.socket_path == DEFAULT_SOCKET_PATH
    assert host.config.is_local
