"""``TrueNASClient`` -- the historical name for :class:`~pytruenas.host.TrueNASHost`.

The two used to be separate objects that each forwarded half their surface to
the other: ``client.run()`` called ``client.host.run()``, while ``host.api``
called ``host.client.api``, and each held a reference to the other. They are now
one class.

:class:`~pytruenas.host.TrueNASHost` is that class -- a
:class:`hostctl.host.PosixHost` that adds the middleware websocket, the ``api``
namespace, login/2FA, subscriptions, and the upload/download side channels.
``TrueNASClient`` is an alias for it, so every existing import keeps working::

    from pytruenas import TrueNASClient

    client = TrueNASClient("wss://nas", "1-<api-key>")
    client.api.system.info()
    client.run("zpool status")

The alias is not deprecated: "client" is the better word for what a caller
holds, and `TrueNASClient(...)` reads better than `TrueNASHost(...)` at a call
site. `TrueNASHost` is the name the *host* half of the API is documented under
(``run``/``path``/``capabilities``/``last_selection``), and hostctl's registry
dispatches ``truenas+wss://`` URIs to it.
"""

from __future__ import annotations

from .host import TrueNASConfig as TrueNASConfig
from .host import TrueNASHost
from .host import TrueNASHost as TrueNASClient

__all__ = ["TrueNASClient", "TrueNASConfig", "TrueNASHost"]
