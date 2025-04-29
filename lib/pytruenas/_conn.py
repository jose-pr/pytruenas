import os as _os
import typing as _ty

if _os.environ.get("VENDORED_TRUENAS_API_CLIENT", False):
    from .vendor.truenas_api_client import *  # type:ignore
else:
    try:
        from truenas_api_client import *  # type:ignore
    except ImportError:
        from .vendor.truenas_api_client import *  # type:ignore

if _ty.TYPE_CHECKING:
    import truenas_api_client

    class Client(truenas_api_client.JSONRPCClient): ...
