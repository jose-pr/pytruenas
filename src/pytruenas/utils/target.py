import typing as _ty
import urllib.parse as _urlparse

import netimps as _netimps

# The websocket schemes are absent from every system services database, so
# ``getservbyname("wss")`` fails -- which left a TrueNAS websocket URL with
# port 0, the schemes this client uses most. Registering them here teaches
# netimps' scheme table about them; it already knows http/https/ssh.
_netimps.register_port("ws", 80)
_netimps.register_port("wss", 443)


class Target(_ty.NamedTuple):
    scheme: str
    username: str
    password: str
    host: str
    port: int
    path: str
    query: str
    fragment: str

    @classmethod
    def parse(cls, connectionstring: str, resolve_port=True, **defaults):
        for default in defaults:
            if default not in cls._fields:
                raise ValueError(default)
        if "://" not in connectionstring:
            connectionstring = (
                f"{defaults.get('scheme') or 'http'}://{connectionstring or ''}"
            )
        parts = _urlparse.urlsplit(connectionstring)
        scheme = parts.scheme
        username = (
            _urlparse.unquote(parts.username or "") or defaults.get("username") or ""
        )
        password = (
            _urlparse.unquote(parts.password or "") or defaults.get("password") or ""
        )
        path = _urlparse.unquote(parts.path or "") or defaults.get("path") or ""
        host = parts.hostname or defaults.get("host") or ""
        port = int(parts.port or defaults.get("port") or 0)
        if port == 0 and resolve_port:
            # netimps consults its own table before the system services
            # database, so ws/wss resolve here where getservbyname cannot.
            port = _netimps.get_default_port(scheme) or 0

        return cls(
            scheme, username, password, host, port, path, parts.query, parts.fragment
        )

    # NOTE: these were ``@property @lru_cache``; that keeps every Target alive in
    # a module-global cache (a leak) for a trivial concat/lookup. Plain
    # properties -- the work is cheap and Targets are short-lived.
    @property
    def uri(self):
        uri = self.scheme + "://"
        if self.username or self.password:
            uri = f"{uri}{self.username}:{self.password}@"
        uri = f"{uri}{self.host}"
        if self.port:
            uri = f"{uri}:{self.port}"
        if self.path:
            uri = f"{uri}{self.path}"

        return uri

    @property
    def is_local(self):
        return self.host.lower() in ["", "localhost", "127.0.0.1"]

    @property
    def qsl(self):
        query: dict[str, list[str]] = {}
        for k, v in _urlparse.parse_qsl(self.query):
            query.setdefault(k, []).append(v)
        return query

    def query_val(self, key: str, default=None, *, islist=False):
        val = self.qsl.get(key)
        if val is None:
            return [] if islist else default
        if not islist:
            return val[-1]
        else:
            return val
