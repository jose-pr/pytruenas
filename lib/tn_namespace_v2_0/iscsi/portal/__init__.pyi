
from pytruenas import Namespace, TrueNASClient
import typing
class IscsiPortal(Namespace):
    _namespace:typing.Literal['iscsi.portal']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        iscsiportal_create:'IscsiportalCreate'={},
    /) -> 'dict[str]': 
        """
        Create a new iSCSI Portal.
        
        `discovery_authgroup` is required for CHAP and CHAP_MUTUAL.

        Parameters
        ----------
        iscsiportal_create:
            iscsiportal_create
        Returns
        -------
        dict[str]:
            iscsi_portal_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete iSCSI Portal `id`.

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
    def listen_ip_choices(self, 
    /) -> None: 
        """
        Returns possible choices for `listen.ip` attribute of portal create and update.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'list[dict[str]]|dict[str]|int|dict[str]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[dict[str]]:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        iscsiportal_update:'IscsiportalUpdate'={},
    /) -> 'dict[str]': 
        """
        Update iSCSI Portal `id`.

        Parameters
        ----------
        id:
            Update iSCSI Portal `id`.
            Create a new iSCSI Portal.
        iscsiportal_update:
            iscsiportal_update
        Returns
        -------
        dict[str]:
            iscsi_portal_update_returns
        """
        ...

class IscsiportalCreate(typing.TypedDict):
        comment:'str'
        discovery_authmethod:'str'
        discovery_authgroup:'typing.Optional[int]'
        listen:'list[Listen]'
        ...
class Listen(typing.TypedDict):
        ip:'str'
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
class IscsiportalUpdate(typing.TypedDict):
        comment:'str'
        discovery_authmethod:'str'
        discovery_authgroup:'typing.Optional[int]'
        listen:'list[Listen]'
        ...
