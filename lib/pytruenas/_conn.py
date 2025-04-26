import os as _os

if _os.environ.get("VENDORED_TRUENAS_API_CLIENT", False):
    from .vendor.truenas_api_client import *
else:    
    try:
        from truenas_api_client import * #type:ignore
    except ImportError:
        from .vendor.truenas_api_client import * #type:ignore