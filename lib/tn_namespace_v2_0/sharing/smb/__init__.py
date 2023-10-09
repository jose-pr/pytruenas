
from pytruenas.base import Namespace

import typing
from enum import Enum

class SharingSmb(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'sharing.smb')

    class Purpose(str,Enum):
        NOPRESET = 'NO_PRESET'
        DEFAULTCLUSTERSHARE = 'DEFAULT_CLUSTER_SHARE'
        DEFAULTSHARE = 'DEFAULT_SHARE'
        TIMEMACHINE = 'TIMEMACHINE'
        ENHANCEDTIMEMACHINE = 'ENHANCED_TIMEMACHINE'
        MULTIPROTOCOLNFS = 'MULTI_PROTOCOL_NFS'
        PRIVATEDATASETS = 'PRIVATE_DATASETS'
        READONLY = 'READ_ONLY'
        WORMDROPBOX = 'WORM_DROPBOX'
        ...
    SharingsmbCreate = typing.TypedDict('SharingsmbCreate', {
            'purpose':'Purpose',
            'path':'str',
            'path_suffix':'str',
            'home':'bool',
            'name':'str',
            'comment':'str',
            'ro':'bool',
            'browsable':'bool',
            'timemachine':'bool',
            'timemachine_quota':'int',
            'recyclebin':'bool',
            'guestok':'bool',
            'abe':'bool',
            'hostsallow':'list',
            'hostsdeny':'list',
            'aapl_name_mangling':'bool',
            'acl':'bool',
            'durablehandle':'bool',
            'shadowcopy':'bool',
            'streams':'bool',
            'fsrvp':'bool',
            'auxsmbconf':'str',
            'enabled':'bool',
            'cluster_volname':'str',
            'afp':'bool',
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
    SmbGetacl = typing.TypedDict('SmbGetacl', {
            'share_name':'str',
    })
    class IdType(str,Enum):
        USER = 'USER'
        GROUP = 'GROUP'
        BOTH = 'BOTH'
        ...
    AeWhoId = typing.TypedDict('AeWhoId', {
            'id_type':'IdType',
            'id':'int',
    })
    class AePerm(str,Enum):
        FULL = 'FULL'
        CHANGE = 'CHANGE'
        READ = 'READ'
        ...
    class AeType(str,Enum):
        ALLOWED = 'ALLOWED'
        DENIED = 'DENIED'
        ...
    Aclentry = typing.TypedDict('Aclentry', {
            'ae_who_sid':'str',
            'ae_who_id':'AeWhoId',
            'ae_perm':'AePerm',
            'ae_type':'AeType',
    })
    SmbShareAcl = typing.TypedDict('SmbShareAcl', {
            'share_name':'str',
            'share_acl':'list[Aclentry]',
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
    SmbShareAcl_ = typing.TypedDict('SmbShareAcl_', {
            'share_name':'str',
            'share_acl':'list[Aclentry]',
    })
    SmbShareAcl__ = typing.TypedDict('SmbShareAcl__', {
            'share_name':'str',
            'share_acl':'list[Aclentry]',
    })
    SharingsmbUpdate = typing.TypedDict('SharingsmbUpdate', {
            'purpose':'Purpose',
            'path':'str',
            'path_suffix':'str',
            'home':'bool',
            'name':'str',
            'comment':'str',
            'ro':'bool',
            'browsable':'bool',
            'timemachine':'bool',
            'timemachine_quota':'int',
            'recyclebin':'bool',
            'guestok':'bool',
            'abe':'bool',
            'hostsallow':'list',
            'hostsdeny':'list',
            'aapl_name_mangling':'bool',
            'acl':'bool',
            'durablehandle':'bool',
            'shadowcopy':'bool',
            'streams':'bool',
            'fsrvp':'bool',
            'auxsmbconf':'str',
            'enabled':'bool',
            'cluster_volname':'str',
            'afp':'bool',
    })
