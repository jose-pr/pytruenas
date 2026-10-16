"""Percent-encoding for a host path that is about to be spelled as a URI.

Every path URI pytruenas builds by hand -- ``truenas://`` and ``truenas+ws://``
in :mod:`pytruenas.fs`, and the socket path of a ``ws+unix://`` target --
interpolates a filesystem path into a string that a URI parser then reads and
**percent-decodes**. Interpolated raw, a ``?`` or ``#`` in a filename is read
as the start of a query or fragment and silently truncates the path, and a
genuine ``%xx`` decodes into a different name again.

Every site goes through :func:`quote_uri_path`, so there is one constant and
one function rather than a convention per call site.
"""

from __future__ import annotations

from urllib.parse import quote as _quote

#: RFC 3986 ``pchar``, plus ``/``. Everything legal in a URI path segment is
#: left as written -- including ``:``, so a Windows-flavoured remote path still
#: reads as ``truenas://nas/C:/Temp`` rather than ``/C%3A/Temp`` -- while
#: ``%``, ``?``, ``#``, space and non-ASCII are percent-encoded, because those
#: are what a URI parser would otherwise take for syntax.
URI_PATH_SAFE = "/:@-._~!$&'()*+,;="


def quote_uri_path(path: str) -> str:
    """``path`` percent-encoded for use as the path component of a URI.

    Encode **once**, on the way in. The decoded name is what ``URIPath.path``
    hands back, and that decoded name is what every leg sends -- the SFTP leg
    takes a plain path, not a URI -- so ``100%`` is never doubled into
    ``100%25``.
    """
    return _quote(path, safe=URI_PATH_SAFE)
