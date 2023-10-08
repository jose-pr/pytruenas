
from pytruenas import Namespace, TrueNASClient
import typing
class Staticroute(Namespace):
    _namespace:typing.Literal['staticroute']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        staticroute_create:'StaticrouteCreate'={},
    /) -> 'StaticrouteCreateReturns': 
        """
        Create a Static Route.
        
        Address families of `gateway` and `destination` should match when creating a static route.
        
        `description` is an optional attribute for any notes regarding the static route.

        Parameters
        ----------
        staticroute_create:
            staticroute_create
        Returns
        -------
        StaticrouteCreateReturns:
            staticroute_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete Static Route of `id`.

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
    /) -> 'list[StaticrouteEntry]|StaticrouteEntry|int|StaticrouteEntry': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[StaticrouteEntry]:
            
        StaticrouteEntry:
            
        int:
            
        StaticrouteEntry:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        staticroute_update:'StaticrouteUpdate'={},
    /) -> 'StaticrouteUpdateReturns': 
        """
        Update Static Route of `id`.

        Parameters
        ----------
        id:
            Update Static Route of `id`.
            Create a Static Route.
        staticroute_update:
            staticroute_update
        Returns
        -------
        StaticrouteUpdateReturns:
            staticroute_update_returns
        """
        ...

class StaticrouteCreate(typing.TypedDict):
        destination:'str'
        gateway:'str'
        description:'str'
        ...
class StaticrouteCreateReturns(typing.TypedDict):
        destination:'str'
        gateway:'str'
        description:'str'
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
class StaticrouteEntry(typing.TypedDict):
        destination:'str'
        gateway:'str'
        description:'str'
        id:'int'
        ...
class StaticrouteUpdate(typing.TypedDict):
        destination:'str'
        gateway:'str'
        description:'str'
        ...
class StaticrouteUpdateReturns(typing.TypedDict):
        destination:'str'
        gateway:'str'
        description:'str'
        id:'int'
        ...
