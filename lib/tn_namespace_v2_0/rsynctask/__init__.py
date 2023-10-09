
from pytruenas.base import Namespace

import typing
class Rsynctask(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'rsynctask')

    Schedule = typing.TypedDict('Schedule', {
            'minute':'str',
            'hour':'str',
            'dom':'str',
            'month':'str',
            'dow':'str',
    })
    RsyncTaskCreate = typing.TypedDict('RsyncTaskCreate', {
            'path':'str',
            'user':'str',
            'mode':'str',
            'remotehost':'typing.Optional[str]',
            'remoteport':'typing.Optional[int]',
            'remotemodule':'typing.Optional[str]',
            'ssh_credentials':'typing.Optional[int]',
            'remotepath':'str',
            'validate_rpath':'bool',
            'ssh_keyscan':'bool',
            'direction':'str',
            'desc':'str',
            'schedule':'Schedule',
            'recursive':'bool',
            'times':'bool',
            'compress':'bool',
            'archive':'bool',
            'delete':'bool',
            'quiet':'bool',
            'preserveperm':'bool',
            'preserveattr':'bool',
            'delayupdates':'bool',
            'extra':'list[str]',
            'enabled':'bool',
    })
    RsynctaskCreateReturns = typing.TypedDict('RsynctaskCreateReturns', {
            'path':'str',
            'user':'str',
            'mode':'str',
            'remotehost':'typing.Optional[str]',
            'remoteport':'typing.Optional[int]',
            'remotemodule':'typing.Optional[str]',
            'remotepath':'str',
            'direction':'str',
            'desc':'str',
            'schedule':'Schedule',
            'recursive':'bool',
            'times':'bool',
            'compress':'bool',
            'archive':'bool',
            'delete':'bool',
            'quiet':'bool',
            'preserveperm':'bool',
            'preserveattr':'bool',
            'delayupdates':'bool',
            'extra':'list[str]',
            'enabled':'bool',
            'id':'int',
            'ssh_credentials':'dict[str]',
            'locked':'bool',
            'job':'dict[str]',
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
    RsyncTaskEntry = typing.TypedDict('RsyncTaskEntry', {
            'path':'str',
            'user':'str',
            'mode':'str',
            'remotehost':'typing.Optional[str]',
            'remoteport':'typing.Optional[int]',
            'remotemodule':'typing.Optional[str]',
            'remotepath':'str',
            'direction':'str',
            'desc':'str',
            'schedule':'Schedule',
            'recursive':'bool',
            'times':'bool',
            'compress':'bool',
            'archive':'bool',
            'delete':'bool',
            'quiet':'bool',
            'preserveperm':'bool',
            'preserveattr':'bool',
            'delayupdates':'bool',
            'extra':'list[str]',
            'enabled':'bool',
            'id':'int',
            'ssh_credentials':'dict[str]',
            'locked':'bool',
            'job':'dict[str]',
    })
    RsyncTaskEntry_ = typing.TypedDict('RsyncTaskEntry_', {
            'path':'str',
            'user':'str',
            'mode':'str',
            'remotehost':'typing.Optional[str]',
            'remoteport':'typing.Optional[int]',
            'remotemodule':'typing.Optional[str]',
            'remotepath':'str',
            'direction':'str',
            'desc':'str',
            'schedule':'Schedule',
            'recursive':'bool',
            'times':'bool',
            'compress':'bool',
            'archive':'bool',
            'delete':'bool',
            'quiet':'bool',
            'preserveperm':'bool',
            'preserveattr':'bool',
            'delayupdates':'bool',
            'extra':'list[str]',
            'enabled':'bool',
            'id':'int',
            'ssh_credentials':'dict[str]',
            'locked':'bool',
            'job':'dict[str]',
    })
    RsyncTaskEntry__ = typing.TypedDict('RsyncTaskEntry__', {
            'path':'str',
            'user':'str',
            'mode':'str',
            'remotehost':'typing.Optional[str]',
            'remoteport':'typing.Optional[int]',
            'remotemodule':'typing.Optional[str]',
            'remotepath':'str',
            'direction':'str',
            'desc':'str',
            'schedule':'Schedule',
            'recursive':'bool',
            'times':'bool',
            'compress':'bool',
            'archive':'bool',
            'delete':'bool',
            'quiet':'bool',
            'preserveperm':'bool',
            'preserveattr':'bool',
            'delayupdates':'bool',
            'extra':'list[str]',
            'enabled':'bool',
            'id':'int',
            'ssh_credentials':'dict[str]',
            'locked':'bool',
            'job':'dict[str]',
    })
    RsyncTaskUpdate = typing.TypedDict('RsyncTaskUpdate', {
            'path':'str',
            'user':'str',
            'mode':'str',
            'remotehost':'typing.Optional[str]',
            'remoteport':'typing.Optional[int]',
            'remotemodule':'typing.Optional[str]',
            'ssh_credentials':'typing.Optional[int]',
            'remotepath':'str',
            'validate_rpath':'bool',
            'ssh_keyscan':'bool',
            'direction':'str',
            'desc':'str',
            'schedule':'Schedule',
            'recursive':'bool',
            'times':'bool',
            'compress':'bool',
            'archive':'bool',
            'delete':'bool',
            'quiet':'bool',
            'preserveperm':'bool',
            'preserveattr':'bool',
            'delayupdates':'bool',
            'extra':'list[str]',
            'enabled':'bool',
    })
    RsynctaskUpdateReturns = typing.TypedDict('RsynctaskUpdateReturns', {
            'path':'str',
            'user':'str',
            'mode':'str',
            'remotehost':'typing.Optional[str]',
            'remoteport':'typing.Optional[int]',
            'remotemodule':'typing.Optional[str]',
            'remotepath':'str',
            'direction':'str',
            'desc':'str',
            'schedule':'Schedule',
            'recursive':'bool',
            'times':'bool',
            'compress':'bool',
            'archive':'bool',
            'delete':'bool',
            'quiet':'bool',
            'preserveperm':'bool',
            'preserveattr':'bool',
            'delayupdates':'bool',
            'extra':'list[str]',
            'enabled':'bool',
            'id':'int',
            'ssh_credentials':'dict[str]',
            'locked':'bool',
            'job':'dict[str]',
    })
