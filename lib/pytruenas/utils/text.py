import keyword as _kw
import typing as _ty
import re as _re

try:
    from gettext import gettext, ngettext  # type:ignore
except ImportError:

    def gettext(message):
        return message

    def ngettext(singular, plural, n):
        if n == 1:
            return singular
        else:
            return plural



def str_(txt: "bytes|str") -> str:
    if isinstance(txt, str):
        return txt
    return _ty.cast(bytes, txt).decode()

def snakecase(name: str) -> str: #WIP
    std = _re.sub(r"[-\s_]+", "_", name)
    std = _re.sub(r"\W|^(?=\d)", "_", std)
    std = std[0].lower() + _re.sub("[A-Z]", lambda m: m.group(0)[1:].lower(), std[1:])
    return std

PYREPLACE = {
    '+': 'plus',
    "!": 'not',
    '*': 'all'
}

def pysafe(text: str, separator: str = "."):
    text = separator.join(
        [(f"{n}_" if _kw.iskeyword(n) else n) for n in text.split(separator)]
    ).replace('-','_').replace(' ','_')
    for symbol, replacement in PYREPLACE.items():
        if text == symbol:
            return replacement
        if text.startswith(symbol):
            text = replacement +'_'+ text.removeprefix(symbol)
        if text.endswith(symbol):
            text = text.removeprefix(symbol) + '_' + replacement
        text = text.replace(symbol, replacement)

    return text or '_'


def camelcase(text: str, separators: _ty.Sequence[str] | str | None = None):
    if text:
        separators = separators or (".", "_", "-")
        if isinstance(separators, str):
            separators = (separators,)
        for sep in separators:
            text = "".join([part[0].upper() + part[1:] for part in text.split(sep)])
    return text


_EXPAND_PATTERN = _re.compile(
    r".*(\[([A-Z0-9]+)-([A-Z0-9]+)(:[^\[\]]*)?\]).*", _re.IGNORECASE
)
_range = range


def unicode_range(start: str, end: str, step: int = 1):
    for c in _range(ord(start), ord(end) + 1, step):
        yield chr(c)


def range(start: str, end: str, step: int = 1, format: str | None = None):
    format = format or ""
    if start.isdigit():
        start = int(start)  # type:ignore
        end = int(end)  # type:ignore
        func = lambda a, b, c: _range(a, b + 1, c)
    else:
        func = unicode_range

    for i in func(start, end, step):  # type:ignore
        yield f"{{{format}}}".format(i)


def expand(text: str):
    template = _EXPAND_PATTERN.match(text)
    if template:
        _, start, end, format = template.groups()
        s, e = template.span(1)
        for i in range(start, end, format=format):
            yield from expand(f"{text[:s]}{i}{text[e:]}")
    else:
        yield text
