from pytruenas import Namespace as _NS 
class VirtGlobal(_NS):
    
    def bridge_choices(
    ) -> VirtGlobalBridge_choices:
        """Bridge choices for virtualization purposes.

Empty means it will be managed/created automatically."""
        ...
    def config(
    ) -> VirtGlobalConfig:
        """"""
        ...
    def get_network(
        name,
    ) -> VirtGlobalGet_network:
        """Details for the given network."""
        ...
    def pool_choices(
    ) -> VirtGlobalPool_choices:
        """Pool choices for virtualization purposes."""
        ...
    def update(
        virt_global_update,
    ) -> VirtGlobalUpdate:
        """Update global virtualization settings.

`pool` which pool to use to store instances. None will disable the service.

`bridge` which bridge interface to use by default. None means it will automatically create one."""
        ...
class VirtGlobalBridge_choices:
    ...
class VirtGlobalConfig:
    ...
class VirtGlobalGet_network:
    ...
class VirtGlobalPool_choices:
    ...
class VirtGlobalUpdate:
    ... 