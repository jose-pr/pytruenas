
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin
from enum import Enum
import typing
class Vmware(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['vmware']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        _vmware_create:'VmwareCreate',
    /) -> 'dict[str]': 
        """
        Create VMWare snapshot.
        
        `hostname` is a valid IP address / hostname of a VMWare host. When clustering, this is the vCenter server for
        the cluster.
        
        `username` and `password` are the credentials used to authorize access to the VMWare host.
        
        `datastore` is a valid datastore name which exists on the VMWare host.

        Parameters
        ----------
        vmware_create:
            vmware_create
        Returns
        -------
        dict[str]:
            vmware_create_returns
        """
        ...
    @typing.overload
    def dataset_has_vms(self, 
        _dataset:'str',
        _recursive:'bool',
    /) -> None: 
        """
        Returns "true" if `dataset` is configured with a VMWare snapshot

        Parameters
        ----------
        dataset:
            dataset
        recursive:
            recursive
        Returns
        -------
        """
        ...
    @typing.overload
    def delete(self, 
        _id:'int',
    /) -> 'bool': 
        """
        Delete VMWare snapshot of `id`.

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
    @typing.overload
    def get_datastores(self, 
        _vmware_creds:'VmwareCreds',
    /) -> None: 
        """
        Get datastores from VMWare.

        Parameters
        ----------
        vmware_creds:
            vmware-creds
        Returns
        -------
        """
        ...
    @typing.overload
    def get_instance(self, 
        _id:'typing.Union[str, int, bool, dict[str], list]',
        _query_options_get_instance:'QueryOptionsGetInstance',
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
    @typing.overload
    def get_virtual_machines(self, 
        _pk:'int',
    /) -> None: 
        """
        Returns Virtual Machines on the VMWare host identified by `pk`.

        Parameters
        ----------
        pk:
            pk
        Returns
        -------
        """
        ...
    @typing.overload
    def match_datastores_with_datasets(self, 
        _vmware_creds:'VmwareCreds',
    /) -> None: 
        """
        Requests datastores from vCenter server and tries to match them with local filesystems.
        
        Returns a list of datastores, a list of local filesystems and guessed relationship between them.

        Parameters
        ----------
        vmware_creds:
            vmware-creds
        Returns
        -------
        """
        ...
    @typing.overload
    def query(self, 
        _query_filters:'list[list]',
        _query_options:'QueryOptions',
    /) -> 'typing.Union[list, dict[str], int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list, dict[str], int]:
            
        """
        ...
    @typing.overload
    def update(self, 
        _id:'int',
        _vmware_update:'VmwareUpdate',
    /) -> 'dict[str]': 
        """
        Update VMWare snapshot of `id`.

        Parameters
        ----------
        id:
            Update VMWare snapshot of `id`.
            Create VMWare snapshot.
        vmware_update:
            vmware_update
        Returns
        -------
        dict[str]:
            vmware_update_returns
        """
        ...
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    VmwareCreate = typing.TypedDict('VmwareCreate', {
            'datastore':'str',
            'filesystem':'str',
            'hostname':'str',
            'password':'str',
            'username':'str',
    })
    VmwareCreds = typing.TypedDict('VmwareCreds', {
            'hostname':'str',
            'username':'str',
            'password':'str',
    })
    VmwareUpdate = typing.TypedDict('VmwareUpdate', {
            'datastore':'str',
            'filesystem':'str',
            'hostname':'str',
            'password':'str',
            'username':'str',
    })
