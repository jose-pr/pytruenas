
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Bootenv(Namespace):
    _namespace:_ty.Literal['bootenv']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
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
    @_ty.overload
    def create(self, 
        bootenv_create:'dict[str]'={},
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
    @_ty.overload
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
        Query all Boot Environments with `query-filters` and `query-options`.

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
    def set_attribute(self, 
        id:'str',
        attributes:'dict[str]'={},
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
    @_ty.overload
    def update(self, 
        id:'str',
        bootenv_update:'dict[str]'={},
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
