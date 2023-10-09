
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class SharingSmb(
    Namespace
    ):
    _namespace:typing.Literal['sharing.smb']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        sharingsmb_create:'SharingsmbCreate'={},
    /) -> 'dict[str]': 
        """
        Create a SMB Share.
        
        `purpose` applies common configuration presets depending on intended purpose.
        
        `path` path to export over the SMB protocol. If server is clustered, then this path will be
        relative to the `cluster_volname`.
        
        `timemachine` when set, enables Time Machine backups for this share.
        
        `ro` when enabled, prohibits write access to the share.
        
        `guestok` when enabled, allows access to this share without a password.
        
        `hostsallow` is a list of hostnames / IP addresses which have access to this share.
        
        `hostsdeny` is a list of hostnames / IP addresses which are not allowed access to this share. If a handful
        of hostnames are to be only allowed access, `hostsdeny` can be passed "ALL" which means that it will deny
        access to ALL hostnames except for the ones which have been listed in `hostsallow`.
        
        `acl` enables support for storing the SMB Security Descriptor as a Filesystem ACL.
        
        `streams` enables support for storing alternate datastreams as filesystem extended attributes.
        
        `fsrvp` enables support for the filesystem remote VSS protocol. This allows clients to create
        ZFS snapshots through RPC.
        
        `shadowcopy` enables support for the volume shadow copy service.
        
        `auxsmbconf` is a string of additional smb4.conf parameters not covered by the system's API.

        Parameters
        ----------
        sharingsmb_create:
            sharingsmb_create
        Returns
        -------
        dict[str]:
            sharing_smb_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete SMB Share of `id`. This will forcibly disconnect SMB clients
        that are accessing the share.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    @typing.overload
    def get_instance(self, 
        id:'typing.Union[str, int, bool, dict[str], list]',
        query_options_get_instance:'QueryOptionsGetInstance'={},
    /) -> None: 
        """
        Returns instance matching `id`. If `id` is not found, Validation error is raised.
        
        Please see `query` method documentation for `options`.

        Parameters
        ----------
        id:
            Returns instance matching `id`. If `id` is not found, Validation error is raised.
        query_options_get_instance:
            query-options-get_instance
        Returns
        -------
        """
        ...
    @typing.overload
    def getacl(self, 
        smb_getacl:'SmbGetacl'={},
    /) -> 'SmbShareAcl': 
        """
        

        Parameters
        ----------
        smb_getacl:
            smb_getacl
        Returns
        -------
        SmbShareAcl:
            smb_share_acl
        """
        ...
    @typing.overload
    def presets(self, 
    /) -> None: 
        """
        Retrieve pre-defined configuration sets for specific use-cases. These parameter
        combinations are often non-obvious, but beneficial in these scenarios.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[list[dict[str]], dict[str], int]': 
        """
        Query shares with filters. In clustered environments, local datastore query
        is bypassed in favor of clustered registry.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[dict[str]], dict[str], int]:
            
        """
        ...
    @typing.overload
    def setacl(self, 
        smb_share_acl:'SmbShareAcl_'={},
    /) -> 'SmbShareAcl__': 
        """
        Set an ACL on `share_name`. This only impacts access through the SMB protocol.
        Either ae_who_sid, ae_who_id must, ae_who_str be specified for each ACL entry in the
        share_acl. If multiple are specified, preference is in the following order: SID,
        unix id, name.
        
        `share_name` the name of the share
        
        `share_acl` a list of ACL entries (dictionaries) with the following keys:
        
        `ae_who_sid` who the ACL entry applies to expressed as a Windows SID
        
        `ae_who_id` Unix ID information for user or group to which the ACL entry applies.
        
        `ae_perm` string representation of the permissions granted to the user or group.
        FULL - grants read, write, execute, delete, write acl, and change owner.
        CHANGE - grants read, write, execute, and delete.
        READ - grants read and execute.
        
        `ae_type` can be ALLOWED or DENIED.

        Parameters
        ----------
        smb_share_acl:
            smb_share_acl
        Returns
        -------
        SmbShareAcl__:
            smb_share_acl
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        sharingsmb_update:'SharingsmbUpdate'={},
    /) -> 'dict[str]': 
        """
        Update SMB Share of `id`.

        Parameters
        ----------
        id:
            Update SMB Share of `id`.
            Create a SMB Share.
        sharingsmb_update:
            sharingsmb_update
        Returns
        -------
        dict[str]:
            sharing_smb_update_returns
        """
        ...
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
