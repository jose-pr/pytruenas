
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Directoryservices(
    Namespace
    ):
    _namespace:typing.Literal['directoryservices']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def cache_refresh(self, 
    /) -> None: 
        """
        This method refreshes the directory services cache for users and groups that is
        used as a backing for `user.query` and `group.query` methods. The first cache fill in
        an Active Directory domain may take a significant amount of time to complete and
        so it is performed as within a job. The most likely situation in which a user may
        desire to refresh the directory services cache is after new users or groups  to a remote
        directory server with the intention to have said users or groups appear in the
        results of the aforementioned account-related methods.
        
        A cache refresh is not required in order to use newly-added users and groups for in
        permissions and ACL related methods. Likewise, a cache refresh will not resolve issues
        with users being unable to authenticate to shares.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def get_state(self, 
    /) -> 'DirectoryServicesStates': 
        """
        `DISABLED` Directory Service is disabled.
        
        `FAULTED` Directory Service is enabled, but not HEALTHY. Review logs and generated alert
        messages to debug the issue causing the service to be in a FAULTED state.
        
        `LEAVING` Directory Service is in process of stopping.
        
        `JOINING` Directory Service is in process of starting.
        
        `HEALTHY` Directory Service is enabled, and last status check has passed.

        Parameters
        ----------
        Returns
        -------
        DirectoryServicesStates:
            directory_services_states
        """
        ...
    DirectoryServicesStates = typing.TypedDict('DirectoryServicesStates', {
            'activedirectory':'Activedirectory',
            'ldap':'Ldap',
    })
    class Activedirectory(str,Enum):
        DISABLED = 'DISABLED'
        FAULTED = 'FAULTED'
        LEAVING = 'LEAVING'
        JOINING = 'JOINING'
        HEALTHY = 'HEALTHY'
        ...
    class Ldap(str,Enum):
        DISABLED = 'DISABLED'
        FAULTED = 'FAULTED'
        LEAVING = 'LEAVING'
        JOINING = 'JOINING'
        HEALTHY = 'HEALTHY'
        ...
