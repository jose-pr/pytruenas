"""Unit-file syntax: parse and render systemd's INI-shaped format.

Separate from the units themselves because it is pure text handling -- no host,
no client, no I/O -- and that is what makes it testable on its own.
"""

from __future__ import annotations

import configparser as _configparser

__all__ = ["UnitConfigParser", "render_unit", "parse_unit"]


class UnitConfigParser(_configparser.ConfigParser):
    """A ``ConfigParser`` configured for systemd unit files.

    Unit files look like INI but are not, in three ways that each break the
    stdlib defaults:

    * keys are **case-sensitive** (``ExecStart``, never ``execstart``), so
      ``optionxform`` must not lower-case;
    * ``=`` is the only delimiter -- ``:`` is a legal character in a value
      (paths, times), and treating it as a delimiter silently truncates;
    * ``%`` introduces a *systemd* specifier (``%i``, ``%H``), so the parser's
      own interpolation has to be off or a valid unit raises at write time.
    """

    def __init__(self) -> None:
        super().__init__(
            defaults=None,
            dict_type=dict,
            allow_no_value=False,
            delimiters=("=",),
            comment_prefixes=("#", ";"),
            inline_comment_prefixes=None,
            strict=True,
            empty_lines_in_values=True,
            default_section=None,  # type: ignore[arg-type]
            interpolation=None,
        )

    def optionxform(self, optionstr: str) -> str:
        return optionstr


def render_unit(conf: "dict[str, dict]") -> str:
    """Render ``{section: {key: value}}`` as unit-file text.

    A list or tuple value is written as one ``Key = item`` line per item,
    which is how a unit file repeats a key (``ExecStartPre``, ``Environment``).
    A value containing a line break raises ``ValueError``: systemd has no way
    to carry one, and a continuation line would be read as a separate,
    malformed entry. ``None`` raises ``TypeError``.
    """
    lines: "list[str]" = []
    for section, entries in conf.items():
        lines.append(f"[{section}]")
        for key, value in entries.items():
            values = value if isinstance(value, (list, tuple)) else [value]
            for item in values:
                if item is None:
                    raise TypeError(
                        f"{section}.{key}: a unit file value cannot be None"
                    )
                text = str(item)
                if "\n" in text or "\r" in text:
                    raise ValueError(
                        f"{section}.{key}: a unit file value cannot span lines: {text!r}"
                    )
                lines.append(f"{key} = {text}")
        lines.append("")
    return "\n".join(lines) + "\n" if lines else ""


def parse_unit(text: str) -> "dict[str, dict]":
    """Parse unit-file text back into ``{section: {key: value}}``.

    Follows systemd.syntax(7) rather than INI: a key given more than once
    becomes a list of its values in order, a section given more than once is
    merged, a line ending in a backslash continues on the next one (comment
    lines in between are skipped), and lines starting with ``#`` or ``;`` are
    comments. Raises ``ValueError`` for a line that is neither a section, a
    comment nor ``key=value``, or a key before any section.
    """
    conf: "dict[str, dict]" = {}
    section: "dict | None" = None
    pending = ""
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if line.startswith(("#", ";")):
            continue
        if line.endswith("\\"):
            pending += line[:-1] + " "
            continue
        line, pending = (pending + line).strip(), ""
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            section = conf.setdefault(line[1:-1].strip(), {})
            continue
        key, sep, value = line.partition("=")
        if not sep:
            raise ValueError(f"line {number}: expected key=value: {raw!r}")
        if section is None:
            raise ValueError(f"line {number}: {key.strip()!r} is outside any section")
        key, value = key.strip(), value.strip()
        if key not in section:
            section[key] = value
        elif isinstance(section[key], list):
            section[key].append(value)
        else:
            section[key] = [section[key], value]
    return conf
