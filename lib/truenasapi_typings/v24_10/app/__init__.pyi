from pytruenas import Namespace as _NS
from .image import AppImage
from .ix_volume import AppIx_volume
from .registry import AppRegistry 
class App(_NS):
    
    def available(self,
        filters,
        options,
    ) -> AppAvailable:
        """Retrieve all available applications from all configured catalogs."""
        ...
    def available_space(self,
    ) -> AppAvailable_space:
        """Returns space available in bytes in the configured apps pool which apps can consume"""
        ...
    def categories(self,
    ) -> AppCategories:
        """Retrieve list of valid categories which have associated applications."""
        ...
    def certificate_authority_choices(self,
    ) -> AppCertificate_authority_choices:
        """Returns certificate authorities which can be used by applications."""
        ...
    def certificate_choices(self,
    ) -> AppCertificate_choices:
        """Returns certificates which can be used by applications."""
        ...
    def config(self,
        app_name,
    ) -> AppConfig:
        """Retrieve user specified configuration of `app_name`."""
        ...
    def container_console_choices(self,
        app_name,
    ) -> AppContainer_console_choices:
        """Returns container console choices for `app_name`."""
        ...
    def container_ids(self,
        app_name,
        options,
    ) -> AppContainer_ids:
        """Returns container IDs for `app_name`."""
        ...
    def convert_to_custom(self,
        app_name,
    ) -> AppConvert_to_custom:
        """Convert `app_name` to a custom app."""
        ...
    def create(self,
        app_create,
    ) -> AppCreate:
        """Create an app with `app_name` using `catalog_app` with `train` and `version`.

TODO: Add support for advanced mode which will enable users to use their own compose files"""
        ...
    def delete(self,
        app_name,
        options,
    ) -> AppDelete:
        """Delete `app_name` app.

`force_remove_ix_volumes` should be set when the ix-volumes were created by the system for apps which were migrated from k8s to docker and the user wants to remove them. This is to prevent accidental deletion of the original ix-volumes which were created in dragonfish and before for kubernetes based apps. When this is set, it will result in the deletion of ix-volumes from both docker based apps and k8s based apps and should be carefully set.

`force_remove_custom_app` should be set when the app being deleted is a custom app and the user wants to forcefully remove the app. A use-case for this attribute is that user had an invalid yaml in his custom app and there are no actual docker resources (network/containers/volumes) in place for the custom app, then docker compose down will fail as the yaml itself is invalid. In this case this flag can be set to proceed with the deletion of the custom app. However if this app had any docker resources in place, then this flag will have no effect."""
        ...
    def get_instance(self,
        id,
        options,
    ) -> AppGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def gpu_choices(self,
    ) -> AppGpu_choices:
        """Returns GPU choices which can be used by applications."""
        ...
    def ip_choices(self,
    ) -> AppIp_choices:
        """Returns IP choices which can be used by applications."""
        ...
    def latest(self,
        filters,
        options,
    ) -> AppLatest:
        """Retrieve latest updated apps."""
        ...
    def outdated_docker_images(self,
        app_name,
    ) -> AppOutdated_docker_images:
        """Returns a list of outdated docker images for the specified app `name`."""
        ...
    def pull_images(self,
        app_name,
        options,
    ) -> AppPull_images:
        """Pulls docker images for the specified app `name`."""
        ...
    def query(self,
        filters,
        options,
    ) -> AppQuery:
        """Query all apps with `query-filters` and `query-options`.

`query-options.extra.host_ip` is a string which can be provided to override portal IP address if it is a wildcard.

`query-options.extra.include_app_schema` is a boolean which can be set to include app schema in the response.

`query-options.extra.retrieve_config` is a boolean which can be set to retrieve app configuration used to install/manage app."""
        ...
    def redeploy(self,
        app_name,
    ) -> AppRedeploy:
        """Redeploy `app_name` app."""
        ...
    def rollback(self,
        app_name,
        options,
    ) -> AppRollback:
        """Rollback `app_name` app to previous version."""
        ...
    def rollback_versions(self,
        app_name,
    ) -> AppRollback_versions:
        """Retrieve versions available for rollback for `app_name` app."""
        ...
    def similar(self,
        app_name,
        train,
    ) -> AppSimilar:
        """Retrieve applications which are similar to `app_name`."""
        ...
    def start(self,
        app_name,
    ) -> AppStart:
        """Start `app_name` app."""
        ...
    def stop(self,
        app_name,
    ) -> AppStop:
        """Stop `app_name` app."""
        ...
    def update(self,
        app_name,
        update,
    ) -> AppUpdate:
        """Update `app_name` app with new configuration."""
        ...
    def upgrade(self,
        app_name,
        options,
    ) -> AppUpgrade:
        """Upgrade `app_name` app to `app_version`."""
        ...
    def upgrade_summary(self,
        app_name,
        options,
    ) -> AppUpgrade_summary:
        """Retrieve upgrade summary for `app_name`."""
        ...
    def used_ports(self,
    ) -> AppUsed_ports:
        """Returns ports in use by applications."""
        ...
    image: AppImage
    ix_volume: AppIx_volume
    registry: AppRegistry
class AppAvailable:
    ...
class AppAvailable_space:
    ...
class AppCategories:
    ...
class AppCertificate_authority_choices:
    ...
class AppCertificate_choices:
    ...
class AppConfig:
    ...
class AppContainer_console_choices:
    ...
class AppContainer_ids:
    ...
class AppConvert_to_custom:
    ...
class AppCreate:
    ...
class AppDelete:
    ...
class AppGet_instance:
    ...
class AppGpu_choices:
    ...
class AppIp_choices:
    ...
class AppLatest:
    ...
class AppOutdated_docker_images:
    ...
class AppPull_images:
    ...
class AppQuery:
    ...
class AppRedeploy:
    ...
class AppRollback:
    ...
class AppRollback_versions:
    ...
class AppSimilar:
    ...
class AppStart:
    ...
class AppStop:
    ...
class AppUpdate:
    ...
class AppUpgrade:
    ...
class AppUpgrade_summary:
    ...
class AppUsed_ports:
    ... 