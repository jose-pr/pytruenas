from pytruenas import Namespace as _NS 
class Config(_NS):
    
    def reset(self,
        options,
    ) -> ConfigReset:
        """Reset database to configuration defaults.

If `reboot` is true this job will reboot the system after its completed with a delay of 10 seconds."""
        ...
    def save(self,
        options,
    ) -> ConfigSave:
        """Create a tar file of security-sensitive information. These options select which information is included in the tar file:

`secretseed` bool: When true, include password secret seed. `pool_keys` bool: IGNORED and DEPRECATED as it does not apply on SCALE systems. `root_authorized_keys` bool: When true, include "/root/.ssh/authorized_keys" file for the root user.

If none of these options are set, the tar file is not generated and the database file is returned."""
        ...
    def upload(self,
    ) -> ConfigUpload:
        """Accepts a configuration file via job pipe."""
        ...
class ConfigReset:
    ...
class ConfigSave:
    ...
class ConfigUpload:
    ... 