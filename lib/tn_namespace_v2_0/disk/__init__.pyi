
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Disk(Namespace):
    _namespace:_ty.Literal['disk']
    def __init__(self, client:TrueNASClient) -> None: ...
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
    def get_unused(self, 
        join_partitions:'bool'=False,
    /) -> None: 
        """
        Return disks that are not in use by any zpool that is currently imported. It will
        also return disks that are in use by any zpool that is exported.
        
        `join_partitions`: Bool, when True will return all partitions currently written to disk
            NOTE: this is an expensive operation

        Parameters
        ----------
        join_partitions:
            join_partitions
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
        Query disks.
        
        The following extra options are supported:
        
             include_expired: true - will also include expired disks (default: false)
             passwords: true - will not hide KMIP password for the disks (default: false)
             supports_smart: true - will query if disks support S.M.A.R.T. Only supported if resulting disks count is
                                    not larger than one; otherwise, raises an error.
             pools: true - will join pool name for each disk (default: false)

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
    def resize(self, 
        disks:'list',
        sync:'bool'=True,
        raise_error:'bool'=False,
    /) -> None: 
        """
        Takes a list of disks. Each list entry is a dict that requires a key, value pair.
        `name`: string (the name of the disk (i.e. sda))
        `size`: integer (given in gigabytes)
        `sync`: boolean, when true (default) will synchronize the new size of the disk(s)
            with the database cache.
        `raise_error`: boolean
            when true, will raise a `CallError` if any failures occur
            when false, will will log the errors if any failures occur
        
        NOTE:
            if `size` is given, the disk with `name` will be resized
                to `size` (overprovision).
            if `size` is not given, the disk with `name` will be resized
                to it's original size (unoverprovision).

        Parameters
        ----------
        disks:
            disks
        sync:
            `sync`: boolean, when true (default) will synchronize the new size of the disk(s)
                with the database cache.
        raise_error:
            `raise_error`: boolean
                when true, will raise a `CallError` if any failures occur
                when false, will will log the errors if any failures occur
        Returns
        -------
        """
        ...
    @_ty.overload
    def retaste(self, 
        disks:'list'=None,
    /) -> None: 
        """
        

        Parameters
        ----------
        disks:
            disks
        Returns
        -------
        """
        ...
    @_ty.overload
    def smart_attributes(self, 
        name:'str',
    /) -> 'list': 
        """
        Returns S.M.A.R.T. attributes values for specified disk name.

        Parameters
        ----------
        name:
            name
        Returns
        -------
        list:
            smart_attributes
        """
        ...
    @_ty.overload
    def temperature(self, 
        name:'str',
        options:'dict[str]'={},
    /) -> 'int|None': 
        """
        Returns temperature for device `name` using specified S.M.A.R.T. `powermode`. If `cache` is not null
        then the last cached within `cache` seconds value is used.

        Parameters
        ----------
        name:
            name
        options:
            options
        Returns
        -------
        int:
            temperature
        None:
            temperature
        """
        ...
    @_ty.overload
    def temperature_agg(self, 
        names:'list'=[],
        days:'int'=7,
    /) -> 'dict[str]': 
        """
        Returns min/max/avg temperature for `names` disks for the last `days` days

        Parameters
        ----------
        names:
            names
        days:
            days
        Returns
        -------
        dict[str]:
            temperatures
        """
        ...
    @_ty.overload
    def temperature_alerts(self, 
        names:'list'=[],
    /) -> 'dict[str]': 
        """
        Returns existing temperature alerts for specified disk `names.`

        Parameters
        ----------
        names:
            names
        Returns
        -------
        dict[str]:
            alert
        """
        ...
    @_ty.overload
    def temperatures(self, 
        names:'list'=[],
        options:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Returns temperatures for a list of devices (runs in parallel).
        See `disk.temperature` documentation for more details.
        If `only_cached` is specified then this method only returns disk temperatures that exist in cache.

        Parameters
        ----------
        names:
            names
        options:
            options
        Returns
        -------
        dict[str]:
            disks_temperatures
        """
        ...
    @_ty.overload
    def update(self, 
        id:'str',
        disk_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update disk of `id`.
        
        If extra options need to be passed to SMART which we don't already support, they can be passed by
        `smartoptions`.
        
        `critical`, `informational` and `difference` are integer values on which alerts for SMART are configured
        if the disk temperature crosses the assigned threshold for each respective attribute.
        If they are set to null, then SMARTD config values are used as defaults.
        
        Email of log level LOG_CRIT is issued when disk temperature crosses `critical`.
        
        Email of log level LOG_INFO is issued when disk temperature crosses `informational`.
        
        If temperature of a disk changes by `difference` degree Celsius since the last report, SMART reports this.

        Parameters
        ----------
        id:
            Update disk of `id`.
        disk_update:
            disk_update
        Returns
        -------
        dict[str]:
            disk_update_returns
        """
        ...
    @_ty.overload
    def wipe(self, 
        dev:'str',
        mode:'str',
        synccache:'bool'=True,
        swap_removal_options:'dict[str]'={},
    /) -> None: 
        """
        Performs a wipe of a disk `dev`.
        It can be of the following modes:
          - QUICK: clean the first and last 32 megabytes on `dev`
          - FULL: write whole disk with zero's
          - FULL_RANDOM: write whole disk with random bytes

        Parameters
        ----------
        dev:
            dev
        mode:
            mode
        synccache:
            synccache
        swap_removal_options:
            swap_removal_options
        Returns
        -------
        """
        ...
