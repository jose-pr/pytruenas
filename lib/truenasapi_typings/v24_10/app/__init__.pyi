from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .image import Image
from .ix_volume import IxVolume
from .registry import Registry 
class App(_NS):
    
    def _create(self,
        **fields:_ty.Unpack[AppCreate],
    ) -> CreateReturn:
        """"""
        ...
    def _update(self,
        __selector:_jsonschema.JsonValue=None,
        **fields:_ty.Unpack[Update]={'values': '{}', 'custom_compose_config': '{}', 'custom_compose_config_string': ''},
    ) -> UpdateReturn:
        """"""
        ...
    def available(self,
        filters:_jsonschema.JsonArray=[],
        options:AvailableOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[AvailableAppAvailableResponseQueryResultItem]|AvailableAppAvailableResponseQueryResultItem|int:
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
    ) -> list[CertificateAuthorityChoicesAppCertificate]:
        """Returns certificate authorities which can be used by applications."""
        ...
    def certificate_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[CertificateChoicesAppCertificate]:
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
        options:ContainerIdsOptions={'alive_only': True},
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
    ) -> ConvertToCustomReturn:
        """Convert `app_name` to a custom app."""
        ...
    def create(self,
        app_create:CreateAppCreate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
        """Create an app with `app_name` using `catalog_app` with `train` and `version`.

TODO: Add support for advanced mode which will enable users to use their own compose files"""
        ...
    def delete(self,
        app_name:str,
        options:DeleteOptions={'remove_images': True, 'remove_ix_volumes': False, 'force_remove_ix_volumes': False, 'force_remove_custom_app': False},
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
        options:GetInstanceOptions={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GetInstanceReturn:
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
        options:LatestOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[LatestAppAvailableResponseQueryResultItem]|LatestAppAvailableResponseQueryResultItem|int:
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
        options:PullImagesOptions={'redeploy': True},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Pulls docker images for the specified app `name`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:QueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[QueryAppQueryResultItem]|QueryAppQueryResultItem|int:
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
    ) -> RedeployReturn:
        """Redeploy `app_name` app."""
        ...
    def rollback(self,
        app_name:str,
        options:RollbackOptions,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> RollbackReturn:
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
    ) -> list[SimilarAppAvailableResponse]:
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
        update:UpdateUpdate={'values': '{}', 'custom_compose_config': '{}', 'custom_compose_config_string': ''},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update `app_name` app with new configuration."""
        ...
    def upgrade(self,
        app_name:str,
        options:UpgradeOptions={'app_version': 'latest', 'values': '{}', 'snapshot_hostpaths': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpgradeReturn:
        """Upgrade `app_name` app to `app_version`."""
        ...
    def upgrade_summary(self,
        app_name:str,
        options:UpgradeSummaryOptions={'app_version': 'latest'},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpgradeSummaryReturn:
        """Retrieve upgrade summary for `app_name`."""
        ...
    def used_ports(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[int]:
        """Returns ports in use by applications."""
        ...
    image: Image
    ix_volume: IxVolume
    registry: Registry
AppCreate = _ty.TypedDict('AppCreate', {
    'custom_app': _ty.NotRequired[bool],
    'values': _ty.NotRequired[_jsonschema.JsonObject],
    'custom_compose_config': _ty.NotRequired[_jsonschema.JsonObject],
    'custom_compose_config_string': _ty.NotRequired[str],
    'catalog_app': _ty.NotRequired[str|None],
    'app_name': str,
    'train': _ty.NotRequired[str],
    'version': _ty.NotRequired[str], 
})
Update = _ty.TypedDict('Update', {
    'values': _ty.NotRequired[_jsonschema.JsonObject],
    'custom_compose_config': _ty.NotRequired[_jsonschema.JsonObject],
    'custom_compose_config_string': _ty.NotRequired[str], 
})
AvailableOptions = _ty.TypedDict('AvailableOptions', {
    'relationships': _ty.NotRequired[bool],
    'extend': _ty.NotRequired[str|None],
    'extend_context': _ty.NotRequired[str|None],
    'prefix': _ty.NotRequired[str|None],
    'extra': _ty.NotRequired[_jsonschema.JsonObject],
    'order_by': _ty.NotRequired[list[str]],
    'select': _ty.NotRequired[list[str|_jsonschema.JsonArray]],
    'count': _ty.NotRequired[bool],
    'get': _ty.NotRequired[bool],
    'offset': _ty.NotRequired[int],
    'limit': _ty.NotRequired[int],
    'force_sql_filters': _ty.NotRequired[bool], 
})
AvailableAppAvailableResponseQueryResultItem = _ty.TypedDict('AvailableAppAvailableResponseQueryResultItem', {
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
CertificateAuthorityChoicesAppCertificate = _ty.TypedDict('CertificateAuthorityChoicesAppCertificate', {
    'id': int,
    'name': str, 
})
CertificateChoicesAppCertificate = _ty.TypedDict('CertificateChoicesAppCertificate', {
    'id': int,
    'name': str, 
})
ContainerIdsOptions = _ty.TypedDict('ContainerIdsOptions', {
    'alive_only': _ty.NotRequired[bool], 
})
ConvertToCustomReturn = _ty.TypedDict('ConvertToCustomReturn', {
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
CreateAppCreate = _ty.TypedDict('CreateAppCreate', {
    'custom_app': _ty.NotRequired[bool],
    'values': _ty.NotRequired[_jsonschema.JsonObject],
    'custom_compose_config': _ty.NotRequired[_jsonschema.JsonObject],
    'custom_compose_config_string': _ty.NotRequired[str],
    'catalog_app': _ty.NotRequired[str|None],
    'app_name': str,
    'train': _ty.NotRequired[str],
    'version': _ty.NotRequired[str], 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
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
DeleteOptions = _ty.TypedDict('DeleteOptions', {
    'remove_images': _ty.NotRequired[bool],
    'remove_ix_volumes': _ty.NotRequired[bool],
    'force_remove_ix_volumes': _ty.NotRequired[bool],
    'force_remove_custom_app': _ty.NotRequired[bool], 
})
GetInstanceOptions = _ty.TypedDict('GetInstanceOptions', {
    'relationships': _ty.NotRequired[bool],
    'extend': _ty.NotRequired[str|None],
    'extend_context': _ty.NotRequired[str|None],
    'prefix': _ty.NotRequired[str|None],
    'extra': _ty.NotRequired[_jsonschema.JsonObject],
    'order_by': _ty.NotRequired[list[str]],
    'select': _ty.NotRequired[list[str|_jsonschema.JsonArray]],
    'count': _ty.NotRequired[bool],
    'get': _ty.NotRequired[bool],
    'offset': _ty.NotRequired[int],
    'limit': _ty.NotRequired[int],
    'force_sql_filters': _ty.NotRequired[bool], 
})
GetInstanceReturn = _ty.TypedDict('GetInstanceReturn', {
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
LatestOptions = _ty.TypedDict('LatestOptions', {
    'relationships': _ty.NotRequired[bool],
    'extend': _ty.NotRequired[str|None],
    'extend_context': _ty.NotRequired[str|None],
    'prefix': _ty.NotRequired[str|None],
    'extra': _ty.NotRequired[_jsonschema.JsonObject],
    'order_by': _ty.NotRequired[list[str]],
    'select': _ty.NotRequired[list[str|_jsonschema.JsonArray]],
    'count': _ty.NotRequired[bool],
    'get': _ty.NotRequired[bool],
    'offset': _ty.NotRequired[int],
    'limit': _ty.NotRequired[int],
    'force_sql_filters': _ty.NotRequired[bool], 
})
LatestAppAvailableResponseQueryResultItem = _ty.TypedDict('LatestAppAvailableResponseQueryResultItem', {
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
PullImagesOptions = _ty.TypedDict('PullImagesOptions', {
    'redeploy': _ty.NotRequired[bool], 
})
QueryOptions = _ty.TypedDict('QueryOptions', {
    'relationships': _ty.NotRequired[bool],
    'extend': _ty.NotRequired[str|None],
    'extend_context': _ty.NotRequired[str|None],
    'prefix': _ty.NotRequired[str|None],
    'extra': _ty.NotRequired[_jsonschema.JsonObject],
    'order_by': _ty.NotRequired[list[str]],
    'select': _ty.NotRequired[list[str|_jsonschema.JsonArray]],
    'count': _ty.NotRequired[bool],
    'get': _ty.NotRequired[bool],
    'offset': _ty.NotRequired[int],
    'limit': _ty.NotRequired[int],
    'force_sql_filters': _ty.NotRequired[bool], 
})
QueryAppQueryResultItem = _ty.TypedDict('QueryAppQueryResultItem', {
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
RedeployReturn = _ty.TypedDict('RedeployReturn', {
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
RollbackOptions = _ty.TypedDict('RollbackOptions', {
    'app_version': str,
    'rollback_snapshot': _ty.NotRequired[bool], 
})
RollbackReturn = _ty.TypedDict('RollbackReturn', {
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
SimilarAppAvailableResponse = _ty.TypedDict('SimilarAppAvailableResponse', {
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
UpdateUpdate = _ty.TypedDict('UpdateUpdate', {
    'values': _ty.NotRequired[_jsonschema.JsonObject],
    'custom_compose_config': _ty.NotRequired[_jsonschema.JsonObject],
    'custom_compose_config_string': _ty.NotRequired[str], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
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
UpgradeOptions = _ty.TypedDict('UpgradeOptions', {
    'app_version': _ty.NotRequired[str],
    'values': _ty.NotRequired[_jsonschema.JsonObject],
    'snapshot_hostpaths': _ty.NotRequired[bool], 
})
UpgradeReturn = _ty.TypedDict('UpgradeReturn', {
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
UpgradeSummaryOptions = _ty.TypedDict('UpgradeSummaryOptions', {
    'app_version': _ty.NotRequired[str], 
})
UpgradeSummaryReturn = _ty.TypedDict('UpgradeSummaryReturn', {
    'latest_version': str,
    'latest_human_version': str,
    'upgrade_version': str,
    'upgrade_human_version': str,
    'available_versions_for_upgrade': _jsonschema.JsonArray,
    'changelog': str|None, 
})