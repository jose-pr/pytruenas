"""Real TLS handshakes on the API websocket and the HTTP side channels.

A loopback server with certificates from a throwaway CA (nothing touches the
OS store): the trust contract of `verify=` -- a bundle, the OS trust, off, a
caller's context with a client certificate -- checked against an actual peer
rather than the objects that would be handed to one.
"""

import base64
import hashlib
import socket
import ssl
import threading

import pytest

issuing = pytest.importorskip("sslcontext.issuing")

from pytruenas import TrueNASClient  # noqa: E402
from pytruenas.connection import TrueNASWSConnection  # noqa: E402

_GUID = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
_LOOPBACK = ["127.0.0.1", "localhost"]


@pytest.fixture(scope="module")
def pki(tmp_path_factory):
    out = tmp_path_factory.mktemp("pki")
    good = issuing.CertificateAuthority.create("pytruenas test CA", days=2)
    rogue = issuing.CertificateAuthority.create("unrelated CA", days=2)
    (out / "ca.pem").write_bytes(good.certificate)
    for name, ca, names in (
        ("good", good, _LOOPBACK),
        ("rogue", rogue, _LOOPBACK),
        ("mismatch", good, ["other.example"]),
        ("client", good, ["client-alice"]),
    ):
        issued = ca.issue(names, days=1)
        (out / f"{name}.pem").write_bytes(issued.certificate + issued.chain)
        (out / f"{name}.key").write_bytes(issued.key)
    return out


class _Server:
    """Answers a websocket upgrade with 101 and any other request with `ok`."""

    def __init__(self, pki, cert, client_ca=None):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.load_cert_chain(pki / f"{cert}.pem", pki / f"{cert}.key")
        if client_ca:
            self.context.verify_mode = ssl.CERT_REQUIRED
            self.context.load_verify_locations(pki / client_ca)
        self.listener = socket.socket()
        self.listener.bind(("127.0.0.1", 0))
        self.listener.listen(8)
        self.port = self.listener.getsockname()[1]
        self.open = []
        threading.Thread(target=self._serve, daemon=True).start()

    def _serve(self):
        while True:
            try:
                raw, _ = self.listener.accept()
            except OSError:
                return
            threading.Thread(target=self._answer, args=(raw,), daemon=True).start()

    def _answer(self, raw):
        conn = raw  # until the handshake succeeds; wrap_socket detaches raw
        try:
            conn = self.context.wrap_socket(raw, server_side=True)
            request = b""
            while b"\r\n\r\n" not in request:
                chunk = conn.recv(4096)
                if not chunk:
                    conn.close()
                    return
                request += chunk
        except (OSError, ssl.SSLError):
            conn.close()
            return
        self.open.append(conn)
        key = [
            line.split(b":", 1)[1].strip()
            for line in request.split(b"\r\n")
            if line.lower().startswith(b"sec-websocket-key:")
        ]
        if key:
            accept = base64.b64encode(hashlib.sha1(key[0] + _GUID).digest())
            conn.sendall(
                b"HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\n"
                b"Connection: Upgrade\r\nSec-WebSocket-Accept: " + accept + b"\r\n\r\n"
            )
        else:
            conn.sendall(
                b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\nConnection: close\r\n\r\nok"
            )

    def close(self):
        self.listener.close()
        for conn in self.open:
            conn.close()


def _verify(pki, kind):
    if kind == "bundle":
        return str(pki / "ca.pem")
    if kind == "os":
        return True
    if kind == "off":
        return False
    context = ssl.create_default_context(cafile=str(pki / "ca.pem"))
    if kind == "client-cert":
        context.load_cert_chain(pki / "client.pem", pki / "client.key")
    return context


def _websocket_leg(port, verify):
    conn = TrueNASWSConnection(f"wss://127.0.0.1:{port}/api/current", verify=verify)
    conn.connect().close()


def _side_channel_leg(port, verify):
    host = TrueNASClient(f"wss://127.0.0.1:{port}", autologin=False, verify=verify)
    try:
        assert (
            host._side_request("GET", f"https://127.0.0.1:{port}/ok").content == b"ok"
        )
    finally:
        host.close()


# verify=False is meant to be loud: urllib3 warns on each unverified request.
@pytest.mark.filterwarnings("ignore::urllib3.exceptions.InsecureRequestWarning")
@pytest.mark.parametrize("leg", [_websocket_leg, _side_channel_leg])
@pytest.mark.parametrize(
    "cert, client_ca, kind, accepted",
    [
        ("good", None, "bundle", True),
        ("good", None, "context", True),
        ("rogue", None, "bundle", False),
        ("mismatch", None, "bundle", False),
        ("good", None, "os", False),  # the test CA is in no OS store
        ("rogue", None, "off", True),
        ("good", "ca.pem", "context", False),  # the server wants a certificate
        ("good", "ca.pem", "client-cert", True),
    ],
)
def test_every_leg_honours_verify(pki, leg, cert, client_ca, kind, accepted):
    server = _Server(pki, cert, client_ca)
    try:
        if accepted:
            leg(server.port, _verify(pki, kind))
        else:
            with pytest.raises(OSError) as raised:
                leg(server.port, _verify(pki, kind))
            # Both legs raise the TLS layer's own error, never requests' type.
            assert type(raised.value).__module__ in ("ssl", "builtins")
            if client_ca is None:
                assert isinstance(raised.value, ssl.SSLCertVerificationError)
    finally:
        server.close()
