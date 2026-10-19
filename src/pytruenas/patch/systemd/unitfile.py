"""Unit-file syntax: render systemd's INI-shaped format.

Separate from the units themselves because it is pure text handling -- no host,
no client, no I/O -- and that is what makes it testable on its own.
"""

from __future__ import annotations

import configparser as _configparser

__all__ = ["UnitConfigParser", "render_unit"]


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
