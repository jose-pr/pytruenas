"""Typings generator: every generated stub must be valid, self-consistent Python.

Runs the generator against a small hand-written API dump (``fixtures/api_min.json``)
covering the shapes that historically broke it: nested objects, arrays, anyOf,
defaults (including an optional-before-required ordering), an object return type,
create/update/get_instance (which grow synthetic ``_create``/``_update``/
``_upsert``/``_get`` helpers), and a keyword-like/space-y title.
"""

import ast
import json
import re
from pathlib import Path

import pytest

from pytruenas.codegen import Codegen, _camelcase, docstring
from pytruenas.models.jsonschema import _typeddict_name
from duho.qualname import PythonName

FIXTURE = Path(__file__).parent / "fixtures" / "api_min.json"


@pytest.fixture
def generated(tmp_path):
    api = json.loads(FIXTURE.read_text(encoding="utf-8"))
    out = tmp_path / "typings"
    Codegen().generate(api["versions"][0], out)
    return out


def test_all_stubs_parse(generated):
    files = list(generated.rglob("*.pyi"))
    assert files, "no stubs generated"
    for path in files:
        src = path.read_text(encoding="utf-8")
        ast.parse(src)  # raises SyntaxError on any invalid stub


def test_no_undefined_uppercase_return_types(generated):
    for path in generated.rglob("*.pyi"):
        src = path.read_text(encoding="utf-8")
        tree = ast.parse(src)
        defined = set()
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                defined.update(t.id for t in node.targets if isinstance(t, ast.Name))
            elif isinstance(node, ast.ClassDef):
                defined.add(node.name)
            elif isinstance(node, ast.ImportFrom):
                imported.update(a.asname or a.name for a in node.names)
        for match in re.finditer(r"->\s*([A-Za-z_][A-Za-z0-9_]*)", src):
            name = match.group(1)
            if name[0].isupper():
                assert name in defined or name in imported, (
                    f"{path.name}: undefined return type {name!r}"
                )


def test_expected_namespaces_and_methods(generated):
    user = (generated / "user" / "__init__.pyi").read_text(encoding="utf-8")
    assert "class User(_NS):" in user
    assert "def query(" in user
    assert "def create(" in user
    # synthetic helpers exist
    assert "def _create(" in user
    assert "def _update(" in user
    assert "def _get(" in user
    system = (generated / "system" / "__init__.pyi").read_text(encoding="utf-8")
    assert "class System(_NS):" in system
    assert "def info(" in system


def test_root_namespace_valid_class_name(generated):
    root = (generated / "__init__.pyi").read_text(encoding="utf-8")
    # version v25.04.0 must not become `class 0`
    assert re.search(r"class\s+[A-Za-z_]\w*\(_NS\):", root)
    assert "class 0" not in root


# -- unit tests on the helpers -------------------------------------------------


def test_camelcase_handles_trailing_separator():
    assert _camelcase("global_") == "Global"
    assert _camelcase("query-options") == "QueryOptions"
    assert _camelcase("a__b") == "AB"


def test_docstring_escapes_triple_quotes_and_nulls():
    out = docstring('ends with "pong"')
    assert '"""' not in out
    assert "\x00" not in docstring("a\x00b")


def test_typeddict_name_from_spacey_title():
    ns = PythonName("user")
    name = _typeddict_name(ns, "Filesystem Count")
    assert name.isidentifier()
    assert " " not in name
