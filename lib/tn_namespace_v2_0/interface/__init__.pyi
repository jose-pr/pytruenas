
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Interface(Namespace):
    _namespace:_ty.Literal['interface']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def bridge_members_choices(self, 
        id:'str|None'=None,
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
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
    def checkin_waiting(self, 
    /) -> 'int|None': 
        """
        Returns whether or not we are waiting user to checkin the applied network changes
        before they are rolled back.
        Value is in number of seconds or null.

        Parameters
        ----------
        Returns
        -------
        int:
            remaining_seconds
        None:
            remaining_seconds
        """
        ...
    @_ty.overload
    def choices(self, 
        options:'dict[str]'={},
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
    @_ty.overload
    def commit(self, 
        options:'dict[str]'={},
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
    @_ty.overload
    def create(self, 
        interface_create:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            interface_create_returns
        """
        ...
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
    def ip_in_use(self, 
        ips:'dict[str]'={},
    /) -> 'list': 
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
        list:
            in_use_ips
        """
        ...
    @_ty.overload
    def lacpdu_rate_choices(self, 
    /) -> 'dict[str]': 
        """
        Available lacpdu rate policies for the LACP lagg type interfaces.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            lacpdu_rate_choices
        """
        ...
    @_ty.overload
    def lag_ports_choices(self, 
        id:'str|None'=None,
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
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
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
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
    def services_restarted_on_sync(self, 
    /) -> 'list': 
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
        list:
            services_to_be_restarted
        """
        ...
    @_ty.overload
    def update(self, 
        id:'str',
        interface_update:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            interface_update_returns
        """
        ...
    @_ty.overload
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
    @_ty.overload
    def websocket_interface(self, 
    /) -> 'str|None': 
        """
        Returns the interface this websocket is connected to.

        Parameters
        ----------
        Returns
        -------
        str:
            websocket_interface
        None:
            websocket_interface
        """
        ...
    @_ty.overload
    def websocket_local_ip(self, 
    /) -> 'str|None': 
        """
        Returns the ip this websocket is connected to.

        Parameters
        ----------
        Returns
        -------
        str:
            websocket_local_ip
        None:
            websocket_local_ip
        """
        ...
    @_ty.overload
    def xmit_hash_policy_choices(self, 
    /) -> 'dict[str]': 
        """
        Available transmit hash policies for the LACP or LOADBALANCE
        lagg type interfaces.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            xmit_hash_policy_choices
        """
        ...
