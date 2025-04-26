from pytruenas import Namespace as _NS
import typing as _ty 
class VirtGlobal(_NS):
    
    def bridge_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtGlobalBridge_choices:
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
        name,
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
    ) -> VirtGlobalPool_choices:
        """Pool choices for virtualization purposes."""
        ...
    def update(self,
        virt_global_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VirtGlobalUpdate:
        """Update global virtualization settings.

`pool` which pool to use to store instances. None will disable the service.

`bridge` which bridge interface to use by default. None means it will automatically create one."""
        ...
class VirtGlobalBridge_choices(_ty.TypedDict):
    ...
class VirtGlobalConfig(_ty.TypedDict):
    ...
class VirtGlobalGet_network(_ty.TypedDict):
    ...
class VirtGlobalPool_choices(_ty.TypedDict):
    ...
class VirtGlobalUpdate(_ty.TypedDict):
    ... 