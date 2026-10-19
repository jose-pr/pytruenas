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
import sys
from pathlib import Path

import pytest

from pytruenas.codegen import Codegen
from pytruenas.codegen._declarations import docstring
from pytruenas.codegen._types import class_name, typeddict_name
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
        # compile(), not ast.parse(): only compiling rejects a duplicate argument.
        compile(src, str(path), "exec")


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
                assert (
                    name in defined or name in imported
                ), f"{path.name}: undefined return type {name!r}"


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


# -- the output directory is never destroyed by mistake -----------------------


def _api_version():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))["versions"][0]


def test_generate_refuses_a_directory_it_did_not_create(tmp_path):
    """`--path .` (or any directory with other files) must not be emptied.

    The generator used to `rmtree` the output path before rendering: pointed at
    a checkout, it deleted `.git` and exited 0.
    """
    target = tmp_path / "project"
    (target / ".git").mkdir(parents=True)
    (target / ".git" / "HEAD").write_text("ref: refs/heads/main\n")
    (target / "notes.txt").write_text("keep me")
    with pytest.raises(FileExistsError, match="not a tree generate-typings wrote"):
        Codegen().generate(_api_version(), target)
    assert (target / ".git" / "HEAD").read_text() == "ref: refs/heads/main\n"
    assert (target / "notes.txt").read_text() == "keep me"


def test_hand_written_stubs_are_not_a_typings_tree(tmp_path):
    """A directory of nothing but `.pyi` files was replaced -- and `typings/`,
    the old default `--path`, is where pyright looks for a project's own stubs."""
    target = tmp_path / "typings"
    (target / "somelib").mkdir(parents=True)
    (target / "somelib" / "__init__.pyi").write_text("def f() -> int: ...\n")
    with pytest.raises(FileExistsError, match="not a tree generate-typings wrote"):
        Codegen().generate(_api_version(), target)
    assert (target / "somelib" / "__init__.pyi").exists()


def test_the_default_path_is_not_pyrights_stub_directory():
    from pytruenas.cmd.generate_typings import Args

    assert Args.path.as_posix() == "truenasapi_typings/current"


def test_generate_replaces_its_own_previous_output(tmp_path):
    target = tmp_path / "typings"
    Codegen().generate(_api_version(), target)
    (target / "stale.pyi").write_text("# from an older API")
    Codegen().generate(_api_version(), target)
    assert (target / _INIT_NAME).exists()
    assert not (target / "stale.pyi").exists()


def test_a_failed_render_keeps_the_previous_output(tmp_path, monkeypatch):
    target = tmp_path / "typings"
    Codegen().generate(_api_version(), target)
    before = sorted(p.relative_to(target) for p in target.rglob("*"))

    import pytruenas.codegen as codegen_pkg

    def boom(ns, alias=None):
        raise RuntimeError("render failed")

    monkeypatch.setattr(codegen_pkg, "_render", boom)
    with pytest.raises(RuntimeError, match="render failed"):
        Codegen().generate(_api_version(), target)
    assert sorted(p.relative_to(target) for p in target.rglob("*")) == before
    assert [p.name for p in tmp_path.iterdir()] == ["typings"]  # no temp dir left


_INIT_NAME = "__init__.pyi"


# -- unit tests on the helpers -------------------------------------------------


def test_class_name_handles_trailing_separator():
    assert class_name("global_") == "Global"
    assert class_name("query-options") == "QueryOptions"
    assert class_name("a__b") == "AB"


def test_docstring_escapes_triple_quotes_and_nulls():
    out = docstring('ends with "pong"')
    assert '"""' not in out
    assert "\x00" not in docstring("a\x00b")


def test_typeddict_name_from_spacey_title():
    ns = PythonName("user")
    name = typeddict_name(ns, "Filesystem Count")
    assert name.isidentifier()
    assert " " not in name


def test_properties_not_listed_in_required_are_optional(generated):
    """A schema with no `required` list requires nothing (JSON Schema), but
    every property was rendered as required -- so an update payload, a
    query-options dict and a _get filter all demanded every field."""
    src = (generated / "user" / "__init__.pyi").read_text(encoding="utf-8")
    update = re.search(r"UpdateUserUpdate = .*?\}\)", src, re.S).group(0)
    fields = [line for line in update.splitlines() if line.startswith('    "')]
    assert fields and all("_NotRequired[" in line for line in fields), update
    # A field the dump DOES list as required stays required.
    create = re.search(r"CreateUserCreate = .*?\}\)", src, re.S).group(0)
    assert '"username": str' in create
    assert '"full_name": _NotRequired[str]' in create


def test_optionality_markers_resolve_on_the_39_floor(generated):
    """typing.NotRequired/Unpack exist only from 3.11; a consumer checking
    against 3.9 (this project's floor) could not resolve the stubs at all."""
    for path in generated.rglob("*.pyi"):
        src = path.read_text(encoding="utf-8")
        assert "_ty.NotRequired" not in src and "_ty.Unpack" not in src
        if "_NotRequired[" in src or "_Unpack[" in src:
            assert "from typing_extensions import" in src
            assert "sys.version_info >= (3, 11)" in src
            assert "import sys as" not in src


def test_the_root_module_exports_current(generated):
    """`TrueNASClient[Current]` is the documented spelling, but the generated
    root class is named after the version, so nothing resolved."""
    root = (generated / "__init__.pyi").read_text(encoding="utf-8")
    alias = re.search(r"^Current = (\w+)$", root, re.M)
    assert alias, root
    assert f"class {alias.group(1)}(_NS)" in root
    # Only in the root module -- not repeated per namespace.
    assert "Current = " not in (generated / "user" / "__init__.pyi").read_text(
        encoding="utf-8"
    )


def test_the_helpers_fields_are_the_payload_not_a_call_option(tmp_path):
    """`**fields` was `_Unpack[bool]`: a fixed index from the end picked the
    `_ioerror` option once the call options grew from three to five."""
    Codegen().generate(_api_version(), tmp_path / "out")
    stub = (tmp_path / "out" / "user" / "__init__.pyi").read_text(encoding="utf-8")
    fields = re.findall(r"\*\*fields:_Unpack\[(\w+)\]", stub)
    assert "bool" not in fields
    assert {"CreateUserCreate", "UpdateUserUpdate", "UpsertUserUpdate"} <= set(fields)


def _tree(root: Path) -> "dict[str, str]":
    return {
        p.relative_to(root).as_posix(): p.read_text(encoding="utf-8")
        for p in root.rglob("*")
        if p.is_file()
    }


def test_a_failed_swap_keeps_the_previous_output_whole(tmp_path, monkeypatch):
    """Moving the new tree into place fails (a stub held open on Windows):
    the previous output stays whole and no temporary sibling is left."""
    target = tmp_path / "typings"
    Codegen().generate(_api_version(), target)
    (target / "user" / "extra.pyi").write_text("# from the previous run")
    before = _tree(target)

    real = Path.rename
    blocked = []

    def locked(self, other):
        # Moving the first tree into place always fails (retries included);
        # putting another one back works.
        if Path(other) == target and (not blocked or self in blocked):
            blocked.append(self)
            raise PermissionError(13, "in use", str(self))
        return real(self, other)

    monkeypatch.setattr(Path, "rename", locked)
    with pytest.raises(PermissionError):
        Codegen().generate(_api_version(), target)
    assert _tree(target) == before
    assert [p.name for p in tmp_path.iterdir()] == ["typings"]


def test_an_undeletable_previous_output_does_not_fail_the_run(
    tmp_path, monkeypatch, caplog
):
    """Deleting the previous tree fails part-way: the new tree is in place in
    full, and the run says where the leftover is."""
    import logging
    import shutil

    reference = tmp_path / "reference"
    Codegen().generate(_api_version(), reference)
    target = tmp_path / "typings"
    Codegen().generate(_api_version(), target)
    (target / "stale.pyi").write_text("# from an older API")

    def partly(path, ignore_errors=False, **kwargs):
        next(p for p in Path(path).rglob("*.pyi")).unlink()
        if not ignore_errors:
            raise PermissionError(13, "in use", str(path))

    monkeypatch.setattr(shutil, "rmtree", partly)
    with caplog.at_level(logging.WARNING, logger="pytruenas.codegen"):
        Codegen().generate(_api_version(), target)
    assert _tree(target) == _tree(reference)
    assert "could not delete the previous output" in caplog.text


@pytest.mark.skipif(sys.platform != "win32", reason="Windows file locking")
def test_a_stub_held_open_leaves_the_previous_output_whole(tmp_path):
    target = tmp_path / "typings"
    Codegen().generate(_api_version(), target)
    (target / "user" / "extra.pyi").write_text("# from the previous run")
    before = _tree(target)
    with open(target / "system" / "__init__.pyi", encoding="utf-8"):
        with pytest.raises(PermissionError):
            Codegen().generate(_api_version(), target)
    assert _tree(target) == before
    assert [p.name for p in tmp_path.iterdir()] == ["typings"]


_NO_JINJA = """import runpy, sys


class Blocked:
    def find_spec(self, name, path=None, target=None):
        if name.partition(".")[0] == "jinja2":
            raise ImportError(name + " is blocked")


sys.meta_path.insert(0, Blocked())
sys.argv = ["pytruenas", *sys.argv[1:]]
runpy.run_module("pytruenas", run_name="__main__")
"""


def test_generate_typings_from_a_dump_file_needs_no_extra(tmp_path):
    """The core install generates stubs: nothing imports a template engine."""
    import os
    import subprocess

    import pytruenas

    source = Path(pytruenas.__file__).resolve().parent.parent
    env = {**os.environ, "PYTHONPATH": str(source)}
    out = tmp_path / "out"
    run = subprocess.run(
        [
            sys.executable,
            "-c",
            _NO_JINJA,
            "generate-typings",
            "--api-cache",
            str(FIXTURE),
            "--path",
            str(out),
            "nas.invalid",
        ],
        capture_output=True,
        text=True,
        env=env,
        timeout=120,
    )
    assert run.returncode == 0, run.stdout + run.stderr
    assert (out / "user" / "__init__.pyi").exists()
