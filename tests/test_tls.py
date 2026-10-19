"""One trust decision for every TLS leg -- `verify=`, made in pytruenas._tls."""

import ssl
import sys
from types import SimpleNamespace

import pytest

from pytruenas import _tls
from pytruenas.host import TrueNASClient, _TrustAdapter


@pytest.fixture(autouse=True)
def _no_bundle_env(monkeypatch):
    for name in _tls.CA_BUNDLE_ENV:
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def bundle(tmp_path):
    # A real PEM, so load_verify_locations accepts it: a throwaway CA, else
    # the OS store's own first CA (not exportable on some Linux).
    path = tmp_path / "ca.pem"
    try:
        from sslcontext.issuing import CertificateAuthority
    except ImportError:
        ders = ssl.create_default_context().get_ca_certs(binary_form=True)
        if not ders:
            pytest.skip("no sslcontext, and no exportable CA in the OS store")
        path.write_text(ssl.DER_cert_to_PEM_cert(ders[0]))
    else:
        path.write_bytes(
            CertificateAuthority.create("bundle test CA", days=1).certificate
        )
    return path


@pytest.mark.skipif(sys.version_info < (3, 10), reason="truststore needs 3.10")
def test_true_is_the_platform_verifier():
    """What hostctl's own verify=True means, so both name one trust."""
    import truststore

    assert isinstance(_tls.context(True), truststore.SSLContext)


@pytest.mark.skipif(sys.version_info >= (3, 10), reason="3.9 has no truststore")
def test_true_is_openssls_store_on_39():
    context = _tls.context(True)
    assert type(context) is ssl.SSLContext and context.verify_mode == ssl.CERT_REQUIRED


def test_verification_off_means_no_context():
    assert _tls.context(False) is None
    assert _tls.sslopt(False) == {"cert_reqs": ssl.CERT_NONE}


def test_a_callers_context_is_used_as_it_is():
    """How a client certificate (mTLS) or a pinned CA reaches every leg."""
    mine = ssl.create_default_context()
    assert _tls.context(mine) is mine
    assert _tls.sslopt(mine) == {"context": mine}


def test_a_path_is_the_bundle_and_replaces_the_os_store(bundle):
    context = _tls.context(str(bundle))
    assert context.verify_mode == ssl.CERT_REQUIRED and context.check_hostname
    assert len(context.get_ca_certs()) == 1  # the bundle only, no OS store


def test_an_env_bundle_replaces_the_platform_verifier(monkeypatch, bundle):
    """truststore ignores SSL_CERT_FILE on Windows and macOS, so it is read here."""
    monkeypatch.setenv("REQUESTS_CA_BUNDLE", "/nope/requests.pem")
    monkeypatch.setenv("SSL_CERT_FILE", str(bundle))
    context = _tls.context(True)
    assert type(context) is ssl.SSLContext and len(context.get_ca_certs()) == 1


def test_empty_env_is_unset(monkeypatch):
    monkeypatch.setenv("SSL_CERT_FILE", "")
    assert _tls._bundle(True) is None


def test_missing_bundle_names_the_path_and_its_source(monkeypatch, tmp_path):
    monkeypatch.setenv("CURL_CA_BUNDLE", str(tmp_path / "gone.pem"))
    with pytest.raises(FileNotFoundError, match="CURL_CA_BUNDLE.*gone.pem"):
        _tls.context(True)
    with pytest.raises(FileNotFoundError, match="verify.*gone.pem"):
        _tls.context(str(tmp_path / "gone.pem"))


def test_a_directory_is_a_hashed_capath(tmp_path):
    assert isinstance(_tls.context(tmp_path), ssl.SSLContext)


@pytest.mark.parametrize("value", ["", " ", "false", "0", "True"])
def test_a_boolean_word_or_empty_string_is_not_a_bundle(value):
    with pytest.raises(ValueError, match="not a CA bundle path"):
        _tls.check(value)


def test_anything_else_is_a_type_error():
    with pytest.raises(TypeError, match="ssl.SSLContext"):
        _tls.check(1)


def test_the_config_keeps_a_path_as_a_string_and_a_context_as_it_is(tmp_path):
    host = TrueNASClient("wss://nas", autologin=False, verify=tmp_path / "ca.pem")
    assert host.config.verify == str(tmp_path / "ca.pem")
    mine = ssl.create_default_context()
    assert (
        TrueNASClient("wss://nas", autologin=False, verify=mine).config.verify is mine
    )


def test_sslverify_is_gone_and_says_what_replaced_it():
    with pytest.raises(TypeError, match="verify="):
        TrueNASClient("wss://nas", autologin=False, sslverify=False)


@pytest.mark.parametrize("verify", ["ca.pem", "context"])
def test_a_path_or_a_context_still_verifies_ssh_host_keys(verify):
    """hostctl's SSHConfig takes a bool: anything but False means verify."""
    value = ssl.create_default_context() if verify == "context" else verify
    host = TrueNASClient("wss://nas", autologin=False, verify=value, shell="root@nas")
    assert host.config.ssh.verify is True


def test_side_channels_use_the_shared_context_and_no_bundle_file(bundle):
    """requests verified against certifi, the websocket against the OS store,
    so a certificate trusted by one leg failed the other (measured: the API
    connected and every download raised SSLError)."""
    host = TrueNASClient("wss://nas", autologin=False, verify=bundle)
    adapter = host._http.get_adapter("https://nas/_upload")
    assert isinstance(adapter, _TrustAdapter)
    assert len(adapter._context.get_ca_certs()) == 1
    conn = SimpleNamespace(cert_reqs=None, ca_certs=None, ca_cert_dir=None)
    adapter.cert_verify(conn, "https://nas/_upload", True, None)
    assert (conn.ca_certs, conn.ca_cert_dir) == (None, None)
    assert conn.cert_reqs == "CERT_REQUIRED"


def test_a_proxied_side_channel_gets_the_shared_context(bundle):
    """Behind HTTPS_PROXY, requests built a proxy manager with its own trust,
    so uploads and downloads ignored the bundle the websockets used."""
    host = TrueNASClient("wss://nas", autologin=False, verify=bundle)
    adapter = host._http.get_adapter("https://nas/_upload")
    manager = adapter.proxy_manager_for("http://127.0.0.1:3128")
    assert manager.connection_pool_kw["ssl_context"] is adapter._context


def test_a_callers_context_reaches_the_side_channels_and_the_websocket():
    mine = ssl.create_default_context()
    host = TrueNASClient("wss://nas", autologin=False, verify=mine)
    assert host._http.get_adapter("https://nas/")._context is mine
    assert host._http_verify is True  # urllib3 writes it into the context
    assert _tls.sslopt(host.config.verify) == {"context": mine}


def test_side_channels_do_not_verify_when_verification_is_off(monkeypatch):
    host = TrueNASClient("wss://nas", autologin=False, verify=False)
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

        def connect(self, uri, timeout=None):
            seen["timeout"] = timeout

        def settimeout(self, value):
            seen["settimeout"] = value

    monkeypatch.setattr(connection._websocket, "WebSocket", _WS)
    conn = connection.TrueNASWSConnection.__new__(connection.TrueNASWSConnection)
    conn.uri, conn.verify = "wss://nas/api/current", str(bundle)
    conn.connect_timeout = connection.CONNECT_TIMEOUT
    conn._connect()
    assert len(seen["sslopt"]["context"].get_ca_certs()) == 1
    conn.verify = False
    conn._connect()
    assert seen["sslopt"] == {"cert_reqs": ssl.CERT_NONE}


def test_turning_verification_off_is_logged_once(caplog):
    """It logged nothing: a lab setting copied to production went unnoticed."""
    import logging

    host = TrueNASClient("wss://nas", autologin=False, verify=False)
    with caplog.at_level(logging.WARNING):
        host._http
        host._warn_if_unverified()
    assert caplog.text.count("TLS certificate verification is off") == 1
    caplog.clear()
    with caplog.at_level(logging.WARNING):
        TrueNASClient("ws://nas", autologin=False, verify=False)._http
        TrueNASClient(None, autologin=False, verify=False)._http
    assert "verification is off" not in caplog.text  # no TLS to skip
