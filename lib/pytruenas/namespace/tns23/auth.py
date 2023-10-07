from enum import Enum as _Enum
from typing import (
    TYPE_CHECKING as _TYPING,
    TypedDict as _Dict,
)
from .. import _utils
from ..base import TrueNASClient, Namespace

if _TYPING:

    class _Auth(Namespace):
        def check_password(self, username: str, password: str, /) -> bool:
            ...

        def check_user(self, username: str, password: str, /) -> bool:
            ...

        def generate_token(
            self, ttl: int = 600, attrs: dict = {}, match_origin: bool = False, /
        ) -> str:
            ...

        def login(self, username: str, password: str, otp_token: str = None, /) -> bool:
            ...

        def login_with_api_key(self, api_key: str, /) -> bool:
            ...

        def login_with_api_token(self, token: str, /) -> bool:
            ...

        def logout(self) -> bool:
            ...

        def me(self) -> "CurrentUser":
            ...

        def sessions(
            self, filters: list = [], options: dict = {}, /
        ) -> "list[Session]":
            ...

        def set_attribute(self, key: str, value: "str|int|bool|dict|list", /):
            ...

        def terminate_other_sessions(self):
            ...

        def terminate_session(self, id: str, /) -> bool:
            ...

        def two_factor_auth(self, username: str, password: str, /) -> bool:
            ...

else:
    _Auth = Namespace

class Auth(_Auth):
    ...
class Session(_Dict):
    id: str
    current: bool
    internal: bool
    origin: str
    credentials: str
    created_at: str


class CurrentUser(_Dict):
    pw_name: str
    pw_gecos: str
    pw_dir: str
    pw_shell: str
    pw_uid: int
    pw_gid: int
    grouplist: list[int]
    sid_info: dict[str]
    attributes: dict[str]



