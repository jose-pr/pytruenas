"""How many positional arguments a user-written callable takes.

The RunPath step adapter hands a step a fixed argument list, so whether a
parameter with a default counts, and what ``*args`` means, decide whether an
argument lands in the parameter its author meant. duho's public
``accepts_positional`` answers a yes/no question; this returns the count.
"""

import inspect as _inspect
import typing as _ty

_POSITIONAL = (
    _inspect.Parameter.POSITIONAL_ONLY,
    _inspect.Parameter.POSITIONAL_OR_KEYWORD,
)


def positional_arity(
    func: "_ty.Callable[..., object]",
    *,
    required_only: bool = False,
    cap: "int | None" = None,
    varargs: "int | None" = None,
    unknown: int = 0,
) -> int:
    """Positional parameters ``func`` accepts.

    ``required_only`` counts only parameters without a default -- what a caller
    must supply. ``varargs`` is the answer for a ``*args`` catch-all (``None``
    counts the named parameters only). ``unknown`` is returned when the
    signature cannot be read at all (a C builtin), so each caller picks the
    safe direction for itself. ``cap`` bounds the result.
    """
    try:
        params = _inspect.signature(func).parameters
    except (TypeError, ValueError):  # pragma: no cover - builtins/C callables
        return unknown
    count = 0
    for param in params.values():
        if param.kind is _inspect.Parameter.VAR_POSITIONAL:
            if varargs is not None:
                return varargs
            continue
        if param.kind not in _POSITIONAL:
            continue
        if required_only and param.default is not _inspect.Parameter.empty:
            continue
        count += 1
    return min(count, cap) if cap is not None else count


__all__ = ["positional_arity"]
