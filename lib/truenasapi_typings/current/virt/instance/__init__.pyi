from pytruenas import Namespace as _NS
import typing as _ty 
class VirtInstance(_NS):
    
    def create(self,
        virt_instance_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtInstanceCreate:
        """Create a new virtualized instance."""
        ...
    def delete(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtInstanceDelete:
        """Delete an instance."""
        ...
    def device_add(self,
        id,
        device,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtInstanceDevice_add:
        """Add a device to an instance."""
        ...
    def device_delete(self,
        id,
        name,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtInstanceDevice_delete:
        """Delete a device from an instance."""
        ...
    def device_list(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtInstanceDevice_list:
        """List all devices associated to an instance."""
        ...
    def device_update(self,
        id,
        device,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtInstanceDevice_update:
        """Update a device in an instance."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtInstanceGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def image_choices(self,
        virt_instances_image_choices,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtInstanceImage_choices:
        """Provide choices for instance image from a remote repository."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtInstanceQuery:
        """Query all instances with `query-filters` and `query-options`."""
        ...
    def restart(self,
        id,
        stop_args,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtInstanceRestart:
        """Restart an instance.

Timeout is how long it should wait for the instance to shutdown cleanly."""
        ...
    def start(self,
        id,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtInstanceStart:
        """Start an instance."""
        ...
    def stop(self,
        id,
        stop_args,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtInstanceStop:
        """Stop an instance.

Timeout is how long it should wait for the instance to shutdown cleanly."""
        ...
    def update(self,
        id,
        virt_instance_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtInstanceUpdate:
        """Update instance."""
        ...
class VirtInstanceCreate(_ty.TypedDict):
    ...
class VirtInstanceDelete(_ty.TypedDict):
    ...
class VirtInstanceDevice_add(_ty.TypedDict):
    ...
class VirtInstanceDevice_delete(_ty.TypedDict):
    ...
class VirtInstanceDevice_list(_ty.TypedDict):
    ...
class VirtInstanceDevice_update(_ty.TypedDict):
    ...
class VirtInstanceGet_instance(_ty.TypedDict):
    ...
class VirtInstanceImage_choices(_ty.TypedDict):
    ...
class VirtInstanceQuery(_ty.TypedDict):
    ...
class VirtInstanceRestart(_ty.TypedDict):
    ...
class VirtInstanceStart(_ty.TypedDict):
    ...
class VirtInstanceStop(_ty.TypedDict):
    ...
class VirtInstanceUpdate(_ty.TypedDict):
    ... 