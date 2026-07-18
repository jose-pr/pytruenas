"""Credential parsing / dispatch."""

import pytest

from pytruenas.auth import (
    ApiKeyAuth,
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
