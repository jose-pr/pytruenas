"""Unit-file syntax: parse and render systemd's INI-shaped format.

Separate from the units themselves because it is pure text handling -- no host,
no client, no I/O -- and that is what makes it testable on its own.
"""

from __future__ import annotations

import configparser as _configparser
import io as _io

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
    """Render ``{section: {key: value}}`` as unit-file text."""
    parser = UnitConfigParser()
    parser.read_dict(conf)
    stream = _io.StringIO()
    parser.write(stream)
    return stream.getvalue()


def parse_unit(text: str) -> "dict[str, dict]":
    """Parse unit-file text back into ``{section: {key: value}}``."""
    parser = UnitConfigParser()
    parser.read_string(text)
    return {section: dict(parser[section]) for section in parser.sections()}
