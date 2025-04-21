from pytruenas import Namespace as _NS 
class IscsiGlobal(_NS):
    
    def alua_enabled(
    ) -> IscsiGlobalAlua_enabled:
        """Returns whether iSCSI ALUA is enabled or not."""
        ...
    def client_count(
    ) -> IscsiGlobalClient_count:
        """Return currently connected clients count."""
        ...
    def config(
    ) -> IscsiGlobalConfig:
        """"""
        ...
    def iser_enabled(
    ) -> IscsiGlobalIser_enabled:
        """Returns whether iSER is enabled or not."""
        ...
    def sessions(
        query_filters,
        query_options,
    ) -> IscsiGlobalSessions:
        """Get a list of currently running iSCSI sessions. This includes initiator and target names and the unique connection IDs."""
        ...
    def update(
        iscsi_update,
    ) -> IscsiGlobalUpdate:
        """`alua` is a no-op for FreeNAS."""
        ...
class IscsiGlobalAlua_enabled:
    ...
class IscsiGlobalClient_count:
    ...
class IscsiGlobalConfig:
    ...
class IscsiGlobalIser_enabled:
    ...
class IscsiGlobalSessions:
    ...
class IscsiGlobalUpdate:
    ... 