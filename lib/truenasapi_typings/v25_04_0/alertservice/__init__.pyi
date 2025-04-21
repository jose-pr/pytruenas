from pytruenas import Namespace as _NS 
class Alertservice(_NS):
    
    def create(
        alert_service_create,
    ) -> AlertserviceCreate:
        """Create an Alert Service of specified `type`.

If `enabled`, it sends alerts to the configured `type` of Alert Service."""
        ...
    def delete(
        id,
    ) -> AlertserviceDelete:
        """Delete Alert Service of `id`."""
        ...
    def get_instance(
        id,
        options,
    ) -> AlertserviceGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(
        filters,
        options,
    ) -> AlertserviceQuery:
        """"""
        ...
    def test(
        alert_service_create,
    ) -> AlertserviceTest:
        """Send a test alert using `type` of Alert Service."""
        ...
    def update(
        id,
        alert_service_update,
    ) -> AlertserviceUpdate:
        """Update Alert Service of `id`."""
        ...
class AlertserviceCreate:
    ...
class AlertserviceDelete:
    ...
class AlertserviceGet_instance:
    ...
class AlertserviceQuery:
    ...
class AlertserviceTest:
    ...
class AlertserviceUpdate:
    ... 