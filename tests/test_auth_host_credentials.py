"""``Credentials.from_host_credentials`` -- the hostctl credential bridge.

hostctl parses a URI's password field (splitting off ``otp:`` and friends)
before pytruenas ever sees it, so this adapter only *selects* a subclass. These
tests pin that mapping, and -- more importantly -- pin that the two projects
actually agree on the wire format, by feeding hostctl's own parser output in.
"""

import pytest

from pytruenas.auth import (
    ApiKeyAuth,
    BasicAuth,
    Credentials,
    LocalAuth,
    TokenAuth,
)


def test_password_maps_to_basic_auth():
    cred = Credentials.from_host_credentials(username="root", password="hunter2")
    assert isinstance(cred, BasicAuth)
    assert cred.username == "root"
    assert cred.password == "hunter2"
    assert cred.otp_token is None


def test_password_with_otp_carries_the_token():
    cred = Credentials.from_host_credentials(
        username="admin", password="hunter2", otp="123456"
    )
    assert isinstance(cred, BasicAuth)
    assert cred.otp_token == "123456"
    # The OTP must reach the legacy auth.login positionally, third.
    assert cred._args() == ["admin", "hunter2", "123456"]


def test_password_without_username_defaults_to_root():
    cred = Credentials.from_host_credentials(password="hunter2")
    assert isinstance(cred, BasicAuth)
    assert cred.username == "root"


def test_api_key_maps_to_api_key_auth():
    cred = Credentials.from_host_credentials(api_key="1-" + "a" * 64)
    assert isinstance(cred, ApiKeyAuth)
    assert cred.username is None
    # No username -> no login_ex form, so it must fall back to the legacy path.
    assert cred._login_data() is None


def test_api_key_with_username_enables_login_ex():
    cred = Credentials.from_host_credentials(username="admin", api_key="k")
    assert isinstance(cred, ApiKeyAuth)
    assert cred._login_data() == {
        "mechanism": "API_KEY_PLAIN",
        "username": "admin",
        "api_key": "k",
    }


def test_token_maps_to_token_auth():
    cred = Credentials.from_host_credentials(token="abc123")
    assert isinstance(cred, TokenAuth)
    assert cred.token == "abc123"


def test_empty_mapping_is_local_auth():
    assert isinstance(Credentials.from_host_credentials(), LocalAuth)


def test_username_alone_is_local_auth():
    # A bare `user@host` with no secret cannot authenticate; local-socket auth
    # is the only sane reading, and it is what a local target means today.
    assert isinstance(Credentials.from_host_credentials(username="root"), LocalAuth)


def test_otp_without_password_is_an_error():
    # Silently dropping it would surface much later as a confusing auth failure.
    with pytest.raises(ValueError, match="otp requires a password"):
        Credentials.from_host_credentials(otp="123456")


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({"token": "t", "api_key": "k"}, TokenAuth),
        ({"api_key": "k", "password": "p"}, ApiKeyAuth),
        ({"token": "t", "password": "p"}, TokenAuth),
    ],
)
def test_precedence_is_deterministic(kwargs, expected):
    # Supplying several mechanisms is a caller error; the documented order just
    # makes the result predictable instead of arbitrary.
    assert isinstance(Credentials.from_host_credentials(**kwargs), expected)


# -- agreement with hostctl's parser ---------------------------------------

hostctl_common = pytest.importorskip("hostctl.host._common")


@pytest.mark.parametrize(
    "raw, password, otp",
    [
        ("hunter2", "hunter2", None),
        ("hunter2\notp:123456", "hunter2", "123456"),
        ("hunter2\r\notp:123456", "hunter2", "123456"),
    ],
)
def test_round_trip_through_hostctl_parse_credentials(raw, password, otp):
    """hostctl splits the string; this adapter consumes the pieces.

    This is the load-bearing test of the whole bridge: it proves the two
    projects agree on the newline/``otp:`` encoding without pytruenas parsing
    anything itself. The CRLF row matters because a password pasted from a file
    or a Windows prompt arrives that way.
    """
    parsed_password, extras = hostctl_common.parse_credentials(raw)
    cred = Credentials.from_host_credentials(
        username="root", password=parsed_password, **extras
    )
    assert isinstance(cred, BasicAuth)
    assert cred.password == password
    assert cred.otp_token == otp


def test_hostctl_extras_are_lowercased_keys():
    # from_host_credentials takes `otp=` as a keyword, so hostctl's casefolding
    # of extra names is what makes `**extras` splat cleanly. Pin it.
    _, extras = hostctl_common.parse_credentials("pw\nOTP:9999")
    assert extras == {"otp": "9999"}
    cred = Credentials.from_host_credentials(password="pw", **extras)
    assert isinstance(cred, BasicAuth)
    assert cred.otp_token == "9999"
