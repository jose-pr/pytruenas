
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Boot(Namespace):
    _namespace:_ty.Literal['boot']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def attach(self, 
        dev:'str',
        options:'dict[str]'={},
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
    @_ty.overload
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
    @_ty.overload
    def get_disks(self, 
    /) -> 'list': 
        """
        Returns disks of the boot pool.

        Parameters
        ----------
        Returns
        -------
        list:
            disks
        """
        ...
    @_ty.overload
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
    @_ty.overload
    def get_state(self, 
    /) -> 'dict[str]': 
        """
        Returns the current state of the boot pool, including all vdevs, properties and datasets.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            get_state
        """
        ...
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
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
