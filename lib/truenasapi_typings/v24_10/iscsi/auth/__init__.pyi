from pytruenas import Namespace as _NS 
class IscsiAuth(_NS):
    
    def create(
        data,
    ) -> IscsiAuthCreate:
        """Create an iSCSI Authorized Access.

`tag` should be unique among all configured iSCSI Authorized Accesses.

`secret` and `peersecret` should have length between 12-16 letters inclusive.

`peeruser` and `peersecret` are provided only when configuring mutual CHAP. `peersecret` should not be similar to `secret`."""
        ...
    def delete(
        id,
    ) -> IscsiAuthDelete:
        """Delete iSCSI Authorized Access of `id`."""
        ...
    def get_instance(
        id,
        options,
    ) -> IscsiAuthGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(
        filters,
        options,
    ) -> IscsiAuthQuery:
        """"""
        ...
    def update(
        id,
        data,
    ) -> IscsiAuthUpdate:
        """Update iSCSI Authorized Access of `id`."""
        ...
class IscsiAuthCreate:
    ...
class IscsiAuthDelete:
    ...
class IscsiAuthGet_instance:
    ...
class IscsiAuthQuery:
    ...
class IscsiAuthUpdate:
    ... 