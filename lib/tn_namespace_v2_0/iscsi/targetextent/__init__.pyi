
from pytruenas import Namespace, TrueNASClient
import typing
class IscsiTargetextent(Namespace):
    _namespace:typing.Literal['iscsi.targetextent']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        iscsi_targetextent_create:'IscsiTargetextentCreate'={},
    /) -> 'dict[str]': 
        """
        Create an Associated Target.
        
        `lunid` will be automatically assigned if it is not provided based on the `target`.

        Parameters
        ----------
        iscsi_targetextent_create:
            iscsi_targetextent_create
        Returns
        -------
        dict[str]:
            iscsi_targetextent_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
        force:'bool'=False,
    /) -> 'bool': 
        """
        Delete Associated Target of `id`.

        Parameters
        ----------
        id:
            id
        force:
            force
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
        iscsi_targetextent_update:'IscsiTargetextentUpdate'={},
    /) -> 'dict[str]': 
        """
        Update Associated Target of `id`.

        Parameters
        ----------
        id:
            Update Associated Target of `id`.
            Create an Associated Target.
        iscsi_targetextent_update:
            iscsi_targetextent_update
        Returns
        -------
        dict[str]:
            iscsi_targetextent_update_returns
        """
        ...

class IscsiTargetextentCreate(typing.TypedDict):
        target:'int'
        lunid:'typing.Optional[int]'
        extent:'int'
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
class IscsiTargetextentUpdate(typing.TypedDict):
        target:'int'
        lunid:'int'
        extent:'int'
        ...
