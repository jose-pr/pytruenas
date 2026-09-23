"""Generated stubs must agree with the runtime, and generation must not crash.

A stub that lies is worse than no stub: the checker blesses a call that fails.
Every case here comes from a real API dump shape.
"""

import ast
import copy
import json
import logging
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


# -- the call options -----------------------------------------------------


def test_the_call_options_are_keyword_only_and_complete(tmp_path):
    """The stub offered `_method`/`_ioerror`/`_filetransfer` POSITIONALLY while
    the runtime takes middleware parameters positionally and raises TypeError
    for any other keyword -- so following the stub shifted a real parameter.
    `_timeout` and `_tries` were missing entirely."""
    codegen.Codegen().generate(_api(), tmp_path / "out")
    src = (tmp_path / "out" / "user" / "__init__.pyi").read_text(encoding="utf-8")
    tree = ast.parse(src)
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef))
    query = next(
        n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "query"
    )
    kwonly = [a.arg for a in query.args.kwonlyargs]
    assert kwonly == ["_method", "_ioerror", "_filetransfer", "_timeout", "_tries"]
    # And none of them is positional any more.
    assert not [a.arg for a in query.args.args if a.arg.startswith("_")]


def test_the_option_defaults_are_python_not_strings(tmp_path):
    """`_ioerror:bool='False'` (a string!) is what quoting every string default
    would produce if the synthetic options were not marked as source."""
    codegen.Codegen().generate(_api(), tmp_path / "out")
    src = (tmp_path / "out" / "user" / "__init__.pyi").read_text(encoding="utf-8")
    assert "_ioerror:bool=False" in src.replace(" ", "")
    assert "_ioerror:bool='False'" not in src.replace(" ", "")


def test_no_parameter_is_named_all(tmp_path):
    """`duho.text.pysafe("*")` is `"all"`, so a `*` faked as a parameter turned
    into a bogus `all:` argument in every signature."""
    codegen.Codegen().generate(_api(), tmp_path / "out")
    for path in (tmp_path / "out").rglob("*.pyi"):
        src = path.read_text(encoding="utf-8")
        assert "all:_jsonschema" not in src, path


# -- precision ------------------------------------------------------------


@pytest.mark.parametrize(
    "schema,expected",
    [
        ({"enum": ["a", "b"]}, "_ty.Literal['a', 'b']"),
        ({"enum": ["a", None]}, "_ty.Literal['a']|None"),
        ({"enum": [1, 2, 3]}, "_ty.Literal[1, 2, 3]"),
        ({"const": 5}, "_ty.Literal[5]"),
        ({"const": True}, "_ty.Literal[True]"),
        # What a Literal cannot carry falls back to the ordinary handling.
        ({"enum": [[1], [2]]}, "_jsonschema.JsonValue"),
        ({"enum": []}, "_jsonschema.JsonValue"),
        # A typed `additionalProperties` is a map, not "some object".
        (
            {"type": "object", "additionalProperties": {"type": "string"}},
            "_ty.Mapping[str, str]",
        ),
        ({"type": "object", "additionalProperties": True}, "_jsonschema.JsonObject"),
        ({"allOf": [{"type": "string"}]}, "str"),
    ],
)
def test_enum_const_and_maps_render_precisely(schema, expected):
    """All of these read as `JsonValue`/`JsonObject` before -- and the
    appliance's dump uses enum 6413 times and const 6420 times, so this is most
    of what the stubs describe."""
    assert js.Schema.python_declaration(schema, {}, None) == expected


def test_a_literal_annotation_is_valid_python():
    rendered = js.Schema.python_declaration({"enum": ["a", None]}, {}, None)
    ast.parse(f"x: {rendered}")


# -- the runtime wins a name clash ----------------------------------------


def test_a_method_named_like_a_namespace_method_is_not_emitted(tmp_path, caplog):
    """`core.subscribe` is a middleware method AND `Namespace.subscribe` is a
    real one. Emitting it redefined the class member, so a checker accepted
    `ns.subscribe(event)` -- which at runtime calls the real method with a
    positional callback -- and rejected the correct `ns.subscribe()`."""
    api = _api()
    api["methods"].append(
        {
            "name": "user.subscribe",
            "doc": "",
            "roles": [],
            "schemas": {
                "type": "object",
                "properties": {
                    "Call parameters": {
                        "type": "array",
                        "prefixItems": [{"title": "event", "type": "string"}],
                    },
                    "Return value": {"type": "string"},
                },
            },
        }
    )
    with caplog.at_level(logging.INFO, logger="pytruenas.codegen"):
        codegen.Codegen().generate(api, tmp_path / "out")
    src = (tmp_path / "out" / "user" / "__init__.pyi").read_text(encoding="utf-8")
    assert "def subscribe" not in src
    assert "_method=" in caplog.text  # it says how to reach it instead
    # The synthetic helpers, whose names also exist on Namespace, stay.
    assert "def _update" in src and "def _get" in src
