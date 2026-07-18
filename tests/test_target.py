"""Connection-string parsing (utils.target.Target)."""

from pytruenas.utils.target import Target


def test_bare_host_defaults_to_http_scheme():
    t = Target.parse("nas.example.com")
    assert t.host == "nas.example.com"
    assert t.scheme == "http"


def test_scheme_override_default():
    t = Target.parse("nas.example.com", scheme="wss")
    assert t.scheme == "wss"
    assert t.host == "nas.example.com"


def test_userinfo_parsed():
    t = Target.parse("wss://root:secret@nas:8443/api/current")
    assert t.username == "root"
    assert t.password == "secret"
    assert t.host == "nas"
    assert t.port == 8443
    assert t.path == "/api/current"


def test_is_local():
    assert Target.parse("localhost").is_local
    assert Target.parse("127.0.0.1").is_local
    assert Target.parse("").is_local
    assert not Target.parse("nas.example.com").is_local


def test_uri_roundtrip():
    t = Target.parse("wss://nas:8443/api/current")
    assert t.uri == "wss://nas:8443/api/current"


def test_query_val():
    t = Target.parse("http://h/p?a=1&a=2&b=3")
    assert t.query_val("b") == "3"
    assert t.query_val("a") == "2"  # last wins
    assert t.query_val("a", islist=True) == ["1", "2"]
    assert t.query_val("missing", "default") == "default"


def test_replace_is_namedtuple():
    t = Target.parse("http://h")
    t2 = t._replace(scheme="ws")
    assert t2.scheme == "ws"
    assert t.scheme == "http"  # original unchanged
