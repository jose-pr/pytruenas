from pytruenas import Namespace as _NS 
class IscsiTarget(_NS):
    
    def create(
        iscsi_target_create,
    ) -> IscsiTargetCreate:
        """Create an iSCSI Target.

`groups` is a list of group dictionaries which provide information related to using a `portal`, `initiator`, `authmethod` and `auth` with this target. `auth` represents a valid iSCSI Authorized Access and defaults to null.

`auth_networks` is a list of IP/CIDR addresses which are allowed to use this initiator. If all networks are to be allowed, this field should be left empty."""
        ...
    def delete(
        id,
        force,
        delete_extents,
    ) -> IscsiTargetDelete:
        """Delete iSCSI Target of `id`.

Deleting an iSCSI Target makes sure we delete all Associated Targets which use `id` iSCSI Target."""
        ...
    def get_instance(
        id,
        options,
    ) -> IscsiTargetGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(
        filters,
        options,
    ) -> IscsiTargetQuery:
        """"""
        ...
    def update(
        id,
        iscsi_target_update,
    ) -> IscsiTargetUpdate:
        """Update iSCSI Target of `id`."""
        ...
    def validate_name(
        name,
        existing_id,
    ) -> IscsiTargetValidate_name:
        """Returns validation error for iSCSI target name :param name: name to be validated :param existing_id: id of an existing iSCSI target that will receive this name (or `None` if a new target is being created) :return: error message (or `None` if there is no error)"""
        ...
class IscsiTargetCreate:
    ...
class IscsiTargetDelete:
    ...
class IscsiTargetGet_instance:
    ...
class IscsiTargetQuery:
    ...
class IscsiTargetUpdate:
    ...
class IscsiTargetValidate_name:
    ... 