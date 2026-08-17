"""Percent-encoding for a host path that is about to be spelled as a URI.

Every path URI pytruenas builds by hand -- ``truenas://`` and ``truenas+ws://``
in :mod:`pytruenas.fs`, ``sftp://`` on :class:`~pytruenas.fs.truenas.TruenasPath`'s
SFTP leg -- interpolates a remote filesystem path into a string that a
``UriPath`` then parses and **uridecodes**. Interpolated raw, a ``?`` or ``#``
in a filename is read as the start of a query or fragment and silently
truncates the path, and a genuine ``%xx`` decodes into a different name again.

Both sites go through :func:`quote_uri_path`, so there is one constant and one
function rather than a convention per call site: 0.4.4 fixed the SFTP leg with
its own local copy of the safe set and left the construction path wrong for a
release, which is the drift this module exists to stop.
"""

from __future__ import annotations

from urllib.parse import quote as _quote

#: RFC 3986 ``pchar``, plus ``/``. Everything legal in a URI path segment is
#: left as written -- including ``:``, so a Windows-flavoured remote path still
#: reads as ``sftp://host:22/C:/Temp`` rather than ``/C%3A/Temp`` -- while
#: ``%``, ``?``, ``#``, space and non-ASCII are percent-encoded, because those
#: are what a URI parser would otherwise take for syntax. Deliberately the same
#: safe set ``hostctl`` uses for its own SFTP leg (``hostctl.host._ssh``, fixed
#: in 0.2.6): two SFTP legs reach the same host, and they must agree on what a
#: filename means.
URI_PATH_SAFE = "/:@-._~!$&'()*+,;="


def quote_uri_path(path: str) -> str:
    """``path`` percent-encoded for use as the path component of a URI.

    Encode **once**, on the way in. The decoded name is what ``UriPath.path``
    hands back, so a leg that re-spells a path as another URI (the SFTP one)
    quotes that decoded value and never an already-quoted one -- which is why
    the two encoding sites compose to a single round trip instead of doubling
    ``100%`` into ``100%25``.
    """
    return _quote(path, safe=URI_PATH_SAFE)
