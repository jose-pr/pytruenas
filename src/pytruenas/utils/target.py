import re as _re
import typing as _ty
import urllib.parse as _urlparse

import netimps as _netimps

# The websocket schemes are absent from every system services database, so
# ``getservbyname("wss")`` fails -- which left a TrueNAS websocket URL with
# port 0, the schemes this client uses most. Registering them here teaches
# netimps' scheme table about them; it already knows http/https/ssh.
# NOTE: newer netimps seeds ws/wss in its OWN built-in table, so these two
# calls become redundant once the netimps floor is bumped -- they are
# idempotent (re-set the same value) so they stay harmless until then.
_netimps.register_port("ws", 80)
_netimps.register_port("wss", 443)


def redact(connectionstring: str) -> str:
    """Mask the password in a raw connection string for safe logging.

    A best-effort wrapper over :meth:`Target.redacted` that never raises on odd
    input: a string with no parseable userinfo (a bare host, a unix-socket path)
    comes back unchanged. Reach for this at every point a user-supplied target
    reaches a log record or a ``--logto`` filename, so a
    ``wss://root:secret@nas`` positional does not leak ``secret`` by accident.
    Passing credentials in the target is still supported -- this only stops them
    being written where they were never meant to go.
    """
    if not connectionstring or "@" not in connectionstring:
        # No userinfo delimiter -> nothing to mask; also the fast path for the
        # overwhelmingly common ``host``/``host:port`` positional.
        return connectionstring
    try:
        return Target.parse(connectionstring, resolve_port=False).redacted
    except Exception:
        # A malformed target must never turn a log call into a crash; fall back
        # to a blunt mask of any ``user:pass@`` run so we still don't leak.
        return _re.sub(r"://([^/@]*):([^/@]*)@", r"://\1:***@", connectionstring)


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
            pw = _urlparse.quote(self.password, safe="")
            uri = f"{uri}{user}:{pw}@"
        uri = f"{uri}{self.host}"
        if self.port:
            uri = f"{uri}:{self.port}"
        if self.path:
            uri = f"{uri}{_urlparse.quote(self.path, safe='/')}"

        return uri

    @property
    def redacted(self):
        """``uri`` with the password masked -- safe to log or embed in a path.

        The username is kept (it aids diagnostics and is not a secret); only the
        password is replaced with ``***``. A target with no password is
        unchanged. Use this anywhere a connection string reaches a log record or
        a ``--logto`` filename, so a ``wss://root:secret@nas`` positional never
        writes ``secret`` to disk by accident.
        """
        if not self.password:
            return self.uri
        # Build the display string off the already-encoded ``uri`` rather than
        # re-quoting a ``***`` placeholder (``*`` is not URI-unreserved, so it
        # would come back as ``%2A%2A%2A``). Swap the encoded password run for a
        # literal ``***`` between the userinfo ``:`` and the ``@``.
        real = self.uri
        encoded_pw = _urlparse.quote(self.password, safe="")
        return real.replace(f":{encoded_pw}@", ":***@", 1)

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
