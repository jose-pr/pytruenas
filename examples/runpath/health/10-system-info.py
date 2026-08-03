"""Step 1 -- the full module-command signature, no decorator needed.

A step may take ``(client, args, logger)``: exactly what a command module's
``run()`` takes, so the same body works in either kind without being rewritten.
Three arguments is unambiguous -- duho never calls a step with more than two --
so pytruenas adapts it automatically. Nothing to import.

All three are used here:

* ``client`` -- the per-target :class:`~pytruenas.TrueNASClient` that
  ``__main__.py`` ``init`` returned (duho's ``ctx``).
* ``args``   -- the parsed command for THIS target: the global options
  (``--sslverify``), this flow's own (``--rcopts``), ``args.target``, and any
  state an earlier hook stashed (``args.findings``).
* ``logger`` -- already ``[target]``-prefixed by the fan-out, so it needs no
  target of its own and honors ``-v``/``-q``/``--logto``.

A step with a SHORTER app-shaped signature (``(client, args)``) is ambiguous --
duho's own steps are ``(cmd, ctx)`` -- so those still need an explicit
``@step``. See ``20-pools.py``.
"""

from __future__ import annotations


def main(client, args, logger):
    info = client.api.system.info()

    logger.info("%s -- TrueNAS %s", info["hostname"], info["version"])
    logger.debug("uptime %s, %s cores", info["uptime"], info["cores"])

    # `args` carries both the parsed options and the per-target state that
    # `__main__.py` stashed; a later step reads what this one appends.
    args.findings.append(("version", info["version"]))
    if args.sslverify:
        logger.debug("TLS verification is on for %s", args.target)
