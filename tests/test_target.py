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


def test_uri_roundtrips_reserved_chars_in_credentials():
    """A password with reserved chars must survive parse -> uri -> parse.

    ``parse`` unquotes userinfo, so ``uri`` must re-quote it; otherwise a
    password like ``p@ss/w:rd`` reassembles into a URL that reparses as a
    different host/port/path.
    """
    original = "wss://root:p%40ss%2Fw%3Ard@nas:8443/api"
    t = Target.parse(original)
    assert t.password == "p@ss/w:rd"  # decoded on parse
    round_tripped = Target.parse(t.uri, resolve_port=False)
    assert round_tripped.password == "p@ss/w:rd"
    assert round_tripped.host == "nas"
    assert round_tripped.port == 8443
    assert round_tripped.path == "/api"


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


def test_websocket_schemes_resolve_to_a_port():
    """ws/wss are absent from every system services database.

    getservbyname("wss") raises, which left a TrueNAS websocket URL with
    port 0 -- the schemes this client uses most. netimps' scheme table is
    consulted first, and utils/target.py registers these two into it.
    """
    assert Target.parse("ws://host").port == 80
    assert Target.parse("wss://host").port == 443


def test_known_schemes_still_resolve():
    """The schemes that already worked must keep working."""
    assert Target.parse("http://host").port == 80
    assert Target.parse("https://host").port == 443
    assert Target.parse("host").port == 80  # bare host defaults to http


def test_explicit_port_wins_over_the_scheme():
    assert Target.parse("wss://host:8443").port == 8443


def test_unknown_scheme_leaves_port_zero():
    """An unresolvable scheme must not invent a port."""
    assert Target.parse("definitelynotascheme://host").port == 0


def test_resolve_port_can_be_disabled():
    assert Target.parse("wss://host", resolve_port=False).port == 0
