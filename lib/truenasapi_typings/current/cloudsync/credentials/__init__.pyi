from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Credentials(_NS):
    
    def create(self,
        cloud_sync_credentials_create:CreateCloudSyncCredentialsCreate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CreateReturn:
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
        options:GetInstanceOptions={},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GetInstanceReturn:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters:_jsonschema.JsonArray=[],
        options:QueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[QueryCloudCredentialQueryResultItem]|QueryCloudCredentialQueryResultItem|int:
        """"""
        ...
    def update(self,
        id:int,
        cloud_sync_credentials_update:UpdateCloudSyncCredentialsUpdate,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> UpdateReturn:
        """Update Cloud Sync Credentials of `id`."""
        ...
    def verify(self,
        cloud_sync_credentials_create:VerifyAzureBlobCredentialsModel|VerifyB2CredentialsModel|VerifyBoxCredentialsModel|VerifyDropboxCredentialsModel|VerifyFTPCredentialsModel|VerifyGoogleCloudStorageCredentialsModel|VerifyGoogleDriveCredentialsModel|VerifyGooglePhotosCredentialsModel|VerifyHTTPCredentialsModel|VerifyHubicCredentialsModel|VerifyMegaCredentialsModel|VerifyOneDriveCredentialsModel|VerifyPCloudCredentialsModel|VerifyS3CredentialsModel|VerifySFTPCredentialsModel|VerifyStorjIxCredentialsModel|VerifySwiftCredentialsModel|VerifyWebDavCredentialsModel|VerifyYandexCredentialsModel,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> VerifyReturn:
        """Verify if `attributes` provided for `provider` are authorized by the `provider`."""
        ...
CreateCloudSyncCredentialsCreate = _ty.TypedDict('CreateCloudSyncCredentialsCreate', {
    'name': str,
    'provider': _jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue, 
})
CreateReturn = _ty.TypedDict('CreateReturn', {
    'id': int,
    'name': str,
    'provider': _jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue, 
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
    'id': int,
    'name': str,
    'provider': _jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue, 
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
QueryCloudCredentialQueryResultItem = _ty.TypedDict('QueryCloudCredentialQueryResultItem', {
    'id': _ty.NotRequired[int],
    'name': _ty.NotRequired[str],
    'provider': _ty.NotRequired[_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue], 
})
UpdateCloudSyncCredentialsUpdate = _ty.TypedDict('UpdateCloudSyncCredentialsUpdate', {
    'name': _ty.NotRequired[str],
    'provider': _ty.NotRequired[_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue], 
})
UpdateReturn = _ty.TypedDict('UpdateReturn', {
    'id': int,
    'name': str,
    'provider': _jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue|_jsonschema.JsonValue, 
})
VerifyAzureBlobCredentialsModel = _ty.TypedDict('VerifyAzureBlobCredentialsModel', {
    'type': str,
    'account': str,
    'key': str,
    'endpoint': _ty.NotRequired[str|str], 
})
VerifyB2CredentialsModel = _ty.TypedDict('VerifyB2CredentialsModel', {
    'type': str,
    'account': str,
    'key': str, 
})
VerifyBoxCredentialsModel = _ty.TypedDict('VerifyBoxCredentialsModel', {
    'type': str,
    'client_id': _ty.NotRequired[str],
    'client_secret': _ty.NotRequired[str],
    'token': str, 
})
VerifyDropboxCredentialsModel = _ty.TypedDict('VerifyDropboxCredentialsModel', {
    'type': str,
    'client_id': _ty.NotRequired[str],
    'client_secret': _ty.NotRequired[str],
    'token': str, 
})
VerifyFTPCredentialsModel = _ty.TypedDict('VerifyFTPCredentialsModel', {
    'type': str,
    'host': str,
    'port': _ty.NotRequired[int],
    'user': str,
    'pass': str, 
})
VerifyGoogleCloudStorageCredentialsModel = _ty.TypedDict('VerifyGoogleCloudStorageCredentialsModel', {
    'type': str,
    'service_account_credentials': str, 
})
VerifyGoogleDriveCredentialsModel = _ty.TypedDict('VerifyGoogleDriveCredentialsModel', {
    'type': str,
    'client_id': _ty.NotRequired[str],
    'client_secret': _ty.NotRequired[str],
    'token': str,
    'team_drive': _ty.NotRequired[str], 
})
VerifyGooglePhotosCredentialsModel = _ty.TypedDict('VerifyGooglePhotosCredentialsModel', {
    'type': str,
    'client_id': _ty.NotRequired[str],
    'client_secret': _ty.NotRequired[str],
    'token': str, 
})
VerifyHTTPCredentialsModel = _ty.TypedDict('VerifyHTTPCredentialsModel', {
    'type': str,
    'url': str, 
})
VerifyHubicCredentialsModel = _ty.TypedDict('VerifyHubicCredentialsModel', {
    'type': str,
    'token': str, 
})
VerifyMegaCredentialsModel = _ty.TypedDict('VerifyMegaCredentialsModel', {
    'type': str,
    'user': str,
    'pass': str, 
})
VerifyOneDriveCredentialsModel = _ty.TypedDict('VerifyOneDriveCredentialsModel', {
    'type': str,
    'client_id': _ty.NotRequired[str],
    'client_secret': _ty.NotRequired[str],
    'token': str,
    'drive_type': str,
    'drive_id': str, 
})
VerifyPCloudCredentialsModel = _ty.TypedDict('VerifyPCloudCredentialsModel', {
    'type': str,
    'client_id': _ty.NotRequired[str],
    'client_secret': _ty.NotRequired[str],
    'token': str,
    'hostname': _ty.NotRequired[str], 
})
VerifyS3CredentialsModel = _ty.TypedDict('VerifyS3CredentialsModel', {
    'type': str,
    'access_key_id': str,
    'secret_access_key': str,
    'endpoint': _ty.NotRequired[str],
    'region': _ty.NotRequired[str],
    'skip_region': _ty.NotRequired[bool],
    'signatures_v2': _ty.NotRequired[bool],
    'max_upload_parts': _ty.NotRequired[int], 
})
VerifySFTPCredentialsModel = _ty.TypedDict('VerifySFTPCredentialsModel', {
    'type': str,
    'host': str,
    'port': _ty.NotRequired[int],
    'user': str,
    'pass': _ty.NotRequired[str|None],
    'private_key': _ty.NotRequired[int|None], 
})
VerifyStorjIxCredentialsModel = _ty.TypedDict('VerifyStorjIxCredentialsModel', {
    'type': str,
    'access_key_id': str,
    'secret_access_key': str, 
})
VerifySwiftCredentialsModel = _ty.TypedDict('VerifySwiftCredentialsModel', {
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
VerifyWebDavCredentialsModel = _ty.TypedDict('VerifyWebDavCredentialsModel', {
    'type': str,
    'url': str,
    'vendor': str,
    'user': str,
    'pass': str, 
})
VerifyYandexCredentialsModel = _ty.TypedDict('VerifyYandexCredentialsModel', {
    'type': str,
    'client_id': _ty.NotRequired[str],
    'client_secret': _ty.NotRequired[str],
    'token': str, 
})
VerifyReturn = _ty.TypedDict('VerifyReturn', {
    'valid': bool,
    'error': _ty.NotRequired[str|None],
    'excerpt': _ty.NotRequired[str|None], 
})