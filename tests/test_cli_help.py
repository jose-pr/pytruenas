"""Help rendered from an API definition, and the field coercion `call` uses.

Both are pure functions over a dump slice, so everything here runs with no
client and no network. The fixture reproduces the shapes a real 26.0 dump uses,
including the ones that used to be mishandled: a parameter list as
``prefixItems``, an optional field as ``anyOf[<real>, null]``, an ``enum``, a
property-shaped default, and a method taking ``(id, payload)``.
"""

from __future__ import annotations

import pytest

from pytruenas.utils import apihelp, fields

USER_CREATE = {
    "name": "user.create",
    "roles": ["ACCOUNT_WRITE"],
    "doc": "Create a new user.",
    "schemas": {
        "type": "object",
        "properties": {
            "Call parameters": {
                "type": "array",
                "prefixItems": [
                    {
                        "title": "user_create",
                        "type": "object",
                        "required": ["username", "full_name"],
                        "properties": {
                            "username": {"type": "string", "description": "The name."},
                            "full_name": {"type": "string"},
                            "uid": {
                                "anyOf": [{"type": "integer"}, {"type": "null"}],
                                "default": None,
                                "description": "Leave unset to allocate one.",
                            },
                            "shell": {
                                "type": "string",
                                "enum": [
                                    "/usr/bin/zsh",
                                    "/usr/bin/bash",
                                    "/usr/sbin/nologin",
                                ],
                                "default": "/usr/bin/zsh",
                            },
                            "groups": {"type": "array", "items": {"type": "integer"}},
                            "smb": {"type": "boolean", "default": True},
                            "home_create": {"type": "boolean", "default": False},
                        },
                    }
                ],
            },
            "Return value": {"type": "integer", "description": "The new user id."},
        },
    },
}

USER_UPDATE = {
    "name": "user.update",
    "roles": ["ACCOUNT_WRITE"],
    "doc": "Update an existing user.",
    "schemas": {
        "type": "object",
        "properties": {
            "Call parameters": {
                "type": "array",
                "prefixItems": [
                    {"title": "id", "type": "integer"},
                    {
                        "title": "user_update",
                        "type": "object",
                        "properties": {"full_name": {"type": "string"}},
                    },
                ],
            },
            "Return value": {"type": "object"},
        },
    },
}

SYSTEM_INFO = {
    "name": "system.info",
    "roles": [],
    "doc": "Return system information.",
    "schemas": {
        "type": "object",
        "properties": {
            "Call parameters": {"type": "array", "prefixItems": []},
            "Return value": {"type": "object"},
        },
    },
}

VERSION = {
    "version": "v26.0.0",
    "methods": [USER_CREATE, USER_UPDATE, SYSTEM_INFO],
    "events": [],
}

FIELDS = apihelp.fields(USER_CREATE)


# -- apihelp ---------------------------------------------------------------


def test_parameters_and_payload_position():
    assert apihelp.payload_index(USER_CREATE) == 0
    # (id, payload): the payload is the LAST object parameter, so the id stays
    # a `-p` positional.
    assert apihelp.payload_index(USER_UPDATE) == 1
    assert apihelp.payload_index(SYSTEM_INFO) is None


@pytest.mark.parametrize(
    "schema, expected",
    [
        ({"type": "string"}, "string"),
        ({"type": ["string", "null"]}, "string|null"),
        ({"anyOf": [{"type": "integer"}, {"type": "null"}]}, "integer|null"),
        ({"type": "array", "items": {"type": "integer"}}, "array[integer]"),
        ({"type": "array"}, "array"),
        (
            {"type": "object", "additionalProperties": {"type": "string"}},
            "object[str, string]",
        ),
        ({"allOf": [{"type": "boolean"}]}, "boolean"),
        ({}, "any"),
        ({"type": "!SomeRef"}, "SomeRef"),
    ],
)
def test_type_label(schema, expected):
    assert apihelp.type_label(schema) == expected


def test_render_shows_required_defaults_and_enum_values():
    text = apihelp.render("user.create", USER_CREATE)
    assert "pytruenas call user.create <target> -- --field=value ..." in text
    assert "Create a new user." in text
    assert "ACCOUNT_WRITE" in text
    # required vs default
    assert "--username=<string>" in text
    assert "(required)" in text
    assert "default null" in text
    assert "default true" in text  # a JSON true, not Python True
    # the enum values are the point: "some string" is not help
    assert "'/usr/bin/bash'" in text
    assert "The name." in text
    assert "Returns: integer" in text


def test_render_puts_an_id_parameter_on_dash_p():
    text = apihelp.render("user.update", USER_UPDATE)
    assert "-p <id>" in text
    assert "Positional parameters (-p, JSON):" in text
    assert "--full_name=<string>" in text


def test_render_a_method_with_no_fields():
    text = apihelp.render("system.info", SYSTEM_INFO)
    assert "Fields" not in text or "Fields: none" in text
    assert "-- --field=value" not in text


def test_namespace_and_index_listings():
    listing = apihelp.render_namespace(VERSION, "user")
    assert "create" in listing and "update" in listing
    assert "Create a new user" in listing

    index = apihelp.render_index(VERSION)
    assert "user" in index and "system" in index
    assert "3 methods in 2 namespaces" in index


def test_an_unknown_method_suggests_near_misses():
    with pytest.raises(apihelp.UnknownMethod, match="did you mean: user.create"):
        apihelp.find(VERSION, "user.creat")


# -- the shell-free source: core.get_methods --------------------------------

# What `core.get_methods("user")` really returns for one method, reduced to the
# keys that matter. The envelope differs from the dump's: `accepts` is the
# positional parameter list, `returns` a list, the doc is `description`, and
# `job` exists here and nowhere else.
GET_METHODS_ENTRY = {
    "description": "Create a new user.",
    "cli_description": "Create a new user",
    "roles": ["ACCOUNT_WRITE"],
    "job": False,
    "accepts": [
        {
            "title": "user_create",
            "type": "object",
            "additionalProperties": False,
            "required": ["username"],
            "properties": {
                "username": {"type": "string", "description": "The name."},
                "shell": {"type": "string", "enum": ["/usr/bin/zsh", "/usr/bin/bash"]},
            },
        }
    ],
    "returns": [{"type": "integer", "description": "The new user id."}],
}


def test_get_methods_entry_normalizes_to_the_dump_shape():
    method = apihelp.from_get_methods("user.create", GET_METHODS_ENTRY)
    assert method["doc"] == "Create a new user."
    assert method["roles"] == ["ACCOUNT_WRITE"]
    # `accepts` becomes the positional parameter list
    assert apihelp.payload_index(method) == 0
    assert sorted(apihelp.fields(method)) == ["shell", "username"]
    # `returns` is a list here, a single schema in the dump
    assert apihelp.type_label(apihelp.returns(method)) == "integer"


def test_a_normalized_entry_renders_like_a_dump_one():
    text = apihelp.render(
        "user.create", apihelp.from_get_methods("user.create", GET_METHODS_ENTRY)
    )
    assert "--username=<string>" in text
    assert "(required)" in text
    assert "'/usr/bin/bash'" in text
    assert "Returns: integer" in text


def test_a_job_is_called_out_before_the_doc():
    """`job` decides how a caller must treat the result, so it goes first.

    Only core.get_methods reports it. Some docs run to hundreds of words --
    pool.dataset.unlock's does -- and the fact that a job returns an id rather
    than an answer must not be buried in them.
    """
    entry = {**GET_METHODS_ENTRY, "job": True, "description": "word " * 200}
    text = apihelp.render("pool.dataset.unlock", apihelp.from_get_methods("x", entry))
    lines = [line for line in text.splitlines() if line.strip()]
    assert "JOB" in lines[1]
    assert lines[1].index("JOB") < 10
    # ... and a non-job says nothing about jobs at all.
    plain = apihelp.render(
        "user.create", apihelp.from_get_methods("x", GET_METHODS_ENTRY)
    )
    assert "JOB" not in plain


def test_accepts_may_be_a_lone_schema_not_a_list():
    entry = {**GET_METHODS_ENTRY, "accepts": GET_METHODS_ENTRY["accepts"][0]}
    method = apihelp.from_get_methods("user.create", entry)
    assert sorted(apihelp.fields(method)) == ["shell", "username"]


def test_a_method_with_no_parameters_normalizes():
    method = apihelp.from_get_methods(
        "core.ping", {"description": "pong", "accepts": [], "returns": []}
    )
    assert apihelp.parameters(method) == []
    assert apihelp.payload_index(method) is None
    text = apihelp.render("core.ping", method)
    # No payload parameter at all, so no Fields section and no `--` in the usage:
    # offering `-- --field=value` for a method that takes nothing would be a lie.
    assert "Fields" not in text
    assert "--field=value" not in text


def test_methods_from_get_methods_keys_by_name():
    found = apihelp.methods_from_get_methods({"user.create": GET_METHODS_ENTRY})
    assert list(found) == ["user.create"]
    assert found["user.create"]["name"] == "user.create"


# -- fields ----------------------------------------------------------------


def test_bare_and_dashed_spellings_are_the_same():
    assert fields.split("--username=svc") == ("username", "svc")
    assert fields.split("username=svc") == ("username", "svc")


def test_a_field_without_a_value_is_refused():
    # A bare `--smb` cannot mean True: the appliance distinguishes false from
    # "not sent", so guessing would send the wrong thing.
    with pytest.raises(fields.FieldError, match="always required"):
        fields.split("--smb")


def test_booleans_are_json_not_strings():
    payload = fields.collect(["--smb=false", "--home_create=yes"], FIELDS)
    assert payload == {"smb": False, "home_create": True}


def test_integers_and_nullable_fields():
    assert fields.collect(["--uid=1001"], FIELDS) == {"uid": 1001}
    assert fields.collect(["--uid=null"], FIELDS) == {"uid": None}
    assert fields.collect(["--uid="], FIELDS) == {"uid": None}


def test_an_enum_value_is_checked_and_names_the_alternatives():
    assert fields.collect(["--shell=/usr/bin/bash"], FIELDS) == {
        "shell": "/usr/bin/bash"
    }
    with pytest.raises(fields.FieldError, match="is not one of: '/usr/bin/zsh'"):
        fields.collect(["--shell=/bin/fish"], FIELDS)


def test_arrays_from_a_comma_list_or_a_repeated_flag():
    assert fields.collect(["--groups=1,2,3"], FIELDS) == {"groups": [1, 2, 3]}
    assert fields.collect(["--groups=1", "--groups=2"], FIELDS) == {"groups": [1, 2]}


def test_an_unknown_field_is_an_error_with_suggestions():
    # The same class of bug as the swallowed keyword that made
    # `query(filters=...)` return every row: a dropped field must never be silent.
    with pytest.raises(fields.FieldError, match="unknown field 'usernam'"):
        fields.collect(["--usernam=svc"], FIELDS)
    with pytest.raises(fields.FieldError, match="did you mean: username"):
        fields.collect(["--usernam=svc"], FIELDS)


def test_a_bad_integer_reports_the_expected_type():
    with pytest.raises(fields.FieldError, match="not a valid integer"):
        fields.collect(["--uid=abc"], FIELDS)


def test_json_escape_hatch_and_file_values(tmp_path):
    nested = {
        "payload": {
            "type": "object",
            "properties": {"acl": {"type": "boolean"}},
        },
        "key": {"type": "string"},
    }
    assert fields.collect(['--payload:json={"acl": true}'], nested) == {
        "payload": {"acl": True}
    }
    keyfile = tmp_path / "id_rsa.pub"
    keyfile.write_text("ssh-ed25519 AAAA...\n", encoding="utf-8")
    assert fields.collect([f"--key=@{keyfile}"], nested) == {
        "key": "ssh-ed25519 AAAA..."
    }


def test_dotted_names_build_a_nested_object():
    nested = {
        "options": {
            "type": "object",
            "properties": {
                "acl": {"type": "boolean"},
                "purpose": {"type": "string"},
            },
        }
    }
    assert fields.collect(
        ["--options.acl=true", "--options.purpose=share"], nested
    ) == {"options": {"acl": True, "purpose": "share"}}


def test_an_unknown_nested_name_says_where():
    nested = {"options": {"type": "object", "properties": {"acl": {"type": "boolean"}}}}
    with pytest.raises(fields.FieldError, match="unknown field 'acls' for options"):
        fields.collect(["--options.acls=true"], nested)
