
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Systemdataset(Namespace):
    _namespace:_ty.Literal['systemdataset']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def config(self, 
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            systemdataset_entry
        """
        ...
    @_ty.overload
    def pool_choices(self, 
        include_current_pool:'bool'=True,
    /) -> 'dict[str]': 
        """
        Retrieve pool choices which can be used for configuring system dataset.

        Parameters
        ----------
        include_current_pool:
            include_current_pool
        Returns
        -------
        dict[str]:
            systemdataset_pool_choices
        """
        ...
    @_ty.overload
    def update(self, 
        sysdataset_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update System Dataset Service Configuration.
        
        `pool` is the name of a valid pool configured in the system which will be used to host the system dataset.
        
        `pool_exclude` can be specified to make sure that we don't place the system dataset on that pool if `pool`
        is not provided.

        Parameters
        ----------
        sysdataset_update:
            sysdataset_update
        Returns
        -------
        dict[str]:
            systemdataset_update_returns
        """
        ...
