
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
from enum import Enum

class NetworkConfiguration(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'network.configuration')

    ServiceAnnouncement = typing.TypedDict('ServiceAnnouncement', {
            'netbios':'bool',
            'mdns':'bool',
            'wsd':'bool',
    })
    class Type(str,Enum):
        ALLOW = 'ALLOW'
        DENY = 'DENY'
        ...
    Activity = typing.TypedDict('Activity', {
            'type':'Type',
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
    Activity_ = typing.TypedDict('Activity_', {
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
            'activity':'Activity_',
            'hostname_b':'typing.Optional[str]',
            'hostname_virtual':'typing.Optional[str]',
    })
    Activity__ = typing.TypedDict('Activity__', {
            'type':'Type',
            'activities':'list[str]',
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
            'activity':'Activity__',
            'hostname_local':'str',
            'hostname_b':'typing.Optional[str]',
            'hostname_virtual':'typing.Optional[str]',
            'state':'State',
    })
