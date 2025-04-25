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
        username = _urlparse.unquote(parts.username or "") or defaults.get("username") or ''
        password = _urlparse.unquote(parts.password or "") or defaults.get("password") or ''
        path = _urlparse.unquote(parts.path or "") or defaults.get("path") or ''
        host = parts.hostname or defaults.get('host') or ''
        port = int(parts.port or defaults.get("port") or 0)
        try:
            if port == 0 and resolve_port:
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
    
    @property
    @_func.lru_cache    
    def is_local(self):
        return self.host.lower() in ["", "localhost", "127.0.0.1"]