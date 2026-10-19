"""The base class of the errors pytruenas raises at run time.

``except pytruenas.TrueNASError`` catches a refused or failed middleware call,
a call timeout, a dropped connection, a failed job and a refused login. Each
class lives beside the code that raises it, and every one is exported from
:mod:`pytruenas`:

* :class:`~pytruenas.connection.ClientException` -- a call the middleware
  failed; ``errno`` carries its error number when it has one.
* :class:`~pytruenas.connection.ValidationErrors` -- the server rejected the
  arguments, per field.
* :class:`~pytruenas.connection.CallTimeout` -- no answer within the timeout.
* :class:`~pytruenas.connection.ConnectionClosed` -- the connection dropped
  before the answer arrived.
* :class:`~pytruenas.connection.JobFailed` -- a middleware job ended in
  ``FAILED`` or ``ABORTED``.
* :class:`~pytruenas.auth.AuthenticationError` -- a login was refused.

A caller's mistake -- an unknown keyword, a malformed connection string -- is
a plain ``TypeError`` or ``ValueError``, not a ``TrueNASError``. A failure
before the websocket is open (a refused port, a TLS or HTTP error during the
handshake) is raised by the socket or websocket-client layer as it is.
"""

from __future__ import annotations

__all__ = ["TrueNASError"]


class TrueNASError(Exception):
    """Base class of every error pytruenas raises at run time."""
