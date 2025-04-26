from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class CloudsyncCredentials(_NS):
    
    def create(self,
        cloud_sync_credentials_create:cloud_sync_credentials_create,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CloudsyncCredentialsCreate:
        """Create Cloud Sync Credentials.

`attributes` is a dictionary of valid values which will be used to authorize with the `provider`."""
        ...
    def delete(self,
        id:int,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Delete Cloud Sync Credentials of `id`."""
        ...
    def get_instance(self,
        id:int,
        options:options={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CloudsyncCredentialsGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:options={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[CloudCredentialQueryResultItem]|CloudCredentialQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        cloud_sync_credentials_update:cloud_sync_credentials_update,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CloudsyncCredentialsUpdate:
        """Update Cloud Sync Credentials of `id`."""
        ...
    def verify(self,
        cloud_sync_credentials_create:AzureBlobCredentialsModel|B2CredentialsModel|BoxCredentialsModel|DropboxCredentialsModel|FTPCredentialsModel|GoogleCloudStorageCredentialsModel|GoogleDriveCredentialsModel|GooglePhotosCredentialsModel|HTTPCredentialsModel|HubicCredentialsModel|MegaCredentialsModel|OneDriveCredentialsModel|PCloudCredentialsModel|S3CredentialsModel|SFTPCredentialsModel|StorjIxCredentialsModel|SwiftCredentialsModel|WebDavCredentialsModel|YandexCredentialsModel,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CloudsyncCredentialsVerify:
        """Verify if `attributes` provided for `provider` are authorized by the `provider`."""
        ...
cloud_sync_credentials_create = _ty.TypedDict('cloud_sync_credentials_create', {
    'name': str,
    'provider': _jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue, 
})
CloudsyncCredentialsCreate = _ty.TypedDict('CloudsyncCredentialsCreate', {
    'id': int,
    'name': str,
    'provider': _jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue, 
})
options = _ty.TypedDict('options', {
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
CloudsyncCredentialsGet_instance = _ty.TypedDict('CloudsyncCredentialsGet_instance', {
    'id': int,
    'name': str,
    'provider': _jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue, 
})
CloudCredentialQueryResultItem = _ty.TypedDict('CloudCredentialQueryResultItem', {
    'id': _ty.NotRequired[int],
    'name': _ty.NotRequired[str],
    'provider': _ty.NotRequired[_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue], 
})
cloud_sync_credentials_update = _ty.TypedDict('cloud_sync_credentials_update', {
    'name': _ty.NotRequired[str],
    'provider': _ty.NotRequired[_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue], 
})
CloudsyncCredentialsUpdate = _ty.TypedDict('CloudsyncCredentialsUpdate', {
    'id': int,
    'name': str,
    'provider': _jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue, 
})
AzureBlobCredentialsModel = _ty.TypedDict('AzureBlobCredentialsModel', {
    'type': str,
    'account': str,
    'key': str,
    'endpoint': _ty.NotRequired[str|str], 
})
B2CredentialsModel = _ty.TypedDict('B2CredentialsModel', {
    'type': str,
    'account': str,
    'key': str, 
})
BoxCredentialsModel = _ty.TypedDict('BoxCredentialsModel', {
    'type': str,
    'client_id': _ty.NotRequired[str],
    'client_secret': _ty.NotRequired[str],
    'token': str, 
})
DropboxCredentialsModel = _ty.TypedDict('DropboxCredentialsModel', {
    'type': str,
    'client_id': _ty.NotRequired[str],
    'client_secret': _ty.NotRequired[str],
    'token': str, 
})
FTPCredentialsModel = _ty.TypedDict('FTPCredentialsModel', {
    'type': str,
    'host': str,
    'port': _ty.NotRequired[int],
    'user': str,
    'pass': str, 
})
GoogleCloudStorageCredentialsModel = _ty.TypedDict('GoogleCloudStorageCredentialsModel', {
    'type': str,
    'service_account_credentials': str, 
})
GoogleDriveCredentialsModel = _ty.TypedDict('GoogleDriveCredentialsModel', {
    'type': str,
    'client_id': _ty.NotRequired[str],
    'client_secret': _ty.NotRequired[str],
    'token': str,
    'team_drive': _ty.NotRequired[str], 
})
GooglePhotosCredentialsModel = _ty.TypedDict('GooglePhotosCredentialsModel', {
    'type': str,
    'client_id': _ty.NotRequired[str],
    'client_secret': _ty.NotRequired[str],
    'token': str, 
})
HTTPCredentialsModel = _ty.TypedDict('HTTPCredentialsModel', {
    'type': str,
    'url': str, 
})
HubicCredentialsModel = _ty.TypedDict('HubicCredentialsModel', {
    'type': str,
    'token': str, 
})
MegaCredentialsModel = _ty.TypedDict('MegaCredentialsModel', {
    'type': str,
    'user': str,
    'pass': str, 
})
OneDriveCredentialsModel = _ty.TypedDict('OneDriveCredentialsModel', {
    'type': str,
    'client_id': _ty.NotRequired[str],
    'client_secret': _ty.NotRequired[str],
    'token': str,
    'drive_type': str,
    'drive_id': str, 
})
PCloudCredentialsModel = _ty.TypedDict('PCloudCredentialsModel', {
    'type': str,
    'client_id': _ty.NotRequired[str],
    'client_secret': _ty.NotRequired[str],
    'token': str,
    'hostname': _ty.NotRequired[str], 
})
S3CredentialsModel = _ty.TypedDict('S3CredentialsModel', {
    'type': str,
    'access_key_id': str,
    'secret_access_key': str,
    'endpoint': _ty.NotRequired[str],
    'region': _ty.NotRequired[str],
    'skip_region': _ty.NotRequired[bool],
    'signatures_v2': _ty.NotRequired[bool],
    'max_upload_parts': _ty.NotRequired[int], 
})
SFTPCredentialsModel = _ty.TypedDict('SFTPCredentialsModel', {
    'type': str,
    'host': str,
    'port': _ty.NotRequired[int],
    'user': str,
    'pass': _ty.NotRequired[str|None],
    'private_key': _ty.NotRequired[int|None], 
})
StorjIxCredentialsModel = _ty.TypedDict('StorjIxCredentialsModel', {
    'type': str,
    'access_key_id': str,
    'secret_access_key': str, 
})
SwiftCredentialsModel = _ty.TypedDict('SwiftCredentialsModel', {
    'type': str,
    'user': str,
    'key': str,
    'auth': str,
    'user_id': _ty.NotRequired[str],
    'domain': _ty.NotRequired[str],
    'tenant': _ty.NotRequired[str],
    'tenant_id': _ty.NotRequired[str],
    'tenant_domain': _ty.NotRequired[str],
    'region': _ty.NotRequired[str],
    'storage_url': _ty.NotRequired[str],
    'auth_token': _ty.NotRequired[str],
    'application_credential_id': _ty.NotRequired[str],
    'application_credential_name': _ty.NotRequired[str],
    'application_credential_secret': _ty.NotRequired[str],
    'auth_version': int|None,
    'endpoint_type': str|None, 
})
WebDavCredentialsModel = _ty.TypedDict('WebDavCredentialsModel', {
    'type': str,
    'url': str,
    'vendor': str,
    'user': str,
    'pass': str, 
})
YandexCredentialsModel = _ty.TypedDict('YandexCredentialsModel', {
    'type': str,
    'client_id': _ty.NotRequired[str],
    'client_secret': _ty.NotRequired[str],
    'token': str, 
})
CloudsyncCredentialsVerify = _ty.TypedDict('CloudsyncCredentialsVerify', {
    'valid': bool,
    'error': _ty.NotRequired[str|None],
    'excerpt': _ty.NotRequired[str|None], 
})