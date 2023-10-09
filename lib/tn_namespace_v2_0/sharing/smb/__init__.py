
from pytruenas import Namespace
import typing
class SharingSmb(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'sharing.smb')

    SharingsmbCreate = typing.TypedDict('SharingsmbCreate', {
            'purpose':'str',
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
    AeWhoId = typing.TypedDict('AeWhoId', {
            'id_type':'str',
            'id':'int',
    })
    Aclentry = typing.TypedDict('Aclentry', {
            'ae_who_sid':'str',
            'ae_who_id':'AeWhoId',
            'ae_perm':'str',
            'ae_type':'str',
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
    AeWhoId_ = typing.TypedDict('AeWhoId_', {
            'id_type':'str',
            'id':'int',
    })
    Aclentry_ = typing.TypedDict('Aclentry_', {
            'ae_who_sid':'str',
            'ae_who_id':'AeWhoId_',
            'ae_perm':'str',
            'ae_type':'str',
    })
    SmbShareAcl_ = typing.TypedDict('SmbShareAcl_', {
            'share_name':'str',
            'share_acl':'list[Aclentry_]',
    })
    AeWhoId__ = typing.TypedDict('AeWhoId__', {
            'id_type':'str',
            'id':'int',
    })
    Aclentry__ = typing.TypedDict('Aclentry__', {
            'ae_who_sid':'str',
            'ae_who_id':'AeWhoId__',
            'ae_perm':'str',
            'ae_type':'str',
    })
    SmbShareAcl__ = typing.TypedDict('SmbShareAcl__', {
            'share_name':'str',
            'share_acl':'list[Aclentry__]',
    })
    SharingsmbUpdate = typing.TypedDict('SharingsmbUpdate', {
            'purpose':'str',
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
