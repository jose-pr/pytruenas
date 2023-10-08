
from pytruenas import Namespace, TrueNASClient
import typing
class Systemdataset(Namespace):
    _namespace:typing.Literal['systemdataset']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def config(self, 
    /) -> 'SystemdatasetEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        SystemdatasetEntry:
            systemdataset_entry
        """
        ...
    @typing.overload
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
    @typing.overload
    def update(self, 
        sysdataset_update:'SysdatasetUpdate'={},
    /) -> 'SystemdatasetUpdateReturns': 
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
        SystemdatasetUpdateReturns:
            systemdataset_update_returns
        """
        ...

class SystemdatasetEntry(typing.TypedDict):
        id:'int'
        pool:'str'
        pool_set:'bool'
        uuid:'str'
        uuid_b:'typing.Optional[str]'
        basename:'str'
        uuid_a:'str'
        syslog:'bool'
        path:'typing.Optional[str]'
        ...
class SysdatasetUpdate(typing.TypedDict):
        pool:'typing.Optional[str]'
        pool_exclude:'typing.Optional[str]'
        syslog:'bool'
        ...
class SystemdatasetUpdateReturns(typing.TypedDict):
        id:'int'
        pool:'str'
        pool_set:'bool'
        uuid:'str'
        uuid_b:'typing.Optional[str]'
        basename:'str'
        uuid_a:'str'
        syslog:'bool'
        path:'typing.Optional[str]'
        ...
