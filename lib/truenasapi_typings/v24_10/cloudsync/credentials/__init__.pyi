from pytruenas import Namespace as _NS 
class CloudsyncCredentials(_NS):
    
    def create(self,
        cloud_sync_credentials_create,
    ) -> CloudsyncCredentialsCreate:
        """Create Cloud Sync Credentials.

`attributes` is a dictionary of valid values which will be used to authorize with the `provider`."""
        ...
    def delete(self,
        id,
    ) -> CloudsyncCredentialsDelete:
        """Delete Cloud Sync Credentials of `id`."""
        ...
    def get_instance(self,
        id,
        options,
    ) -> CloudsyncCredentialsGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
    ) -> CloudsyncCredentialsQuery:
        """"""
        ...
    def update(self,
        id,
        cloud_sync_credentials_update,
    ) -> CloudsyncCredentialsUpdate:
        """Update Cloud Sync Credentials of `id`."""
        ...
    def verify(self,
        cloud_sync_credentials_create,
    ) -> CloudsyncCredentialsVerify:
        """Verify if `attributes` provided for `provider` are authorized by the `provider`."""
        ...
class CloudsyncCredentialsCreate:
    ...
class CloudsyncCredentialsDelete:
    ...
class CloudsyncCredentialsGet_instance:
    ...
class CloudsyncCredentialsQuery:
    ...
class CloudsyncCredentialsUpdate:
    ...
class CloudsyncCredentialsVerify:
    ... 