
from pytruenas.base import Namespace

import typing
from enum import Enum

class CtdbGeneral(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ctdb.general')

    CtdbIps = typing.TypedDict('CtdbIps', {
            'all_nodes':'bool',
    })
    CtdbPublicIp = typing.TypedDict('CtdbPublicIp', {
            'public_ip':'str',
            'pnn':'int',
            'interfaces':'list[CtdbInterfaceInfo]',
    })
    CtdbInterfaceInfo = typing.TypedDict('CtdbInterfaceInfo', {
            'name':'str',
            'active':'bool',
            'available':'bool',
    })
    CtdbNode = typing.TypedDict('CtdbNode', {
            'pnn':'int',
            'address':'str',
            'address_type':'AddressType',
            'enabled':'bool',
            'this_node':'bool',
    })
    class AddressType(str,Enum):
        INET = 'INET'
        INET6 = 'INET6'
        ...
    CtdbStatus = typing.TypedDict('CtdbStatus', {
            'all_nodes':'bool',
    })
    CtdbStatus_ = typing.TypedDict('CtdbStatus_', {
            'nodemap':'Nodemap',
            'vnnmap':'Vnnmap',
            'recovery_mode_raw':'int',
            'recovery_mode_str':'RecoveryModeStr',
            'recovery_master':'int',
            'all_healthy':'bool',
    })
    Nodemap = typing.TypedDict('Nodemap', {
            'node_count':'int',
            'deleted_node_count':'int',
            'nodes':'list[CtdbNodemapEntry]',
    })
    CtdbNodemapEntry = typing.TypedDict('CtdbNodemapEntry', {
            'pnn':'int',
            'address':'Address',
            'flags':'list[CtdbStatusFlag]',
            'flags_raw':'int',
            'partially_online':'bool',
            'this_node':'bool',
    })
    Address = typing.TypedDict('Address', {
            'type':'Type',
            'address':'str',
    })
    class Type(str,Enum):
        INET = 'INET'
        INET6 = 'INET6'
        ...
    class CtdbStatusFlag(str,Enum):
        DISCONNECTED = 'DISCONNECTED'
        UNHEALTHY = 'UNHEALTHY'
        INACTIVE = 'INACTIVE'
        DISABLED = 'DISABLED'
        STOPPED = 'STOPPED'
        DELETED = 'DELETED'
        BANNED = 'BANNED'
        ...
    Vnnmap = typing.TypedDict('Vnnmap', {
            'size':'int',
            'generation':'int',
            'entries':'list[StatusProperties]',
    })
    StatusProperties = typing.TypedDict('StatusProperties', {
            'hash':'int',
            'lmaster':'int',
    })
    class RecoveryModeStr(str,Enum):
        NORMAL = 'NORMAL'
        RECOVERY = 'RECOVERY'
        ...
