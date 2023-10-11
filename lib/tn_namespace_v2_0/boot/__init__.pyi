
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Boot(
    Namespace
    ):
    _namespace:typing.Literal['boot']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def attach(self, 
        dev:'str',
        options:'Options',
    /) -> None: 
        """
        Attach a disk to the boot pool, turning a stripe into a mirror.
        
        `expand` option will determine whether the new disk partition will be
                 the maximum available or the same size as the current disk.

        Parameters
        ----------
        dev:
            dev
        options:
            options
        Returns
        -------
        """
        ...
    @typing.overload
    def detach(self, 
        dev:'str',
    /) -> None: 
        """
        Detach given `dev` from boot pool.

        Parameters
        ----------
        dev:
            dev
        Returns
        -------
        """
        ...
    @typing.overload
    def get_disks(self, 
    /) -> 'list[str]': 
        """
        Returns disks of the boot pool.

        Parameters
        ----------
        Returns
        -------
        list[str]:
            disks
        """
        ...
    @typing.overload
    def get_scrub_interval(self, 
    /) -> 'int': 
        """
        Get Automatic Scrub Interval value in days.

        Parameters
        ----------
        Returns
        -------
        int:
            interval
        """
        ...
    @typing.overload
    def get_state(self, 
    /) -> 'GetState': 
        """
        Returns the current state of the boot pool, including all vdevs, properties and datasets.

        Parameters
        ----------
        Returns
        -------
        GetState:
            get_state
        """
        ...
    @typing.overload
    def replace(self, 
        label:'str',
        dev:'str',
    /) -> None: 
        """
        Replace device `label` on boot pool with `dev`.

        Parameters
        ----------
        label:
            label
        dev:
            dev
        Returns
        -------
        """
        ...
    @typing.overload
    def scrub(self, 
    /) -> None: 
        """
        Scrub on boot pool.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def set_scrub_interval(self, 
        interval:'int',
    /) -> 'int': 
        """
        Set Automatic Scrub Interval value in days.

        Parameters
        ----------
        interval:
            interval
        Returns
        -------
        int:
            interval
        """
        ...
    GetState = typing.TypedDict('GetState', {
            'name':'str',
            'status':'str',
            'path':'str',
            'scan':'dict[str]',
            'is_upgraded':'bool',
            'healthy':'bool',
            'warning':'bool',
            'status_code':'typing.Optional[str]',
            'status_detail':'typing.Optional[str]',
            'size':'typing.Optional[int]',
            'allocated':'typing.Optional[int]',
            'free':'typing.Optional[int]',
            'freeing':'typing.Optional[int]',
            'fragmentation':'typing.Optional[str]',
            'size_str':'typing.Optional[str]',
            'allocated_str':'typing.Optional[str]',
            'free_str':'typing.Optional[str]',
            'freeing_str':'typing.Optional[str]',
            'autotrim':'dict[str]',
            'topology':'Topology',
    })
    Options = typing.TypedDict('Options', {
            'expand':'bool',
    })
    Topology = typing.TypedDict('Topology', {
            'data':'list',
            'log':'list',
            'cache':'list',
            'spare':'list',
            'special':'list',
            'dedup':'list',
    })
