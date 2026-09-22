"""What TLS certificates the client trusts -- one decision for every leg.

The API websocket, the web shell and the HTTP side channels (upload, download)
all build their context here, so they cannot disagree. They once did: the
websocket trusted the OS store and ``requests`` its own certifi bundle, so a
certificate trusted by one leg failed the other (measured: the API connected
and every ``filesystem.get`` download raised ``SSLError``).
"""

import os as _os
import ssl as _ssl
import typing as _ty

#: Environment variables naming a CA bundle, in precedence order. The first one
#: set (non-empty) replaces the OS trust store. ``REQUESTS_CA_BUNDLE`` /
#: ``CURL_CA_BUNDLE`` are the ones ``requests`` honors and
#: ``WEBSOCKET_CLIENT_CA_BUNDLE`` the one websocket-client did, so a bundle
#: configured for either library before still applies -- now to both legs.
CA_BUNDLE_ENV = (
    "SSL_CERT_FILE",
    "REQUESTS_CA_BUNDLE",
    "CURL_CA_BUNDLE",
    "WEBSOCKET_CLIENT_CA_BUNDLE",
)

SslVerify = _ty.Union[bool, str, "_os.PathLike[str]"]


def ca_bundle(sslverify: SslVerify) -> "tuple[str, str] | None":
    """The CA bundle to trust instead of the OS store, and where it came from.

    A path given as ``sslverify`` wins; otherwise the first of
    :data:`CA_BUNDLE_ENV` that is set. ``None`` means "the OS trust store".
    """
    if not isinstance(sslverify, bool):
        return _os.fspath(sslverify), "sslverify"
    for name in CA_BUNDLE_ENV:
        value = _os.environ.get(name)
        if value:
            return value, name
    return None


def context(sslverify: SslVerify) -> "_ssl.SSLContext | None":
    """A verifying client context, or ``None`` when verification is off.

    A bundle (see :func:`ca_bundle`) is trusted *instead of* the OS store, not
    in addition to it -- a file or an OpenSSL hashed directory. Without one the
    OS store is the only trust source; certifi is never consulted.
    """
    if sslverify is False:
        return None
    found = ca_bundle(sslverify)
    if found is None:
        return _ssl.create_default_context()
    path, source = found
    if _os.path.isdir(path):
        return _ssl.create_default_context(capath=path)
    if not _os.path.isfile(path):
        # ssl's own error names neither the path nor where it came from.
        raise FileNotFoundError(f"CA bundle from {source} not found: {path}")
    return _ssl.create_default_context(cafile=path)
