import typing as _ty

from . import _utils

if _ty.TYPE_CHECKING:
    from . import TrueNASClient


class _CredentialsMeta(type):
    def __call__(cls, *args, **kwargs):
        if cls is not Credentials:
            inst = cls.__new__(cls, *args, **kwargs)
            inst.__init__(*args, **kwargs)
            return inst
        if not (args or kwargs):
            return LocalAuth()
        if args and kwargs:
            raise AttributeError(args, kwargs)
        if args and len(args) == 1:
            cred = args[0]
            if isinstance(cred, Credentials):
                return cred
            if isinstance(cred, (list, tuple)):
                return BasicAuth(*cred)
            cred = _utils.str_(cred)
            if ":" in cred:
                # : is not valid char in key or token assume is user/pass
                usr, pwd = cred.split(":", maxsplit=1)
                if "\n" in pwd:
                    # assume newline not a common/valid password char
                    pwd, token = pwd.split("\n", maxsplit=1)
                else:
                    token = None
                return BasicAuth(usr, pwd, token)
            else:
                #
                # From what i can see an apikey format is <id>-<64 alpha/numeric chars>
                #
                try:
                    i, k = cred.split("-", maxsplit=1)
                    if i.isnumeric() and k.isalnum() and len(k) == 64:
                        return ApiKeyAuth(cred)
                except:
                    return TokenAuth(cred)
        elif args:
            return BasicAuth(*args)
        else:
            for scls in [scls.__name__ for scls in Credentials.__subclasses__()]:
                try:
                    return scls(**kwargs)
                except:
                    pass

        raise ValueError("Credentials not supported", kwargs)


class Credentials(metaclass=_CredentialsMeta):
    METHOD = None

    def _args(self):
        return NotImplementedError()

    def login(self, client: "TrueNASClient"):
        if self.METHOD:
            return client.call("auth." + self.METHOD, *self._args())
        return None

    @staticmethod
    def from_env(env: _ty.Mapping = None):
        if env is None:
            import os

            env = os.environ
        return Credentials(env.get("TN_CREDS"))


class LocalAuth(Credentials):
    ...


class ApiKeyAuth(Credentials):
    METHOD = "login_with_api_key"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def _args(self):
        return [self.api_key]


class TokenAuth(Credentials):
    METHOD = "login_with_token"

    def __init__(self, token: str) -> None:
        self.token = token

    def _args(self):
        return [self.token]


class BasicAuth(Credentials):
    METHOD = "login"

    def __init__(self, username: str, password: str, otp_token: str = None) -> None:
        self.username = username
        self.password = password
        self.otp_token = otp_token

    def _args(self):
        args = [self.username, self.password]
        if self.otp_token:
            args.append(self.otp_token)
        return args
