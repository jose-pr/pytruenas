from pytruenas import Namespace as _NS
import typing as _ty
from .image import AppImage
from .ix_volume import AppIx_volume
from .registry import AppRegistry 
class App(_NS):
    
    def available(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppAvailable:
        """Retrieve all available applications from all configured catalogs."""
        ...
    def available_space(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppAvailable_space:
        """Returns space available in bytes in the configured apps pool which apps can consume"""
        ...
    def categories(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppCategories:
        """Retrieve list of valid categories which have associated applications."""
        ...
    def certificate_authority_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppCertificate_authority_choices:
        """Returns certificate authorities which can be used by applications."""
        ...
    def certificate_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppCertificate_choices:
        """Returns certificates which can be used by applications."""
        ...
    def config(self,
        app_name,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppConfig:
        """Retrieve user specified configuration of `app_name`."""
        ...
    def container_console_choices(self,
        app_name,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppContainer_console_choices:
        """Returns container console choices for `app_name`."""
        ...
    def container_ids(self,
        app_name,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppContainer_ids:
        """Returns container IDs for `app_name`."""
        ...
    def convert_to_custom(self,
        app_name,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppConvert_to_custom:
        """Convert `app_name` to a custom app."""
        ...
    def create(self,
        app_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppCreate:
        """Create an app with `app_name` using `catalog_app` with `train` and `version`.

TODO: Add support for advanced mode which will enable users to use their own compose files"""
        ...
    def delete(self,
        app_name,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppDelete:
        """Delete `app_name` app.

`force_remove_ix_volumes` should be set when the ix-volumes were created by the system for apps which were migrated from k8s to docker and the user wants to remove them. This is to prevent accidental deletion of the original ix-volumes which were created in dragonfish and before for kubernetes based apps. When this is set, it will result in the deletion of ix-volumes from both docker based apps and k8s based apps and should be carefully set.

`force_remove_custom_app` should be set when the app being deleted is a custom app and the user wants to forcefully remove the app. A use-case for this attribute is that user had an invalid yaml in his custom app and there are no actual docker resources (network/containers/volumes) in place for the custom app, then docker compose down will fail as the yaml itself is invalid. In this case this flag can be set to proceed with the deletion of the custom app. However if this app had any docker resources in place, then this flag will have no effect."""
        ...
    def get_instance(self,
        id,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def gpu_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppGpu_choices:
        """Returns GPU choices which can be used by applications."""
        ...
    def ip_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppIp_choices:
        """Returns IP choices which can be used by applications."""
        ...
    def latest(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppLatest:
        """Retrieve latest updated apps."""
        ...
    def outdated_docker_images(self,
        app_name,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppOutdated_docker_images:
        """Returns a list of outdated docker images for the specified app `name`."""
        ...
    def pull_images(self,
        app_name,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppPull_images:
        """Pulls docker images for the specified app `name`."""
        ...
    def query(self,
        filters,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppQuery:
        """Query all apps with `query-filters` and `query-options`.

`query-options.extra.host_ip` is a string which can be provided to override portal IP address if it is a wildcard.

`query-options.extra.include_app_schema` is a boolean which can be set to include app schema in the response.

`query-options.extra.retrieve_config` is a boolean which can be set to retrieve app configuration used to install/manage app."""
        ...
    def redeploy(self,
        app_name,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppRedeploy:
        """Redeploy `app_name` app."""
        ...
    def rollback(self,
        app_name,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppRollback:
        """Rollback `app_name` app to previous version."""
        ...
    def rollback_versions(self,
        app_name,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppRollback_versions:
        """Retrieve versions available for rollback for `app_name` app."""
        ...
    def similar(self,
        app_name,
        train,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppSimilar:
        """Retrieve applications which are similar to `app_name`."""
        ...
    def start(self,
        app_name,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppStart:
        """Start `app_name` app."""
        ...
    def stop(self,
        app_name,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppStop:
        """Stop `app_name` app."""
        ...
    def update(self,
        app_name,
        update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppUpdate:
        """Update `app_name` app with new configuration."""
        ...
    def upgrade(self,
        app_name,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppUpgrade:
        """Upgrade `app_name` app to `app_version`."""
        ...
    def upgrade_summary(self,
        app_name,
        options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppUpgrade_summary:
        """Retrieve upgrade summary for `app_name`."""
        ...
    def used_ports(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppUsed_ports:
        """Returns ports in use by applications."""
        ...
    image: AppImage
    ix_volume: AppIx_volume
    registry: AppRegistry
class AppAvailable(_ty.TypedDict):
    ...
class AppAvailable_space(_ty.TypedDict):
    ...
class AppCategories(_ty.TypedDict):
    ...
class AppCertificate_authority_choices(_ty.TypedDict):
    ...
class AppCertificate_choices(_ty.TypedDict):
    ...
class AppConfig(_ty.TypedDict):
    ...
class AppContainer_console_choices(_ty.TypedDict):
    ...
class AppContainer_ids(_ty.TypedDict):
    ...
class AppConvert_to_custom(_ty.TypedDict):
    ...
class AppCreate(_ty.TypedDict):
    ...
class AppDelete(_ty.TypedDict):
    ...
class AppGet_instance(_ty.TypedDict):
    ...
class AppGpu_choices(_ty.TypedDict):
    ...
class AppIp_choices(_ty.TypedDict):
    ...
class AppLatest(_ty.TypedDict):
    ...
class AppOutdated_docker_images(_ty.TypedDict):
    ...
class AppPull_images(_ty.TypedDict):
    ...
class AppQuery(_ty.TypedDict):
    ...
class AppRedeploy(_ty.TypedDict):
    ...
class AppRollback(_ty.TypedDict):
    ...
class AppRollback_versions(_ty.TypedDict):
    ...
class AppSimilar(_ty.TypedDict):
    ...
class AppStart(_ty.TypedDict):
    ...
class AppStop(_ty.TypedDict):
    ...
class AppUpdate(_ty.TypedDict):
    ...
class AppUpgrade(_ty.TypedDict):
    ...
class AppUpgrade_summary(_ty.TypedDict):
    ...
class AppUsed_ports(_ty.TypedDict):
    ... 