
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
from enum import Enum

class NetworkConfiguration(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'network.configuration')

    Activity = typing.TypedDict('Activity', {
            'type':'Type',
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
            'service_announcement':'ServiceAnnouncement',
            'activity':'Activity',
            'hostname_b':'typing.Optional[str]',
            'hostname_virtual':'typing.Optional[str]',
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
            'service_announcement':'ServiceAnnouncement',
            'activity':'Activity',
            'hostname_local':'str',
            'hostname_b':'typing.Optional[str]',
            'hostname_virtual':'typing.Optional[str]',
            'state':'State',
    })
    ServiceAnnouncement = typing.TypedDict('ServiceAnnouncement', {
            'netbios':'bool',
            'mdns':'bool',
            'wsd':'bool',
    })
    State = typing.TypedDict('State', {
            'ipv4gateway':'str',
            'ipv6gateway':'str',
            'nameserver1':'str',
            'nameserver2':'str',
            'nameserver3':'str',
    })
    class Type(str,Enum):
        ALLOW = 'ALLOW'
        DENY = 'DENY'
        ...
