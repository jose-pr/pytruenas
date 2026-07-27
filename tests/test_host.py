"""``TrueNASHost`` -- provider composition (step 4 of the migration).

The point of this step is that the *generic* half is inherited: ``run``,
``path``, ``spawn``, ``info``, ``connect``, ``close`` and the shell all come
from :class:`hostctl.host.PosixHost`. What is tested here is therefore the
composition -- which providers exist, in what order, and what the host declines
when a transport is absent -- rather than re-testing hostctl's own dispatch.
"""

from unittest.mock import MagicMock

import pytest

pytest.importorskip("hostctl")

from hostctl.host import HostConfig, PosixHost, SshConfig  # noqa: E402
from hostctl.shell import POSIX_SHELL  # noqa: E402

from pytruenas.host import (  # noqa: E402
    DEFAULT_SOCKET_PATH,
    TrueNASConfig,
    TrueNASHost,
)
from pytruenas.providers import TnasWsPathProvider  # noqa: E402

#: A minimal SSH leg, for the cases that need one to exist.
SSH = SshConfig(host="nas")


def _host(target="wss://nas", **options):
    return TrueNASHost(TrueNASConfig.from_target(target), client=MagicMock(), **options)


def _names(providers):
    return [item.name for item in providers]


# -- identity --------------------------------------------------------------


def test_is_a_posix_host():
    host = _host()
    assert isinstance(host, PosixHost)
    assert host.system_family == "posix"
    assert host.shell_flavour is POSIX_SHELL


def test_config_round_trips_onto_the_host():
    host = _host("wss://nas:444/api/current")
    assert host.scheme == "truenas+wss"
    assert host.connection_uri == "truenas+wss://nas:444/api/current"


def test_config_creates_the_host():
    config = TrueNASConfig.from_target("wss://nas")
    assert isinstance(config._create_host(), TrueNASHost)


def test_dispatches_from_a_uri():
    host = HostConfig("truenas+wss://nas")._create_host()
    assert isinstance(host, TrueNASHost)


# -- construction from a connection string ---------------------------------


def test_constructs_from_a_connection_string():
    """`TrueNASHost("wss://nas")` -- no need to build a config first.

    hostctl's own `Host("uri")` shortcut cannot cover this: its metaclass only
    intercepts when `cls is Host`, so a subclass falls through to normal
    construction.
    """
    host = TrueNASHost("wss://nas")
    assert isinstance(host, TrueNASHost)
    assert host.connection_uri == "truenas+wss://nas"


@pytest.mark.parametrize(
    "target, expected",
    [
        ("wss://nas", "truenas+wss://nas"),
        ("nas", "truenas+auto://nas"),
        ("https://nas", "truenas+wss://nas"),
        (None, f"truenas+unix://{DEFAULT_SOCKET_PATH}"),
    ],
)
def test_string_construction_accepts_every_target_form(target, expected):
    assert TrueNASHost(target).connection_uri == expected


def test_string_construction_takes_config_options():
    host = TrueNASHost("wss://nas", ssh=SSH, executor=["ssh"])
    assert _names(host._executor_selector.providers) == ["ssh"]
    # The selectors are independent: overriding one leaves the other default.
    assert _names(host._path_selector.providers) == ["sftp", "tnasws"]


def test_string_construction_takes_credentials():
    from pytruenas.auth import ApiKeyAuth

    host = TrueNASHost("wss://nas", credentials="1-" + "a" * 64)
    assert isinstance(host._config.credentials, ApiKeyAuth)


def test_an_existing_config_is_used_as_is():
    config = TrueNASConfig.from_target("wss://nas")
    assert TrueNASHost(config)._config is config


def test_config_options_alongside_a_config_are_rejected():
    """Silently ignoring them would be the worst outcome.

    The config is already built, so a late `executor=` could not take effect;
    saying so beats letting a caller believe it did.
    """
    config = TrueNASConfig.from_target("wss://nas")
    with pytest.raises(TypeError, match="may not be combined"):
        TrueNASHost(config, executor=["ssh"])


def test_every_client_setting_is_reachable():
    """`TrueNASHost` must be able to express whatever `TrueNASClient` can.

    Checked against the real signature so a new client setting cannot be added
    without either surfacing here or failing this test. `target` and `creds`
    differ only in spelling (positional, and `credentials=`); `fsbackend` is
    superseded by the finer-grained `path=` override.
    """
    import inspect

    from pytruenas import TrueNASClient
    from pytruenas.host import TrueNASConfig as _Config

    equivalents = {"target", "creds", "fsbackend"}
    config_params = set(inspect.signature(_Config.__init__).parameters)

    for name, parameter in inspect.signature(TrueNASClient.__init__).parameters.items():
        if name in ("self", *equivalents):
            continue
        assert name in config_params, f"{name} is not reachable from TrueNASHost"
        assert (
            parameter.default
            == inspect.signature(_Config.__init__).parameters[name].default
        ), f"{name} default differs"


@pytest.mark.parametrize(
    "shell, expected",
    [
        ("ssh://root@nas", ("nas", 22, "root")),
        ("ssh://admin@nas:2222", ("nas", 2222, "admin")),
        ("nas", ("nas", 22, "root")),
    ],
)
def test_shell_string_builds_the_ssh_leg(shell, expected):
    """`shell=` takes the connection string the client always took.

    Requiring a prebuilt SshConfig for the common case would be a step
    backwards from `TrueNASClient(shell="ssh://root@nas")`.
    """
    config = TrueNASConfig.from_target("wss://nas", shell=shell)
    assert (config.ssh.host, config.ssh.port, config.ssh.username) == expected


def test_shell_string_unpacks_the_legacy_client_keys_form():
    """`client_keys|root` was a string hack; SshConfig has a real field."""
    config = TrueNASConfig.from_target(
        "wss://nas", shell="ssh://client_keys|root:PRIVATEKEY@nas"
    )
    assert config.ssh.username == "root"
    assert config.ssh.client_keys == [b"PRIVATEKEY"]
    assert config.ssh.password is None


def test_autologin_and_logger_reach_the_client(monkeypatch):
    import requests

    monkeypatch.setattr(
        requests,
        "get",
        lambda *a, **k: pytest.fail("built the client over the network"),
    )
    host = TrueNASHost("wss://nas", autologin=False, logger="mylog")
    assert host.client.autologin is False
    assert host.client.logger.name == "mylog"


def test_ssh_property_raises_clearly_without_a_transport():
    with pytest.raises(RuntimeError, match="no SSH transport"):
        _host().ssh


def test_host_options_still_reach_systemhost():
    """`info=` and friends belong to SystemHost, not the config."""
    from hostctl.host import HostInfo

    host = TrueNASHost("wss://nas", info=HostInfo(hostname="pinned"))
    assert host.info().hostname == "pinned"


# -- provider composition --------------------------------------------------


def test_without_ssh_the_webshell_stands_in():
    """A remote host with no SSH still gets a command channel.

    The web shell is the last resort for a remote target, so it only ever
    serves a host that would otherwise have no executor at all -- which is
    exactly the NAT/firewall case it exists for.
    """
    host = _host()
    assert _names(host._executor_selector.providers) == ["webshell"]
    assert _names(host._path_selector.providers) == ["tnasws"]


def _built(target="wss://nas", **options):
    return TrueNASHost(TrueNASConfig.from_target(target, **options), client=MagicMock())


# -- explicit provider overrides -------------------------------------------
#
# `executor=`/`path=` name the providers to use, in preference order. They
# replaced a `webshell: bool` flag, which was only ever one hardcoded case of
# this -- `executor=["ssh"]` says the same thing, and also expresses "SSH
# only", "force the web shell", or any other combination.


def test_executor_override_forces_a_single_provider():
    host = _built(ssh=SSH, executor="ssh")
    assert _names(host._executor_selector.providers) == ["ssh"]


def test_path_override_forces_a_single_provider():
    host = _built(ssh=SSH, path=["tnasws"])
    assert _names(host._path_selector.providers) == ["tnasws"]


def test_override_can_reorder_preference():
    """Order is the caller's, not ours -- webshell can be made to outrank SSH."""
    host = _built(ssh=SSH, executor=["webshell", "ssh"])
    assert _names(host._executor_selector.providers) == ["webshell", "ssh"]


def test_excluding_the_webshell_leaves_a_host_with_no_executor():
    """What the old `webshell=False` did, now expressible without a flag."""
    host = _built(executor=[])
    assert _names(host._executor_selector.providers) == []
    assert "run" not in host.capabilities


def test_override_can_add_tnasws_to_a_local_target():
    """Forcing the websocket leg locally, e.g. to exercise it in a test.

    It is not offered by default there -- `filesystem.get` routes reads through
    the HTTP side channel, which a unix-socket client cannot reach -- but a
    caller who wants it can ask.
    """
    host = _built(None, path=["local", "tnasws"])
    assert _names(host._path_selector.providers) == ["local", "tnasws"]


def test_unknown_provider_name_is_rejected():
    """A typo must fail loudly, not compose a host with no executor."""
    with pytest.raises(ValueError, match="unknown executor provider"):
        _built(executor=["shh"])
    with pytest.raises(ValueError, match="unknown path provider"):
        _built(path=["sftpp"])


def test_requesting_ssh_without_a_config_is_an_error():
    """Better than silently yielding a host that cannot run anything."""
    with pytest.raises(ValueError, match="no SSH configuration"):
        _built(executor=["ssh"])
    with pytest.raises(ValueError, match="no SSH configuration"):
        _built(path=["sftp"])


def test_ssh_providers_share_one_transport():
    """Both legs must come from a single factory call.

    Two transports would open two connections, only one of which is ever
    closed -- which is why hostctl exposes them as a pair.
    """
    host = _built(ssh=SSH, executor=["ssh"], path=["sftp"])
    executor = host._executor_selector.providers[0]
    path = host._path_selector.providers[0]
    assert executor.transport is path.transport


def test_local_target_uses_only_hostctls_local_providers():
    """On the NAS, plain subprocess and plain local paths -- and nothing else.

    No remote provider is built at all. `tnasws` in particular would be a
    fallback that can only ever fail here: `filesystem.get` routes reads
    through the HTTP side channel, which resolves to https://localhost and
    trips the appliance's self-signed certificate.
    """
    host = TrueNASHost(TrueNASConfig.from_target(None), client=MagicMock())
    assert _names(host._executor_selector.providers) == ["local"]
    assert _names(host._path_selector.providers) == ["local"]


def test_local_target_ignores_an_ssh_config():
    """SSH to reach the machine you are already on is never the right answer."""
    from hostctl.host import SshConfig

    config = TrueNASConfig.from_target(None, ssh=SshConfig(host="nas"))
    host = TrueNASHost(config, client=MagicMock())
    assert _names(host._executor_selector.providers) == ["local"]
    assert _names(host._path_selector.providers) == ["local"]


def test_with_ssh_the_ssh_providers_come_first():
    """SSH must outrank the middleware -- it is the only remote exec channel,
    and its path surface (symlink/rename/realpath) is richer."""
    from hostctl.host import SshConfig

    host = TrueNASHost(
        TrueNASConfig.from_target("wss://nas", ssh=SshConfig(host="nas")),
        client=MagicMock(),
    )
    assert _names(host._executor_selector.providers) == ["ssh", "webshell"]
    assert _names(host._path_selector.providers) == ["sftp", "tnasws"]


def test_provider_types():
    host = _host()
    assert isinstance(host._path_selector.providers[0], TnasWsPathProvider)


# -- capabilities are reported truthfully ----------------------------------


def test_remote_without_ssh_still_has_run_via_the_webshell():
    """The gap step 3 exposed is closed by the web shell.

    Before it existed, a remote host with no SSH had *no* executor: the
    JSON-RPC API offers no remote command execution. `/_shell` is a real
    channel on the same port, so `run` is available again.
    """
    host = _host("wss://nas")
    assert "run" in host.capabilities
    assert "path" in host.capabilities


def test_remote_without_any_executor_reports_no_run():
    """With every executor excluded, the honest answer is "no run"."""
    host = TrueNASHost(
        TrueNASConfig.from_target("wss://nas", executor=[]), client=MagicMock()
    )
    assert "run" not in host.capabilities
    # Paths still work -- the websocket serves those.
    assert "path" in host.capabilities


def test_local_target_reports_run():
    host = TrueNASHost(TrueNASConfig.from_target(None), client=MagicMock())
    assert "run" in host.capabilities


def test_remote_with_ssh_reports_run():
    from hostctl.host import SshConfig

    host = TrueNASHost(
        TrueNASConfig.from_target("wss://nas", ssh=SshConfig(host="nas")),
        client=MagicMock(),
    )
    assert "run" in host.capabilities


# -- the TrueNAS surface delegates to the client ---------------------------


@pytest.mark.parametrize(
    "method, args",
    [
        ("ping", ()),
        ("me", ()),
        ("logout", ()),
        ("dump_api", ()),
        ("subscribe", ("alert.list",)),
    ],
)
def test_api_surface_delegates_to_the_client(method, args):
    client = MagicMock()
    host = TrueNASHost(TrueNASConfig.from_target("wss://nas"), client=client)
    getattr(host, method)(*args)
    getattr(client, method).assert_called_once_with(*args)


def test_api_property_is_the_clients_namespace():
    client = MagicMock()
    host = TrueNASHost(TrueNASConfig.from_target("wss://nas"), client=client)
    assert host.api is client.api
    assert host.websocket is client.websocket


def test_close_tears_down_the_websocket_after_the_providers():
    client = MagicMock()
    host = TrueNASHost(TrueNASConfig.from_target("wss://nas"), client=client)
    host.close()
    client._conn.close.assert_called_once()


def test_close_survives_a_websocket_that_raises():
    # close() must be safe to call repeatedly and must not mask provider errors.
    client = MagicMock()
    client._conn.close.side_effect = RuntimeError("already gone")
    host = TrueNASHost(TrueNASConfig.from_target("wss://nas"), client=client)
    host.close()


# -- install_sshcreds wires a real SshConfig -------------------------------

PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\nfake\n-----END PRIVATE KEY-----"


def _host_with_client_key():
    client = MagicMock()
    client.install_sshcreds.return_value = PRIVATE_KEY
    host = TrueNASHost(TrueNASConfig.from_target("wss://nas"), client=client)
    return host, client


def test_install_sshcreds_creates_an_ssh_config():
    """The `client_keys|root` string encoding is gone -- it is a real field."""
    from hostctl.host import SshConfig

    host, _ = _host_with_client_key()
    assert host._config.ssh is None
    host.install_sshcreds()

    ssh = host._config.ssh
    assert isinstance(ssh, SshConfig)
    assert ssh.host == "nas"
    assert ssh.username == "root"
    assert ssh.client_keys == [PRIVATE_KEY.encode()]


def test_install_sshcreds_rebuilds_the_providers():
    """Gaining an SSH transport must change what the host can do.

    Before: a remote host with no SSH has no executor at all. After: it does.
    """
    host, _ = _host_with_client_key()
    assert _names(host._executor_selector.providers) == ["webshell"]
    assert _names(host._path_selector.providers) == ["tnasws"]

    host.install_sshcreds()

    # SSH is now available and outranks the web shell, and paths gain the
    # richer SFTP leg -- neither of which existed a moment ago.
    assert _names(host._executor_selector.providers) == ["ssh", "webshell"]
    assert _names(host._path_selector.providers) == ["sftp", "tnasws"]
    assert "run" in host.capabilities


def test_install_sshcreds_does_not_override_explicit_credentials():
    from hostctl.host import SshConfig

    client = MagicMock()
    client.install_sshcreds.return_value = PRIVATE_KEY
    config = TrueNASConfig.from_target(
        "wss://nas", ssh=SshConfig(host="nas", password="hunter2")
    )
    host = TrueNASHost(config, client=client)
    host.install_sshcreds()
    assert config.ssh.password == "hunter2"
    assert config.ssh.client_keys is None


def test_install_sshcreds_fills_an_ssh_config_lacking_auth():
    from hostctl.host import SshConfig

    client = MagicMock()
    client.install_sshcreds.return_value = PRIVATE_KEY
    config = TrueNASConfig.from_target("wss://nas", ssh=SshConfig(host="nas"))
    host = TrueNASHost(config, client=client)
    host.install_sshcreds()
    assert config.ssh.client_keys == [PRIVATE_KEY.encode()]


def test_install_sshcreds_forwards_arguments():
    host, client = _host_with_client_key()
    host.install_sshcreds(name="custom", private_key=PRIVATE_KEY)
    client.install_sshcreds.assert_called_once_with(
        name="custom", private_key=PRIVATE_KEY
    )


# -- construction stays offline -------------------------------------------


def test_building_a_host_does_no_network_io(monkeypatch):
    import requests

    def explode(*args, **kwargs):
        raise AssertionError("host construction performed network I/O")

    monkeypatch.setattr(requests, "get", explode)
    monkeypatch.setattr(requests, "post", explode)
    TrueNASHost(TrueNASConfig.from_target("wss://nas"), client=MagicMock())
    TrueNASHost(TrueNASConfig.from_target("nas"), client=MagicMock())
