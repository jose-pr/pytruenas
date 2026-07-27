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

from hostctl.host import HostConfig, PosixHost  # noqa: E402
from hostctl.shell import POSIX_SHELL  # noqa: E402

from pytruenas.host import TrueNASConfig, TrueNASHost  # noqa: E402
from pytruenas.providers import TnasWsPathProvider  # noqa: E402


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


def test_webshell_can_be_turned_off():
    """With it declined, a remote host without SSH has no executor at all."""
    host = TrueNASHost(
        TrueNASConfig.from_target("wss://nas", webshell=False), client=MagicMock()
    )
    assert _names(host._executor_selector.providers) == []


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


def test_remote_without_ssh_or_webshell_reports_no_run():
    """With the web shell declined, the honest answer is still "no run"."""
    host = TrueNASHost(
        TrueNASConfig.from_target("wss://nas", webshell=False), client=MagicMock()
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
