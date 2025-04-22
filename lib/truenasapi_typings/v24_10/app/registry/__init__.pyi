from pytruenas import Namespace as _NS 
class AppRegistry(_NS):
    
    def create(self,
        app_registry_create,
    ) -> AppRegistryCreate:
        """Create an app registry entry."""
        ...
    def delete(self,
        id,
    ) -> AppRegistryDelete:
        """Delete an app registry entry."""
        ...
    def get_instance(self,
        id,
        options,
    ) -> AppRegistryGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
    ) -> AppRegistryQuery:
        """"""
        ...
    def update(self,
        id,
        data,
    ) -> AppRegistryUpdate:
        """Update an app registry entry."""
        ...
class AppRegistryCreate:
    ...
class AppRegistryDelete:
    ...
class AppRegistryGet_instance:
    ...
class AppRegistryQuery:
    ...
class AppRegistryUpdate:
    ... 