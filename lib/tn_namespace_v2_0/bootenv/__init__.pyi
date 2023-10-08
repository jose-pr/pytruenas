
from pytruenas import Namespace, TrueNASClient
import typing
class Bootenv(Namespace):
    _namespace:typing.Literal['bootenv']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def activate(self, 
        id:'str',
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
        bootenv_create:'BootenvCreate'={},
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
        id:'str',
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
    /) -> 'list[BootenvEntry]|BootenvEntry|int|BootenvEntry': 
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
        list[BootenvEntry]:
            
        BootenvEntry:
            
        int:
            
        BootenvEntry:
            
        """
        ...
    @typing.overload
    def set_attribute(self, 
        id:'str',
        attributes:'Attributes'={},
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
        id:'str',
        bootenv_update:'BootenvUpdate'={},
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

class BootenvCreate(typing.TypedDict):
        name:'str'
        source:'str'
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
class BootenvEntry(typing.TypedDict):
        id:'str'
        realname:'str'
        name:'str'
        active:'str'
        activated:'bool'
        can_activate:'bool'
        mountpoint:'str'
        space:'str'
        created:'str'
        keep:'bool'
        rawspace:'int'
        ...
class Attributes(typing.TypedDict):
        keep:'bool'
        ...
class BootenvUpdate(typing.TypedDict):
        name:'str'
        ...
