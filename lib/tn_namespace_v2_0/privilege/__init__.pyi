
from pytruenas import Namespace, TrueNASClient
import typing
class Privilege(Namespace):
    _namespace:typing.Literal['privilege']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        privilege_create:'PrivilegeCreate'={},
    /) -> 'PrivilegeCreateReturns': 
        """
        Creates a privilege.
        
        `name` is a name for privilege (must be unique).
        
        `local_groups` is a list of local user account group GIDs that gain this privilege.
        
        `ds_groups` is list of Directory Service group GIDs that will gain this privilege.
        
        `allowlist` is a list of API endpoints allowed for this privilege.
        
        `web_shell` controls whether users with this privilege are allowed to log in to the Web UI.

        Parameters
        ----------
        privilege_create:
            privilege_create
        Returns
        -------
        PrivilegeCreateReturns:
            privilege_create_returns
        """
        ...
    AllowlistItem = typing.TypedDict('AllowlistItem', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeCreate = typing.TypedDict('PrivilegeCreate', {
            'id':'int',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem_ = typing.TypedDict('AllowlistItem_', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeCreateReturns = typing.TypedDict('PrivilegeCreateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem_]',
            'roles':'list[str]',
            'web_shell':'bool',
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
    AllowlistItem__ = typing.TypedDict('AllowlistItem__', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry = typing.TypedDict('PrivilegeEntry', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem__]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem___ = typing.TypedDict('AllowlistItem___', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry_ = typing.TypedDict('PrivilegeEntry_', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem___]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem____ = typing.TypedDict('AllowlistItem____', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry__ = typing.TypedDict('PrivilegeEntry__', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem____]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem_____ = typing.TypedDict('AllowlistItem_____', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeUpdate = typing.TypedDict('PrivilegeUpdate', {
            'id':'int',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem_____]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem______ = typing.TypedDict('AllowlistItem______', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeUpdateReturns = typing.TypedDict('PrivilegeUpdateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem______]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete the privilege `id`.

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
    AllowlistItem = typing.TypedDict('AllowlistItem', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeCreate = typing.TypedDict('PrivilegeCreate', {
            'id':'int',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem_ = typing.TypedDict('AllowlistItem_', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeCreateReturns = typing.TypedDict('PrivilegeCreateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem_]',
            'roles':'list[str]',
            'web_shell':'bool',
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
    AllowlistItem__ = typing.TypedDict('AllowlistItem__', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry = typing.TypedDict('PrivilegeEntry', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem__]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem___ = typing.TypedDict('AllowlistItem___', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry_ = typing.TypedDict('PrivilegeEntry_', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem___]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem____ = typing.TypedDict('AllowlistItem____', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry__ = typing.TypedDict('PrivilegeEntry__', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem____]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem_____ = typing.TypedDict('AllowlistItem_____', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeUpdate = typing.TypedDict('PrivilegeUpdate', {
            'id':'int',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem_____]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem______ = typing.TypedDict('AllowlistItem______', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeUpdateReturns = typing.TypedDict('PrivilegeUpdateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem______]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    @typing.overload
    def get_instance(self, 
        id:'typing.Union[str, int, bool, dict[str], list]',
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
    AllowlistItem = typing.TypedDict('AllowlistItem', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeCreate = typing.TypedDict('PrivilegeCreate', {
            'id':'int',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem_ = typing.TypedDict('AllowlistItem_', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeCreateReturns = typing.TypedDict('PrivilegeCreateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem_]',
            'roles':'list[str]',
            'web_shell':'bool',
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
    AllowlistItem__ = typing.TypedDict('AllowlistItem__', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry = typing.TypedDict('PrivilegeEntry', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem__]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem___ = typing.TypedDict('AllowlistItem___', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry_ = typing.TypedDict('PrivilegeEntry_', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem___]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem____ = typing.TypedDict('AllowlistItem____', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry__ = typing.TypedDict('PrivilegeEntry__', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem____]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem_____ = typing.TypedDict('AllowlistItem_____', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeUpdate = typing.TypedDict('PrivilegeUpdate', {
            'id':'int',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem_____]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem______ = typing.TypedDict('AllowlistItem______', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeUpdateReturns = typing.TypedDict('PrivilegeUpdateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem______]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[list[PrivilegeEntry], ForwardRef(PrivilegeEntry_), int, ForwardRef(PrivilegeEntry__)]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[PrivilegeEntry], ForwardRef(PrivilegeEntry_), int, ForwardRef(PrivilegeEntry__)]:
            
        """
        ...
    AllowlistItem = typing.TypedDict('AllowlistItem', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeCreate = typing.TypedDict('PrivilegeCreate', {
            'id':'int',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem_ = typing.TypedDict('AllowlistItem_', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeCreateReturns = typing.TypedDict('PrivilegeCreateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem_]',
            'roles':'list[str]',
            'web_shell':'bool',
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
    AllowlistItem__ = typing.TypedDict('AllowlistItem__', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry = typing.TypedDict('PrivilegeEntry', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem__]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem___ = typing.TypedDict('AllowlistItem___', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry_ = typing.TypedDict('PrivilegeEntry_', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem___]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem____ = typing.TypedDict('AllowlistItem____', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry__ = typing.TypedDict('PrivilegeEntry__', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem____]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem_____ = typing.TypedDict('AllowlistItem_____', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeUpdate = typing.TypedDict('PrivilegeUpdate', {
            'id':'int',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem_____]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem______ = typing.TypedDict('AllowlistItem______', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeUpdateReturns = typing.TypedDict('PrivilegeUpdateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem______]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    @typing.overload
    def update(self, 
        id:'int',
        privilege_update:'PrivilegeUpdate'={},
    /) -> 'PrivilegeUpdateReturns': 
        """
        Update the privilege `id`.

        Parameters
        ----------
        id:
            Update the privilege `id`.
            Creates a privilege.
        privilege_update:
            privilege_update
        Returns
        -------
        PrivilegeUpdateReturns:
            privilege_update_returns
        """
        ...
    AllowlistItem = typing.TypedDict('AllowlistItem', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeCreate = typing.TypedDict('PrivilegeCreate', {
            'id':'int',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem_ = typing.TypedDict('AllowlistItem_', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeCreateReturns = typing.TypedDict('PrivilegeCreateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem_]',
            'roles':'list[str]',
            'web_shell':'bool',
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
    AllowlistItem__ = typing.TypedDict('AllowlistItem__', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry = typing.TypedDict('PrivilegeEntry', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem__]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem___ = typing.TypedDict('AllowlistItem___', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry_ = typing.TypedDict('PrivilegeEntry_', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem___]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem____ = typing.TypedDict('AllowlistItem____', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeEntry__ = typing.TypedDict('PrivilegeEntry__', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem____]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem_____ = typing.TypedDict('AllowlistItem_____', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeUpdate = typing.TypedDict('PrivilegeUpdate', {
            'id':'int',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem_____]',
            'roles':'list[str]',
            'web_shell':'bool',
    })
    AllowlistItem______ = typing.TypedDict('AllowlistItem______', {
            'method':'str',
            'resource':'str',
    })
    PrivilegeUpdateReturns = typing.TypedDict('PrivilegeUpdateReturns', {
            'id':'int',
            'builtin_name':'typing.Optional[str]',
            'name':'str',
            'local_groups':'list[int]',
            'ds_groups':'list[typing.Union[int, str]]',
            'allowlist':'list[AllowlistItem______]',
            'roles':'list[str]',
            'web_shell':'bool',
    })

