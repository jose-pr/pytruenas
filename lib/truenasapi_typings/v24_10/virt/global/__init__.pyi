from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Global(_NS):
    
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
    ) -> ConfigReturn:
        """"""
        ...
    def get_network(self,
        name:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GetNetworkReturn:
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
        virt_global_update:UpdateVirtGlobalUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update global virtualization settings.

`pool` which pool to use to store instances. None will disable the service.

`bridge` which bridge interface to use by default. None means it will automatically create one."""
        ...
ConfigReturn = _ty.TypedDict('ConfigReturn', {
    'id': int,
    'pool': _ty.NotRequired[str|None],
    'dataset': _ty.NotRequired[str|None],
    'storage_pools': _ty.NotRequired[list[str]|None],
    'bridge': _ty.NotRequired[str|None],
    'v4_network': _ty.NotRequired[str|None],
    'v6_network': _ty.NotRequired[str|None],
    'state': _ty.NotRequired[str|None], 
})
GetNetworkReturn = _ty.TypedDict('GetNetworkReturn', {
    'type': str,
    'managed': bool,
    'ipv4_address': str,
    'ipv4_nat': bool,
    'ipv6_address': str,
    'ipv6_nat': bool, 
})
UpdateVirtGlobalUpdate = _ty.TypedDict('UpdateVirtGlobalUpdate', {
    'pool': _ty.NotRequired[str|None],
    'bridge': _ty.NotRequired[str|None],
    'storage_pools': _ty.NotRequired[list[str]|None],
    'v4_network': _ty.NotRequired[str|None],
    'v6_network': _ty.NotRequired[str|None], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'pool': _ty.NotRequired[str|None],
    'dataset': _ty.NotRequired[str|None],
    'storage_pools': _ty.NotRequired[list[str]|None],
    'bridge': _ty.NotRequired[str|None],
    'v4_network': _ty.NotRequired[str|None],
    'v6_network': _ty.NotRequired[str|None],
    'state': _ty.NotRequired[str|None], 
})