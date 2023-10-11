
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Interface(
    Namespace
    ):
    _namespace:typing.Literal['interface']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def bridge_members_choices(self, 
        id:'typing.Optional[str]',
    /) -> 'dict[str]': 
        """
        Return available interface choices that can be added to a `br` (bridge) interface.
        
        `id` is name of existing bridge interface on the system that will have its member
                interfaces included.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        dict[str]:
            bridge_members_choices
        """
        ...
    @typing.overload
    def cancel_rollback(self, 
    /) -> None: 
        """
        If this method is called after interface changes have been committed and within the checkin timeout,
        then the task that automatically rollsback any interface changes is cancelled and the in-memory snapshot
        of database tables for the various interface tables will NOT be cleared.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def checkin(self, 
    /) -> None: 
        """
        If this method is called after interface changes have been committed and within the checkin timeout,
        then the task that automatically rollsback any interface changes is cancelled and the in-memory snapshot
        of database tables for the various interface tables will be cleared. The idea is that the end-user has
        verified the changes work as intended and need to be committed permanently.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def checkin_waiting(self, 
    /) -> 'typing.Optional[int]': 
        """
        Returns whether or not we are waiting user to checkin the applied network changes
        before they are rolled back.
        Value is in number of seconds or null.

        Parameters
        ----------
        Returns
        -------
        typing.Optional[int]:
            remaining_seconds
        """
        ...
    @typing.overload
    def choices(self, 
        options:'Options',
    /) -> 'dict[str]': 
        """
        Choices of available network interfaces.
        
        `bridge_members` will include BRIDGE members.
        `lag_ports` will include LINK_AGGREGATION ports.
        `vlan_parent` will include VLAN parent interface.
        `exclude` is a list of interfaces prefix to remove.
        `include` is a list of interfaces that should not be removed.

        Parameters
        ----------
        options:
            options
        Returns
        -------
        dict[str]:
            available_interfaces
        """
        ...
    @typing.overload
    def commit(self, 
        options:'Options_',
    /) -> None: 
        """
        Commit/apply pending interfaces changes.
        
        `rollback` as true (default) will rollback changes in case they fail to apply.
        `checkin_timeout` is the time in seconds it will wait for the checkin call to acknowledge
        the interfaces changes happened as planned from the user. If checkin does not happen
        within this period of time the changes will get reverted.

        Parameters
        ----------
        options:
            options
        Returns
        -------
        """
        ...
    @typing.overload
    def create(self, 
        interface_create:'InterfaceCreate',
    /) -> 'InterfaceCreateReturns': 
        """
        Create virtual interfaces (Link Aggregation, VLAN)
        
        For BRIDGE `type` the following attribute is required: bridge_members.
        
        For LINK_AGGREGATION `type` the following attributes are required: lag_ports,
        lag_protocol.
        
        For VLAN `type` the following attributes are required: vlan_parent_interface,
        vlan_tag and vlan_pcp.

        Parameters
        ----------
        interface_create:
            interface_create
        Returns
        -------
        InterfaceCreateReturns:
            interface_create_returns
        """
        ...
    @typing.overload
    def default_route_will_be_removed(self, 
    /) -> 'bool': 
        """
        On a fresh install of SCALE, dhclient is started for every interface so IP
        addresses/routes could be installed via that program. However, when the
        end-user goes to configure the first interface we tear down all other interfaces
        configs AND delete the default route. We also remove the default route if the
        configured gateway doesn't match the one currently installed in kernel.

        Parameters
        ----------
        Returns
        -------
        bool:
            default_route_will_be_removed
        """
        ...
    @typing.overload
    def delete(self, 
        id:'str',
    /) -> 'str': 
        """
        Delete Interface of `id`.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        str:
            interface_id
        """
        ...
    @typing.overload
    def get_instance(self, 
        id:'typing.Union[str, int, bool, dict[str], list]',
        query_options_get_instance:'QueryOptionsGetInstance',
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
    def has_pending_changes(self, 
    /) -> 'bool': 
        """
        Returns whether there are pending interfaces changes to be applied or not.

        Parameters
        ----------
        Returns
        -------
        bool:
            has_pending_changes
        """
        ...
    @typing.overload
    def ip_in_use(self, 
        ips:'Ips',
    /) -> 'list[InUseIp]': 
        """
        Get all IPv4 / Ipv6 from all valid interfaces, excluding tap and epair.
        
        `loopback` will return loopback interface addresses.
        
        `any` will return wildcard addresses (0.0.0.0 and ::).
        
        `static` when enabled will ensure we only return static ip's configured.
        
        Returns a list of dicts - eg -
        
        [
            {
                "type": "INET6",
                "address": "fe80::5054:ff:fe16:4aac",
                "netmask": 64
            },
            {
                "type": "INET",
                "address": "192.168.122.148",
                "netmask": 24,
                "broadcast": "192.168.122.255"
            },
        ]

        Parameters
        ----------
        ips:
            ips
        Returns
        -------
        list[InUseIp]:
            in_use_ips
        """
        ...
    @typing.overload
    def lacpdu_rate_choices(self, 
    /) -> 'LacpduRateChoices': 
        """
        Available lacpdu rate policies for the LACP lagg type interfaces.

        Parameters
        ----------
        Returns
        -------
        LacpduRateChoices:
            lacpdu_rate_choices
        """
        ...
    @typing.overload
    def lag_ports_choices(self, 
        id:'typing.Optional[str]',
    /) -> 'dict[str]': 
        """
        Return available interface choices that can be added to a `bond` (lag) interface.
        
        `id` is name of existing bond interface on the system that will have its member
                interfaces included.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        dict[str]:
            lag_ports_choices
        """
        ...
    @typing.overload
    def query(self, 
        query_filters:'list[list]',
        query_options:'QueryOptions',
    /) -> 'typing.Union[list[InterfaceEntry], InterfaceEntry, int]': 
        """
        Query Interfaces with `query-filters` and `query-options`

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[InterfaceEntry], InterfaceEntry, int]:
            
        """
        ...
    @typing.overload
    def rollback(self, 
    /) -> None: 
        """
        Rollback pending interfaces changes.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def save_default_route(self, 
        gw:'str',
    /) -> None: 
        """
        This method exists _solely_ to provide a "warning" and therefore
        a path for remediation for when an end-user modifies an interface
        and we rip the default gateway out from underneath them without
        any type of warning.
        
        NOTE: This makes 2 assumptions
        1. interface.create/update/delete must have been called before
            calling this method
        2. this method must be called before `interface.sync` is called
        
        This method exists for the predominant scenario for new users...
        1. fresh install SCALE
        2. all interfaces start DHCPv4 (v6 is ignored for now)
        3. 1 of the interfaces receives an IP address
        4. along with the IP, the kernel receives a default route
            (by design, of course)
        5. user goes to configure this interface as having a static
            IP address
        6. as we go through and "sync" the changes, we remove the default
            route because it exists in the kernel FIB but doesn't exist
            in the database.
        7. IF the user is connecting via layer3, then they will lose all
            access to the TrueNAS and never be able to finalize the changes
            to the network because we ripped out the default route which
            is how they were communicating to begin with.
        
        In the above scenario, we're going to try and prevent this by doing
        the following:
        1. fresh install SCALE
        2. all interfaces start DHCPv4
        3. default route is received
        4. user configures an interface
        5. When user pushes "Test Changes" (interface.sync), webUI will call
            network.configuration.default_route_will_be_removed BEFORE interface.sync
        6. if network.configuration.default_route_will_be_removed returns True,
            then webUI will open a new modal dialog that gives the end-user
            ample warning/verbiage describing the situation. Furthermore, the
            modal will allow the user to input a default gateway
        7. if user gives gateway, webUI will call this method providing the info
            and we'll validate accordingly
        8. OR if user doesn't give gateway, they will need to "confirm" this is
            desired
        9. the default gateway provided to us (if given by end-user) will be stored
            in the same in-memory cache that we use for storing the interface changes
            and will be rolledback accordingly in this plugin just like everything else
        
        There are a few other scenarios where this is beneficial, but the one listed above
        is seen most often by end-users/support team.

        Parameters
        ----------
        gw:
            gw
        Returns
        -------
        """
        ...
    @typing.overload
    def services_restarted_on_sync(self, 
    /) -> 'list[ServiceRestart]': 
        """
        Returns which services will be set to listen on 0.0.0.0 (and, thus, restarted) on sync.
        
        Example result:
        [
            // Samba service will be set ot listen on 0.0.0.0 and restarted because it was set up to listen on
            // 192.168.0.1 which is being removed.
            {"type": "SYSTEM_SERVICE", "service": "cifs", "ips": ["192.168.0.1"]},
        ]

        Parameters
        ----------
        Returns
        -------
        list[ServiceRestart]:
            services_to_be_restarted
        """
        ...
    @typing.overload
    def update(self, 
        id:'str',
        interface_update:'InterfaceUpdate',
    /) -> 'InterfaceUpdateReturns': 
        """
        Update Interface of `id`.

        Parameters
        ----------
        id:
            Update Interface of `id`.
        interface_update:
            interface_update
        Returns
        -------
        InterfaceUpdateReturns:
            interface_update_returns
        """
        ...
    @typing.overload
    def vlan_parent_interface_choices(self, 
    /) -> 'dict[str]': 
        """
        Return available interface choices for `vlan_parent_interface` attribute.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            vlan_parent_interface_choices
        """
        ...
    @typing.overload
    def websocket_interface(self, 
    /) -> 'typing.Optional[str]': 
        """
        Returns the interface this websocket is connected to.

        Parameters
        ----------
        Returns
        -------
        typing.Optional[str]:
            websocket_interface
        """
        ...
    @typing.overload
    def websocket_local_ip(self, 
    /) -> 'typing.Optional[str]': 
        """
        Returns the ip this websocket is connected to.

        Parameters
        ----------
        Returns
        -------
        typing.Optional[str]:
            websocket_local_ip
        """
        ...
    @typing.overload
    def xmit_hash_policy_choices(self, 
    /) -> 'XmitHashPolicyChoices': 
        """
        Available transmit hash policies for the LACP or LOADBALANCE
        lagg type interfaces.

        Parameters
        ----------
        Returns
        -------
        XmitHashPolicyChoices:
            xmit_hash_policy_choices
        """
        ...
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
