"""Credential parsing / dispatch."""

from unittest.mock import MagicMock

import pytest

from pytruenas.auth import (
    ApiKeyAuth,
    AuthenticationError,
    BasicAuth,
    Credentials,
    LocalAuth,
    TokenAuth,
)


def test_no_args_is_local():
    assert isinstance(Credentials(), LocalAuth)


def test_none_is_local():
    assert isinstance(Credentials(None), LocalAuth)


def test_tuple_is_basic():
    cred = Credentials(("root", "secret"))
    assert isinstance(cred, BasicAuth)
    assert cred._args() == ["root", "secret"]


def test_user_password_string():
    cred = Credentials("root:secret")
    assert isinstance(cred, BasicAuth)
    assert cred.username == "root"
    assert cred.password == "secret"


def test_user_password_with_otp():
    cred = Credentials("root:secret\n123456")
    assert isinstance(cred, BasicAuth)
    assert cred._args() == ["root", "secret", "123456"]


def test_api_key():
    key = "1-" + "a" * 64
    cred = Credentials(key)
    assert isinstance(cred, ApiKeyAuth)
    assert cred._args() == [key]


def test_token_fallback():
    # Not user:pass (no colon) and not an api-key shape -> token.
    cred = Credentials("sometoken")
    assert isinstance(cred, (TokenAuth, ApiKeyAuth))


def test_existing_credentials_passthrough():
    inner = BasicAuth("a", "b")
    assert Credentials(inner) is inner


def test_from_env(monkeypatch):
    monkeypatch.setenv("TN_CREDS", "root:pw")
    cred = Credentials.from_env()
    assert isinstance(cred, BasicAuth)
    assert cred.username == "root"


def test_login_method_names():
    assert LocalAuth().METHOD is None
    assert ApiKeyAuth("1-" + "a" * 64).METHOD == "login_with_api_key"
    assert TokenAuth("t").METHOD == "login_with_token"
    assert BasicAuth("u", "p").METHOD == "login"


# -- modern auth.login_ex ---------------------------------------------------


def _client(login_ex_result, continue_result=None):
    """A fake client whose api.auth.login_ex/login_ex_continue return canned
    responses and record their call args."""
    client = MagicMock()
    client.api.auth.login_ex.return_value = login_ex_result
    client.api.auth.login_ex_continue.return_value = continue_result
    return client


def test_login_ex_password_success():
    client = _client({"response_type": "SUCCESS", "user_info": {"username": "root"}})
    resp = BasicAuth("root", "pw").login_ex(client)
    assert resp["response_type"] == "SUCCESS"
    data = client.api.auth.login_ex.call_args[0][0]
    assert data == {"mechanism": "PASSWORD_PLAIN", "username": "root", "password": "pw"}


def test_login_ex_otp_continuation_uses_credential_token():
    client = _client(
        {"response_type": "OTP_REQUIRED"},
        {"response_type": "SUCCESS"},
    )
    resp = BasicAuth("root", "pw", otp_token="123456").login_ex(client)
    assert resp["response_type"] == "SUCCESS"
    cont = client.api.auth.login_ex_continue.call_args[0][0]
    assert cont == {"mechanism": "OTP_TOKEN", "otp_token": "123456"}


def test_login_ex_otp_continuation_uses_provider():
    client = _client({"response_type": "OTP_REQUIRED"}, {"response_type": "SUCCESS"})
    resp = BasicAuth("root", "pw").login_ex(client, otp_provider=lambda: "654321")
    assert resp["response_type"] == "SUCCESS"
    assert client.api.auth.login_ex_continue.call_args[0][0]["otp_token"] == "654321"


def test_login_ex_otp_required_without_token_raises():
    client = _client({"response_type": "OTP_REQUIRED"})
    with pytest.raises(AuthenticationError) as ei:
        BasicAuth("root", "pw").login_ex(client)
    assert ei.value.response_type == "OTP_REQUIRED"


def test_login_ex_auth_error_raises():
    client = _client({"response_type": "AUTH_ERR"})
    with pytest.raises(AuthenticationError) as ei:
        BasicAuth("root", "bad").login_ex(client)
    assert ei.value.response_type == "AUTH_ERR"


def test_login_ex_login_options_override():
    client = _client({"response_type": "SUCCESS"})
    BasicAuth("root", "pw").login_ex(client, login_options={"reconnect_token": True})
    data = client.api.auth.login_ex.call_args[0][0]
    assert data["login_options"] == {"reconnect_token": True}


def test_login_ex_token_and_apikey_data():
    assert TokenAuth("tok")._login_data() == {"mechanism": "TOKEN_PLAIN", "token": "tok"}
    # api key needs a username for login_ex; without one it falls back (None)
    assert ApiKeyAuth("k")._login_data() is None
    assert ApiKeyAuth("k", username="root")._login_data() == {
        "mechanism": "API_KEY_PLAIN", "username": "root", "api_key": "k",
    }


def test_login_ex_falls_back_to_legacy_when_no_mechanism():
    # LocalAuth has no login_ex form -> login_ex calls legacy login (no-op here)
    client = MagicMock()
    assert LocalAuth().login_ex(client) is None
    client.api.auth.login_ex.assert_not_called()
