
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Directoryservices(Namespace):
    _namespace:_ty.Literal['directoryservices']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
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
    @_ty.overload
    def get_state(self, 
    /) -> 'dict[str]': 
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
        dict[str]:
            directory_services_states
        """
        ...
