from pytruenas import Namespace as _NS 
class DockerNetwork(_NS):
    
    def get_instance(self,
        id,
        options,
    ) -> DockerNetworkGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
    ) -> DockerNetworkQuery:
        """Query all docker networks"""
        ...
class DockerNetworkGet_instance:
    ...
class DockerNetworkQuery:
    ... 