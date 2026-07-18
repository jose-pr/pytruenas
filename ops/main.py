# Cleaned ops module – generic utilities for pytruenas
"""General‑purpose utility helpers for the pytruenas client.
This module provides a small wrapper to create a :class:`pytruenas.client.TrueNASClient`
instance from a minimal configuration dictionary.
"""

from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import Any, Dict

import yaml

from pytruenas import TrueNASClient

LOGGER = logging.getLogger(__name__)


def _load_config(*searchpaths: Path) -> tuple[Dict[str, Any], Path | None]:
    """Load the first existing YAML configuration file.
    Returns a tuple of ``(config, path)`` where ``config`` is a dict (empty if no file
    was found) and ``path`` is the Path object that was read or ``None``.
    """
    for p in searchpaths:
        if p and p.exists():
            return yaml.safe_load(p.read_bytes()) or {}, p
    return {}, None


def init(config_path: str | None = None) -> TrueNASClient:
    """Create a :class:`~pytruenas.client.TrueNASClient` using a simple config.

    performed a lot of boot‑strapping (user creation, SSH key handling, etc.).
    For a generic library we only need to know the target host and optional
    credentials.

    Parameters
    ----------
    config_path:
        Optional path to a YAML file containing ``host``, ``username`` and
        ``password`` keys. If omitted the function will look for the environment
        variable ``PYTRUENAS_CONFIG`` and then fall back to ``~/.pytruenas.yaml``.

    Returns
    -------
    TrueNASClient
        An authenticated client ready for API calls.
    """
    # Resolve configuration location
    env_path = os.getenv("PYTRUENAS_CONFIG")
    cfg, cfg_path = _load_config(
        Path(config_path) if config_path else None,
        Path(env_path) if env_path else None,
        Path.home() / ".pytruenas.yaml",
    )

    host = cfg.get("host")
    username = cfg.get("username")
    password = cfg.get("password")
    if not host:
        raise ValueError("Configuration must contain a 'host' entry")

    credentials = (username, password) if username and password else None
    LOGGER.info("Creating pytruenas client for host %s", host)
    client = TrueNASClient(host if host != "localhost" else None, credentials, sslverify=False)
    # Perform a simple login – the client will automatically handle the websocket
    client.login()
    return client

