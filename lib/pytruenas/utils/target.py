import typing as _ty
import urllib.parse as _urlparse
import socket as _socket
import functools as _func


class Target(_ty.NamedTuple):
    scheme: str
    username: str
    password: str
    host: str
    port: int
    path: str

    @classmethod
    def parse(cls, connectionstring: str, **defaults):
        if "://" not in connectionstring:
            connectionstring = (
                f"{defaults.get('scheme') or 'http'}://{connectionstring}"
            )
        parts = _urlparse.urlsplit(connectionstring)
        scheme = parts.scheme
        username = _urlparse.unquote(parts.username or "") or defaults.get("username")
        password = _urlparse.unquote(parts.password or "") or defaults.get("password")
        path = _urlparse.unquote(parts.path or "") or defaults.get("path")
        host = parts.hostname
        port = int(parts.port or defaults.get("port") or 0)
        try:
            if port == 0:
                port = _socket.getservbyname(scheme)
        except OSError:
            pass
        return cls(scheme, username, password, host, port, path)

    @property
    @_func.lru_cache    
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