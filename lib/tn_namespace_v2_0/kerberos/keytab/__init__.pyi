
from pytruenas import Namespace, TrueNASClient
import typing
class KerberosKeytab(Namespace):
    _namespace:typing.Literal['kerberos.keytab']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        kerberos_keytab_create:'KerberosKeytabCreate'={},
    /) -> 'KerberosKeytabCreateReturns': 
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
        KerberosKeytabCreateReturns:
            kerberos_keytab_create_returns
        """
        ...
    @typing.overload
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
    @typing.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'QueryOptionsGetInstance'={},
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
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'list[KerberosKeytabEntry]|KerberosKeytabEntry|int|KerberosKeytabEntry': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[KerberosKeytabEntry]:
            
        KerberosKeytabEntry:
            
        int:
            
        KerberosKeytabEntry:
            
        """
        ...
    @typing.overload
    def system_keytab_list(self, 
    /) -> 'list[KeytabEntry]': 
        """
        Returns content of system keytab (/etc/krb5.keytab).

        Parameters
        ----------
        Returns
        -------
        list[KeytabEntry]:
            system-keytab
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        kerberos_keytab_update:'KerberosKeytabUpdate'={},
    /) -> 'KerberosKeytabUpdateReturns': 
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
        KerberosKeytabUpdateReturns:
            kerberos_keytab_update_returns
        """
        ...
    @typing.overload
    def upload_keytab(self, 
        keytab_data:'KeytabData'={},
    /) -> 'KerberosKeytabEntry': 
        """
        Upload a keytab file. This method expects the keytab file to be uploaded using
        the /_upload/ endpoint.

        Parameters
        ----------
        keytab_data:
            keytab_data
        Returns
        -------
        KerberosKeytabEntry:
            kerberos_keytab_entry
        """
        ...

class KerberosKeytabCreate(typing.TypedDict):
        file:'str'
        name:'str'
        ...
class KerberosKeytabCreateReturns(typing.TypedDict):
        file:'str'
        name:'str'
        id:'int'
        ...
class QueryOptionsGetInstance(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class QueryOptions(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class KerberosKeytabEntry(typing.TypedDict):
        file:'str'
        name:'str'
        id:'int'
        ...
class KeytabEntry(typing.TypedDict):
        slot:'int'
        kvno:'int'
        principal:'str'
        etype:'str'
        etype_deprecated:'bool'
        date:'str'
        ...
class KerberosKeytabUpdate(typing.TypedDict):
        file:'str'
        name:'str'
        ...
class KerberosKeytabUpdateReturns(typing.TypedDict):
        file:'str'
        name:'str'
        id:'int'
        ...
class KeytabData(typing.TypedDict):
        name:'str'
        ...
