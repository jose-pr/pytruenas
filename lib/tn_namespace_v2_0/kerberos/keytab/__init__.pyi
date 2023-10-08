
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class KerberosKeytab(Namespace):
    _namespace:_ty.Literal['kerberos.keytab']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        kerberos_keytab_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create a kerberos keytab. Uploaded keytab files will be merged with the system
        keytab under /etc/krb5.keytab.
        
        `file` b64encoded kerberos keytab
        `name` name for kerberos keytab

        Parameters
        ----------
        kerberos_keytab_create:
            kerberos_keytab_create
        Returns
        -------
        dict[str]:
            kerberos_keytab_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete kerberos keytab by id, and force regeneration of
        system keytab.

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
    def system_keytab_list(self, 
    /) -> 'list': 
        """
        Returns content of system keytab (/etc/krb5.keytab).

        Parameters
        ----------
        Returns
        -------
        list:
            system-keytab
        """
        ...
    @_ty.overload
    def update(self, 
        id:'int',
        kerberos_keytab_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update kerberos keytab by id.

        Parameters
        ----------
        id:
            id
        kerberos_keytab_update:
            kerberos_keytab_update
        Returns
        -------
        dict[str]:
            kerberos_keytab_update_returns
        """
        ...
    @_ty.overload
    def upload_keytab(self, 
        keytab_data:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Upload a keytab file. This method expects the keytab file to be uploaded using
        the /_upload/ endpoint.

        Parameters
        ----------
        keytab_data:
            keytab_data
        Returns
        -------
        dict[str]:
            kerberos_keytab_entry
        """
        ...
