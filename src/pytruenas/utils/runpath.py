"""RunPath support for ``pytruenas``: duho-native steps, fanned out per target.

A **RunPath** (see :mod:`duho.runpath`) is a directory of numbered ``NN-name.py``
step files run in order. ``pytruenas`` adopts duho 0.4.0's RunPath discovery,
ordering, filename modifiers, and ``--rcopts`` selection wholesale, and fans the
whole directory out once per target (:func:`pytruenas.main._dispatch`) -- giving
each target its own connected :class:`~pytruenas.TrueNASClient`. This restores the
private predecessor's per-target ``RunPathCmd`` capability, which the current
duho-based ``pytruenas`` never had.

Step contract (duho-native)
---------------------------

``pytruenas`` uses duho's native RunPath step form rather than the predecessor's
literal ``run(client, args, logger)`` signature -- every CAPABILITY the
predecessor relied on is preserved, only the parameter shape is duho's:

* a directory's ``__main__.py`` defines ``init(cmd, logger) -> ctx`` -- the
  per-target client builder. ``cmd`` is the parsed command instance for THIS
  fan-out iteration (carrying ``cmd.target``); its return value becomes the
  ``ctx`` handed to every step. Re-export :func:`default_init` as a directory's
  ``init`` to build ``TrueNASClient(cmd.target, ...)`` with no boilerplate.
* each numbered step defines ``main(cmd, ctx)`` (a 2-arg entrypoint) or ``main
  (cmd)`` (1-arg, ctx not needed). ``cmd`` carries the parsed args AND any
  per-target state ``init`` stashed on it (``cmd.context = ...``), reachable by
  every step with no cross-target bleed because ``_dispatch`` copies the instance
  per target. ``ctx`` is whatever ``init`` returned (the per-target client). A
  step logs through ``cmd._logger_`` (present because the RunPath command inherits
  :class:`PyTrueNASRunPathArgs` -> ``LoggingArgs``).

Capabilities preserved from the predecessor (through duho's API): the per-target
client built by ``__main__.py`` ``init``; per-target mutable state stashed on
``cmd`` and read by later steps; filename-modifier + ``--rcopts`` step selection
(``!``/``!strict``/``!enable``) and ``REQUIRED`` ordering; and the whole step
directory running once per target via fan-out. Only the literal step signature
differs (``main(cmd, ctx)`` instead of ``run(client, args, logger)``; the logger
travels on ``cmd`` rather than as a separate parameter).
"""

from __future__ import annotations

import typing as _ty
from logging import Logger as _Logger

from .cmd import PyTrueNASArgs, register_targets
from ..client import TrueNASClient

__all__ = ["default_init", "PyTrueNASRunPathArgs"]


class PyTrueNASRunPathArgs(PyTrueNASArgs):
    """Shared root for RunPath commands: ``PyTrueNASArgs`` + trailing targets.

    ``duho.runpath.register(base=...)`` sets the class every provider-built
    RunPath command ALSO inherits from (alongside duho's own ``RunPathCmd``), so
    its METHODS (not just data fields) reach the parsed instance. This base pulls
    in :class:`PyTrueNASArgs` -- the fan-out methods
    (``_expanded_targets_``/``_config_dict_``) and the target fields the
    per-target ``_dispatch`` fan-out needs on the parsed instance -- plus, via
    ``LoggingArgs``, the ``_logger_``/``_set_loglevels_`` a step reads off
    ``cmd``.

    Using bare :class:`PyTrueNASArgs` leaves the ``targets`` field
    ``argparse.SUPPRESS``-ed -- so no trailing ``TARGET`` positional is
    registered on a class command's parser (module commands add it imperatively
    in their own ``register`` hook, which a class command has no equivalent of).
    This subclass closes that gap by overriding :meth:`_initparser_` to add the
    trailing ``targets`` positional LAST, after the RunPath command's own fields
    (``--rcopts`` etc.), exactly as :func:`pytruenas.utils.cmd.register_targets`
    does for a module command -- keeping ``pytruenas <flow> <host>...`` grammar
    uniform across command kinds.
    """

    @classmethod
    def _initparser_(cls, parser, *args, **kwargs):  # type: ignore[override]
        result = super()._initparser_(parser, *args, **kwargs)
        # Add the trailing positional only once (a parents=/re-entrant build may
        # revisit the same parser); register_targets would otherwise duplicate it.
        if not any(action.dest == "targets" for action in parser._actions):
            register_targets(parser)
        return result


def default_init(cmd: "_ty.Any", logger: "_Logger") -> "TrueNASClient":
    """Build the per-target :class:`~pytruenas.TrueNASClient` for a RunPath ``ctx``.

    The duho-native ``__main__.py`` ``init(cmd, logger)`` hook. ``cmd`` is the
    parsed RunPath command instance for one target
    (:func:`pytruenas.main._dispatch` has set ``cmd.target`` to this fan-out
    iteration's target). Returns a :class:`TrueNASClient` connected to that
    target, honoring ``cmd.sslverify`` (defaulting to ``False`` if absent) -- the
    same client :func:`pytruenas.main._run_module_on_target` builds for a plain
    module command, and the ``ctx`` every 2-arg step (``main(cmd, ctx)``)
    receives. Re-export it as a directory's ``init`` (``from
    pytruenas.utils.runpath import default_init as init``) to skip the
    boilerplate; a directory needing per-target state for later steps can wrap it
    (``def init(cmd, logger): c = default_init(cmd, logger); cmd.context = ...;
    return c``).
    """
    return TrueNASClient(cmd.target, sslverify=getattr(cmd, "sslverify", False))
