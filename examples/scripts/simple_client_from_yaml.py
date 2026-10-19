"""Build a client from a small YAML file.

One way to wire a config file to a client, for copying into your own tool.
If you want config loading, targets, fan-out and logging handled for you, use
the CLI (``pytruenas call ...``) or write a command module instead -- see the
"Commands" guide.

Run it::

    python examples/scripts/simple_client_from_yaml.py [path/to/config.yaml]

Config format::

    host: nas.example.com        # omit, or 'localhost', for the local socket
    username: root               # optional
    password: secret             # optional
    sslverify: false             # optional: true (default), false, or a CA file
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from pytruenas import TrueNASClient

LOGGER = logging.getLogger(__name__)

#: Searched in order; the first that exists wins.
DEFAULT_LOCATIONS = (
    Path("./pytruenas.yaml"),
    Path.home() / ".pytruenas.yaml",
)


def load_config(*locations: Path) -> "tuple[dict, Path | None]":
    """Return ``(config, path)`` for the first file that exists."""
    import yaml  # the optional 'config' extra

    for candidate in locations or DEFAULT_LOCATIONS:
        if candidate and candidate.exists():
            return yaml.safe_load(candidate.read_bytes()) or {}, candidate
    return {}, None


def client_from_config(config: dict) -> TrueNASClient:
    """Build a client from ``host``/``username``/``password``/``sslverify``
    keys."""
    host = config.get("host")
    username = config.get("username")
    password = config.get("password")
    # Certificates are verified unless the file says otherwise: a NAS with
    # its default self-signed certificate needs `sslverify: false` or a CA file.
    sslverify = config.get("sslverify", True)

    credentials = (username, password) if username and password else None
    # A local target resolves to the middleware unix socket, which needs no
    # credentials -- passing the host name would take the websocket instead.
    target = None if not host or host == "localhost" else host

    LOGGER.info("Connecting to %s", target or "the local middleware socket")
    return TrueNASClient(target, credentials, sslverify=sslverify)


def main(argv: "list[str] | None" = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)-7s %(message)s")
    argv = list(sys.argv[1:] if argv is None else argv)

    locations = (Path(argv[0]),) if argv else DEFAULT_LOCATIONS
    config, path = load_config(*locations)
    if path is None:
        LOGGER.error(
            "No config file found (looked in: %s)",
            ", ".join(str(p) for p in locations),
        )
        return 1
    LOGGER.info("Using %s", path)

    with client_from_config(config) as nas:
        info = nas.api.system.info()
        print(f"{info['hostname']} -- TrueNAS {info['version']}, {info['cores']} cores")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
