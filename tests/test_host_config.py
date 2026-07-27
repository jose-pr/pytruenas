"""``TrueNASConfig`` + ``_normalize_target`` -- the connection-string contract.

Decision 1 of the hostctl migration: *every* form accepted by
``TrueNASClient(...)`` today must keep working. The table in
``test_normalize_target`` is that contract, transcribed from the plan's input
matrix; each row is a regression test for a form that works today.

Nothing here touches the network. ``TrueNASConfig`` must be constructible
offline -- the scheme/path probe is deferred to connect time -- and
``test_construction_does_no_network_io`` pins exactly that.
"""

import pytest

pytest.importorskip("hostctl")

from hostctl.host import HostConfig  # noqa: E402

from pytruenas.auth import ApiKeyAuth, BasicAuth, LocalAuth, TokenAuth  # noqa: E402
from pytruenas.host import (  # noqa: E402
    DEFAULT_SOCKET_PATH,
    TrueNASConfig,
    _normalize_target,
)

# -- the input matrix ------------------------------------------------------


@pytest.mark.parametrize(
    "given, expected",
    [
        # local socket forms
        (None, f"truenas+unix://{DEFAULT_SOCKET_PATH}"),
        ("", f"truenas+unix://{DEFAULT_SOCKET_PATH}"),
        ("localhost", f"truenas+unix://{DEFAULT_SOCKET_PATH}"),
        ("127.0.0.1", f"truenas+unix://{DEFAULT_SOCKET_PATH}"),
        # local *with* a port is a real websocket, not the socket
        ("localhost:8080", "truenas+ws://localhost:8080"),
        # bare host -> probe on connect
        ("nas", "truenas+auto://nas"),
        ("nas:8080", "truenas+auto://nas:8080"),
        # explicit websocket schemes
        ("ws://nas", "truenas+ws://nas"),
        ("wss://nas", "truenas+wss://nas"),
        # http/https collapse onto the websocket transport
        ("http://nas", "truenas+ws://nas"),
        ("https://nas", "truenas+wss://nas"),
        # already canonical
        ("truenas+wss://nas", "truenas+wss://nas"),
        ("truenas+auto://nas", "truenas+auto://nas"),
        # explicit API path is preserved (skips the path probe)
        ("wss://nas/api/current", "truenas+wss://nas/api/current"),
        ("https://nas:444/websocket", "truenas+wss://nas:444/websocket"),
        # explicit socket
        ("ws+unix:///path/to.sock", "truenas+unix:///path/to.sock"),
        ("truenas+unix:///path/to.sock", "truenas+unix:///path/to.sock"),
    ],
)
def test_normalize_target(given, expected):
    assert _normalize_target(given) == expected


@pytest.mark.parametrize(
    "given",
    [
        "wss://root:secret@nas",
        "https://root:secret@nas",
        "truenas+wss://root:secret@nas",
    ],
)
def test_normalize_target_preserves_userinfo(given):
    # _normalize_target only rewrites the scheme; stripping the password is
    # HostConfig._from_uri's job, and it needs the userinfo intact to do it.
    assert "secret" in _normalize_target(given)
    assert _normalize_target(given).startswith("truenas+wss://")


# -- config construction ---------------------------------------------------


def test_construction_does_no_network_io(monkeypatch):
    """Constructing a config must never probe -- that is the lazy requirement.

    Today the probe runs inside ``TrueNASClient.__init__``. Under HostConfig a
    config is a parsed value, so any HTTP here would fire during URI parsing.
    """

    def explode(*args, **kwargs):
        raise AssertionError("config construction performed network I/O")

    import requests

    monkeypatch.setattr(requests, "get", explode)
    monkeypatch.setattr(requests, "post", explode)

    for uri in ("truenas+auto://nas", "truenas+wss://nas", "nas", "wss://nas"):
        TrueNASConfig.from_target(uri)


@pytest.mark.parametrize(
    "target, scheme, host, port",
    [
        ("wss://nas", "truenas+wss", "nas", 0),
        ("wss://nas:444", "truenas+wss", "nas", 444),
        ("nas", "truenas+auto", "nas", 0),
        ("ws://nas:8080", "truenas+ws", "nas", 8080),
    ],
)
def test_config_fields_from_target(target, scheme, host, port):
    config = TrueNASConfig.from_target(target)
    assert config.scheme == scheme
    assert config.host == host
    assert config.port == port


def test_local_socket_config():
    config = TrueNASConfig.from_target(None)
    assert config.scheme == "truenas+unix"
    assert config.socket_path == DEFAULT_SOCKET_PATH
    assert config.is_local
    assert isinstance(config.credentials, LocalAuth)


def test_explicit_api_path_is_recorded():
    config = TrueNASConfig.from_target("wss://nas/api/current")
    assert config.api_path == "/api/current"
    # An explicit path means nothing left to probe on that axis.
    assert not config.needs_path_probe


def test_missing_api_path_defers_the_probe():
    config = TrueNASConfig.from_target("wss://nas")
    assert config.api_path is None
    assert config.needs_path_probe


def test_auto_scheme_defers_the_scheme_probe():
    config = TrueNASConfig.from_target("nas")
    assert config.needs_scheme_probe
    assert not TrueNASConfig.from_target("wss://nas").needs_scheme_probe


# -- credentials -----------------------------------------------------------


def test_userinfo_becomes_basic_auth():
    config = TrueNASConfig.from_target("wss://root:secret@nas")
    assert isinstance(config.credentials, BasicAuth)
    assert config.credentials.username == "root"
    assert config.credentials.password == "secret"


def test_userinfo_otp_extra_reaches_the_credential():
    """An OTP in the URI must be percent-encoded -- ``%0A``, not a raw newline.

    The newline separator itself is well chosen: a password can never contain
    one, because Enter submits at any prompt rather than being typed into the
    value. So it splits the field without stealing a character or needing an
    escaping scheme.

    A URI is the exception. ``urlsplit`` *silently strips* newlines (a WHATWG
    rule aimed at header injection), so ``"secret\\notp:123456"`` arrives as the
    single string ``"secretotp:123456"`` and the OTP is swallowed into the
    password with no error. Percent-encoding is the only spelling that survives
    that transport; this test pins it, because the failure mode is silent and
    would otherwise surface as a baffling authentication failure.
    """
    config = TrueNASConfig.from_target("wss://root:secret%0Aotp:123456@nas")
    assert isinstance(config.credentials, BasicAuth)
    assert config.credentials.password == "secret"
    assert config.credentials.otp_token == "123456"


def test_raw_newline_in_userinfo_is_honored():
    """A raw newline now works too -- hostctl preserves it through the parse.

    This used to be a trap: ``urlsplit`` strips ``\\t\\r\\n`` from a URI (a
    WHATWG rule against header injection), so the newline vanished before
    ``parse_credentials`` ran and the OTP was silently swallowed into the
    password. hostctl now extracts the userinfo before ``urlsplit`` can discard
    it (commit "preserve raw control characters in URI userinfo, reject them in
    the host"), so both spellings behave identically and nobody has to know to
    write ``%0A``.

    Kept as a regression test because the failure it replaces was *silent* --
    a wrong password and an unexplained auth failure, not an error.
    """
    config = TrueNASConfig.from_target("wss://root:secret\notp:123456@nas")
    assert isinstance(config.credentials, BasicAuth)
    assert config.credentials.password == "secret"
    assert config.credentials.otp_token == "123456"


def test_explicit_credentials_argument():
    config = TrueNASConfig.from_target("wss://nas", credentials="1-" + "a" * 64)
    assert isinstance(config.credentials, ApiKeyAuth)

    config = TrueNASConfig.from_target("wss://nas", credentials=("root", "pw"))
    assert isinstance(config.credentials, BasicAuth)


def test_token_credential_argument():
    config = TrueNASConfig.from_target("wss://nas", credentials="sometoken")
    assert isinstance(config.credentials, TokenAuth)


def test_credentials_in_uri_and_argument_conflict():
    with pytest.raises(ValueError):
        TrueNASConfig.from_target("wss://root:secret@nas", credentials=("a", "b"))


@pytest.mark.parametrize("typo", ["passwrd", "pasword", "api_ky", "totp"])
def test_unknown_credential_is_rejected(typo):
    """A mistyped credential must fail loudly, not silently do nothing.

    Without this, ``TrueNASConfig.from_target("wss://nas", passwrd="s3cret")``
    would build a config with *no* password and no complaint, surfacing much
    later as an unexplained authentication failure. hostctl enforces it from
    the ``uri_credentials`` declaration before construction.
    """
    with pytest.raises(ValueError, match="unknown credential"):
        TrueNASConfig.from_target("wss://nas", **{typo: "value"})


def test_declared_credentials_are_all_accepted():
    """Every declared name must actually reach the constructor.

    Declaring one that `_from_parsed_uri` ignores would let it through the
    strict check and then silently drop it -- the failure mode that once hid
    `webshell=False`. Checked against the real signature rather than a second
    hand-maintained list, so the two cannot drift.
    """
    import inspect

    from pytruenas.auth import Credentials

    accepted = {
        name
        for name, parameter in inspect.signature(
            TrueNASConfig.__init__
        ).parameters.items()
        if parameter.kind is inspect.Parameter.KEYWORD_ONLY
    }
    # These are consumed by `_from_parsed_uri` itself to build the credential
    # rather than passed straight through.
    credential_inputs = set(
        inspect.signature(Credentials.from_host_credentials).parameters
    )

    for name in TrueNASConfig.uri_credentials:
        assert name in accepted | credential_inputs, name


# -- connection_uri is credential-free -------------------------------------


@pytest.mark.parametrize(
    "target",
    [
        "wss://root:secret@nas",
        "https://root:secret@nas",
        "wss://root:secret%0Aotp:123456@nas",
        "truenas+wss://admin:hunter2@nas:444/api/current",
    ],
)
def test_connection_uri_never_renders_a_secret(target):
    config = TrueNASConfig.from_target(target)
    uri = config.connection_uri
    assert "secret" not in uri
    assert "hunter2" not in uri
    assert "123456" not in uri
    # repr() is the other place a secret leaks into a log.
    assert "secret" not in repr(config)
    assert "hunter2" not in repr(config)


def test_connection_uri_round_trips_through_hostctl():
    """The canonical URI must parse back to an equivalent config.

    This is HostConfig's contract -- a config that advertises a URI it cannot
    itself parse is broken (cf. SystemConfig's abstract-base note).
    """
    config = TrueNASConfig.from_target("wss://nas:444/api/current")
    again = HostConfig(config.connection_uri)
    assert isinstance(again, TrueNASConfig)
    assert again.host == config.host
    assert again.port == config.port
    assert again.api_path == config.api_path
    assert again.scheme == config.scheme


def test_unresolved_auto_uri_round_trips():
    config = TrueNASConfig.from_target("nas")
    assert config.connection_uri.startswith("truenas+auto://")
    again = HostConfig(config.connection_uri)
    assert isinstance(again, TrueNASConfig)
    assert again.needs_scheme_probe


# -- registry dispatch -----------------------------------------------------


@pytest.mark.parametrize(
    "uri",
    [
        "truenas://nas",
        "truenas+auto://nas",
        "truenas+ws://nas",
        "truenas+wss://nas",
        f"truenas+unix://{DEFAULT_SOCKET_PATH}",
    ],
)
def test_registered_schemes_dispatch(uri):
    assert isinstance(HostConfig(uri), TrueNASConfig)


@pytest.mark.parametrize("uri", ["wss://nas", "https://nas", "ws://nas"])
def test_bare_schemes_are_not_claimed_globally(uri):
    """pytruenas must not hijack generic schemes in hostctl's registry.

    hostctl is protocol-agnostic; claiming bare ``wss://`` would risk an
    "ambiguous host URI matched" collision with any future config. The bare
    forms are understood only at pytruenas' own entry point.
    """
    with pytest.raises(ValueError, match="unsupported host scheme"):
        HostConfig(uri)


def test_sslverify_defaults_true_and_is_settable():
    assert TrueNASConfig.from_target("wss://nas").sslverify is True
    assert TrueNASConfig.from_target("wss://nas", sslverify=False).sslverify is False


@pytest.mark.parametrize("target", ["wss://nas", None])
def test_options_reach_the_config_on_every_branch(target):
    """Each accepted option must take effect for *both* URI shapes.

    ``_from_parsed_uri`` returns from two places -- the unix-socket branch and
    the host/port branch. An option forwarded in only one is silently ignored
    for the other, which is how ``webshell=False`` was accepted and dropped.
    """
    config = TrueNASConfig.from_target(
        target, sslverify=False, version="v2.0", executor=["local"], path=["local"]
    )
    assert config.sslverify is False
    assert config.version == "v2.0"
    assert config.executors == ("local",)
    assert config.paths == ("local",)


def test_provider_overrides_default_to_none():
    """``None`` means "decide from the target", not "no providers"."""
    config = TrueNASConfig.from_target("wss://nas")
    assert config.executors is None
    assert config.paths is None


def test_a_bare_string_override_is_one_name():
    """``executor="ssh"`` must not become ``("s", "s", "h")``."""
    config = TrueNASConfig.from_target("wss://nas", executor="ssh", path="sftp")
    assert config.executors == ("ssh",)
    assert config.paths == ("sftp",)
