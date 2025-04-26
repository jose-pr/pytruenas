from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class VirtGlobal(_NS):
    
    def bridge_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Bridge choices for virtualization purposes.

Empty means it will be managed/created automatically."""
        ...
    def config(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtGlobalConfig:
        """"""
        ...
    def get_network(self,
        name:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtGlobalGet_network:
        """Details for the given network."""
        ...
    def pool_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Pool choices for virtualization purposes."""
        ...
    def update(self,
        virt_global_update:virt_global_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtGlobalUpdate:
        """Update global virtualization settings.

`pool` which pool to use to store instances. None will disable the service.

`bridge` which bridge interface to use by default. None means it will automatically create one."""
        ...
VirtGlobalConfig = _ty.TypedDict('VirtGlobalConfig', {
    'id': int,
    'pool': _ty.NotRequired[str|None],
    'dataset': _ty.NotRequired[str|None],
    'storage_pools': _ty.NotRequired[list[str]|None],
    'bridge': _ty.NotRequired[str|None],
    'v4_network': _ty.NotRequired[str|None],
    'v6_network': _ty.NotRequired[str|None],
    'state': _ty.NotRequired[str|None], 
})
VirtGlobalGet_network = _ty.TypedDict('VirtGlobalGet_network', {
    'type': str,
    'managed': bool,
    'ipv4_address': str,
    'ipv4_nat': bool,
    'ipv6_address': str,
    'ipv6_nat': bool, 
})
virt_global_update = _ty.TypedDict('virt_global_update', {
    'pool': _ty.NotRequired[str|None],
    'bridge': _ty.NotRequired[str|None],
    'storage_pools': _ty.NotRequired[list[str]|None],
    'v4_network': _ty.NotRequired[str|None],
    'v6_network': _ty.NotRequired[str|None], 
})
VirtGlobalUpdate = _ty.TypedDict('VirtGlobalUpdate', {
    'id': int,
    'pool': _ty.NotRequired[str|None],
    'dataset': _ty.NotRequired[str|None],
    'storage_pools': _ty.NotRequired[list[str]|None],
    'bridge': _ty.NotRequired[str|None],
    'v4_network': _ty.NotRequired[str|None],
    'v6_network': _ty.NotRequired[str|None],
    'state': _ty.NotRequired[str|None], 
})