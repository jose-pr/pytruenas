"""Package-level exports: __version__ and public names."""

import pytest

import pytruenas


def test_version_exposed_and_matches_metadata():
    from importlib.metadata import version

    assert isinstance(pytruenas.__version__, str)
    assert pytruenas.__version__ == version("pytruenas")


def test_public_api_importable():
    from pytruenas import TrueNASClient, Namespace, Credentials  # noqa: F401

    for name in ("TrueNASClient", "Namespace", "Credentials", "__version__"):
        assert name in pytruenas.__all__


_PUBLIC_MODULES = [
    "pytruenas",
    "pytruenas.auth",
    "pytruenas.connection",
    "pytruenas.exceptions",
    "pytruenas.fs",
    "pytruenas.fs.tnasws",
    "pytruenas.host",
    "pytruenas.models.apidump",
    "pytruenas.models.jsonschema",
    "pytruenas.namespace",
    "pytruenas.providers",
    "pytruenas.utils.io",
    "pytruenas.webshell",
]


@pytest.mark.parametrize("name", _PUBLIC_MODULES)
def test_public_module_declares_all(name):
    import importlib

    module = importlib.import_module(name)
    declared = getattr(module, "__all__", None)
    assert declared is not None, f"{name} has no __all__"
    assert [n for n in declared if not hasattr(module, n)] == []


def test_the_root_declares_the_auth_classes_it_documents():
    """`from pytruenas import ApiKeyAuth` is what the docs write; a name
    outside `__all__` is private to a type checker."""
    for name in (
        "Credentials",
        "LocalAuth",
        "ApiKeyAuth",
        "TokenAuth",
        "BasicAuth",
        "AuthenticationError",
    ):
        assert name in pytruenas.__all__


def test_names_the_root_always_had_stay_importable():
    """Explicit imports replaced `from .auth import *`; nothing it brought in
    is gone."""
    from pytruenas import redact_call_args  # noqa: F401


def test_the_client_class_has_one_name():
    """`TrueNASClient` is the class; there is no second name for it."""
    import pytruenas.host

    assert pytruenas.TrueNASClient.__name__ == "TrueNASClient"
    assert "TrueNASHost" not in pytruenas.__all__
    assert not hasattr(pytruenas, "TrueNASHost")
    assert not hasattr(pytruenas.host, "TrueNASHost")
