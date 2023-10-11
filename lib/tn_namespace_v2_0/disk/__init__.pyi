
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Disk(
    Namespace
    ):
    _namespace:typing.Literal['disk']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def get_instance(self, 
        _id:'typing.Union[str, int, bool, dict[str], list]',
        _query_options_get_instance:'QueryOptionsGetInstance',
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
    @typing.overload
    def get_unused(self, 
        _join_partitions:'bool',
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
    @typing.overload
    def query(self, 
        _query_filters:'list[list]',
        _query_options:'QueryOptions',
    /) -> 'typing.Union[list[DiskEntry], DiskEntry, int]': 
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
        typing.Union[list[DiskEntry], DiskEntry, int]:
            
        """
        ...
    @typing.overload
    def resize(self, 
        _disks:'list[ResizeProperties]',
        _sync:'bool',
        _raise_error:'bool',
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
    @typing.overload
    def retaste(self, 
        _disks:'list[str]',
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
    @typing.overload
    def smart_attributes(self, 
        _name:'str',
    /) -> 'list[SmartAttribute]': 
        """
        Returns S.M.A.R.T. attributes values for specified disk name.

        Parameters
        ----------
        name:
            name
        Returns
        -------
        list[SmartAttribute]:
            smart_attributes
        """
        ...
    @typing.overload
    def temperature(self, 
        _name:'str',
        _options:'Options',
    /) -> 'typing.Optional[int]': 
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
        typing.Optional[int]:
            temperature
        """
        ...
    @typing.overload
    def temperature_agg(self, 
        _names:'list[str]',
        _days:'int',
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
    @typing.overload
    def temperature_alerts(self, 
        _names:'list[str]',
    /) -> 'Alert': 
        """
        Returns existing temperature alerts for specified disk `names.`

        Parameters
        ----------
        names:
            names
        Returns
        -------
        Alert:
            alert
        """
        ...
    @typing.overload
    def temperatures(self, 
        _names:'list[str]',
        _options:'Options_',
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
    @typing.overload
    def update(self, 
        _id:'str',
        _disk_update:'DiskUpdate',
    /) -> 'DiskUpdateReturns': 
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
        DiskUpdateReturns:
            disk_update_returns
        """
        ...
    @typing.overload
    def wipe(self, 
        _dev:'str',
        _mode:'Mode',
        _synccache:'bool',
        _swap_removal_options:'SwapRemovalOptions',
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
    class Advpowermgmt(str,Enum):
        DISABLED = 'DISABLED'
        _1 = '1'
        _64 = '64'
        _127 = '127'
        _128 = '128'
        _192 = '192'
        _254 = '254'
        ...
    Alert = typing.TypedDict('Alert', {
            'uuid':'str',
            'source':'str',
            'klass':'str',
            'args':'typing.Union[str, int, bool, dict[str], list]',
            'node':'str',
            'key':'str',
            'datetime':'str',
            'last_occurrence':'str',
            'dismissed':'bool',
            'mail':'typing.Union[str, int, bool, dict[str], list]',
            'text':'str',
            'id':'str',
            'level':'str',
            'formatted':'typing.Optional[str]',
            'one_shot':'bool',
    })
    DiskEntry = typing.TypedDict('DiskEntry', {
            'identifier':'str',
            'name':'str',
            'subsystem':'str',
            'number':'int',
            'serial':'str',
            'lunid':'typing.Optional[str]',
            'size':'int',
            'description':'str',
            'transfermode':'str',
            'hddstandby':'Hddstandby',
            'togglesmart':'bool',
            'advpowermgmt':'Advpowermgmt',
            'smartoptions':'str',
            'expiretime':'typing.Optional[str]',
            'critical':'typing.Optional[int]',
            'difference':'typing.Optional[int]',
            'informational':'typing.Optional[int]',
            'model':'typing.Optional[str]',
            'rotationrate':'typing.Optional[int]',
            'type':'typing.Optional[str]',
            'zfs_guid':'typing.Optional[str]',
            'bus':'str',
            'devname':'str',
            'enclosure':'Enclosure',
            'pool':'typing.Optional[str]',
            'passwd':'str',
            'kmip_uid':'typing.Optional[str]',
            'supports_smart':'typing.Optional[bool]',
    })
    DiskUpdate = typing.TypedDict('DiskUpdate', {
            'number':'int',
            'lunid':'typing.Optional[str]',
            'description':'str',
            'hddstandby':'Hddstandby',
            'togglesmart':'bool',
            'advpowermgmt':'Advpowermgmt',
            'smartoptions':'str',
            'critical':'typing.Optional[int]',
            'difference':'typing.Optional[int]',
            'informational':'typing.Optional[int]',
            'bus':'str',
            'enclosure':'Enclosure',
            'pool':'typing.Optional[str]',
            'passwd':'str',
            'supports_smart':'typing.Optional[bool]',
    })
    DiskUpdateReturns = typing.TypedDict('DiskUpdateReturns', {
            'identifier':'str',
            'name':'str',
            'subsystem':'str',
            'number':'int',
            'serial':'str',
            'lunid':'typing.Optional[str]',
            'size':'int',
            'description':'str',
            'transfermode':'str',
            'hddstandby':'Hddstandby',
            'togglesmart':'bool',
            'advpowermgmt':'Advpowermgmt',
            'smartoptions':'str',
            'expiretime':'typing.Optional[str]',
            'critical':'typing.Optional[int]',
            'difference':'typing.Optional[int]',
            'informational':'typing.Optional[int]',
            'model':'typing.Optional[str]',
            'rotationrate':'typing.Optional[int]',
            'type':'typing.Optional[str]',
            'zfs_guid':'typing.Optional[str]',
            'bus':'str',
            'devname':'str',
            'enclosure':'Enclosure',
            'pool':'typing.Optional[str]',
            'passwd':'str',
            'kmip_uid':'typing.Optional[str]',
            'supports_smart':'typing.Optional[bool]',
    })
    Enclosure = typing.TypedDict('Enclosure', {
            'number':'int',
            'slot':'int',
    })
    Flags = typing.TypedDict('Flags', {
            'value':'int',
            'string':'str',
            'prefailure':'bool',
            'updated_online':'bool',
            'performance':'bool',
            'error_rate':'bool',
            'event_count':'bool',
            'auto_keep':'bool',
    })
    class Hddstandby(str,Enum):
        ALWAYSON = 'ALWAYS ON'
        _5 = '5'
        _10 = '10'
        _20 = '20'
        _30 = '30'
        _60 = '60'
        _120 = '120'
        _180 = '180'
        _240 = '240'
        _300 = '300'
        _330 = '330'
        ...
    class Mode(str,Enum):
        QUICK = 'QUICK'
        FULL = 'FULL'
        FULLRANDOM = 'FULL_RANDOM'
        ...
    Options = typing.TypedDict('Options', {
            'cache':'typing.Optional[int]',
            'powermode':'Powermode',
    })
    Options_ = typing.TypedDict('Options_', {
            'cache':'typing.Optional[int]',
            'only_cached':'bool',
            'powermode':'Powermode',
    })
    class Powermode(str,Enum):
        NEVER = 'NEVER'
        SLEEP = 'SLEEP'
        STANDBY = 'STANDBY'
        IDLE = 'IDLE'
        ...
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    Raw = typing.TypedDict('Raw', {
            'value':'int',
            'string':'str',
    })
    ResizeProperties = typing.TypedDict('ResizeProperties', {
            'name':'str',
            'size':'int',
    })
    SmartAttribute = typing.TypedDict('SmartAttribute', {
            'id':'int',
            'value':'int',
            'worst':'int',
            'thresh':'int',
            'name':'str',
            'when_failed':'str',
            'flags':'Flags',
            'raw':'Raw',
    })
    SwapRemovalOptions = typing.TypedDict('SwapRemovalOptions', {
            'configure_swap':'bool',
    })
