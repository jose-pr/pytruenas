"""Per-target setup for the ``health`` RunPath flow.

``init(cmd, logger)`` runs once per target, before any step. Its return value
becomes the ``ctx`` every step receives -- here, the connected client for this
fan-out iteration.

Re-exporting :func:`~pytruenas.utils.runpath.default_init` is the whole hook for
the common case: it builds ``TrueNASClient(cmd.target, sslverify=cmd.sslverify)``.
This directory wraps it instead, to also stash per-target state on ``cmd`` --
which later steps read back, with no cross-target bleed because the fan-out
copies the command instance per target.
"""

from __future__ import annotations

from pytruenas.utils.runpath import default_init


def init(cmd, logger):
    client = default_init(cmd, logger)
    # Anything stashed on `cmd` is visible to every step for THIS target only.
    cmd.findings = []
    logger.debug("connected to %s", cmd.target)
    return client
