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
from pytruenas.codegen import _declarations, _types
from pytruenas.models import jsonschema as js

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
    assert _types.declaration(schema, {}, None) == expected


def test_an_empty_array_schema_is_an_empty_list():
    rendered = _types.declaration({"type": "array", "items": False}, {}, None)
    assert rendered.startswith("list")


@pytest.mark.parametrize(
    "doc",
    ['ends with """', 'a "quote" inside', 'trailing "', "back\\slash", "null\x00byte"],
)
def test_any_docstring_still_compiles(doc):
    """A doc ending in `\"\"\"` produced a stub that would not parse."""
    rendered = _declarations.docstring(doc)
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
    assert _types.class_name(raw) == expected
    assert expected.isidentifier()


def test_a_typeddict_name_is_an_identifier():
    from duho.qualname import PythonName

    name = _types.typeddict_name(PythonName("pool.dataset"), "acl(nfs4) options")
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
    name_a = _types.declaration(first, typeddicts, ns)
    name_b = _types.declaration(second, typeddicts, ns)
    assert name_a != name_b
    assert typeddicts[name_a] != typeddicts[name_b]
    # The same shape twice reuses the one name.
    assert _types.declaration(dict(first), typeddicts, ns) == name_a


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
    assert _declarations._default_literal(default) == expected


def test_the_packages_own_source_defaults_still_render_as_source():
    assert _declarations._default_literal(_declarations.Source("None")) == "None"


def test_the_schema_models_are_data_only():
    """`pytruenas.models` holds TypedDicts and aliases; rendering is codegen's."""
    import pytruenas.models as models

    for path in Path(models.__file__).parent.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        functions = [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        assert functions == [], (path.name, functions)


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
    with pytest.raises(codegen.BadAPIName):
        codegen._check_inside(root, root.parent / "elsewhere" / "__init__.pyi")
    codegen._check_inside(root, root / "user" / "__init__.pyi")  # fine


@pytest.mark.parametrize("name", ["nul", "con", "com1"])
def test_a_name_cannot_be_a_windows_device(tmp_path, name):
    """A valid identifier, and on Windows a write to a device."""
    root = tmp_path / "typings"
    with pytest.raises(codegen.BadAPIName, match=name):
        codegen._check_inside(root, root / name / "__init__.pyi")


def test_a_bad_name_is_a_pytruenas_error_and_a_value_error():
    from pytruenas import TrueNASError

    assert issubclass(codegen.BadAPIName, TrueNASError)
    assert issubclass(codegen.BadAPIName, ValueError)


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


# -- the call options -----------------------------------------------------


def test_the_call_options_are_keyword_only_and_complete(tmp_path):
    """The stub offered `_method`/`_ioerror`/`_filetransfer` POSITIONALLY while
    the runtime takes middleware parameters positionally and raises TypeError
    for any other keyword -- so following the stub shifted a real parameter.
    `_timeout` and the retry count were missing entirely."""
    codegen.Codegen().generate(_api(), tmp_path / "out")
    src = (tmp_path / "out" / "user" / "__init__.pyi").read_text(encoding="utf-8")
    tree = ast.parse(src)
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef))
    query = next(
        n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name == "query"
    )
    kwonly = [a.arg for a in query.args.kwonlyargs]
    assert kwonly == ["_method", "_ioerror", "_filetransfer", "_timeout", "_retries"]
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
    assert _types.declaration(schema, {}, None) == expected


def test_a_literal_annotation_is_valid_python():
    rendered = _types.declaration({"enum": ["a", None]}, {}, None)
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


# -- dump shapes that are valid JSON Schema but unusual -------------------


def _method(api, name):
    return next(m for m in api["methods"] if m["name"] == name)


def _params(api, name):
    return _method(api, name)["schemas"]["properties"]["Call parameters"]["prefixItems"]


def _set_return(name, schema):
    def mutate(api):
        _method(api, name)["schemas"]["properties"]["Return value"] = schema

    return mutate


def _add_params(name, *schemas):
    def mutate(api):
        _params(api, name).extend(copy.deepcopy(schemas))

    return mutate


def _drop_params(name):
    def mutate(api):
        _params(api, name).clear()

    return mutate


#: ``{label: mutate(api)}`` over the fixture: each one a shape the generator
#: must turn into stubs that compile and type-check.
EDGE_SHAPES = {
    "duplicate_title": _add_params("user.update", {"title": "id", "type": "string"}),
    "sanitized_collision": _add_params(
        "system.info", {"title": "a-b", "type": "string"}, {"title": "a_b"}
    ),
    "self_title": _add_params("system.info", {"title": "self", "type": "string"}),
    "untitled_parameter": _add_params("system.info", {"type": "integer"}),
    "empty_array": _add_params(
        "system.info", {"title": "nothing", "type": "array", "items": False}
    ),
    "get_instance_optional_return": _set_return(
        "user.get_instance",
        {
            "anyOf": [
                {
                    "type": "object",
                    "title": "entry",
                    "properties": {"x": {"type": "string"}},
                },
                {"type": "null"},
            ]
        },
    ),
    "get_instance_bare_object_return": _set_return(
        "user.get_instance", {"type": "object"}
    ),
    "get_instance_array_return": _set_return(
        "user.get_instance", {"type": "array", "items": {"type": "string"}}
    ),
    "create_without_parameters": _drop_params("user.create"),
}


def edge_dump(label):
    api = _api()
    EDGE_SHAPES[label](api)
    return api


def _compile_all(root: Path) -> None:
    files = list(root.rglob("*.pyi"))
    assert files
    for path in files:
        # compile(), not ast.parse(): a duplicate argument parses.
        compile(path.read_text(encoding="utf-8"), str(path), "exec")


@pytest.mark.parametrize("label", sorted(EDGE_SHAPES))
def test_an_unusual_shape_generates_stubs_that_compile(tmp_path, label):
    codegen.Codegen().generate(edge_dump(label), tmp_path / "out")
    _compile_all(tmp_path / "out")


def test_parameter_names_are_unique_in_a_signature(tmp_path):
    api = edge_dump("sanitized_collision")
    EDGE_SHAPES["self_title"](api)
    EDGE_SHAPES["untitled_parameter"](api)
    codegen.Codegen().generate(api, tmp_path / "out")
    tree = ast.parse(
        (tmp_path / "out" / "system" / "__init__.pyi").read_text(encoding="utf-8")
    )
    info = next(n for n in ast.walk(tree) if getattr(n, "name", "") == "info")
    names = [a.arg for a in info.args.args]
    assert names[:5] == ["self", "a_b", "a_b_", "self_", "arg4"]


def test_an_optional_get_instance_return_still_gets_a_get_helper(tmp_path):
    codegen.Codegen().generate(
        edge_dump("get_instance_optional_return"), tmp_path / "out"
    )
    src = (tmp_path / "out" / "user" / "__init__.pyi").read_text(encoding="utf-8")
    tree = ast.parse(src)
    get = next(n for n in ast.walk(tree) if getattr(n, "name", "") == "_get")
    members = [m.strip() for m in ast.unparse(get.returns).split("|")]
    assert members[-1] == "None" and len(members) == 2, members
    # The object member is a TypedDict this module defines.
    assert f"\n{members[0]} = _ty.TypedDict(" in src, members


@pytest.mark.parametrize(
    "label",
    ["get_instance_bare_object_return", "get_instance_array_return"],
)
def test_no_get_helper_without_properties_to_filter_on(tmp_path, caplog, label):
    with caplog.at_level(logging.INFO, logger="pytruenas.codegen"):
        codegen.Codegen().generate(edge_dump(label), tmp_path / "out")
    src = (tmp_path / "out" / "user" / "__init__.pyi").read_text(encoding="utf-8")
    assert "def _get(" not in src
    assert "def get_instance(" in src
    assert "no _get stub emitted" in caplog.text


def test_no_create_helper_without_a_payload(tmp_path, caplog):
    with caplog.at_level(logging.INFO, logger="pytruenas.codegen"):
        codegen.Codegen().generate(
            edge_dump("create_without_parameters"), tmp_path / "out"
        )
    src = (tmp_path / "out" / "user" / "__init__.pyi").read_text(encoding="utf-8")
    assert "def _create(" not in src
    assert "_Unpack[int]" not in src
    assert "no _create stub emitted" in caplog.text


@pytest.mark.parametrize("has_never", [True, False])
def test_an_empty_array_names_never_whatever_interpreter_generates(
    tmp_path, monkeypatch, has_never
):
    """`typing.Never` exists from 3.11 and the stubs target 3.9: the output
    names the template's `_Never` alias on every generating interpreter."""
    monkeypatch.setattr(_types, "_HAS_NEVER", has_never)
    codegen.Codegen().generate(edge_dump("empty_array"), tmp_path / "out")
    src = (tmp_path / "out" / "system" / "__init__.pyi").read_text(encoding="utf-8")
    assert "nothing:list[_Never]" in src.replace(" ", "")
    assert "_ty.Never" not in src
    assert "from typing_extensions import (" in src and "Never as _Never" in src


def test_a_closed_tuple_is_any_json_array(tmp_path):
    api = _api()
    _add_params(
        "system.info",
        {
            "title": "pair",
            "type": "array",
            "prefixItems": [{"type": "string"}, {"type": "integer"}],
            "items": False,
        },
    )(api)
    codegen.Codegen().generate(api, tmp_path / "out")
    src = (tmp_path / "out" / "system" / "__init__.pyi").read_text(encoding="utf-8")
    assert "pair:_jsonschema.JsonArray" in src.replace(" ", "")
