
from pytruenas import Namespace
import typing
class Interface(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'interface')

    Options = typing.TypedDict('Options', {
            'bridge_members':'bool',
            'lag_ports':'bool',
            'vlan_parent':'bool',
            'exclude':'list',
            'exclude_types':'list[str]',
            'include':'list',
    })
    Options_ = typing.TypedDict('Options_', {
            'rollback':'bool',
            'checkin_timeout':'int',
    })
    InterfaceAlias = typing.TypedDict('InterfaceAlias', {
            'type':'str',
            'address':'str',
            'netmask':'int',
    })
    InterfaceFailoverAlias = typing.TypedDict('InterfaceFailoverAlias', {
            'type':'str',
            'address':'str',
    })
    InterfaceVirtualAlias = typing.TypedDict('InterfaceVirtualAlias', {
            'type':'str',
            'address':'str',
    })
    InterfaceCreate = typing.TypedDict('InterfaceCreate', {
            'name':'str',
            'description':'str',
            'type':'str',
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
            'lag_protocol':'str',
            'xmit_hash_policy':'typing.Optional[str]',
            'lacpdu_rate':'typing.Optional[str]',
            'lag_ports':'list[str]',
            'vlan_parent_interface':'str',
            'vlan_tag':'int',
            'vlan_pcp':'typing.Optional[int]',
            'mtu':'typing.Optional[int]',
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
    Alias_ = typing.TypedDict('Alias_', {
            'type':'str',
            'address':'str',
            'netmask':'str',
    })
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
            'SLOW':'str',
            'FAST':'str',
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
    Alias__ = typing.TypedDict('Alias__', {
            'type':'str',
            'address':'str',
            'netmask':'str',
            'broadcast':'str',
    })
    LagPorts_ = typing.TypedDict('LagPorts_', {
            'name':'str',
            'flags':'list[str]',
    })
    State_ = typing.TypedDict('State_', {
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
            'aliases':'list[Alias__]',
            'vrrp_config':'typing.Optional[list]',
            'protocol':'typing.Optional[str]',
            'ports':'list[LagPorts_]',
            'xmit_hash_policy':'typing.Optional[str]',
            'lacpdu_rate':'typing.Optional[str]',
            'parent':'typing.Optional[str]',
            'tag':'typing.Optional[int]',
            'pcp':'typing.Optional[int]',
    })
    Alias___ = typing.TypedDict('Alias___', {
            'type':'str',
            'address':'str',
            'netmask':'str',
    })
    InterfaceEntry = typing.TypedDict('InterfaceEntry', {
            'id':'str',
            'name':'str',
            'fake':'bool',
            'type':'str',
            'state':'State_',
            'aliases':'list[Alias___]',
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
    Alias____ = typing.TypedDict('Alias____', {
            'type':'str',
            'address':'str',
            'netmask':'str',
            'broadcast':'str',
    })
    LagPorts__ = typing.TypedDict('LagPorts__', {
            'name':'str',
            'flags':'list[str]',
    })
    State__ = typing.TypedDict('State__', {
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
            'aliases':'list[Alias____]',
            'vrrp_config':'typing.Optional[list]',
            'protocol':'typing.Optional[str]',
            'ports':'list[LagPorts__]',
            'xmit_hash_policy':'typing.Optional[str]',
            'lacpdu_rate':'typing.Optional[str]',
            'parent':'typing.Optional[str]',
            'tag':'typing.Optional[int]',
            'pcp':'typing.Optional[int]',
    })
    Alias_____ = typing.TypedDict('Alias_____', {
            'type':'str',
            'address':'str',
            'netmask':'str',
    })
    InterfaceEntry_ = typing.TypedDict('InterfaceEntry_', {
            'id':'str',
            'name':'str',
            'fake':'bool',
            'type':'str',
            'state':'State__',
            'aliases':'list[Alias_____]',
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
    Alias______ = typing.TypedDict('Alias______', {
            'type':'str',
            'address':'str',
            'netmask':'str',
            'broadcast':'str',
    })
    LagPorts___ = typing.TypedDict('LagPorts___', {
            'name':'str',
            'flags':'list[str]',
    })
    State___ = typing.TypedDict('State___', {
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
            'aliases':'list[Alias______]',
            'vrrp_config':'typing.Optional[list]',
            'protocol':'typing.Optional[str]',
            'ports':'list[LagPorts___]',
            'xmit_hash_policy':'typing.Optional[str]',
            'lacpdu_rate':'typing.Optional[str]',
            'parent':'typing.Optional[str]',
            'tag':'typing.Optional[int]',
            'pcp':'typing.Optional[int]',
    })
    Alias_______ = typing.TypedDict('Alias_______', {
            'type':'str',
            'address':'str',
            'netmask':'str',
    })
    InterfaceEntry__ = typing.TypedDict('InterfaceEntry__', {
            'id':'str',
            'name':'str',
            'fake':'bool',
            'type':'str',
            'state':'State___',
            'aliases':'list[Alias_______]',
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
    InterfaceAlias_ = typing.TypedDict('InterfaceAlias_', {
            'type':'str',
            'address':'str',
            'netmask':'int',
    })
    InterfaceFailoverAlias_ = typing.TypedDict('InterfaceFailoverAlias_', {
            'type':'str',
            'address':'str',
    })
    InterfaceVirtualAlias_ = typing.TypedDict('InterfaceVirtualAlias_', {
            'type':'str',
            'address':'str',
    })
    InterfaceUpdate = typing.TypedDict('InterfaceUpdate', {
            'name':'str',
            'description':'str',
            'ipv4_dhcp':'bool',
            'ipv6_auto':'bool',
            'aliases':'list[InterfaceAlias_]',
            'failover_critical':'bool',
            'failover_group':'typing.Optional[int]',
            'failover_vhid':'typing.Optional[int]',
            'failover_aliases':'list[InterfaceFailoverAlias_]',
            'failover_virtual_aliases':'list[InterfaceVirtualAlias_]',
            'bridge_members':'list',
            'stp':'bool',
            'lag_protocol':'str',
            'xmit_hash_policy':'typing.Optional[str]',
            'lacpdu_rate':'typing.Optional[str]',
            'lag_ports':'list[str]',
            'vlan_parent_interface':'str',
            'vlan_tag':'int',
            'vlan_pcp':'typing.Optional[int]',
            'mtu':'typing.Optional[int]',
    })
    Alias________ = typing.TypedDict('Alias________', {
            'type':'str',
            'address':'str',
            'netmask':'str',
            'broadcast':'str',
    })
    LagPorts____ = typing.TypedDict('LagPorts____', {
            'name':'str',
            'flags':'list[str]',
    })
    State____ = typing.TypedDict('State____', {
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
            'aliases':'list[Alias________]',
            'vrrp_config':'typing.Optional[list]',
            'protocol':'typing.Optional[str]',
            'ports':'list[LagPorts____]',
            'xmit_hash_policy':'typing.Optional[str]',
            'lacpdu_rate':'typing.Optional[str]',
            'parent':'typing.Optional[str]',
            'tag':'typing.Optional[int]',
            'pcp':'typing.Optional[int]',
    })
    Alias_________ = typing.TypedDict('Alias_________', {
            'type':'str',
            'address':'str',
            'netmask':'str',
    })
    InterfaceUpdateReturns = typing.TypedDict('InterfaceUpdateReturns', {
            'id':'str',
            'name':'str',
            'fake':'bool',
            'type':'str',
            'state':'State____',
            'aliases':'list[Alias_________]',
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
            'LAYER2':'str',
            'LAYER2+3':'str',
            'LAYER3+4':'str',
    })
