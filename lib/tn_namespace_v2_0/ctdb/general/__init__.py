
from pytruenas import Namespace
import typing
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
    CtdbNode = typing.TypedDict('CtdbNode', {
            'pnn':'int',
            'address':'str',
            'address_type':'str',
            'enabled':'bool',
            'this_node':'bool',
    })
    CtdbStatus = typing.TypedDict('CtdbStatus', {
            'all_nodes':'bool',
    })
    Address = typing.TypedDict('Address', {
            'type':'str',
            'address':'str',
    })
    CtdbNodemapEntry = typing.TypedDict('CtdbNodemapEntry', {
            'pnn':'int',
            'address':'Address',
            'flags':'list[str]',
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
    CtdbStatus_ = typing.TypedDict('CtdbStatus_', {
            'nodemap':'Nodemap',
            'vnnmap':'Vnnmap',
            'recovery_mode_raw':'int',
            'recovery_mode_str':'str',
            'recovery_master':'int',
            'all_healthy':'bool',
    })
