"""The error hierarchy: one base, exported from the package root."""

import pytest

import pytruenas
from pytruenas import TrueNASError
from pytruenas.auth import AuthenticationError
from pytruenas.connection import (
    CallTimeout,
    ClientException,
    ConnectionClosed,
    JobFailed,
    ValidationErrors,
)

_ERRORS = [
    ClientException("[ENOENT] gone", 2),
    ValidationErrors([("user.name", "required", 22)]),
    CallTimeout(),
    ConnectionClosed(sent=False),
    JobFailed({"id": 7, "state": "FAILED", "error": "boom"}),
    AuthenticationError("AUTH_ERR", {}),
]


@pytest.mark.parametrize("error", _ERRORS, ids=lambda e: type(e).__name__)
def test_every_runtime_error_is_a_truenas_error(error):
    with pytest.raises(TrueNASError):
        raise error


@pytest.mark.parametrize("error", _ERRORS, ids=lambda e: type(e).__name__)
def test_every_error_is_exported_from_the_root(error):
    name = type(error).__name__
    assert getattr(pytruenas, name) is type(error)
    assert name in pytruenas.__all__
    assert "TrueNASError" in pytruenas.__all__


def test_the_existing_bases_still_hold():
    """Code catching `ClientException` keeps catching every call error."""
    for kind in (ValidationErrors, CallTimeout, ConnectionClosed, JobFailed):
        assert issubclass(kind, ClientException)
