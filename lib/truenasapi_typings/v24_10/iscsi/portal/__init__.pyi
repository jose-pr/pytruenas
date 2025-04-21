from pytruenas import Namespace as _NS 
class IscsiPortal(_NS):
    
    def create(
        iscsi_portal_create,
    ) -> IscsiPortalCreate:
        """Create a new iSCSI Portal."""
        ...
    def delete(
        id,
    ) -> IscsiPortalDelete:
        """Delete iSCSI Portal `id`."""
        ...
    def get_instance(
        id,
        options,
    ) -> IscsiPortalGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def listen_ip_choices(
    ) -> IscsiPortalListen_ip_choices:
        """Returns possible choices for `listen.ip` attribute of portal create and update."""
        ...
    def query(
        filters,
        options,
    ) -> IscsiPortalQuery:
        """"""
        ...
    def update(
        id,
        iscsi_portal_update,
    ) -> IscsiPortalUpdate:
        """Update iSCSI Portal `id`."""
        ...
class IscsiPortalCreate:
    ...
class IscsiPortalDelete:
    ...
class IscsiPortalGet_instance:
    ...
class IscsiPortalListen_ip_choices:
    ...
class IscsiPortalQuery:
    ...
class IscsiPortalUpdate:
    ... 