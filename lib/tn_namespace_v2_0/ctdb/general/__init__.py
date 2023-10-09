
from pytruenas.base import Namespace

import typing
from enum import Enum

class CtdbGeneral(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ctdb.general')

    CtdbIps = typing.TypedDict('CtdbIps', {
            'all_nodes':'bool',
    })
    CtdbInterfaceInfo = typing.TypedDict('CtdbInterfaceInfo', {
            'name':'str',
            'active':'bool',
            'available':'bool',
    })
    CtdbPublicIp = typing.TypedDict('CtdbPublicIp', {
            'public_ip':'str',
            'pnn':'int',
            'interfaces':'list[CtdbInterfaceInfo]',
    })
    class AddressType(str,Enum):
        INET = 'INET'
        INET6 = 'INET6'
        ...
    CtdbNode = typing.TypedDict('CtdbNode', {
            'pnn':'int',
            'address':'str',
            'address_type':'AddressType',
            'enabled':'bool',
            'this_node':'bool',
    })
    CtdbStatus = typing.TypedDict('CtdbStatus', {
            'all_nodes':'bool',
    })
    class Type(str,Enum):
        INET = 'INET'
        INET6 = 'INET6'
        ...
    Address = typing.TypedDict('Address', {
            'type':'Type',
            'address':'str',
    })
    class CtdbStatusFlag(str,Enum):
        DISCONNECTED = 'DISCONNECTED'
        UNHEALTHY = 'UNHEALTHY'
        INACTIVE = 'INACTIVE'
        DISABLED = 'DISABLED'
        STOPPED = 'STOPPED'
        DELETED = 'DELETED'
        BANNED = 'BANNED'
        ...
    CtdbNodemapEntry = typing.TypedDict('CtdbNodemapEntry', {
            'pnn':'int',
            'address':'Address',
            'flags':'list[CtdbStatusFlag]',
            'flags_raw':'int',
            'partially_online':'bool',
            'this_node':'bool',
    })
    Nodemap = typing.TypedDict('Nodemap', {
            'node_count':'int',
            'deleted_node_count':'int',
            'nodes':'list[CtdbNodemapEntry]',
    })
    Object = typing.TypedDict('Object', {
            'hash':'int',
            'lmaster':'int',
    })
    Vnnmap = typing.TypedDict('Vnnmap', {
            'size':'int',
            'generation':'int',
            'entries':'list[Object]',
    })
    class RecoveryModeStr(str,Enum):
        NORMAL = 'NORMAL'
        RECOVERY = 'RECOVERY'
        ...
    CtdbStatus_ = typing.TypedDict('CtdbStatus_', {
            'nodemap':'Nodemap',
            'vnnmap':'Vnnmap',
            'recovery_mode_raw':'int',
            'recovery_mode_str':'RecoveryModeStr',
            'recovery_master':'int',
            'all_healthy':'bool',
    })
