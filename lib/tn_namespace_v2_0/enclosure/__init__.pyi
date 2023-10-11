
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Enclosure(
    Namespace
    ):
    _namespace:typing.Literal['enclosure']
    def __init__(self, client:TrueNASClient) -> None: ...
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
    def set_slot_status(self, 
        _enclosure_id:'str',
        _slot:'int',
        _status:'Status',
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
        _id:'str',
        _enclosure_update:'EnclosureUpdate',
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
    EnclosureUpdate = typing.TypedDict('EnclosureUpdate', {
            'label':'str',
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
    class Status(str,Enum):
        CLEAR = 'CLEAR'
        FAULT = 'FAULT'
        IDENTIFY = 'IDENTIFY'
        ...
