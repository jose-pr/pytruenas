from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class VirtInstance(_NS):
    
    def create(self,
        virt_instance_create:virt_instance_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtInstanceCreate:
        """Create a new virtualized instance."""
        ...
    def delete(self,
        id:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete an instance."""
        ...
    def device_add(self,
        id:str,
        device:Disk|GPU|Proxy|TPM|USB|NIC|PCI,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Add a device to an instance."""
        ...
    def device_delete(self,
        id:str,
        name:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete a device from an instance."""
        ...
    def device_list(self,
        id:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[Disk|GPU|Proxy|TPM|USB|NIC|PCI]:
        """List all devices associated to an instance."""
        ...
    def device_update(self,
        id:str,
        device:Disk|GPU|Proxy|TPM|USB|NIC|PCI,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Update a device in an instance."""
        ...
    def get_instance(self,
        id:str,
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtInstanceGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def image_choices(self,
        virt_instances_image_choices:virt_instances_image_choices={'remote': 'LINUX_CONTAINERS'},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Provide choices for instance image from a remote repository."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[VirtInstanceQueryResultItem]|VirtInstanceQueryResultItem|int:
        """Query all instances with `query-filters` and `query-options`."""
        ...
    def restart(self,
        id:str,
        stop_args:stop_args={'timeout': -1, 'force': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Restart an instance.

Timeout is how long it should wait for the instance to shutdown cleanly."""
        ...
    def start(self,
        id:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Start an instance."""
        ...
    def stop(self,
        id:str,
        stop_args:stop_args={'timeout': -1, 'force': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Stop an instance.

Timeout is how long it should wait for the instance to shutdown cleanly."""
        ...
    def update(self,
        id:str,
        virt_instance_update:virt_instance_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtInstanceUpdate:
        """Update instance."""
        ...
virt_instance_create = _ty.TypedDict('virt_instance_create', {
    'name': str,
    'iso_volume': _ty.NotRequired[str|None],
    'source_type': _ty.NotRequired[_jsonschema.JsonValue],
    'storage_pool': _ty.NotRequired[str|None],
    'image': _ty.NotRequired[str|None],
    'root_disk_size': _ty.NotRequired[int],
    'root_disk_io_bus': _ty.NotRequired[str],
    'remote': _ty.NotRequired[str],
    'instance_type': _ty.NotRequired[str],
    'environment': _ty.NotRequired[_jsonschema.JsonObject|None],
    'autostart': _ty.NotRequired[bool|None],
    'cpu': _ty.NotRequired[str|None],
    'devices': _ty.NotRequired[list[_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue]|None],
    'memory': _ty.NotRequired[int|None],
    'secure_boot': _ty.NotRequired[bool],
    'enable_vnc': _ty.NotRequired[bool],
    'vnc_port': _ty.NotRequired[int|None],
    'zvol_path': _ty.NotRequired[str|None],
    'volume': _ty.NotRequired[str|None],
    'vnc_password': _ty.NotRequired[str|None], 
})
VirtInstanceCreate = _ty.TypedDict('VirtInstanceCreate', {
    'id': str,
    'name': str,
    'type': _ty.NotRequired[str],
    'status': str,
    'cpu': str|None,
    'memory': int|None,
    'autostart': bool,
    'environment': _jsonschema.JsonObject,
    'aliases': _jsonschema.JsonArray,
    'image': _jsonschema.JsonValue,
    'userns_idmap': _jsonschema.JsonValue|None,
    'raw': _jsonschema.JsonObject|None,
    'vnc_enabled': bool,
    'vnc_port': int|None,
    'vnc_password': str|None,
    'secure_boot': bool|None,
    'root_disk_size': int|None,
    'root_disk_io_bus': _jsonschema.JsonValue,
    'storage_pool': str, 
})
Disk = _ty.TypedDict('Disk', {
    'name': _ty.NotRequired[str|None],
    'description': _ty.NotRequired[str|None],
    'readonly': _ty.NotRequired[bool],
    'dev_type': str,
    'source': _ty.NotRequired[str|None],
    'destination': _ty.NotRequired[str|None],
    'boot_priority': _ty.NotRequired[int|None],
    'io_bus': _ty.NotRequired[_jsonschema.JsonValue],
    'storage_pool': _ty.NotRequired[str|None], 
})
GPU = _ty.TypedDict('GPU', {
    'name': _ty.NotRequired[str|None],
    'description': _ty.NotRequired[str|None],
    'readonly': _ty.NotRequired[bool],
    'dev_type': str,
    'gpu_type': str,
    'id': _ty.NotRequired[str|None],
    'gid': _ty.NotRequired[int|None],
    'uid': _ty.NotRequired[int|None],
    'mode': _ty.NotRequired[str|None],
    'mdev': _ty.NotRequired[str|None],
    'mig_uuid': _ty.NotRequired[str|None],
    'pci': _ty.NotRequired[str|None],
    'productid': _ty.NotRequired[str|None],
    'vendorid': _ty.NotRequired[str|None], 
})
Proxy = _ty.TypedDict('Proxy', {
    'name': _ty.NotRequired[str|None],
    'description': _ty.NotRequired[str|None],
    'readonly': _ty.NotRequired[bool],
    'dev_type': str,
    'source_proto': str,
    'source_port': int,
    'dest_proto': str,
    'dest_port': int, 
})
TPM = _ty.TypedDict('TPM', {
    'name': _ty.NotRequired[str|None],
    'description': _ty.NotRequired[str|None],
    'readonly': _ty.NotRequired[bool],
    'dev_type': str,
    'path': _ty.NotRequired[str|None],
    'pathrm': _ty.NotRequired[str|None], 
})
USB = _ty.TypedDict('USB', {
    'name': _ty.NotRequired[str|None],
    'description': _ty.NotRequired[str|None],
    'readonly': _ty.NotRequired[bool],
    'dev_type': str,
    'bus': _ty.NotRequired[int|None],
    'dev': _ty.NotRequired[int|None],
    'product_id': _ty.NotRequired[str|None],
    'vendor_id': _ty.NotRequired[str|None], 
})
NIC = _ty.TypedDict('NIC', {
    'name': _ty.NotRequired[str|None],
    'description': _ty.NotRequired[str|None],
    'readonly': _ty.NotRequired[bool],
    'dev_type': str,
    'network': _ty.NotRequired[str|None],
    'nic_type': _ty.NotRequired[str|None],
    'parent': _ty.NotRequired[str|None], 
})
PCI = _ty.TypedDict('PCI', {
    'name': _ty.NotRequired[str|None],
    'description': _ty.NotRequired[str|None],
    'readonly': _ty.NotRequired[bool],
    'dev_type': str,
    'address': str, 
})
options = _ty.TypedDict('options', {
    'relationships': _ty.NotRequired[bool],
    'extend': _ty.NotRequired[str|None],
    'extend_context': _ty.NotRequired[str|None],
    'prefix': _ty.NotRequired[str|None],
    'extra': _ty.NotRequired[_jsonschema.JsonObject],
    'order_by': _ty.NotRequired[list[str]],
    'select': _ty.NotRequired[list[str|_jsonschema.JsonArray]],
    'count': _ty.NotRequired[bool],
    'get': _ty.NotRequired[bool],
    'offset': _ty.NotRequired[int],
    'limit': _ty.NotRequired[int],
    'force_sql_filters': _ty.NotRequired[bool], 
})
VirtInstanceGet_instance = _ty.TypedDict('VirtInstanceGet_instance', {
    'id': str,
    'name': str,
    'type': _ty.NotRequired[str],
    'status': str,
    'cpu': str|None,
    'memory': int|None,
    'autostart': bool,
    'environment': _jsonschema.JsonObject,
    'aliases': _jsonschema.JsonArray,
    'image': _jsonschema.JsonValue,
    'userns_idmap': _jsonschema.JsonValue|None,
    'raw': _jsonschema.JsonObject|None,
    'vnc_enabled': bool,
    'vnc_port': int|None,
    'vnc_password': str|None,
    'secure_boot': bool|None,
    'root_disk_size': int|None,
    'root_disk_io_bus': _jsonschema.JsonValue,
    'storage_pool': str, 
})
virt_instances_image_choices = _ty.TypedDict('virt_instances_image_choices', {
    'remote': _ty.NotRequired[str], 
})
VirtInstanceQueryResultItem = _ty.TypedDict('VirtInstanceQueryResultItem', {
    'id': _ty.NotRequired[str],
    'name': _ty.NotRequired[str],
    'type': _ty.NotRequired[str],
    'status': _ty.NotRequired[str],
    'cpu': _ty.NotRequired[str|None],
    'memory': _ty.NotRequired[int|None],
    'autostart': _ty.NotRequired[bool],
    'environment': _ty.NotRequired[_jsonschema.JsonObject],
    'aliases': _ty.NotRequired[_jsonschema.JsonArray],
    'image': _ty.NotRequired[_jsonschema.JsonValue],
    'userns_idmap': _ty.NotRequired[_jsonschema.JsonValue|None],
    'raw': _ty.NotRequired[_jsonschema.JsonObject|None],
    'vnc_enabled': _ty.NotRequired[bool],
    'vnc_port': _ty.NotRequired[int|None],
    'vnc_password': _ty.NotRequired[str|None],
    'secure_boot': _ty.NotRequired[bool|None],
    'root_disk_size': _ty.NotRequired[int|None],
    'root_disk_io_bus': _ty.NotRequired[_jsonschema.JsonValue],
    'storage_pool': _ty.NotRequired[str], 
})
stop_args = _ty.TypedDict('stop_args', {
    'timeout': _ty.NotRequired[int],
    'force': _ty.NotRequired[bool], 
})
virt_instance_update = _ty.TypedDict('virt_instance_update', {
    'environment': _ty.NotRequired[_jsonschema.JsonObject|None],
    'autostart': _ty.NotRequired[bool|None],
    'cpu': _ty.NotRequired[str|None],
    'memory': _ty.NotRequired[int|None],
    'vnc_port': _ty.NotRequired[int|None],
    'enable_vnc': _ty.NotRequired[bool],
    'vnc_password': _ty.NotRequired[str|None],
    'secure_boot': _ty.NotRequired[bool],
    'root_disk_size': _ty.NotRequired[int|None],
    'root_disk_io_bus': _ty.NotRequired[_jsonschema.JsonValue], 
})
VirtInstanceUpdate = _ty.TypedDict('VirtInstanceUpdate', {
    'id': str,
    'name': str,
    'type': _ty.NotRequired[str],
    'status': str,
    'cpu': str|None,
    'memory': int|None,
    'autostart': bool,
    'environment': _jsonschema.JsonObject,
    'aliases': _jsonschema.JsonArray,
    'image': _jsonschema.JsonValue,
    'userns_idmap': _jsonschema.JsonValue|None,
    'raw': _jsonschema.JsonObject|None,
    'vnc_enabled': bool,
    'vnc_port': int|None,
    'vnc_password': str|None,
    'secure_boot': bool|None,
    'root_disk_size': int|None,
    'root_disk_io_bus': _jsonschema.JsonValue,
    'storage_pool': str, 
})