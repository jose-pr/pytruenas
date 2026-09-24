"""Per-target setup for the ``provision`` RunPath flow.

This flow is **dry-run by default**. Every step describes what it would change
and changes nothing until you pass ``--apply``::

    pytruenas --cmdspath examples provision nas1              # plan only
    pytruenas --cmdspath examples provision nas1 -- --apply   # do it

``--apply`` arrives after a literal ``--`` for the same reason ``call``'s fields
do: a RunPath command's own options are duho's (``--rcopts`` and friends), and
everything after the separator reaches the parsed instance as
``cmd._passthrough_`` without colliding with the global flags.

``init`` stashes a :class:`Plan` on ``cmd``. Steps call ``cmd.plan.change(...)``
instead of mutating directly, which is what makes the whole flow safe to read
before it is safe to run -- and because the fan-out copies the command instance
per target, one target's plan cannot leak into another's.
"""

from __future__ import annotations

from pytruenas.utils.runpath import default_init


class Plan:
    """Collects intended changes, and performs them only when applying.

    The point is not ceremony: a provisioning script that cannot be read before
    it is run is a script nobody runs twice. Each entry is a one-line summary
    plus a thunk, so the dry run prints exactly the work the apply would do.
    """

    def __init__(self, apply: bool, logger):
        self.apply = apply
        self.logger = logger
        self.changed: "list[str]" = []
        self.unchanged: "list[str]" = []

    def change(self, summary: str, action=None):
        """Record (and when applying, perform) one change."""
        if not self.apply:
            self.logger.info("WOULD %s", summary)
            self.changed.append(summary)
            return None
        self.logger.info("%s", summary)
        result = action() if action is not None else None
        self.changed.append(summary)
        return result

    def ok(self, summary: str):
        """Record something already in the desired state."""
        self.logger.info("ok: %s", summary)
        self.unchanged.append(summary)

    def report(self):
        verb = "applied" if self.apply else "planned"
        self.logger.info(
            "%d change(s) %s, %d already correct",
            len(self.changed),
            verb,
            len(self.unchanged),
        )
        if not self.apply and self.changed:
            self.logger.info("re-run with `-- --apply` to make these changes")


def init(cmd, logger):
    client = default_init(cmd, logger)
    tokens = list(getattr(cmd, "_passthrough_", None) or [])
    unknown = [t for t in tokens if t not in ("--apply", "apply")]
    if unknown:
        # Refused rather than ignored: a typo'd flag must not look like a
        # successful dry run.
        raise SystemExit(f"provision: unknown argument(s) after --: {unknown}")
    cmd.plan = Plan(apply=bool(tokens), logger=logger)
    if not cmd.plan.apply:
        logger.info("dry run -- nothing will be changed (pass `-- --apply` to act)")
    return client


def success(ctx, cmd, logger):
    cmd.plan.report()
