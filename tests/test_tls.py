"""One trust decision for every TLS leg -- pytruenas.utils.tls."""

import ssl
from types import SimpleNamespace

import pytest

from pytruenas.host import TrueNASHost, _TrustAdapter
from pytruenas.utils import tls


@pytest.fixture(autouse=True)
def _no_bundle_env(monkeypatch):
    for name in tls.CA_BUNDLE_ENV:
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def bundle(tmp_path):
    # A real PEM, so load_verify_locations accepts it: the OS store's own
    # first CA, or skip where the store is not exportable (e.g. some Linux).
    ders = ssl.create_default_context().get_ca_certs(binary_form=True)
    if not ders:
        pytest.skip("no exportable CA in the OS store")
    path = tmp_path / "ca.pem"
    path.write_text(ssl.DER_cert_to_PEM_cert(ders[0]))
    return path


def test_no_bundle_means_the_os_store():
    assert tls.ca_bundle(True) is None
    assert isinstance(tls.context(True), ssl.SSLContext)


def test_verification_off_means_no_context():
    assert tls.context(False) is None


def test_a_path_is_the_bundle_and_replaces_the_os_store(bundle):
    assert tls.ca_bundle(bundle) == (str(bundle), "sslverify")
    context = tls.context(str(bundle))
    assert context.verify_mode == ssl.CERT_REQUIRED and context.check_hostname
    assert len(context.get_ca_certs()) == 1  # the bundle only, no OS store


def test_env_bundle_precedence(monkeypatch, bundle):
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", "/nope/requests.pem")
    monkeypatch.setenv("SSL_CERT_FILE", str(bundle))
    assert tls.ca_bundle(True) == (str(bundle), "SSL_CERT_FILE")
    assert len(tls.context(True).get_ca_certs()) == 1
    # An explicit path beats the environment.
    assert tls.ca_bundle("/given.pem") == ("/given.pem", "sslverify")


def test_empty_env_is_unset(monkeypatch):
    monkeypatch.setenv("SSL_CERT_FILE", "")
    assert tls.ca_bundle(True) is None


def test_missing_bundle_names_the_path_and_its_source(monkeypatch, tmp_path):
    monkeypatch.setenv("CURL_CA_BUNDLE", str(tmp_path / "gone.pem"))
    with pytest.raises(FileNotFoundError, match="CURL_CA_BUNDLE.*gone.pem"):
        tls.context(True)


def test_a_directory_is_a_hashed_capath(tmp_path):
    assert isinstance(tls.context(tmp_path), ssl.SSLContext)


def test_config_keeps_a_path_as_a_string(tmp_path):
    host = TrueNASHost("wss://nas", autologin=False, sslverify=tmp_path / "ca.pem")
    assert host.sslverify == str(tmp_path / "ca.pem")
    assert TrueNASHost("wss://nas", autologin=False, verify=False).sslverify is False


def test_side_channels_use_the_shared_context_and_no_bundle_file(bundle):
    """requests verified against certifi, the websocket against the OS store,
    so a certificate trusted by one leg failed the other (measured: the API
    connected and every download raised SSLError)."""
    host = TrueNASHost("wss://nas", autologin=False, sslverify=bundle)
    adapter = host._http.get_adapter("https://nas/_upload")
    assert isinstance(adapter, _TrustAdapter)
    assert len(adapter._context.get_ca_certs()) == 1
    conn = SimpleNamespace(cert_reqs=None, ca_certs=None, ca_cert_dir=None)
    adapter.cert_verify(conn, "https://nas/_upload", True, None)
    assert (conn.ca_certs, conn.ca_cert_dir) == (None, None)
    assert conn.cert_reqs == "CERT_REQUIRED"


def test_side_channels_do_not_verify_when_verification_is_off(monkeypatch):
    host = TrueNASHost("wss://nas", autologin=False, verify=False)
    assert not isinstance(host._http.get_adapter("https://nas/"), _TrustAdapter)
    # A bundle in the environment must not switch verification back on:
    # requests fills an unset per-request verify from $REQUESTS_CA_BUNDLE.
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", "/some/bundle.pem")
    settings = host._http.merge_environment_settings(
        "https://nas/", {}, None, host._http_verify, None
    )
    assert settings["verify"] is False


def test_the_websocket_gets_the_shared_context(monkeypatch, bundle):
    from pytruenas import connection

    seen = {}

    class _WS:
        def __init__(self, sslopt=None):
            seen["sslopt"] = sslopt

        def connect(self, uri):
            pass

    monkeypatch.setattr(connection._websocket, "WebSocket", _WS)
    conn = connection.TrueNASWSConnection.__new__(connection.TrueNASWSConnection)
    conn.uri, conn.verify_ssl = "wss://nas/api/current", str(bundle)
    conn._connect()
    assert len(seen["sslopt"]["context"].get_ca_certs()) == 1
    conn.verify_ssl = False
    conn._connect()
    assert seen["sslopt"] == {"cert_reqs": ssl.CERT_NONE}
