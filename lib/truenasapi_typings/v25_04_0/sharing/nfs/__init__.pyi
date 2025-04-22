from pytruenas import Namespace as _NS 
class SharingNfs(_NS):
    
    def create(self,
        data,
    ) -> SharingNfsCreate:
        """Create a NFS Share.

`path` local path to be exported.

`aliases` IGNORED, for now.

`networks` is a list of authorized networks that are allowed to access the share having format "network/mask" CIDR notation. If empty, all networks are allowed.

`hosts` is a list of IP's/hostnames which are allowed to access the share. If empty, all IP's/hostnames are allowed.

`expose_snapshots` enable TrueNAS Enterprise feature to allow access to the ZFS snapshot directory over NFS. This feature requires a valid enterprise license."""
        ...
    def delete(self,
        id,
    ) -> SharingNfsDelete:
        """Delete NFS Share of `id`."""
        ...
    def get_instance(self,
        id,
        options,
    ) -> SharingNfsGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
    ) -> SharingNfsQuery:
        """"""
        ...
    def update(self,
        id,
        data,
    ) -> SharingNfsUpdate:
        """Update NFS Share of `id`."""
        ...
class SharingNfsCreate:
    ...
class SharingNfsDelete:
    ...
class SharingNfsGet_instance:
    ...
class SharingNfsQuery:
    ...
class SharingNfsUpdate:
    ... 