"""Generated stubs must agree with the runtime, and generation must not crash.

A stub that lies is worse than no stub: the checker blesses a call that fails.
Every case here comes from a real API dump shape.
"""

import ast
import copy
import json
import sys
from pathlib import Path

import pytest

from pytruenas import codegen
from pytruenas.models import jsonschema as js

pytestmark = pytest.mark.requires("jinja2")

FIXTURE = Path(__file__).parent / "fixtures" / "api_min.json"


def _api():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))["versions"][0]


# -- generation must survive real schema shapes ---------------------------


@pytest.mark.parametrize(
    "schema,expected",
    [
        ({"type": ["string", "null"]}, "str|None"),
        ({"type": ["integer", "string"]}, "int|str"),
        ({"type": "array", "items": True}, "_jsonschema.JsonArray"),
        ({"type": "array", "items": {}}, "_jsonschema.JsonArray"),
        ({"type": "definitely-not-a-type"}, "_jsonschema.JsonValue"),
    ],
)
def test_valid_schema_forms_do_not_crash(schema, expected):
    """A list `type` raised NotImplementedError and `items: true` a TypeError,
    each aborting the whole generation."""
    assert js.Schema.python_declaration(schema, {}, None) == expected


def test_an_empty_array_schema_is_an_empty_list():
    rendered = js.Schema.python_declaration({"type": "array", "items": False}, {}, None)
    assert rendered.startswith("list")


@pytest.mark.parametrize(
    "doc",
    ['ends with """', 'a "quote" inside', 'trailing "', "back\\slash", "null\x00byte"],
)
def test_any_docstring_still_compiles(doc):
    """A doc ending in `\"\"\"` produced a stub that would not parse."""
    rendered = codegen.docstring(doc)
    ast.parse(f'def f():\n    """{rendered}"""\n')


# -- names ----------------------------------------------------------------


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("plain", "Plain"),
        ("global_", "Global"),  # what pysafe produces
        ("with space", "WithSpace"),
        ("with-dash", "WithDash"),
        ("dotted.name", "DottedName"),
        ("acl(nfs4)", "AclNfs4"),
        ("smb:share", "SmbShare"),
        ("quote'name", "QuoteName"),
        ("bracket[x]", "BracketX"),
        ("1leading", "N1leading"),
        ("", "Unnamed"),
    ],
)
def test_every_name_becomes_an_identifier(raw, expected):
    """Parens, colons, quotes, brackets and leading digits used to survive into
    a name no stub can define."""
    assert codegen._camelcase(raw) == expected
    assert expected.isidentifier()


def test_a_typeddict_name_is_an_identifier():
    from duho.qualname import PythonName

    name = js._typeddict_name(PythonName("pool.dataset"), "acl(nfs4) options")
    assert name.isidentifier(), name


def test_two_shapes_with_one_name_do_not_overwrite_each_other():
    """The later definition replaced the earlier, so every reference to the
    first pointed at the wrong shape."""
    from duho.qualname import PythonName

    ns = PythonName("user")
    typeddicts: dict = {}
    first = {"type": "object", "title": "Opts", "properties": {"a": {"type": "string"}}}
    second = {
        "type": "object",
        "title": "Opts",
        "properties": {"b": {"type": "integer"}},
    }
    name_a = js.Schema.python_declaration(first, typeddicts, ns)
    name_b = js.Schema.python_declaration(second, typeddicts, ns)
    assert name_a != name_b
    assert typeddicts[name_a] != typeddicts[name_b]
    # The same shape twice reuses the one name.
    assert js.Schema.python_declaration(dict(first), typeddicts, ns) == name_a


# -- values ---------------------------------------------------------------


@pytest.mark.parametrize(
    "default,expected",
    [
        ("0", "'0'"),
        ("1.5", "'1.5'"),
        ("true", "'true'"),
        ("None", "'None'"),
        ("text", "'text'"),
        (0, "0"),
        (None, "None"),
        (True, "True"),
        ([], "[]"),
    ],
)
def test_a_string_default_stays_a_string(default, expected):
    """It was parsed with literal_eval and passed through when that worked, so a
    default of "0" became the integer 0 and the stub lied about the type."""
    assert codegen._default_literal(default) == expected


def test_the_packages_own_source_defaults_still_render_as_source():
    assert codegen._default_literal(codegen.Source("None")) == "None"


def test_the_json_aliases_are_types_not_strings():
    """A stub annotation naming `_jsonschema.JsonValue` resolved to a `str`
    variable, which is not a type at all."""
    for name in ("JsonValue", "JsonObject", "JsonArray"):
        value = getattr(js, name)
        assert not isinstance(value, str), name


# -- the caller's data ----------------------------------------------------


def test_generate_does_not_touch_the_callers_dump(tmp_path):
    """It prefixed the method names of the caller's own dict, so generating
    twice from one dump produced different output the second time."""
    api = _api()
    before = copy.deepcopy(api)
    codegen.Codegen().generate(api, tmp_path / "one")
    assert api == before
    codegen.Codegen().generate(api, tmp_path / "two")
    first = sorted(
        p.relative_to(tmp_path / "one").as_posix()
        for p in (tmp_path / "one").rglob("*.pyi")
    )
    second = sorted(
        p.relative_to(tmp_path / "two").as_posix()
        for p in (tmp_path / "two").rglob("*.pyi")
    )
    assert first == second


def test_a_name_cannot_escape_the_output_directory(tmp_path):
    """Every path component comes from the dump."""
    root = tmp_path / "typings"
    with pytest.raises(codegen.BadApiName):
        codegen._check_inside(root, root.parent / "elsewhere" / "__init__.pyi")
    codegen._check_inside(root, root / "user" / "__init__.pyi")  # fine


def test_get_instance_without_an_id_parameter_generates(tmp_path):
    """`idtype` was only bound inside the `id` branch, so this raised
    UnboundLocalError (or reused the previous namespace's type)."""
    api = _api()
    for method in api["methods"]:
        if method["name"].endswith("get_instance"):
            # Strip the `id` parameter, keeping the rest of the shape.
            params = method["schemas"]["properties"]["Call parameters"]["prefixItems"]
            method["schemas"]["properties"]["Call parameters"]["prefixItems"] = [
                p for p in params if p.get("title") != "id"
            ]
    codegen.Codegen().generate(api, tmp_path / "out")
    assert list((tmp_path / "out").rglob("*.pyi"))


# -- the template ---------------------------------------------------------


def test_the_template_loads_without_a_filesystem_path(monkeypatch):
    """`deploy --mode pyz` installs a zipapp, where a FileSystemLoader cannot
    read the template at all."""
    from pytruenas.codegen import jinja

    assert jinja._TEMPLATES["namespace.pyi.j2"].strip()
    renderer = jinja.Renderer("namespace.pyi")
    assert renderer.template is not None
