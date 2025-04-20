from functools import cached_property
import logging

from . import _conn
from . import auth as _auth
from .namespace import Namespace

class TrueNASClient:
    def __init__(
        self,
        target: str = None,
        creds: "tuple[str,str]|str|dict" = None,
        autologin=True,
        sslverify=True,
        *,
        api=None,
        logger: logging.Logger = None,
    ) -> None:
        self._target = target or "localhost"
        self._creds = _auth.Credentials(creds)
        self._conn: _conn.JSONRPCClient = None
        self.sslverify = sslverify
        self.autologin = autologin
        self.api_uri = api or self._target
        if not logger:
            logger = logging.getLogger("pytruenas")
        self.logger = logging.getLogger(logger) if isinstance(logger, str) else logger

    @property
    def api_uri(self):
        return self._api

    @api_uri.setter
    def api_uri(self, value: str):
        if not value or value.lower() in ["localhost", "127.0.0.1"]:
            self._api = None
        else:
            self._api = f"wss://{value}/api/current"

    @property
    def conn(self):
        if self._conn is None or self._conn._closed.is_set():
            self._conn = _conn.Client(self.api_uri, verify_ssl=self.sslverify)
            if self.autologin:
                self._creds.login(self)
        return self._conn

    @cached_property
    def api(self):
        return Namespace(self)
