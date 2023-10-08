
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Vmware(Namespace):
    _namespace:_ty.Literal['vmware']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        vmware_create:'dict[str]'={},
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
    @_ty.overload
    def dataset_has_vms(self, 
        dataset:'str',
        recursive:'bool',
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
    @_ty.overload
    def delete(self, 
        id:'int',
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
    @_ty.overload
    def get_datastores(self, 
        vmware_creds:'dict[str]'={},
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
    def get_virtual_machines(self, 
        pk:'int',
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
    @_ty.overload
    def match_datastores_with_datasets(self, 
        vmware_creds:'dict[str]'={},
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
    def update(self, 
        id:'int',
        vmware_update:'dict[str]'={},
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
