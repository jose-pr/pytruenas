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

A step that would rather use the MODULE command signature -- ``run(client, args,
logger)``, client first, logger as a real parameter -- can decorate its
entrypoint with :func:`step`, which adapts the two shapes so the same body works
in either command kind. Without it, writing a step that way fails at runtime:
duho passes exactly two positionals, in the other order.

Capabilities preserved from the predecessor (through duho's API): the per-target
client built by ``__main__.py`` ``init``; per-target mutable state stashed on
``cmd`` and read by later steps; filename-modifier + ``--rcopts`` step selection
(``!``/``!strict``/``!enable``) and ``REQUIRED`` ordering; and the whole step
directory running once per target via fan-out. Only the literal step signature
differs (``main(cmd, ctx)`` instead of ``run(client, args, logger)``; the logger
travels on ``cmd`` rather than as a separate parameter).
"""

from __future__ import annotations

import functools as _functools
import inspect as _inspect
import typing as _ty
from logging import Logger as _Logger

from .cmd import PyTrueNASArgs, register_targets
from ..host import TrueNASHost as TrueNASClient

__all__ = ["default_init", "PyTrueNASRunPathArgs", "step"]


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


#: Marks a callable as already wrapped by :func:`step`, so the automatic
#: adapter does not wrap it a second time (which would feed the wrapper's own
#: ``(cmd, ctx)`` signature back in as if it were ``(client, args)``).
_ADAPTED = "_pytruenas_step_adapted_"


def step_adapter(
    entrypoint: "_ty.Callable[..., object]",
) -> "_ty.Callable[..., object]":
    """duho ``register(step_adapter=...)`` hook: auto-apply :func:`step`.

    Installed once by :mod:`pytruenas.main`, so a step written with the module
    command signature works with no decorator and no import in the step file.

    Only a **3-argument** step is adapted automatically, plus anything already
    decorated with :func:`step`. Three positionals is unambiguous -- duho never
    calls a step with more than two, so such a step is broken as-is and can
    only have meant ``(client, args, logger)``.

    A 1- or 2-arg step is left alone, deliberately: ``(cmd, ctx)`` is duho's
    own contract and ``(client, args)`` is this app's, and nothing in the
    signature distinguishes them. Guessing would silently swap a caller's two
    arguments, which is worse than the explicit ``@step`` that shorter
    signatures still have.
    """
    if getattr(entrypoint, _ADAPTED, False):
        return entrypoint
    if _positional_count(entrypoint) >= 3:
        return step(entrypoint)
    return entrypoint


def _positional_count(entrypoint: "_ty.Callable[..., object]") -> int:
    """How many of ``(client, args, logger)`` a decorated step will accept.

    Capped at 3 -- the full module-command signature -- and 3 for a ``*args``
    catch-all, which can take all of them. Falls back to 3 when the signature
    cannot be introspected, matching the documented shape rather than silently
    dropping the logger.
    """
    try:
        params = _inspect.signature(entrypoint).parameters
    except (TypeError, ValueError):  # pragma: no cover - builtins/C callables
        return 3
    count = 0
    for param in params.values():
        if param.kind is _inspect.Parameter.VAR_POSITIONAL:
            return 3
        if param.kind in (
            _inspect.Parameter.POSITIONAL_ONLY,
            _inspect.Parameter.POSITIONAL_OR_KEYWORD,
        ):
            count += 1
    return min(count, 3)


def step(entrypoint: "_ty.Callable[..., object]") -> "_ty.Callable[..., object]":
    """Let a RunPath step use the module command signature ``(client, args, logger)``.

    The two command kinds otherwise disagree on the shape of the same three
    values. A module command's entrypoint is ``run(client, args, logger)``;
    duho calls a step ``main(cmd, ctx)`` -- the client second (as ``ctx``)
    rather than first, and no logger at all. So the same body cannot move
    between a ``NN-step.py`` and a ``cmd/`` module without being rewritten, and
    writing a step with the module signature fails at *runtime*, not import:
    duho supplies exactly two positionals, so the third is a ``TypeError`` and
    the first two silently bind in the wrong order.

    Decorating with ``@step`` closes that gap::

        from pytruenas.utils.runpath import step

        @step
        def main(client, args, logger):
            logger.info("%s", client.api.system.info())

    ``client`` is the ``ctx`` built by the directory's ``init``
    (:func:`default_init` unless overridden), ``args`` is the per-target ``cmd``
    instance, and ``logger`` is ``cmd._logger_`` -- the same logger duho hands a
    module command, already ``[target]``-prefixed by the fan-out. A step may
    declare fewer parameters (``(client, args)`` or ``(client)``) and is handed
    only those.

    ``__wrapped__`` is explicitly cleared after :func:`functools.wraps`: it makes
    ``inspect.signature`` report the *decorated* function's signature instead of
    the wrapper's, and duho decides the call arity from exactly that. Left in
    place, a ``@step``-decorated ``main(client)`` reports one positional, duho
    takes the 1-arg branch, and the step is handed ``ctx=None`` -- a client that
    is silently ``None`` rather than an error. The name and docstring that
    ``wraps`` copies are still wanted for tracebacks; only the signature link is
    harmful.

    A 1-arg or 2-arg duho-native step needs no decorator -- ``main(cmd, ctx)``
    still works untouched, and this is purely opt-in.
    """
    wants = _positional_count(entrypoint)

    @_functools.wraps(entrypoint)
    def _adapter(cmd, ctx=None):
        # `_logger_` comes from LoggingArgs via PyTrueNASRunPathArgs, so it is
        # present on any step reached through a pytruenas RunPath command.
        # Truncated to the arity the step actually declares, the same way duho
        # trims its own step call: a step that ignores the logger (or the args)
        # should not have to name a parameter just to be callable.
        return entrypoint(*(ctx, cmd, getattr(cmd, "_logger_", None))[:wants])

    # See the docstring: this must go, or arity detection reads through it.
    del _adapter.__wrapped__
    setattr(_adapter, _ADAPTED, True)
    return _adapter


def default_init(cmd: "_ty.Any", logger: "_Logger") -> "TrueNASClient":
    """Build the per-target :class:`~pytruenas.TrueNASClient` for a RunPath ``ctx``.

    The duho-native ``__main__.py`` ``init(cmd, logger)`` hook. ``cmd`` is the
    parsed RunPath command instance for one target
    (:func:`pytruenas.main._dispatch` has set ``cmd.target`` to this fan-out
    iteration's target). Returns a :class:`TrueNASClient` connected to that
    target, honoring ``cmd.sslverify`` -- the
    same client :func:`pytruenas.main._run_module_on_target` builds for a plain
    module command, and the ``ctx`` every 2-arg step (``main(cmd, ctx)``)
    receives. Re-export it as a directory's ``init`` (``from
    pytruenas.utils.runpath import default_init as init``) to skip the
    boilerplate; a directory needing per-target state for later steps can wrap it
    (``def init(cmd, logger): c = default_init(cmd, logger); cmd.context = ...;
    return c``).
    """
    # `cmd.sslverify` is read directly rather than via getattr: every RunPath
    # command inherits PyTrueNASRunPathArgs -> PyTrueNASArgs, so the field is
    # always present. A `getattr(..., False)` fallback would turn a missing
    # field into "silently stop verifying TLS", which is the wrong direction to
    # fail -- and would hide the real error (a command built off the wrong base).
    return TrueNASClient(cmd.target, sslverify=cmd.sslverify)
