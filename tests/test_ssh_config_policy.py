"""The SSH leg built from ``shell=`` reads the user's ``~/.ssh/config``.

Precedence is the one ``ssh`` has, plus TrueNAS's administrative login as the
last default: a user or port in ``shell`` wins over the file's ``User``/``Port``,
the file wins over ``root`` and 22. The file is the fake home's
(``tests/conftest.py``), and the server is asyncssh on 127.0.0.1, which records
the user each login asked for.
"""

import asyncio
import threading

import pytest

from pytruenas import TrueNASClient
from pytruenas.host import TrueNASConfig

pytestmark = pytest.mark.requires("asyncssh")


@pytest.fixture(scope="module")
def server():
    """An SSH server that lets anyone in and records each login's user."""
    import asyncssh

    logins = []

    class _Server(asyncssh.SSHServer):
        def begin_auth(self, username):
            logins.append(username)
            return False

    loop = asyncio.new_event_loop()
    thread = threading.Thread(target=loop.run_forever, daemon=True)
    thread.start()

    async def start():
        key = asyncssh.generate_private_key("ssh-ed25519")
        return await asyncssh.listen(
            "127.0.0.1", 0, server_host_keys=[key], server_factory=_Server
        )

    listener = asyncio.run_coroutine_threadsafe(start(), loop).result(30)
    port = listener.sockets[0].getsockname()[1]
    try:
        yield port, logins
    finally:
        listener.close()
        asyncio.run_coroutine_threadsafe(listener.wait_closed(), loop).result(30)
        loop.call_soon_threadsafe(loop.stop)
        thread.join(30)
        loop.close()


def _login_user(server, shell):
    """The user the server saw when ``shell=`` connected."""
    _, logins = server
    client = TrueNASClient("wss://nas", autologin=False, shell=shell, verify=False)
    try:
        del logins[:]
        client.ssh
        return logins[-1]
    finally:
        client.close()


def _write_config(home, text):
    (home / ".ssh" / "config").write_bytes(text.encode())


def test_an_alias_takes_hostname_port_and_user_from_the_file(server, fake_home):
    port, _ = server
    _write_config(
        fake_home, f"Host nasalias\n  HostName 127.0.0.1\n  Port {port}\n  User admin\n"
    )
    assert _login_user(server, "nasalias") == "admin"


def test_with_no_user_anywhere_the_login_is_root(server, fake_home):
    port, _ = server
    _write_config(fake_home, f"Host nasalias\n  HostName 127.0.0.1\n  Port {port}\n")
    assert _login_user(server, "nasalias") == "root"


def test_a_user_in_shell_wins_over_the_file(server, fake_home):
    port, _ = server
    _write_config(
        fake_home, f"Host nasalias\n  HostName 127.0.0.1\n  Port {port}\n  User admin\n"
    )
    assert _login_user(server, "ssh://ops@nasalias") == "ops"


def test_a_port_in_shell_wins_over_the_file(server, fake_home):
    port, _ = server
    _write_config(fake_home, "Host 127.0.0.1\n  Port 1\n  User admin\n")
    assert _login_user(server, f"127.0.0.1:{port}") == "admin"


def test_without_a_config_file_the_login_is_root(server):
    port, _ = server
    assert _login_user(server, f"127.0.0.1:{port}") == "root"


def test_no_port_in_shell_leaves_it_to_the_config():
    """``None`` is hostctl's "the config's Port, else 22"."""
    config = TrueNASConfig.from_target("wss://nas", shell="nas")
    assert config.ssh.port is None
    assert config.ssh.username is None
