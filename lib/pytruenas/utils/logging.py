import logging as _logging
from logging import *  # type:ignore

import typing as _ty


if _ty.TYPE_CHECKING:
    import colorama as __coloroma

try:
    import colorama as _color  # type: ignore

except ImportError:

    _color = _ty.cast("__coloroma", None)


def _asicode(*codes):
    return "".join(["\033[" + str(c) + "m" for c in codes])

def _getcolor(color:str):
    if color.isalpha() and _color:
        fore, back, *_ = color.split("+") + ["", ""]
        if fore:
            fore: str = getattr(_color.Fore, fore.upper(), "") or ""
        if back:
            back: str = getattr(_color.Back, back.upper(), "") or ""
        color = fore + back

    if color.isalpha():
        return ''
    return color

if not hasattr(_logging, "getLevelNamesMapping"):
    _logging.getLevelNamesMapping = lambda: _logging._nameToLevel.copy()


def add_logging_level(name: str, level: int, force=False, color: str | None = None):
    name = name.upper()
    if hasattr(_logging, name) and not force:
        return
    setattr(_logging, name, level)
    addLevelName(level, name)

    def log_logger(self: Logger, message, *args, **kwargs):
        if self.isEnabledFor(level):
            self._log(level, message, args, **kwargs)

    name = name.lower()
    setattr(getLoggerClass(), name, log_logger)

    def log_root(msg, *args, **kwargs):
        log(level, msg, *args, **kwargs)

    if color is not None:
        DefaultFormatter.COLORS[level] = _getcolor(color)


    setattr(_logging, name, log_root)


class DefaultFormatter(Formatter):  # type:ignore
    COLORS: dict[int, str] = {
        DEBUG: _asicode(34),  # color.Fore.BLUE
        INFO: _asicode(32),  # _color.Fore.GREEN,
        WARNING: _asicode(33),  # _color.Fore.YELLOW,
        ERROR: _asicode(31),  # _color.Fore.RED,
        CRITICAL: _asicode(31, 47),  # color.Fore.RED + _color.Back.WHITE,
    }
    RESET_ALL = _asicode(0)

    def __init__(
        self,
        fmt="%(asctime)s | %(levelname)8s | %(name)s: %(message)s",
        datefmt=None,
        style: "_logging._FormatStyle" = "%",
        validate=True,
    ) -> None:
        self._levelsize: int | None = None
        super().__init__(fmt, datefmt, style, validate)


    def format(self, record):
        record.levelname = record.levelname.center(_LEVELSIZE)
        color = self.COLORS.get(record.levelno, None)
        if color:
            record.levelname = (
                f"{color}{record.levelname}{self.RESET_ALL}"
            )
        return super().format(record)


VERBOSE_LEVELS: dict[int, list[str]] = {}
VERBOSE_HELP = ""
_LEVELSIZE = 4

def initverbose():
    global VERBOSE_LEVELS, VERBOSE_HELP, _LEVELSIZE

    for name, loglevel in getLevelNamesMapping().items():
        if not loglevel:
            continue
        aliases: list[str] = VERBOSE_LEVELS.setdefault(loglevel, [])
        _LEVELSIZE = max(_LEVELSIZE, len(name))
        if name not in aliases:
            aliases.append(name)

    VERBOSE_LEVELS = dict(
        sorted(VERBOSE_LEVELS.items(), key=lambda l: l[0], reverse=True)
    )

    VERBOSE_HELP = ", ".join([aliases[0] for aliases in VERBOSE_LEVELS.values()])


import sys as _sys


def init_stderr_logging(name=None):
    handler = StreamHandler(_sys.stderr)
    getLogger(name).addHandler(handler)
    handler.setFormatter(DefaultFormatter())
