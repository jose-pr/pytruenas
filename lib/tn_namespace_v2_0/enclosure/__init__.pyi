
from pytruenas import Namespace, TrueNASClient
import typing
class Enclosure(Namespace):
    _namespace:typing.Literal['enclosure']
    def __init__(self, client:TrueNASClient) -> None: ...
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
    def set_slot_status(self, 
        enclosure_id:'str',
        slot:'int',
        status:'str',
    /) -> None: 
        """
        

        Parameters
        ----------
        enclosure_id:
            enclosure_id
        slot:
            slot
        status:
            status
        Returns
        -------
        """
        ...
    @typing.overload
    def update(self, 
        id:'str',
        enclosure_update:'EnclosureUpdate'={},
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        id:
            id
        enclosure_update:
            enclosure_update
        Returns
        -------
        dict[str]:
            enclosure_update_returns
        """
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
class EnclosureUpdate(typing.TypedDict):
        label:'str'
        ...
