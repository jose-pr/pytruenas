
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class Interface(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'interface')

    Options = typing.TypedDict('Options', {
            'bridge_members':'bool',
            'lag_ports':'bool',
            'vlan_parent':'bool',
            'exclude':'list',
            'exclude_types':'list[Type]',
            'include':'list',
    })
    class Type(str,Enum):
        BRIDGE = 'BRIDGE'
        LINKAGGREGATION = 'LINK_AGGREGATION'
        PHYSICAL = 'PHYSICAL'
        UNKNOWN = 'UNKNOWN'
        VLAN = 'VLAN'
        ...
    Options_ = typing.TypedDict('Options_', {
            'rollback':'bool',
            'checkin_timeout':'int',
    })
    InterfaceCreate = typing.TypedDict('InterfaceCreate', {
            'name':'str',
            'description':'str',
            'type':'Type_',
            'ipv4_dhcp':'bool',
            'ipv6_auto':'bool',
            'aliases':'list[InterfaceAlias]',
            'failover_critical':'bool',
            'failover_group':'typing.Optional[int]',
            'failover_vhid':'typing.Optional[int]',
            'failover_aliases':'list[InterfaceFailoverAlias]',
            'failover_virtual_aliases':'list[InterfaceVirtualAlias]',
            'bridge_members':'list',
            'stp':'bool',
            'lag_protocol':'LagProtocol',
            'xmit_hash_policy':'typing.Optional[str]',
            'lacpdu_rate':'typing.Optional[str]',
            'lag_ports':'list[str]',
            'vlan_parent_interface':'str',
            'vlan_tag':'int',
            'vlan_pcp':'typing.Optional[int]',
            'mtu':'typing.Optional[int]',
    })
    class Type_(str,Enum):
        BRIDGE = 'BRIDGE'
        LINKAGGREGATION = 'LINK_AGGREGATION'
        VLAN = 'VLAN'
        ...
    InterfaceAlias = typing.TypedDict('InterfaceAlias', {
            'type':'Type__',
            'address':'str',
            'netmask':'int',
    })
    class Type__(str,Enum):
        INET = 'INET'
        INET6 = 'INET6'
        ...
    InterfaceFailoverAlias = typing.TypedDict('InterfaceFailoverAlias', {
            'type':'Type__',
            'address':'str',
    })
    InterfaceVirtualAlias = typing.TypedDict('InterfaceVirtualAlias', {
            'type':'Type__',
            'address':'str',
    })
    class LagProtocol(str,Enum):
        LACP = 'LACP'
        FAILOVER = 'FAILOVER'
        LOADBALANCE = 'LOADBALANCE'
        ROUNDROBIN = 'ROUNDROBIN'
        NONE = 'NONE'
        ...
    InterfaceCreateReturns = typing.TypedDict('InterfaceCreateReturns', {
            'id':'str',
            'name':'str',
            'fake':'bool',
            'type':'str',
            'state':'State',
            'aliases':'list[Alias_]',
            'ipv4_dhcp':'bool',
            'ipv6_auto':'bool',
            'description':'str',
            'mtu':'typing.Optional[int]',
            'vlan_parent_interface':'typing.Optional[str]',
            'vlan_tag':'typing.Optional[int]',
            'vlan_pcp':'typing.Optional[int]',
            'lag_protocol':'str',
            'lag_ports':'list[str]',
            'bridge_members':'list[str]',
    })
    State = typing.TypedDict('State', {
            'name':'str',
            'orig_name':'str',
            'description':'str',
            'mtu':'int',
            'cloned':'bool',
            'flags':'list[str]',
            'nd6_flags':'list',
            'capabilities':'list',
            'link_state':'str',
            'media_type':'str',
            'media_subtype':'str',
            'active_media_type':'str',
            'active_media_subtype':'str',
            'supported_media':'list',
            'media_options':'typing.Optional[list]',
            'link_address':'str',
            'rx_queues':'int',
            'tx_queues':'int',
            'aliases':'list[Alias]',
            'vrrp_config':'typing.Optional[list]',
            'protocol':'typing.Optional[str]',
            'ports':'list[LagPorts]',
            'xmit_hash_policy':'typing.Optional[str]',
            'lacpdu_rate':'typing.Optional[str]',
            'parent':'typing.Optional[str]',
            'tag':'typing.Optional[int]',
            'pcp':'typing.Optional[int]',
    })
    Alias = typing.TypedDict('Alias', {
            'type':'str',
            'address':'str',
            'netmask':'str',
            'broadcast':'str',
    })
    LagPorts = typing.TypedDict('LagPorts', {
            'name':'str',
            'flags':'list[str]',
    })
    Alias_ = typing.TypedDict('Alias_', {
            'type':'str',
            'address':'str',
            'netmask':'str',
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
    Ips = typing.TypedDict('Ips', {
            'ipv4':'bool',
            'ipv6':'bool',
            'ipv6_link_local':'bool',
            'loopback':'bool',
            'any':'bool',
            'static':'bool',
    })
    InUseIp = typing.TypedDict('InUseIp', {
            'type':'str',
            'address':'str',
            'netmask':'int',
            'broadcast':'str',
    })
    LacpduRateChoices = typing.TypedDict('LacpduRateChoices', {
            'SLOW':'SLOW',
            'FAST':'FAST',
    })
    class SLOW(str,Enum):
        SLOW = 'SLOW'
        ...
    class FAST(str,Enum):
        FAST = 'FAST'
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
    InterfaceEntry = typing.TypedDict('InterfaceEntry', {
            'id':'str',
            'name':'str',
            'fake':'bool',
            'type':'str',
            'state':'State',
            'aliases':'list[Alias_]',
            'ipv4_dhcp':'bool',
            'ipv6_auto':'bool',
            'description':'str',
            'mtu':'typing.Optional[int]',
            'vlan_parent_interface':'typing.Optional[str]',
            'vlan_tag':'typing.Optional[int]',
            'vlan_pcp':'typing.Optional[int]',
            'lag_protocol':'str',
            'lag_ports':'list[str]',
            'bridge_members':'list[str]',
    })
    ServiceRestart = typing.TypedDict('ServiceRestart', {
            'type':'str',
            'service':'str',
            'ips':'list[str]',
    })
    InterfaceUpdate = typing.TypedDict('InterfaceUpdate', {
            'name':'str',
            'description':'str',
            'ipv4_dhcp':'bool',
            'ipv6_auto':'bool',
            'aliases':'list[InterfaceAlias]',
            'failover_critical':'bool',
            'failover_group':'typing.Optional[int]',
            'failover_vhid':'typing.Optional[int]',
            'failover_aliases':'list[InterfaceFailoverAlias]',
            'failover_virtual_aliases':'list[InterfaceVirtualAlias]',
            'bridge_members':'list',
            'stp':'bool',
            'lag_protocol':'LagProtocol',
            'xmit_hash_policy':'typing.Optional[str]',
            'lacpdu_rate':'typing.Optional[str]',
            'lag_ports':'list[str]',
            'vlan_parent_interface':'str',
            'vlan_tag':'int',
            'vlan_pcp':'typing.Optional[int]',
            'mtu':'typing.Optional[int]',
    })
    InterfaceUpdateReturns = typing.TypedDict('InterfaceUpdateReturns', {
            'id':'str',
            'name':'str',
            'fake':'bool',
            'type':'str',
            'state':'State',
            'aliases':'list[Alias_]',
            'ipv4_dhcp':'bool',
            'ipv6_auto':'bool',
            'description':'str',
            'mtu':'typing.Optional[int]',
            'vlan_parent_interface':'typing.Optional[str]',
            'vlan_tag':'typing.Optional[int]',
            'vlan_pcp':'typing.Optional[int]',
            'lag_protocol':'str',
            'lag_ports':'list[str]',
            'bridge_members':'list[str]',
    })
    XmitHashPolicyChoices = typing.TypedDict('XmitHashPolicyChoices', {
            'LAYER2':'LAYER2',
            'LAYER2+3':'LAYER2Plus3',
            'LAYER3+4':'LAYER3Plus4',
    })
    class LAYER2(str,Enum):
        LAYER2 = 'LAYER2'
        ...
    class LAYER2Plus3(str,Enum):
        LAYER2Plus3 = 'LAYER2+3'
        ...
    class LAYER3Plus4(str,Enum):
        LAYER3Plus4 = 'LAYER3+4'
        ...
