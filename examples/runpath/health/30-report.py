"""Step 3 -- duho's native signature, for contrast.

No ``@step`` here: this is the shape duho calls a step with by default,
``main(cmd, ctx)`` -- the command first, the client second as ``ctx``, and the
logger reached through ``cmd._logger_`` rather than passed in.

Both forms work in the same directory. ``@step`` is opt-in, for when you want
the module-command signature; nothing about the native shape changed.
"""

from __future__ import annotations


def main(cmd, ctx):
    logger = cmd._logger_

    if not cmd.findings:
        logger.info("no findings for %s", cmd.target)
        return

    for kind, detail in cmd.findings:
        logger.info("%s: %s", kind, detail)
