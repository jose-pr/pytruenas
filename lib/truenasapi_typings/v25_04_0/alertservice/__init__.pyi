from pytruenas import Namespace as _NS
import typing as _ty 
class Alertservice(_NS):
    
    def create(self,
        alert_service_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AlertserviceCreate:
        """Create an Alert Service of specified `type`.

If `enabled`, it sends alerts to the configured `type` of Alert Service."""
        ...
    def delete(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AlertserviceDelete:
        """Delete Alert Service of `id`."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AlertserviceGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AlertserviceQuery:
        """"""
        ...
    def test(self,
        alert_service_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AlertserviceTest:
        """Send a test alert using `type` of Alert Service."""
        ...
    def update(self,
        id,
        alert_service_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AlertserviceUpdate:
        """Update Alert Service of `id`."""
        ...
class AlertserviceCreate(_ty.TypedDict):
    ...
class AlertserviceDelete(_ty.TypedDict):
    ...
class AlertserviceGet_instance(_ty.TypedDict):
    ...
class AlertserviceQuery(_ty.TypedDict):
    ...
class AlertserviceTest(_ty.TypedDict):
    ...
class AlertserviceUpdate(_ty.TypedDict):
    ... 