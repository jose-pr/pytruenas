import logging as _logging
from logging import *  # type:ignore

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
        DefaultFormatter.COLORS[level] = color

    setattr(_logging, name, log_root)


class DefaultFormatter(Formatter):  # type:ignore
    COLORS: dict[int, str] = {}

    def __init__(
        self,
        fmt="%(asctime)s | %(levelname)8s | %(name)s: %(message)s",
        datefmt=None,
        style: "_logging._FormatStyle" = "%",
        validate=True,
    ) -> None:
        self._levelsize: int | None = None
        super().__init__(fmt, datefmt, style, validate)

    @property
    def levelsize(self) -> int:
        if self._levelsize is None:
            for level in getLevelNamesMapping():
                self._levelsize = max(self._levelsize or 0, len(level))
        return self._levelsize  # type:ignore

    def format(self, record):
        record.levelname = record.levelname.center(self.levelsize)
        return super().format(record)


try:
    import colorama as _color  # type: ignore

    class DefaultFormatter(DefaultFormatter):
        COLORS = {
            DEBUG: _color.Fore.BLUE,
            INFO: _color.Fore.GREEN,
            WARNING: _color.Fore.YELLOW,
            ERROR: _color.Fore.RED,
            CRITICAL: _color.Fore.RED + _color.Back.WHITE,
        }

        def format(self, record):
            color = self.COLORS.get(record.levelno, None)
            if color:
                record.levelname = f"{color}{record.levelname:^{self.levelsize}}{_color.Style.RESET_ALL}"
                pass
            return Formatter.format(self, record)

except ImportError:

    pass

VERBOSE_LEVELS = {}
VERBOSE_HELP= ''

def initverbose():
    global VERBOSE_LEVELS, VERBOSE_HELP

    for name, loglevel in getLevelNamesMapping().items():
        if not loglevel:
            continue
        aliases: list[str] = VERBOSE_LEVELS.setdefault(loglevel, [])
        if name not in aliases:
            aliases.append(name)

    VERBOSE_LEVELS = dict(sorted(VERBOSE_LEVELS.items(), key=lambda l: l[0], reverse=True))

    VERBOSE_HELP = ", ".join([aliases[0] for aliases in VERBOSE_LEVELS.values()])