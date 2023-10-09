
from pytruenas import Namespace
import typing
class NetworkConfiguration(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'network.configuration')

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
