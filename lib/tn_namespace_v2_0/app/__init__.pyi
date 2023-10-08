
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class App(Namespace):
    _namespace:_ty.Literal['app']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def available(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'int|dict[str]|list': 
        """
        Retrieve all available applications from all configured catalogs.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        int:
            
        dict[str]:
            
        list:
            
        """
        ...
    @_ty.overload
    def categories(self, 
    /) -> 'list': 
        """
        Retrieve list of valid categories which have associated applications.

        Parameters
        ----------
        Returns
        -------
        list:
            categories
        """
        ...
    @_ty.overload
    def latest(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'int|dict[str]|list': 
        """
        Retrieve latest updated apps.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        int:
            
        dict[str]:
            
        list:
            
        """
        ...
    @_ty.overload
    def similar(self, 
        app_name:'str',
        catalog:'str',
        train:'str',
    /) -> 'list': 
        """
        Retrieve applications which are similar to `app_name`.

        Parameters
        ----------
        app_name:
            app_name
        catalog:
            catalog
        train:
            train
        Returns
        -------
        list:
            similar
        """
        ...
