from pytruenas import Namespace as _NS 
class IscsiTargetextent(_NS):
    
    def create(
        iscsi_target_to_extent_create,
    ) -> IscsiTargetextentCreate:
        """Create an Associated Target.

`lunid` will be automatically assigned if it is not provided based on the `target`."""
        ...
    def delete(
        id,
        force,
    ) -> IscsiTargetextentDelete:
        """Delete Associated Target of `id`."""
        ...
    def get_instance(
        id,
        options,
    ) -> IscsiTargetextentGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(
        filters,
        options,
    ) -> IscsiTargetextentQuery:
        """"""
        ...
    def update(
        id,
        iscsi_target_to_extent_update,
    ) -> IscsiTargetextentUpdate:
        """Update Associated Target of `id`."""
        ...
class IscsiTargetextentCreate:
    ...
class IscsiTargetextentDelete:
    ...
class IscsiTargetextentGet_instance:
    ...
class IscsiTargetextentQuery:
    ...
class IscsiTargetextentUpdate:
    ... 