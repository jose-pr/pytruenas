from pytruenas import Namespace as _NS 
class Staticroute(_NS):
    
    def create(
        data,
    ) -> StaticrouteCreate:
        """Create a Static Route.

Address families of `gateway` and `destination` should match when creating a static route.

`description` is an optional attribute for any notes regarding the static route."""
        ...
    def delete(
        id,
    ) -> StaticrouteDelete:
        """Delete Static Route of `id`."""
        ...
    def get_instance(
        id,
        options,
    ) -> StaticrouteGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(
        filters,
        options,
    ) -> StaticrouteQuery:
        """"""
        ...
    def update(
        id,
        data,
    ) -> StaticrouteUpdate:
        """Update Static Route of `id`."""
        ...
class StaticrouteCreate:
    ...
class StaticrouteDelete:
    ...
class StaticrouteGet_instance:
    ...
class StaticrouteQuery:
    ...
class StaticrouteUpdate:
    ... 