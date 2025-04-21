from pytruenas import Namespace as _NS 
class AppRegistry(_NS):
    
    def create(
        app_registry_create,
    ) -> AppRegistryCreate:
        """Create an app registry entry."""
        ...
    def delete(
        id,
    ) -> AppRegistryDelete:
        """Delete an app registry entry."""
        ...
    def get_instance(
        id,
        options,
    ) -> AppRegistryGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(
        filters,
        options,
    ) -> AppRegistryQuery:
        """"""
        ...
    def update(
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