from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .image import AppImage
from .ix_volume import AppIx_volume
from .registry import AppRegistry 
class App(_NS):
    
    def available(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[AppAvailableResponseQueryResultItem]|AppAvailableResponseQueryResultItem|int:
        """Retrieve all available applications from all configured catalogs."""
        ...
    def available_space(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> int:
        """Returns space available in bytes in the configured apps pool which apps can consume"""
        ...
    def categories(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[str]:
        """Retrieve list of valid categories which have associated applications."""
        ...
    def certificate_authority_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[AppCertificate]:
        """Returns certificate authorities which can be used by applications."""
        ...
    def certificate_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[AppCertificate]:
        """Returns certificates which can be used by applications."""
        ...
    def config(self,
        app_name:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Retrieve user specified configuration of `app_name`."""
        ...
    def container_console_choices(self,
        app_name:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Returns container console choices for `app_name`."""
        ...
    def container_ids(self,
        app_name:str,
        options:options={'alive_only': True},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Returns container IDs for `app_name`."""
        ...
    def convert_to_custom(self,
        app_name:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppConvert_to_custom:
        """Convert `app_name` to a custom app."""
        ...
    def create(self,
        app_create:app_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppCreate:
        """Create an app with `app_name` using `catalog_app` with `train` and `version`.

TODO: Add support for advanced mode which will enable users to use their own compose files"""
        ...
    def delete(self,
        app_name:str,
        options:options={'remove_images': True, 'remove_ix_volumes': False, 'force_remove_ix_volumes': False, 'force_remove_custom_app': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete `app_name` app.

`force_remove_ix_volumes` should be set when the ix-volumes were created by the system for apps which were migrated from k8s to docker and the user wants to remove them. This is to prevent accidental deletion of the original ix-volumes which were created in dragonfish and before for kubernetes based apps. When this is set, it will result in the deletion of ix-volumes from both docker based apps and k8s based apps and should be carefully set.

`force_remove_custom_app` should be set when the app being deleted is a custom app and the user wants to forcefully remove the app. A use-case for this attribute is that user had an invalid yaml in his custom app and there are no actual docker resources (network/containers/volumes) in place for the custom app, then docker compose down will fail as the yaml itself is invalid. In this case this flag can be set to proceed with the deletion of the custom app. However if this app had any docker resources in place, then this flag will have no effect."""
        ...
    def get_instance(self,
        id:str,
        options:options={},
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
    ) -> _jsonschema.JsonObject:
        """Returns GPU choices which can be used by applications."""
        ...
    def ip_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Returns IP choices which can be used by applications."""
        ...
    def latest(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[AppAvailableResponseQueryResultItem]|AppAvailableResponseQueryResultItem|int:
        """Retrieve latest updated apps."""
        ...
    def outdated_docker_images(self,
        app_name:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[str]:
        """Returns a list of outdated docker images for the specified app `name`."""
        ...
    def pull_images(self,
        app_name:str,
        options:options={'redeploy': True},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Pulls docker images for the specified app `name`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[AppQueryResultItem]|AppQueryResultItem|int:
        """Query all apps with `query-filters` and `query-options`.

`query-options.extra.host_ip` is a string which can be provided to override portal IP address if it is a wildcard.

`query-options.extra.include_app_schema` is a boolean which can be set to include app schema in the response.

`query-options.extra.retrieve_config` is a boolean which can be set to retrieve app configuration used to install/manage app."""
        ...
    def redeploy(self,
        app_name:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppRedeploy:
        """Redeploy `app_name` app."""
        ...
    def rollback(self,
        app_name:str,
        options:options,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppRollback:
        """Rollback `app_name` app to previous version."""
        ...
    def rollback_versions(self,
        app_name:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[str]:
        """Retrieve versions available for rollback for `app_name` app."""
        ...
    def similar(self,
        app_name:str,
        train:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[AppAvailableResponse]:
        """Retrieve applications which are similar to `app_name`."""
        ...
    def start(self,
        app_name:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Start `app_name` app."""
        ...
    def stop(self,
        app_name:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Stop `app_name` app."""
        ...
    def update(self,
        app_name:str,
        update:update={'values': '{}', 'custom_compose_config': '{}', 'custom_compose_config_string': ''},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppUpdate:
        """Update `app_name` app with new configuration."""
        ...
    def upgrade(self,
        app_name:str,
        options:options={'app_version': 'latest', 'values': '{}', 'snapshot_hostpaths': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> AppUpgrade:
        """Upgrade `app_name` app to `app_version`."""
        ...
    def upgrade_summary(self,
        app_name:str,
        options:options={'app_version': 'latest'},
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
    ) -> list[int]:
        """Returns ports in use by applications."""
        ...
    image: AppImage
    ix_volume: AppIx_volume
    registry: AppRegistry
options = _ty.TypedDict('options', {
    'app_version': _ty.NotRequired[str], 
})
AppAvailableResponseQueryResultItem = _ty.TypedDict('AppAvailableResponseQueryResultItem', {
    'app_readme': _ty.NotRequired[str|None],
    'categories': _ty.NotRequired[list[str]],
    'description': _ty.NotRequired[str],
    'healthy': _ty.NotRequired[bool],
    'healthy_error': _ty.NotRequired[str|None],
    'home': _ty.NotRequired[str],
    'location': _ty.NotRequired[str],
    'latest_version': _ty.NotRequired[str|None],
    'latest_app_version': _ty.NotRequired[str|None],
    'latest_human_version': _ty.NotRequired[str|None],
    'last_update': _ty.NotRequired[str|None],
    'name': _ty.NotRequired[str],
    'recommended': _ty.NotRequired[bool],
    'title': _ty.NotRequired[str],
    'maintainers': _ty.NotRequired[_jsonschema.JsonArray],
    'tags': _ty.NotRequired[list[str]],
    'screenshots': _ty.NotRequired[list[str]],
    'sources': _ty.NotRequired[list[str]],
    'icon_url': _ty.NotRequired[str|None],
    'catalog': _ty.NotRequired[str],
    'installed': _ty.NotRequired[bool],
    'train': _ty.NotRequired[str], 
})
AppCertificate = _ty.TypedDict('AppCertificate', {
    'id': int,
    'name': str, 
})
AppConvert_to_custom = _ty.TypedDict('AppConvert_to_custom', {
    'name': str,
    'id': str,
    'state': str,
    'upgrade_available': bool,
    'latest_version': str|None,
    'image_updates_available': bool,
    'custom_app': bool,
    'migrated': bool,
    'human_version': str,
    'version': str,
    'metadata': _jsonschema.JsonObject,
    'active_workloads': _jsonschema.JsonValue,
    'notes': str|None,
    'portals': _jsonschema.JsonObject,
    'version_details': _ty.NotRequired[_jsonschema.JsonObject|None],
    'config': _ty.NotRequired[_jsonschema.JsonObject|None], 
})
app_create = _ty.TypedDict('app_create', {
    'custom_app': _ty.NotRequired[bool],
    'values': _ty.NotRequired[_jsonschema.JsonObject],
    'custom_compose_config': _ty.NotRequired[_jsonschema.JsonObject],
    'custom_compose_config_string': _ty.NotRequired[str],
    'catalog_app': _ty.NotRequired[str|None],
    'app_name': str,
    'train': _ty.NotRequired[str],
    'version': _ty.NotRequired[str], 
})
AppCreate = _ty.TypedDict('AppCreate', {
    'name': str,
    'id': str,
    'state': str,
    'upgrade_available': bool,
    'latest_version': str|None,
    'image_updates_available': bool,
    'custom_app': bool,
    'migrated': bool,
    'human_version': str,
    'version': str,
    'metadata': _jsonschema.JsonObject,
    'active_workloads': _jsonschema.JsonValue,
    'notes': str|None,
    'portals': _jsonschema.JsonObject,
    'version_details': _ty.NotRequired[_jsonschema.JsonObject|None],
    'config': _ty.NotRequired[_jsonschema.JsonObject|None], 
})
AppGet_instance = _ty.TypedDict('AppGet_instance', {
    'name': str,
    'id': str,
    'state': str,
    'upgrade_available': bool,
    'latest_version': str|None,
    'image_updates_available': bool,
    'custom_app': bool,
    'migrated': bool,
    'human_version': str,
    'version': str,
    'metadata': _jsonschema.JsonObject,
    'active_workloads': _jsonschema.JsonValue,
    'notes': str|None,
    'portals': _jsonschema.JsonObject,
    'version_details': _ty.NotRequired[_jsonschema.JsonObject|None],
    'config': _ty.NotRequired[_jsonschema.JsonObject|None], 
})
AppQueryResultItem = _ty.TypedDict('AppQueryResultItem', {
    'name': _ty.NotRequired[str],
    'id': _ty.NotRequired[str],
    'state': _ty.NotRequired[str],
    'upgrade_available': _ty.NotRequired[bool],
    'latest_version': _ty.NotRequired[str|None],
    'image_updates_available': _ty.NotRequired[bool],
    'custom_app': _ty.NotRequired[bool],
    'migrated': _ty.NotRequired[bool],
    'human_version': _ty.NotRequired[str],
    'version': _ty.NotRequired[str],
    'metadata': _ty.NotRequired[_jsonschema.JsonObject],
    'active_workloads': _ty.NotRequired[_jsonschema.JsonValue],
    'notes': _ty.NotRequired[str|None],
    'portals': _ty.NotRequired[_jsonschema.JsonObject],
    'version_details': _ty.NotRequired[_jsonschema.JsonObject|None],
    'config': _ty.NotRequired[_jsonschema.JsonObject|None], 
})
AppRedeploy = _ty.TypedDict('AppRedeploy', {
    'name': str,
    'id': str,
    'state': str,
    'upgrade_available': bool,
    'latest_version': str|None,
    'image_updates_available': bool,
    'custom_app': bool,
    'migrated': bool,
    'human_version': str,
    'version': str,
    'metadata': _jsonschema.JsonObject,
    'active_workloads': _jsonschema.JsonValue,
    'notes': str|None,
    'portals': _jsonschema.JsonObject,
    'version_details': _ty.NotRequired[_jsonschema.JsonObject|None],
    'config': _ty.NotRequired[_jsonschema.JsonObject|None], 
})
AppRollback = _ty.TypedDict('AppRollback', {
    'name': str,
    'id': str,
    'state': str,
    'upgrade_available': bool,
    'latest_version': str|None,
    'image_updates_available': bool,
    'custom_app': bool,
    'migrated': bool,
    'human_version': str,
    'version': str,
    'metadata': _jsonschema.JsonObject,
    'active_workloads': _jsonschema.JsonValue,
    'notes': str|None,
    'portals': _jsonschema.JsonObject,
    'version_details': _ty.NotRequired[_jsonschema.JsonObject|None],
    'config': _ty.NotRequired[_jsonschema.JsonObject|None], 
})
AppAvailableResponse = _ty.TypedDict('AppAvailableResponse', {
    'app_readme': str|None,
    'categories': list[str],
    'description': str,
    'healthy': bool,
    'healthy_error': _ty.NotRequired[str|None],
    'home': str,
    'location': str,
    'latest_version': str|None,
    'latest_app_version': str|None,
    'latest_human_version': str|None,
    'last_update': str|None,
    'name': str,
    'recommended': bool,
    'title': str,
    'maintainers': _jsonschema.JsonArray,
    'tags': list[str],
    'screenshots': list[str],
    'sources': list[str],
    'icon_url': _ty.NotRequired[str|None],
    'catalog': str,
    'installed': bool,
    'train': str, 
})
update = _ty.TypedDict('update', {
    'values': _ty.NotRequired[_jsonschema.JsonObject],
    'custom_compose_config': _ty.NotRequired[_jsonschema.JsonObject],
    'custom_compose_config_string': _ty.NotRequired[str], 
})
AppUpdate = _ty.TypedDict('AppUpdate', {
    'name': str,
    'id': str,
    'state': str,
    'upgrade_available': bool,
    'latest_version': str|None,
    'image_updates_available': bool,
    'custom_app': bool,
    'migrated': bool,
    'human_version': str,
    'version': str,
    'metadata': _jsonschema.JsonObject,
    'active_workloads': _jsonschema.JsonValue,
    'notes': str|None,
    'portals': _jsonschema.JsonObject,
    'version_details': _ty.NotRequired[_jsonschema.JsonObject|None],
    'config': _ty.NotRequired[_jsonschema.JsonObject|None], 
})
AppUpgrade = _ty.TypedDict('AppUpgrade', {
    'name': str,
    'id': str,
    'state': str,
    'upgrade_available': bool,
    'latest_version': str|None,
    'image_updates_available': bool,
    'custom_app': bool,
    'migrated': bool,
    'human_version': str,
    'version': str,
    'metadata': _jsonschema.JsonObject,
    'active_workloads': _jsonschema.JsonValue,
    'notes': str|None,
    'portals': _jsonschema.JsonObject,
    'version_details': _ty.NotRequired[_jsonschema.JsonObject|None],
    'config': _ty.NotRequired[_jsonschema.JsonObject|None], 
})
AppUpgrade_summary = _ty.TypedDict('AppUpgrade_summary', {
    'latest_version': str,
    'latest_human_version': str,
    'upgrade_version': str,
    'upgrade_human_version': str,
    'available_versions_for_upgrade': _jsonschema.JsonArray,
    'changelog': str|None, 
})