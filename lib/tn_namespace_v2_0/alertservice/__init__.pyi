
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Alertservice(Namespace):
    _namespace:_ty.Literal['alertservice']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def create(self, 
        alert_service_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create an Alert Service of specified `type`.
        
        If `enabled`, it sends alerts to the configured `type` of Alert Service.

        Parameters
        ----------
        alert_service_create:
            alert_service_create
        Returns
        -------
        dict[str]:
            alertservice_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete Alert Service of `id`.

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
    def list_types(self, 
    /) -> 'list': 
        """
        List all types of supported Alert services which can be configured with the system.

        Parameters
        ----------
        Returns
        -------
        list:
            alert_service_types
        """
        ...
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        

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
    def test(self, 
        alert_service_create:'dict[str]'={},
    /) -> 'bool': 
        """
        Send a test alert using `type` of Alert Service.

        Parameters
        ----------
        alert_service_create:
            alert_service_create
        Returns
        -------
        bool:
            Is `true` if test is successful
        """
        ...
    @_ty.overload
    def update(self, 
        id:'int',
        alert_service_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update Alert Service of `id`.

        Parameters
        ----------
        id:
            Update Alert Service of `id`.
        alert_service_update:
            alert_service_update
        Returns
        -------
        dict[str]:
            alertservice_update_returns
        """
        ...
