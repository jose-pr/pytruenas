
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin
from enum import Enum
import typing
class Bootenv(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['bootenv']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def activate(self, 
        _id:'str',
    /) -> 'bool': 
        """
        Activates boot environment `id`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        bool:
            successfully_activated
        """
        ...
    @typing.overload
    def create(self, 
        _bootenv_create:'BootenvCreate',
    /) -> 'str': 
        """
        Create a new boot environment using `name`.
        
        If a new boot environment is desired which is a clone of another boot environment, `source` can be passed.
        Then, a new boot environment of `name` is created using boot environment `source` by cloning it.
        
        Ensure that `name` and `source` are valid boot environment names.

        Parameters
        ----------
        bootenv_create:
            bootenv_create
        Returns
        -------
        str:
            bootenv_name
        """
        ...
    @typing.overload
    def delete(self, 
        _id:'str',
    /) -> 'bool': 
        """
        Delete `id` boot environment. This removes the clone from the system.

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
    /) -> 'typing.Union[list[BootenvEntry], BootenvEntry, int]': 
        """
        Query all Boot Environments with `query-filters` and `query-options`.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[BootenvEntry], BootenvEntry, int]:
            
        """
        ...
    @typing.overload
    def set_attribute(self, 
        _id:'str',
        _attributes:'Attributes',
    /) -> 'bool': 
        """
        Sets attributes boot environment `id`.
        
        Currently only `keep` attribute is allowed.

        Parameters
        ----------
        id:
            Sets attributes boot environment `id`.
        attributes:
            attributes
        Returns
        -------
        bool:
            successfully_set_attribute
        """
        ...
    @typing.overload
    def update(self, 
        _id:'str',
        _bootenv_update:'BootenvUpdate',
    /) -> 'str': 
        """
        Update `id` boot environment name with a new provided valid `name`.

        Parameters
        ----------
        id:
            Update `id` boot environment name with a new provided valid `name`.
            Create a new boot environment using `name`.
        bootenv_update:
            bootenv_update
        Returns
        -------
        str:
            bootenv_name
        """
        ...
    Attributes = typing.TypedDict('Attributes', {
            'keep':'bool',
    })
    BootenvCreate = typing.TypedDict('BootenvCreate', {
            'name':'str',
            'source':'str',
    })
    BootenvEntry = typing.TypedDict('BootenvEntry', {
            'id':'str',
            'realname':'str',
            'name':'str',
            'active':'str',
            'activated':'bool',
            'can_activate':'bool',
            'mountpoint':'str',
            'space':'str',
            'created':'str',
            'keep':'bool',
            'rawspace':'int',
    })
    BootenvUpdate = typing.TypedDict('BootenvUpdate', {
            'name':'str',
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
