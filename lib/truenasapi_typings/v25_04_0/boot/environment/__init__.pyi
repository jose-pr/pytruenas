from pytruenas import Namespace as _NS 
class BootEnvironment(_NS):
    
    def activate(
        boot_environment_activate,
    ) -> BootEnvironmentActivate:
        """"""
        ...
    def clone(
        boot_environment_clone,
    ) -> BootEnvironmentClone:
        """"""
        ...
    def destroy(
        boot_environment_destroy,
    ) -> BootEnvironmentDestroy:
        """"""
        ...
    def keep(
        boot_environment_destroy,
    ) -> BootEnvironmentKeep:
        """"""
        ...
    def query(
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