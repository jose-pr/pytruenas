
from pytruenas import Namespace
import typing
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
    Enclosure = typing.TypedDict('Enclosure', {
            'number':'int',
            'slot':'int',
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
            'hddstandby':'str',
            'togglesmart':'bool',
            'advpowermgmt':'str',
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
    DiskEntry_ = typing.TypedDict('DiskEntry_', {
            'identifier':'str',
            'name':'str',
            'subsystem':'str',
            'number':'int',
            'serial':'str',
            'lunid':'typing.Optional[str]',
            'size':'int',
            'description':'str',
            'transfermode':'str',
            'hddstandby':'str',
            'togglesmart':'bool',
            'advpowermgmt':'str',
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
    DiskEntry__ = typing.TypedDict('DiskEntry__', {
            'identifier':'str',
            'name':'str',
            'subsystem':'str',
            'number':'int',
            'serial':'str',
            'lunid':'typing.Optional[str]',
            'size':'int',
            'description':'str',
            'transfermode':'str',
            'hddstandby':'str',
            'togglesmart':'bool',
            'advpowermgmt':'str',
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
    Object = typing.TypedDict('Object', {
            'name':'str',
            'size':'int',
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
    Options = typing.TypedDict('Options', {
            'cache':'typing.Optional[int]',
            'powermode':'str',
    })
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
            'powermode':'str',
    })
    DiskUpdate = typing.TypedDict('DiskUpdate', {
            'number':'int',
            'lunid':'typing.Optional[str]',
            'description':'str',
            'hddstandby':'str',
            'togglesmart':'bool',
            'advpowermgmt':'str',
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
            'hddstandby':'str',
            'togglesmart':'bool',
            'advpowermgmt':'str',
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
    SwapRemovalOptions = typing.TypedDict('SwapRemovalOptions', {
            'configure_swap':'bool',
    })
