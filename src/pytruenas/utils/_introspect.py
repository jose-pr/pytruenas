"""One answer to "how many positional arguments does this take?".

Three copies of this walk existed -- two here, one private inside duho -- and
they disagreed in the detail that matters: whether a parameter with a default
counts, and what ``*args`` means. Both callers below hand a user-written
callable a fixed argument list, so the answer decides whether an argument lands
in the parameter its author meant.
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
