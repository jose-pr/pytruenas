
from pytruenas import Namespace, TrueNASClient
import typing
class NetworkConfiguration(Namespace):
    _namespace:typing.Literal['network.configuration']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def activity_choices(self, 
    /) -> 'list[list[str]]': 
        """
        Returns allowed/forbidden network activity choices.

        Parameters
        ----------
        Returns
        -------
        list[list[str]]:
            activity_choices
        """
        ...
    ServiceAnnouncement = typing.TypedDict('ServiceAnnouncement', {
            'netbios':'bool',
            'mdns':'bool',
            'wsd':'bool',
    })
    Activity = typing.TypedDict('Activity', {
            'type':'str',
            'activities':'list[str]',
    })
    State = typing.TypedDict('State', {
            'ipv4gateway':'str',
            'ipv6gateway':'str',
            'nameserver1':'str',
            'nameserver2':'str',
            'nameserver3':'str',
    })
    NetworkConfigurationEntry = typing.TypedDict('NetworkConfigurationEntry', {
            'id':'int',
            'hostname':'str',
            'domain':'str',
            'ipv4gateway':'str',
            'ipv6gateway':'str',
            'nameserver1':'str',
            'nameserver2':'str',
            'nameserver3':'str',
            'httpproxy':'str',
            'hosts':'list[str]',
            'domains':'list[str]',
            'service_announcement':'ServiceAnnouncement',
            'activity':'Activity',
            'hostname_local':'str',
            'hostname_b':'typing.Optional[str]',
            'hostname_virtual':'typing.Optional[str]',
            'state':'State',
    })
    ServiceAnnouncement_ = typing.TypedDict('ServiceAnnouncement_', {
            'netbios':'bool',
            'mdns':'bool',
            'wsd':'bool',
    })
    Activity_ = typing.TypedDict('Activity_', {
            'type':'str',
            'activities':'list[str]',
    })
    GlobalConfigurationUpdate = typing.TypedDict('GlobalConfigurationUpdate', {
            'hostname':'str',
            'domain':'str',
            'ipv4gateway':'str',
            'ipv6gateway':'str',
            'nameserver1':'str',
            'nameserver2':'str',
            'nameserver3':'str',
            'httpproxy':'str',
            'hosts':'list[str]',
            'domains':'list[str]',
            'service_announcement':'ServiceAnnouncement_',
            'activity':'Activity_',
            'hostname_b':'typing.Optional[str]',
            'hostname_virtual':'typing.Optional[str]',
    })
    ServiceAnnouncement__ = typing.TypedDict('ServiceAnnouncement__', {
            'netbios':'bool',
            'mdns':'bool',
            'wsd':'bool',
    })
    Activity__ = typing.TypedDict('Activity__', {
            'type':'str',
            'activities':'list[str]',
    })
    State_ = typing.TypedDict('State_', {
            'ipv4gateway':'str',
            'ipv6gateway':'str',
            'nameserver1':'str',
            'nameserver2':'str',
            'nameserver3':'str',
    })
    NetworkConfigurationUpdateReturns = typing.TypedDict('NetworkConfigurationUpdateReturns', {
            'id':'int',
            'hostname':'str',
            'domain':'str',
            'ipv4gateway':'str',
            'ipv6gateway':'str',
            'nameserver1':'str',
            'nameserver2':'str',
            'nameserver3':'str',
            'httpproxy':'str',
            'hosts':'list[str]',
            'domains':'list[str]',
            'service_announcement':'ServiceAnnouncement__',
            'activity':'Activity__',
            'hostname_local':'str',
            'hostname_b':'typing.Optional[str]',
            'hostname_virtual':'typing.Optional[str]',
            'state':'State_',
    })
    @typing.overload
    def config(self, 
    /) -> 'NetworkConfigurationEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        NetworkConfigurationEntry:
            network_configuration_entry
        """
        ...
    ServiceAnnouncement = typing.TypedDict('ServiceAnnouncement', {
            'netbios':'bool',
            'mdns':'bool',
            'wsd':'bool',
    })
    Activity = typing.TypedDict('Activity', {
            'type':'str',
            'activities':'list[str]',
    })
    State = typing.TypedDict('State', {
            'ipv4gateway':'str',
            'ipv6gateway':'str',
            'nameserver1':'str',
            'nameserver2':'str',
            'nameserver3':'str',
    })
    NetworkConfigurationEntry = typing.TypedDict('NetworkConfigurationEntry', {
            'id':'int',
            'hostname':'str',
            'domain':'str',
            'ipv4gateway':'str',
            'ipv6gateway':'str',
            'nameserver1':'str',
            'nameserver2':'str',
            'nameserver3':'str',
            'httpproxy':'str',
            'hosts':'list[str]',
            'domains':'list[str]',
            'service_announcement':'ServiceAnnouncement',
            'activity':'Activity',
            'hostname_local':'str',
            'hostname_b':'typing.Optional[str]',
            'hostname_virtual':'typing.Optional[str]',
            'state':'State',
    })
    ServiceAnnouncement_ = typing.TypedDict('ServiceAnnouncement_', {
            'netbios':'bool',
            'mdns':'bool',
            'wsd':'bool',
    })
    Activity_ = typing.TypedDict('Activity_', {
            'type':'str',
            'activities':'list[str]',
    })
    GlobalConfigurationUpdate = typing.TypedDict('GlobalConfigurationUpdate', {
            'hostname':'str',
            'domain':'str',
            'ipv4gateway':'str',
            'ipv6gateway':'str',
            'nameserver1':'str',
            'nameserver2':'str',
            'nameserver3':'str',
            'httpproxy':'str',
            'hosts':'list[str]',
            'domains':'list[str]',
            'service_announcement':'ServiceAnnouncement_',
            'activity':'Activity_',
            'hostname_b':'typing.Optional[str]',
            'hostname_virtual':'typing.Optional[str]',
    })
    ServiceAnnouncement__ = typing.TypedDict('ServiceAnnouncement__', {
            'netbios':'bool',
            'mdns':'bool',
            'wsd':'bool',
    })
    Activity__ = typing.TypedDict('Activity__', {
            'type':'str',
            'activities':'list[str]',
    })
    State_ = typing.TypedDict('State_', {
            'ipv4gateway':'str',
            'ipv6gateway':'str',
            'nameserver1':'str',
            'nameserver2':'str',
            'nameserver3':'str',
    })
    NetworkConfigurationUpdateReturns = typing.TypedDict('NetworkConfigurationUpdateReturns', {
            'id':'int',
            'hostname':'str',
            'domain':'str',
            'ipv4gateway':'str',
            'ipv6gateway':'str',
            'nameserver1':'str',
            'nameserver2':'str',
            'nameserver3':'str',
            'httpproxy':'str',
            'hosts':'list[str]',
            'domains':'list[str]',
            'service_announcement':'ServiceAnnouncement__',
            'activity':'Activity__',
            'hostname_local':'str',
            'hostname_b':'typing.Optional[str]',
            'hostname_virtual':'typing.Optional[str]',
            'state':'State_',
    })
    @typing.overload
    def update(self, 
        global_configuration_update:'GlobalConfigurationUpdate'={},
    /) -> 'NetworkConfigurationUpdateReturns': 
        """
        Update Network Configuration Service configuration.
        
        `ipv4gateway` if set is used instead of the default gateway provided by DHCP.
        
        `nameserver1` is primary DNS server.
        
        `nameserver2` is secondary DNS server.
        
        `nameserver3` is tertiary DNS server.
        
        `httpproxy` attribute must be provided if a proxy is to be used for network operations.
        
        `service_announcement` determines the broadcast protocols that will be used to advertise the server.
        `netbios` enables the NetBIOS name server (NBNS), which starts concurrently with the SMB service. SMB clients
        will only perform NBNS lookups if SMB1 is enabled. NBNS may be required for legacy SMB clients.
        `mdns` enables multicast DNS service announcements for enabled services. `wsd` enables Web Service
        Discovery support.

        Parameters
        ----------
        global_configuration_update:
            global_configuration_update
        Returns
        -------
        NetworkConfigurationUpdateReturns:
            network_configuration_update_returns
        """
        ...
    ServiceAnnouncement = typing.TypedDict('ServiceAnnouncement', {
            'netbios':'bool',
            'mdns':'bool',
            'wsd':'bool',
    })
    Activity = typing.TypedDict('Activity', {
            'type':'str',
            'activities':'list[str]',
    })
    State = typing.TypedDict('State', {
            'ipv4gateway':'str',
            'ipv6gateway':'str',
            'nameserver1':'str',
            'nameserver2':'str',
            'nameserver3':'str',
    })
    NetworkConfigurationEntry = typing.TypedDict('NetworkConfigurationEntry', {
            'id':'int',
            'hostname':'str',
            'domain':'str',
            'ipv4gateway':'str',
            'ipv6gateway':'str',
            'nameserver1':'str',
            'nameserver2':'str',
            'nameserver3':'str',
            'httpproxy':'str',
            'hosts':'list[str]',
            'domains':'list[str]',
            'service_announcement':'ServiceAnnouncement',
            'activity':'Activity',
            'hostname_local':'str',
            'hostname_b':'typing.Optional[str]',
            'hostname_virtual':'typing.Optional[str]',
            'state':'State',
    })
    ServiceAnnouncement_ = typing.TypedDict('ServiceAnnouncement_', {
            'netbios':'bool',
            'mdns':'bool',
            'wsd':'bool',
    })
    Activity_ = typing.TypedDict('Activity_', {
            'type':'str',
            'activities':'list[str]',
    })
    GlobalConfigurationUpdate = typing.TypedDict('GlobalConfigurationUpdate', {
            'hostname':'str',
            'domain':'str',
            'ipv4gateway':'str',
            'ipv6gateway':'str',
            'nameserver1':'str',
            'nameserver2':'str',
            'nameserver3':'str',
            'httpproxy':'str',
            'hosts':'list[str]',
            'domains':'list[str]',
            'service_announcement':'ServiceAnnouncement_',
            'activity':'Activity_',
            'hostname_b':'typing.Optional[str]',
            'hostname_virtual':'typing.Optional[str]',
    })
    ServiceAnnouncement__ = typing.TypedDict('ServiceAnnouncement__', {
            'netbios':'bool',
            'mdns':'bool',
            'wsd':'bool',
    })
    Activity__ = typing.TypedDict('Activity__', {
            'type':'str',
            'activities':'list[str]',
    })
    State_ = typing.TypedDict('State_', {
            'ipv4gateway':'str',
            'ipv6gateway':'str',
            'nameserver1':'str',
            'nameserver2':'str',
            'nameserver3':'str',
    })
    NetworkConfigurationUpdateReturns = typing.TypedDict('NetworkConfigurationUpdateReturns', {
            'id':'int',
            'hostname':'str',
            'domain':'str',
            'ipv4gateway':'str',
            'ipv6gateway':'str',
            'nameserver1':'str',
            'nameserver2':'str',
            'nameserver3':'str',
            'httpproxy':'str',
            'hosts':'list[str]',
            'domains':'list[str]',
            'service_announcement':'ServiceAnnouncement__',
            'activity':'Activity__',
            'hostname_local':'str',
            'hostname_b':'typing.Optional[str]',
            'hostname_virtual':'typing.Optional[str]',
            'state':'State_',
    })

