
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Cloudsync(Namespace):
    _namespace:_ty.Literal['cloudsync']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def abort(self, 
        id:'int',
    /) -> None: 
        """
        Aborts cloud sync task.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        """
        ...
    @_ty.overload
    def create(self, 
        cloud_sync_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Creates a new cloud_sync entry.

        Parameters
        ----------
        cloud_sync_create:
            cloud_sync_create
        Returns
        -------
        dict[str]:
            cloudsync_create_returns
        """
        ...
    @_ty.overload
    def create_bucket(self, 
        credentials_id:'int',
        name:'str',
    /) -> None: 
        """
        Creates a new bucket `name` using ` credentials_id`.

        Parameters
        ----------
        credentials_id:
            credentials_id
        name:
            name
        Returns
        -------
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Deletes cloud_sync entry `id`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    @_ty.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'dict[str]'={},
    /) -> None: 
        """
        Returns instance matching `id`. If `id` is not found, Validation error is raised.
        
        Please see `query` method documentation for `options`.

        Parameters
        ----------
        id:
            Returns instance matching `id`. If `id` is not found, Validation error is raised.
        query_options_get_instance:
            query-options-get_instance
        Returns
        -------
        """
        ...
    @_ty.overload
    def list_buckets(self, 
        credentials_id:'int',
    /) -> None: 
        """
        

        Parameters
        ----------
        credentials_id:
            credentials_id
        Returns
        -------
        """
        ...
    @_ty.overload
    def list_directory(self, 
        cloud_sync_ls:'dict[str]'={},
    /) -> None: 
        """
        List contents of a remote bucket / directory.
        
        If remote supports buckets, path is constructed by two keys "bucket"/"folder" in `attributes`.
        If remote does not support buckets, path is constructed using "folder" key only in `attributes`.
        "folder" is directory name and "bucket" is bucket name for remote.
        
        Path examples:
        
        S3 Service
        `bucketname/directory/name`
        
        Dropbox Service
        `directory/name`
        
        `credentials` is a valid id of a Cloud Sync Credential which will be used to connect to the provider.

        Parameters
        ----------
        cloud_sync_ls:
            cloud_sync_ls
        Returns
        -------
        """
        ...
    @_ty.overload
    def providers(self, 
    /) -> None: 
        """
        Returns a list of dictionaries of supported providers for Cloud Sync Tasks.
        
        `credentials_schema` is JSON schema for credentials attributes.
        
        `task_schema` is JSON schema for task attributes.
        
        `buckets` is a boolean value which is set to "true" if provider supports buckets.
        
        Example of a single provider:
        
        [
            {
                "name": "AMAZON_CLOUD_DRIVE",
                "title": "Amazon Cloud Drive",
                "credentials_schema": [
                    {
                        "property": "client_id",
                        "schema": {
                            "title": "Amazon Application Client ID",
                            "_required_": true,
                            "type": "string"
                        }
                    },
                    {
                        "property": "client_secret",
                        "schema": {
                            "title": "Application Key",
                            "_required_": true,
                            "type": "string"
                        }
                    }
                ],
                "credentials_oauth": null,
                "buckets": false,
                "bucket_title": "Bucket",
                "task_schema": []
            }
        ]

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
    def restore(self, 
        id:'int',
        cloud_sync_restore:'dict[str]'={},
    /) -> None: 
        """
        Create the opposite of cloud sync task `id` (PULL if it was PUSH and vice versa).

        Parameters
        ----------
        id:
            id
        cloud_sync_restore:
            cloud_sync_restore
        Returns
        -------
        """
        ...
    @_ty.overload
    def sync(self, 
        id:'int',
        cloud_sync_sync_options:'dict[str]'={},
    /) -> None: 
        """
        Run the cloud_sync job `id`, syncing the local data to remote.

        Parameters
        ----------
        id:
            id
        cloud_sync_sync_options:
            cloud_sync_sync_options
        Returns
        -------
        """
        ...
    @_ty.overload
    def sync_onetime(self, 
        cloud_sync_sync_onetime:'dict[str]'={},
        cloud_sync_sync_onetime_options:'dict[str]'={},
    /) -> None: 
        """
        Run cloud sync task without creating it.

        Parameters
        ----------
        cloud_sync_sync_onetime:
            cloud_sync_sync_onetime
        cloud_sync_sync_onetime_options:
            cloud_sync_sync_onetime_options
        Returns
        -------
        """
        ...
    @_ty.overload
    def update(self, 
        id:'int',
        cloud_sync_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Updates the cloud_sync entry `id` with `data`.

        Parameters
        ----------
        id:
            Updates the cloud_sync entry `id` with `data`.
            Creates a new cloud_sync entry.
        cloud_sync_update:
            cloud_sync_update
        Returns
        -------
        dict[str]:
            cloudsync_update_returns
        """
        ...
