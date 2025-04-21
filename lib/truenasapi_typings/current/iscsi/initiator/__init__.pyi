from pytruenas import Namespace as _NS 
class IscsiInitiator(_NS):
    
    def create(
        iscsi_initiator_create,
    ) -> IscsiInitiatorCreate:
        """Create an iSCSI Initiator.

`initiators` is a list of initiator hostnames which are authorized to access an iSCSI Target. To allow all possible initiators, `initiators` can be left empty."""
        ...
    def delete(
        id,
    ) -> IscsiInitiatorDelete:
        """Delete iSCSI initiator of `id`."""
        ...
    def get_instance(
        id,
        options,
    ) -> IscsiInitiatorGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(
        filters,
        options,
    ) -> IscsiInitiatorQuery:
        """"""
        ...
    def update(
        id,
        iscsi_initiator_update,
    ) -> IscsiInitiatorUpdate:
        """Update iSCSI initiator of `id`."""
        ...
class IscsiInitiatorCreate:
    ...
class IscsiInitiatorDelete:
    ...
class IscsiInitiatorGet_instance:
    ...
class IscsiInitiatorQuery:
    ...
class IscsiInitiatorUpdate:
    ... 