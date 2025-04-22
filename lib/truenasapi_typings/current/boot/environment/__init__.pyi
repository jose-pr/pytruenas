from pytruenas import Namespace as _NS 
class BootEnvironment(_NS):
    
    def activate(self,
        boot_environment_activate,
    ) -> BootEnvironmentActivate:
        """"""
        ...
    def clone(self,
        boot_environment_clone,
    ) -> BootEnvironmentClone:
        """"""
        ...
    def destroy(self,
        boot_environment_destroy,
    ) -> BootEnvironmentDestroy:
        """"""
        ...
    def keep(self,
        boot_environment_destroy,
    ) -> BootEnvironmentKeep:
        """"""
        ...
    def query(self,
        filters,
        options,
    ) -> BootEnvironmentQuery:
        """"""
        ...
class BootEnvironmentActivate:
    ...
class BootEnvironmentClone:
    ...
class BootEnvironmentDestroy:
    ...
class BootEnvironmentKeep:
    ...
class BootEnvironmentQuery:
    ... 