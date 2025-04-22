from pytruenas import Namespace as _NS 
class AppIx_volume(_NS):
    
    def exists(self,
        name,
    ) -> AppIx_volumeExists:
        """Check if ix-volumes exist for `app_name`."""
        ...
    def query(self,
        filters,
        options,
    ) -> AppIx_volumeQuery:
        """Query ix-volumes with `filters` and `options`."""
        ...
class AppIx_volumeExists:
    ...
class AppIx_volumeQuery:
    ... 