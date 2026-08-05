import re as _re
import typing as _ty
import urllib.parse as _urlparse

import netimps as _netimps
from hostctl.host import redact_uri as _redact_uri

# ws/wss default ports (80/443) are provided by netimps' built-in scheme table
# (>=0.0.2); no system services database knows the websocket schemes. Earlier
# releases required registering them here -- the netimps>=0.0.2 floor makes that
# unnecessary.


def redact(connectionstring: str) -> str:
    """Strip the password from a raw connection string, leaving a valid URI.

    ``wss://root:secret@nas`` becomes ``wss://root@nas`` -- the password is
    *removed*, not masked. A ``***`` placeholder would make the rendered string
    round-trip into a wrong credential if anything fed it back in, and is not a
    real password anyway; what comes out here is still a usable target.

    Delegates to :func:`hostctl.host.redact_uri`, which is the same function
    hostctl's own dispatch and error paths use, so a target rendered by
    pytruenas and one rendered by hostctl read identically. It never raises: a
    string with no userinfo (a bare host, a unix-socket path) comes back
    unchanged, and characters ``urlsplit`` would silently delete (tab, CR, LF --
    the OTP separator) are encoded first, so a password written with a raw
    newline is removed whole rather than partly surviving.
    """
    if not connectionstring or "@" not in connectionstring:
        # No userinfo delimiter -> nothing to strip; also the fast path for the
        # overwhelmingly common ``host``/``host:port`` positional.
        return connectionstring
    try:
        return _redact_uri(connectionstring)
    except Exception:
        # A malformed target must never turn a log call into a crash; fall back
        # to dropping any ``:pass@`` run so we still don't leak.
        return _re.sub(r"://([^/@]*):([^/@]*)@", r"://\1@", connectionstring)


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
        # ``parse`` stores userinfo/path already ``unquote``-d, so re-``quote``
        # them here to round-trip a credential or path that contains reserved
        # characters (``@ : / #`` etc.). ``safe=""`` also escapes ``/`` inside
        # userinfo; ``path`` keeps ``/`` as a separator. For the common case
        # (no reserved chars) ``quote`` is a no-op, so output is unchanged.
        uri = self.scheme + "://"
        if self.username or self.password:
            user = _urlparse.quote(self.username, safe="")
            if self.password:
                pw = _urlparse.quote(self.password, safe="")
                uri = f"{uri}{user}:{pw}@"
            else:
                # No password -> no ``:`` separator. A trailing ``user:@host``
                # is legal but means "empty password", which is a different
                # claim from "no password given" -- and it is what `redacted`
                # produces, so it must render as the plain ``user@host`` form.
                uri = f"{uri}{user}@"
        uri = f"{uri}{self.host}"
        if self.port:
            uri = f"{uri}:{self.port}"
        if self.path:
            uri = f"{uri}{_urlparse.quote(self.path, safe='/')}"
        if self.query:
            # `safe` keeps the separators a query is MADE of -- `=` between a
            # key and its value, `&`/`;` between pairs -- while still escaping
            # anything else reserved. Quoting them would turn a query back into
            # one opaque string, which is the bug this renders around: a
            # download link's `?auth_token=abc` must reach the server as a
            # query, not as `%3Fauth_token%3Dabc` glued onto the path.
            uri = f"{uri}?{_urlparse.quote(self.query, safe='=&;/')}"
        if self.fragment:
            uri = f"{uri}#{_urlparse.quote(self.fragment, safe='/')}"

        return uri

    @property
    def redacted(self):
        """``uri`` with the password removed -- still a valid, usable URI.

        The username is kept (it aids diagnostics and is not a secret); the
        password is dropped entirely rather than masked, so
        ``wss://root:secret@nas`` renders as ``wss://root@nas``. A placeholder
        would make the rendered form reparse into a *wrong* credential if
        anything fed it back in; removing the password leaves a string that is
        both safe to log and still correct to reconnect with (it just prompts
        for, or is given, the credential separately). A target with no password
        is unchanged.
        """
        if not self.password:
            return self.uri
        return self._replace(password="").uri

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
