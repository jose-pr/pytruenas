from pytruenas import Namespace as _NS
import typing as _ty 
class BootEnvironment(_NS):
    
    def activate(self,
        boot_environment_activate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> BootEnvironmentActivate:
        """"""
        ...
    def clone(self,
        boot_environment_clone,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> BootEnvironmentClone:
        """"""
        ...
    def destroy(self,
        boot_environment_destroy,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> BootEnvironmentDestroy:
        """"""
        ...
    def keep(self,
        boot_environment_destroy,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> BootEnvironmentKeep:
        """"""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> BootEnvironmentQuery:
        """"""
        ...
class BootEnvironmentActivate(_ty.TypedDict):
    ...
class BootEnvironmentClone(_ty.TypedDict):
    ...
class BootEnvironmentDestroy(_ty.TypedDict):
    ...
class BootEnvironmentKeep(_ty.TypedDict):
    ...
class BootEnvironmentQuery(_ty.TypedDict):
    ... 