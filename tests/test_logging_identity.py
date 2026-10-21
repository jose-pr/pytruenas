"""Every log record must identify the host it came from -- and only that.

Two separate guarantees, which used to be one broken one:

* a record names the machine (``[nas1]``), not the whole connection string;
* nothing on the logging path can carry a password.

The second used to be handled by masking the password with ``***``. That is now
*removal*: what is logged stays a valid, reusable URI, because a placeholder
would reparse into a wrong credential if anything fed it back in.
"""

import logging

import pytest

from pytruenas import TrueNASClient
from pytruenas.host import TrueNASConfig, _HostLogger

# -- the short label ------------------------------------------------------


@pytest.mark.parametrize(
    "target,expected",
    [
        # A bare host or host:port is already the name.
        ("nas1", "nas1"),
        ("nas1:8443", "nas1:8443"),
        # The scheme, API path and userinfo are all noise in a log prefix.
        ("wss://nas1.example.com:8443/api/current", "nas1.example.com:8443"),
        ("https://root@192.0.2.21", "192.0.2.21"),
        # A default port repeats the scheme; a non-default one distinguishes.
        ("wss://nas", "nas"),
        ("ws://nas", "nas"),
        ("wss://nas:8443", "nas:8443"),
        # The local middleware socket has no host to name.
        (None, "localhost"),
        ("", "localhost"),
        ("localhost", "localhost"),
        ("ws://localhost:6000", "localhost:6000"),
        # IPv6 keeps its brackets so the label is unambiguous.
        ("ws://[2001:db8::1]:6000", "[2001:db8::1]:6000"),
    ],
)
def test_name_is_the_machine_not_the_uri(target, expected):
    assert TrueNASConfig.from_target(target).name == expected


def test_name_never_contains_credentials():
    config = TrueNASConfig.from_target("wss://root:hunter2@nas:8443/api")
    assert config.name == "nas:8443"
    assert "hunter2" not in config.name
    assert "root" not in config.name
    # ...while the credentials themselves were still parsed out and kept.
    assert config.credentials is not None


def test_name_preserves_the_typed_hostname_case():
    """A fan-out over nasA/nasB should log [nasA], not [nasa].

    `urlsplit().hostname` folds case -- right for resolution, wrong for a label
    the operator greps for.
    """
    assert TrueNASConfig.from_target("nasA").name == "nasA"
    assert TrueNASConfig.from_target("wss://NAS-Prod.example.COM").name == (
        "NAS-Prod.example.COM"
    )


def test_hostname_case_does_not_depend_on_whether_a_password_was_given():
    """The same machine must not render two ways.

    On hostctl 0.1.0 the credentialed form folded (hostctl rebuilt the
    authority from the folded `hostname` when stripping the password) while the
    bare form did not -- so one host's log lines could not be correlated.
    Fixed upstream in 0.1.1, which the dependency floor requires.
    """
    bare = TrueNASConfig.from_target("wss://nasA:8443").name
    with_user = TrueNASConfig.from_target("wss://root@nasA:8443").name
    with_password = TrueNASConfig.from_target("wss://root:hunter2@nasA:8443").name
    assert bare == with_user == with_password == "nasA:8443"


@pytest.mark.parametrize("spelling", ["localhost", "LOCALHOST", "LocalHost"])
def test_local_detection_ignores_hostname_case(spelling):
    """Preserving the typed case must not change where a target routes.

    `.host` now holds the spelling the caller typed (hostctl >=0.1.2), which is
    a display value. Routing decisions case-fold before comparing, so the local
    shortcut still resolves to the middleware socket however it is written.
    """
    config = TrueNASConfig.from_target(spelling)
    assert config.is_local
    assert config.name == "localhost"


def test_two_spellings_of_one_host_are_not_equal_configs():
    """The deliberate trade-off in hostctl >=0.1.2, pinned so it stays known.

    `.host` is the given spelling rather than a canonical one, so code keying
    on it must casefold explicitly. Resolution is unaffected -- DNS treats the
    two as one name.
    """
    a = TrueNASConfig.from_target("wss://nasA:8443")
    b = TrueNASConfig.from_target("wss://NASA:8443")
    assert a.host != b.host
    assert a.host.casefold() == b.host.casefold()


def test_host_exposes_the_same_name_as_its_config():
    host = TrueNASClient("wss://nas1:8443", autologin=False)
    assert host.name == host.config.name == "nas1:8443"


# -- the connection URI is credential-free, so it needs no redaction ------


def test_connection_uri_is_already_clean():
    """Credentials are extracted at parse time, not masked at render time."""
    config = TrueNASConfig.from_target("wss://root:hunter2@nas:8443/api")
    uri = config.connection_uri
    assert "hunter2" not in uri
    assert "***" not in uri  # nothing to mask -- the password was never in it
    assert uri == "truenas+wss://nas:8443/api"
    # A clean URI is still a usable one: it round-trips.
    assert TrueNASConfig.from_target(uri).connection_uri == uri


def test_repr_cannot_leak_a_password():
    config = TrueNASConfig.from_target("wss://root:hunter2@nas:8443/api")
    assert "hunter2" not in repr(config)


# -- the per-host logger --------------------------------------------------


def test_records_name_their_host_without_any_fanout(caplog):
    """The CLI's fan-out is not the only way a record gets attributed.

    A library caller with two clients open gets two interleaved streams; an
    unattributed "connection was closed" is not actionable.
    """
    a = TrueNASClient("wss://nas1:8443", autologin=False)
    b = TrueNASClient("wss://nas2:8443", autologin=False)
    with caplog.at_level(logging.WARNING, logger="pytruenas"):
        a.logger.warning("connection was closed")
        b.logger.warning("connection was closed")
    messages = [record.getMessage() for record in caplog.records]
    assert messages == [
        "[nas1:8443] connection was closed",
        "[nas2:8443] connection was closed",
    ]


def test_prefix_is_not_applied_twice():
    """The adapter tags at the call site, duho.fanout tags at the handler.

    A record that somehow passed through both must not read ``[nas1] [nas1]``.
    """
    adapter = _HostLogger(logging.getLogger("pytruenas.test"), {"name": "nas1"})
    assert adapter.process("plain", {})[0] == "[nas1] plain"
    assert adapter.process("[nas1] already tagged", {})[0] == "[nas1] already tagged"


def test_host_logger_trace_is_prefixed(caplog):
    """duho installs `.trace` on LoggerAdapter, so the host's adapter has it."""
    from duho.logging import add_logging_level

    add_logging_level("TRACE", 5)
    adapter = _HostLogger(logging.getLogger("pytruenas.test.trace"), {"name": "nas1"})
    with caplog.at_level(5, logger="pytruenas.test.trace"):
        adapter.trace("hello")
    assert [r.getMessage() for r in caplog.records] == ["[nas1] hello"]


def test_the_cli_fanout_label_is_not_repeated_by_the_host_logger():
    """The CLI fans out over connection strings and labels them by host name."""
    from duho.fanout import current_label, current_target

    adapter = _HostLogger(logging.getLogger("pytruenas.test"), {"name": "nas1:8443"})
    for target, label, expected in (
        ("wss://root:hunter2@nas1:8443", "nas1:8443", "plain"),
        ("wss://nas2", "nas2", "[nas1:8443] plain"),
    ):
        tokens = current_target.set(target), current_label.set(label)
        try:
            assert adapter.process("plain", {})[0] == expected
        finally:
            current_label.reset(tokens[1])
            current_target.reset(tokens[0])


def test_call_trace_never_carries_a_password(caplog):
    """The per-call TRACE record rendered raw args: auth.login(user, password)
    and the private key install_sshcreds uploads reached any log at TRACE."""
    from unittest.mock import MagicMock

    host = TrueNASClient("wss://nas1", autologin=False)
    host._conn = MagicMock(_closed=MagicMock(is_set=lambda: False))
    with caplog.at_level(5, logger=host.logger.logger.name):
        host.api.auth.login("root", "hunter2")
        host.api.keychaincredential.create(
            {"attributes": {"private_key": "PEM-SECRET"}}
        )
    rendered = [r.getMessage() for r in caplog.records if r.levelno == 5]
    assert rendered and not any(
        "hunter2" in r or "PEM-SECRET" in r for r in rendered
    ), rendered
    assert "auth.login" in rendered[0] and "<str>" in rendered[0]


def test_a_callers_logger_adapter_works():
    """The header says an adapter is used as-is, and every API call raised
    `AttributeError: 'LoggerAdapter' object has no attribute 'trace'`."""
    from unittest.mock import MagicMock

    adapter = logging.LoggerAdapter(logging.getLogger("pytruenas.test.mine"), {})
    host = TrueNASClient("wss://nas1", autologin=False)
    host.logger = adapter
    assert host.logger is adapter
    host._conn = MagicMock(_closed=MagicMock(is_set=lambda: False))
    host._conn.call.return_value = "pong"
    assert host.api.core.ping() == "pong"


def test_connection_shares_the_hosts_logger():
    """So a record from the transport layer names the host that owns it."""
    host = TrueNASClient("wss://nas1:8443", autologin=False)
    assert host.logger.extra == {"name": "nas1:8443"}


def test_a_record_inside_a_cli_fan_out_names_its_host_once():
    """The fan-out tags each record with its target at the handler, after the
    host's own prefix: a record from `client.logger` read `[nas1] [nas1] ...`."""
    import io

    from duho.fanout import run_targets

    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    logger = logging.getLogger("pytruenas.test.fanout")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    try:
        host = TrueNASClient("wss://nas1", autologin=False)
        host.logger = logger
        run_targets(lambda target: host.logger.info("hello"), ["nas1"], logger=logger)
    finally:
        logger.removeHandler(handler)
    assert "[nas1] hello" in stream.getvalue()
    assert "[nas1] [nas1]" not in stream.getvalue()
