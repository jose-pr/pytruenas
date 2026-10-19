"""What TLS certificates the client trusts -- one decision for every leg.

The API websocket, the web shell and the HTTP side channels (upload, download)
all build their context here, so they cannot disagree. ``verify=True`` trusts
what the operating system trusts, checked by the platform's own verifier
through ``truststore`` on Python 3.10+ (Windows CryptoAPI, the macOS Security
framework, OpenSSL with the system's CA paths elsewhere) and by OpenSSL over
its default store on 3.9 -- what hostctl's own ``verify=True`` means. A CA
bundle, named by ``verify`` or by an environment variable, replaces that
trust; a caller's ``ssl.SSLContext`` is used as it is. certifi is never used.
"""

from __future__ import annotations

import os as _os
import ssl as _ssl
import typing as _ty

__all__ = ["Verify", "check", "context", "sslopt"]

#: Environment variables naming a CA bundle, in precedence order; the first one
#: set (non-empty) replaces the OS trust. ``REQUESTS_CA_BUNDLE``/``CURL_CA_BUNDLE``
#: are the ones ``requests`` honours and ``WEBSOCKET_CLIENT_CA_BUNDLE`` the one
#: websocket-client does. truststore itself ignores ``SSL_CERT_FILE`` on Windows
#: and macOS, so it is read here for every platform.
CA_BUNDLE_ENV = (
    "SSL_CERT_FILE",
    "REQUESTS_CA_BUNDLE",
    "CURL_CA_BUNDLE",
    "WEBSOCKET_CLIENT_CA_BUNDLE",
)

#: ``True`` (the OS trust), ``False`` (no verification), a CA bundle path (a
#: file or an OpenSSL hashed directory), or a ready ``ssl.SSLContext``.
Verify = _ty.Union[bool, str, "_os.PathLike[str]", _ssl.SSLContext]


def check(verify: object) -> "bool | str | _ssl.SSLContext":
    """``verify`` validated and normalized: a path becomes ``str``.

    An empty string, or a spelling of a boolean given as a string, is a
    ``ValueError``: as a path it would name a bundle that verifies nothing.
    """
    if isinstance(verify, (bool, _ssl.SSLContext)):
        return verify
    if not isinstance(verify, (str, _os.PathLike)):
        raise TypeError(
            "verify must be a bool, a CA bundle path or an ssl.SSLContext, "
            f"not {type(verify).__name__}"
        )
    path = _os.fspath(verify)
    if not path.strip() or path.strip().casefold() in _BOOLEAN_WORDS:
        raise ValueError(f"verify={path!r} is not a CA bundle path; pass True or False")
    return path


_BOOLEAN_WORDS = frozenset(
    ("0", "1", "true", "false", "yes", "no", "on", "off", "none")
)


def _bundle(verify: "bool | str") -> "tuple[str, str] | None":
    """The CA bundle trusted instead of the OS store, and where it came from."""
    if not isinstance(verify, bool):
        return verify, "verify"
    for name in CA_BUNDLE_ENV:
        value = _os.environ.get(name)
        if value:
            return value, name
    return None


def _os_trust() -> _ssl.SSLContext:
    try:
        import truststore
    except ImportError:  # Python 3.9: the dependency is not installed there
        return _ssl.create_default_context()
    return truststore.SSLContext(_ssl.PROTOCOL_TLS_CLIENT)


def context(verify: object) -> "_ssl.SSLContext | None":
    """A verifying client context for ``verify``, or ``None`` when it is off."""
    verify = check(verify)
    if verify is False:
        return None
    if isinstance(verify, _ssl.SSLContext):
        return verify
    found = _bundle(verify)
    if found is None:
        return _os_trust()
    path, source = found
    if _os.path.isdir(path):
        return _ssl.create_default_context(capath=path)
    if not _os.path.isfile(path):
        # ssl's own error names neither the path nor where it came from.
        raise FileNotFoundError(f"CA bundle from {source} not found: {path}")
    return _ssl.create_default_context(cafile=path)


def sslopt(verify: object) -> "dict[str, object]":
    """websocket-client's ``sslopt`` for ``verify``."""
    ctx = context(verify)
    return {"cert_reqs": _ssl.CERT_NONE} if ctx is None else {"context": ctx}
