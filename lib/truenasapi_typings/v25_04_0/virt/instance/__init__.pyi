from pytruenas import Namespace as _NS 
class VirtInstance(_NS):
    
    def create(self,
        virt_instance_create,
    ) -> VirtInstanceCreate:
        """Create a new virtualized instance."""
        ...
    def delete(self,
        id,
    ) -> VirtInstanceDelete:
        """Delete an instance."""
        ...
    def device_add(self,
        id,
        device,
    ) -> VirtInstanceDevice_add:
        """Add a device to an instance."""
        ...
    def device_delete(self,
        id,
        name,
    ) -> VirtInstanceDevice_delete:
        """Delete a device from an instance."""
        ...
    def device_list(self,
        id,
    ) -> VirtInstanceDevice_list:
        """List all devices associated to an instance."""
        ...
    def device_update(self,
        id,
        device,
    ) -> VirtInstanceDevice_update:
        """Update a device in an instance."""
        ...
    def get_instance(self,
        id,
        options,
    ) -> VirtInstanceGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def image_choices(self,
        virt_instances_image_choices,
    ) -> VirtInstanceImage_choices:
        """Provide choices for instance image from a remote repository."""
        ...
    def query(self,
        filters,
        options,
    ) -> VirtInstanceQuery:
        """Query all instances with `query-filters` and `query-options`."""
        ...
    def restart(self,
        id,
        stop_args,
    ) -> VirtInstanceRestart:
        """Restart an instance.

Timeout is how long it should wait for the instance to shutdown cleanly."""
        ...
    def start(self,
        id,
    ) -> VirtInstanceStart:
        """Start an instance."""
        ...
    def stop(self,
        id,
        stop_args,
    ) -> VirtInstanceStop:
        """Stop an instance.

Timeout is how long it should wait for the instance to shutdown cleanly."""
        ...
    def update(self,
        id,
        virt_instance_update,
    ) -> VirtInstanceUpdate:
        """Update instance."""
        ...
class VirtInstanceCreate:
    ...
class VirtInstanceDelete:
    ...
class VirtInstanceDevice_add:
    ...
class VirtInstanceDevice_delete:
    ...
class VirtInstanceDevice_list:
    ...
class VirtInstanceDevice_update:
    ...
class VirtInstanceGet_instance:
    ...
class VirtInstanceImage_choices:
    ...
class VirtInstanceQuery:
    ...
class VirtInstanceRestart:
    ...
class VirtInstanceStart:
    ...
class VirtInstanceStop:
    ...
class VirtInstanceUpdate:
    ... 