
from pytruenas.base import Namespace

import typing
from enum import Enum

class Disk(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'disk')

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
    class Advpowermgmt(str,Enum):
        DISABLED = 'DISABLED'
        _1 = '1'
        _64 = '64'
        _127 = '127'
        _128 = '128'
        _192 = '192'
        _254 = '254'
        ...
    Enclosure = typing.TypedDict('Enclosure', {
            'number':'int',
            'slot':'int',
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
    Raw = typing.TypedDict('Raw', {
            'value':'int',
            'string':'str',
    })
    Options = typing.TypedDict('Options', {
            'cache':'typing.Optional[int]',
            'powermode':'Powermode',
    })
    class Powermode(str,Enum):
        NEVER = 'NEVER'
        SLEEP = 'SLEEP'
        STANDBY = 'STANDBY'
        IDLE = 'IDLE'
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
    Options_ = typing.TypedDict('Options_', {
            'cache':'typing.Optional[int]',
            'only_cached':'bool',
            'powermode':'Powermode',
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
    class Mode(str,Enum):
        QUICK = 'QUICK'
        FULL = 'FULL'
        FULLRANDOM = 'FULL_RANDOM'
        ...
    SwapRemovalOptions = typing.TypedDict('SwapRemovalOptions', {
            'configure_swap':'bool',
    })
