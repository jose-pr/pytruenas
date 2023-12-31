
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Filesystem(
    Namespace
    ):
    _namespace:typing.Literal['filesystem']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def acl_is_trivial(self, 
        _path:'str',
    /) -> 'bool': 
        """
        Returns True if the ACL can be fully expressed as a file mode without losing
        any access rules.
        
        Paths on clustered volumes may be specifed with the path prefix
        `CLUSTER:<volume name>`. For example, to list directories
        in the directory 'data' in the clustered volume `smb01`, the
        path should be specified as `CLUSTER:smb01/data`.

        Parameters
        ----------
        path:
            path
        Returns
        -------
        bool:
            paths_acl_is_trivial
        """
        ...
    @typing.overload
    def can_access_as_user(self, 
        _username:'str',
        _path:'str',
        _permissions:'Permissions',
    /) -> 'bool': 
        """
        Check if `username` is able to access `path` with specific `permissions`. At least one of `read/write/execute`
        permission must be specified for checking with each of these defaulting to `null`. `null` for
        `read/write/execute` represents that the permission should not be checked.

        Parameters
        ----------
        username:
            username
        path:
            path
        permissions:
            permissions
        Returns
        -------
        bool:
            can_access_as_user
        """
        ...
    @typing.overload
    def chown(self, 
        _filesystem_ownership:'FilesystemOwnership',
    /) -> None: 
        """
        Change owner or group of file at `path`.
        
        `uid` and `gid` specify new owner of the file. If either
        key is absent or None, then existing value on the file is not
        changed.
        
        `recursive` performs action recursively, but does
        not traverse filesystem mount points.
        
        If `traverse` and `recursive` are specified, then the chown
        operation will traverse filesystem mount points.

        Parameters
        ----------
        filesystem_ownership:
            filesystem_ownership
        Returns
        -------
        """
        ...
    @typing.overload
    def default_acl_choices(self, 
        _path:'str',
    /) -> 'list[str]': 
        """
        `DEPRECATED`
        Returns list of names of ACL templates. Wrapper around
        filesystem.acltemplate.query.

        Parameters
        ----------
        path:
            path
        Returns
        -------
        list[str]:
            acl_choices
        """
        ...
    @typing.overload
    def get(self, 
        _path:'str',
    /) -> None: 
        """
        Job to get contents of `path`.

        Parameters
        ----------
        path:
            path
        Returns
        -------
        """
        ...
    @typing.overload
    def get_default_acl(self, 
        _acl_type:'str',
        _share_type:'ShareType',
    /) -> 'typing.Union[list[Nfs4Ace], list[Posix1eAce]]': 
        """
        `DEPRECATED`
        Returns a default ACL depending on the usage specified by `acl_type`.
        If an admin group is defined, then an entry granting it full control will
        be placed at the top of the ACL. Optionally may pass `share_type` to argument
        to get share-specific template ACL.

        Parameters
        ----------
        acl_type:
            acl_type
        share_type:
            share_type
        Returns
        -------
        typing.Union[list[Nfs4Ace], list[Posix1eAce]]:
            
        """
        ...
    @typing.overload
    def get_dosmode(self, 
        _path:'str',
    /) -> 'Dosmode': 
        """
        

        Parameters
        ----------
        path:
            path
        Returns
        -------
        Dosmode:
            dosmode
        """
        ...
    @typing.overload
    def getacl(self, 
        _path:'str',
        _simplified:'bool',
        _resolve_ids:'bool',
    /) -> 'TruenasAcl': 
        """
        Return ACL of a given path. This may return a POSIX1e ACL or a NFSv4 ACL. The acl type is indicated
        by the `acltype` key.
        
        `simplified` - effect of this depends on ACL type on underlying filesystem. In the case of
        NFSv4 ACLs simplified permissions and flags are returned for ACL entries where applicable.
        NFSv4 errata below. In the case of POSIX1E ACls, this setting has no impact on returned ACL.
        
        `resolve_ids` - adds additional `who` key to each ACL entry, that converts the numeric id to
        a user name or group name. In the case of owner@ and group@ (NFSv4) or USER_OBJ and GROUP_OBJ
        (POSIX1E), st_uid or st_gid will be converted from stat() return for file. In the case of
        MASK (POSIX1E), OTHER (POSIX1E), everyone@ (NFSv4), key `who` will be included, but set to null.
        In case of failure to resolve the id to a name, `who` will be set to null. This option should
        only be used if resolving ids to names is required.
        
        Errata about ACLType NFSv4:
        
        `simplified` returns a shortened form of the ACL permset and flags where applicable. If permissions
        have been simplified, then the `perms` object will contain only a single `BASIC` key with a string
        describing the underlying permissions set.
        
        `TRAVERSE` sufficient rights to traverse a directory, but not read contents.
        
        `READ` sufficient rights to traverse a directory, and read file contents.
        
        `MODIFIY` sufficient rights to traverse, read, write, and modify a file.
        
        `FULL_CONTROL` all permissions.
        
        If the permisssions do not fit within one of the pre-defined simplified permissions types, then
        the full ACL entry will be returned.

        Parameters
        ----------
        path:
            path
        simplified:
            `simplified` - effect of this depends on ACL type on underlying filesystem. In the case of
            NFSv4 ACLs simplified permissions and flags are returned for ACL entries where applicable.
            NFSv4 errata below. In the case of POSIX1E ACls, this setting has no impact on returned ACL.
            `simplified` returns a shortened form of the ACL permset and flags where applicable. If permissions
            have been simplified, then the `perms` object will contain only a single `BASIC` key with a string
            describing the underlying permissions set.
        resolve_ids:
            `resolve_ids` - adds additional `who` key to each ACL entry, that converts the numeric id to
            a user name or group name. In the case of owner@ and group@ (NFSv4) or USER_OBJ and GROUP_OBJ
            (POSIX1E), st_uid or st_gid will be converted from stat() return for file. In the case of
            MASK (POSIX1E), OTHER (POSIX1E), everyone@ (NFSv4), key `who` will be included, but set to null.
            In case of failure to resolve the id to a name, `who` will be set to null. This option should
            only be used if resolving ids to names is required.
        Returns
        -------
        TruenasAcl:
            truenas_acl
        """
        ...
    @typing.overload
    def is_immutable(self, 
        _path:'str',
    /) -> 'bool': 
        """
        Retrieves boolean which is set when immutable flag is set on `path`.

        Parameters
        ----------
        path:
            path
        Returns
        -------
        bool:
            is_immutable
        """
        ...
    @typing.overload
    def listdir(self, 
        _path:'str',
        _query_filters:'list[list]',
        _query_options:'QueryOptions',
    /) -> 'typing.Union[int, PathEntry, list[PathEntry]]': 
        """
        Get the contents of a directory.
        
        Paths on clustered volumes may be specifed with the path prefix
        `CLUSTER:<volume name>`. For example, to list directories
        in the directory 'data' in the clustered volume `smb01`, the
        path should be specified as `CLUSTER:smb01/data`.
        
        Each entry of the list consists of:
          name(str): name of the file
          path(str): absolute path of the entry
          realpath(str): absolute real path of the entry (if SYMLINK)
          type(str): DIRECTORY | FILE | SYMLINK | OTHER
          size(int): size of the entry
          mode(int): file mode/permission
          uid(int): user id of entry owner
          gid(int): group id of entry onwer
          acl(bool): extended ACL is present on file
          is_mountpoint(bool): path is a mountpoint
          is_ctldir(bool): path is within special .zfs directory

        Parameters
        ----------
        path:
            path
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[int, PathEntry, list[PathEntry]]:
            
        """
        ...
    @typing.overload
    def mkdir(self, 
        _path:'str',
    /) -> 'PathEntry': 
        """
        Create a directory at the specified path.

        Parameters
        ----------
        path:
            path
        Returns
        -------
        PathEntry:
            path_entry
        """
        ...
    @typing.overload
    def put(self, 
        _path:'str',
        _options:'Options_',
    /) -> 'bool': 
        """
        Job to put contents to `path`.

        Parameters
        ----------
        path:
            path
        options:
            options
        Returns
        -------
        bool:
            successful_put
        """
        ...
    @typing.overload
    def set_dosmode(self, 
        _set_dosmode:'SetDosmode',
    /) -> None: 
        """
        

        Parameters
        ----------
        set_dosmode:
            set_dosmode
        Returns
        -------
        """
        ...
    @typing.overload
    def set_immutable(self, 
        _set_flag:'bool',
        _path:'str',
    /) -> None: 
        """
        Set/Unset immutable flag at `path`.
        
        `set_flag` when set will set immutable flag and when unset will unset immutable flag at `path`.

        Parameters
        ----------
        set_flag:
            set_flag
        path:
            Set/Unset immutable flag at `path`.
        Returns
        -------
        """
        ...
    @typing.overload
    def setacl(self, 
        _filesystem_acl:'FilesystemAcl',
    /) -> None: 
        """
        Set ACL of a given path. Takes the following parameters:
        `path` full path to directory or file.
        
        Paths on clustered volumes may be specifed with the path prefix
        `CLUSTER:<volume name>`. For example, to list directories
        in the directory 'data' in the clustered volume `smb01`, the
        path should be specified as `CLUSTER:smb01/data`.
        
        `dacl` ACL entries. Formatting depends on the underlying `acltype`. NFS4ACL requires
        NFSv4 entries. POSIX1e requires POSIX1e entries.
        
        `uid` the desired UID of the file user. If set to None (the default), then user is not changed.
        
        `gid` the desired GID of the file group. If set to None (the default), then group is not changed.
        
        `recursive` apply the ACL recursively
        
        `traverse` traverse filestem boundaries (ZFS datasets)
        
        `strip` convert ACL to trivial. ACL is trivial if it can be expressed as a file mode without
        losing any access rules.
        
        `canonicalize` reorder ACL entries so that they are in concanical form as described
        in the Microsoft documentation MS-DTYP 2.4.5 (ACL). This only applies to NFSv4 ACLs.
        
        For case of NFSv4 ACLs  USER_OBJ, GROUP_OBJ, and EVERYONE with owner@, group@, everyone@ for
        consistency with getfacl and setfacl. If one of aforementioned special tags is used, 'id' must
        be set to None.
        
        An inheriting empty everyone@ ACE is appended to non-trivial ACLs in order to enforce Windows
        expectations regarding permissions inheritance. This entry is removed from NT ACL returned
        to SMB clients when 'ixnas' samba VFS module is enabled.

        Parameters
        ----------
        filesystem_acl:
            filesystem_acl
        Returns
        -------
        """
        ...
    @typing.overload
    def setperm(self, 
        _filesystem_permission:'FilesystemPermission',
    /) -> None: 
        """
        Set unix permissions on given `path`.
        
        Paths on clustered volumes may be specifed with the path prefix
        `CLUSTER:<volume name>`. For example, to list directories
        in the directory 'data' in the clustered volume `smb01`, the
        path should be specified as `CLUSTER:smb01/data`.
        
        If `mode` is specified then the mode will be applied to the
        path and files and subdirectories depending on which `options` are
        selected. Mode should be formatted as string representation of octal
        permissions bits.
        
        `uid` the desired UID of the file user. If set to None (the default), then user is not changed.
        
        `gid` the desired GID of the file group. If set to None (the default), then group is not changed.
        
        `stripacl` setperm will fail if an extended ACL is present on `path`,
        unless `stripacl` is set to True.
        
        `recursive` remove ACLs recursively, but do not traverse dataset
        boundaries.
        
        `traverse` remove ACLs from child datasets.
        
        If no `mode` is set, and `stripacl` is True, then non-trivial ACLs
        will be converted to trivial ACLs. An ACL is trivial if it can be
        expressed as a file mode without losing any access rules.

        Parameters
        ----------
        filesystem_permission:
            filesystem_permission
        Returns
        -------
        """
        ...
    @typing.overload
    def stat(self, 
        _path:'str',
    /) -> 'PathStats': 
        """
        Return the filesystem stat(2) for a given `path`.
        
        Paths on clustered volumes may be specifed with the path prefix
        `CLUSTER:<volume name>`. For example, to list directories
        in the directory 'data' in the clustered volume `smb01`, the
        path should be specified as `CLUSTER:smb01/data`.

        Parameters
        ----------
        path:
            Return the filesystem stat(2) for a given `path`.
        Returns
        -------
        PathStats:
            path_stats
        """
        ...
    @typing.overload
    def statfs(self, 
        _path:'str',
    /) -> 'PathStatfs': 
        """
        Return stats from the filesystem of a given path.
        
        Paths on clustered volumes may be specifed with the path prefix
        `CLUSTER:<volume name>`. For example, to list directories
        in the directory 'data' in the clustered volume `smb01`, the
        path should be specified as `CLUSTER:smb01/data`.
        
        Raises:
            CallError(ENOENT) - Path not found

        Parameters
        ----------
        path:
            path
        Returns
        -------
        PathStatfs:
            path_statfs
        """
        ...
    class BASIC(str,Enum):
        FULLCONTROL = 'FULL_CONTROL'
        MODIFY = 'MODIFY'
        READ = 'READ'
        TRAVERSE = 'TRAVERSE'
        ...
    class BASIC_(str,Enum):
        INHERIT = 'INHERIT'
        NOINHERIT = 'NOINHERIT'
        ...
    Dosmode = typing.TypedDict('Dosmode', {
            'readonly':'bool',
            'hidden':'bool',
            'system':'bool',
            'archive':'bool',
            'reparse':'bool',
            'offline':'bool',
            'sparse':'bool',
    })
    FilesystemAcl = typing.TypedDict('FilesystemAcl', {
            'path':'str',
            'uid':'typing.Optional[int]',
            'gid':'typing.Optional[int]',
            'dacl':'typing.Union[list[Nfs4Ace], list[Posix1eAce]]',
            'nfs41_flags':'Nfs41Flags',
            'acltype':'typing.Optional[str]',
            'options':'Options__',
    })
    FilesystemOwnership = typing.TypedDict('FilesystemOwnership', {
            'path':'str',
            'uid':'typing.Optional[int]',
            'gid':'typing.Optional[int]',
            'options':'Options',
    })
    FilesystemPermission = typing.TypedDict('FilesystemPermission', {
            'path':'str',
            'mode':'typing.Optional[str]',
            'uid':'typing.Optional[int]',
            'gid':'typing.Optional[int]',
            'options':'Options___',
    })
    Flags = typing.TypedDict('Flags', {
            'FILE_INHERIT':'bool',
            'DIRECTORY_INHERIT':'bool',
            'NO_PROPAGATE_INHERIT':'bool',
            'INHERIT_ONLY':'bool',
            'INHERITED':'bool',
            'BASIC':'BASIC_',
    })
    Nfs41Flags = typing.TypedDict('Nfs41Flags', {
            'autoinherit':'bool',
            'protected':'bool',
    })
    Nfs4Ace = typing.TypedDict('Nfs4Ace', {
            'tag':'Tag',
            'id':'typing.Optional[int]',
            'type':'Type',
            'perms':'Perms',
            'flags':'Flags',
    })
    Options = typing.TypedDict('Options', {
            'recursive':'bool',
            'traverse':'bool',
    })
    Options_ = typing.TypedDict('Options_', {
            'append':'bool',
            'mode':'int',
    })
    Options__ = typing.TypedDict('Options__', {
            'stripacl':'bool',
            'recursive':'bool',
            'traverse':'bool',
            'canonicalize':'bool',
    })
    Options___ = typing.TypedDict('Options___', {
            'stripacl':'bool',
            'recursive':'bool',
            'traverse':'bool',
    })
    PathEntry = typing.TypedDict('PathEntry', {
            'name':'str',
            'path':'str',
            'realpath':'str',
            'type':'Type_',
            'size':'typing.Optional[int]',
            'mode':'typing.Optional[int]',
            'acl':'typing.Optional[bool]',
            'uid':'typing.Optional[int]',
            'gid':'typing.Optional[int]',
            'is_mountpoint':'bool',
            'is_ctldir':'bool',
    })
    PathStatfs = typing.TypedDict('PathStatfs', {
            'flags':'list',
            'fsid':'list',
            'fstype':'str',
            'source':'str',
            'dest':'str',
            'blocksize':'int',
            'total_blocks':'int',
            'free_blocks':'int',
            'avail_blocks':'int',
            'total_blocks_str':'str',
            'free_blocks_str':'str',
            'avail_blocks_str':'str',
            'files':'int',
            'free_files':'int',
            'name_max':'int',
            'total_bytes':'int',
            'free_bytes':'int',
            'avail_bytes':'int',
            'total_bytes_str':'str',
            'free_bytes_str':'str',
            'avail_bytes_str':'str',
    })
    PathStats = typing.TypedDict('PathStats', {
            'realpath':'str',
            'size':'int',
            'mode':'int',
            'uid':'int',
            'gid':'int',
            'atime':'float',
            'mtime':'float',
            'ctime':'float',
            'btime':'float',
            'dev':'int',
            'inode':'int',
            'nlink':'int',
            'is_mountpoint':'bool',
            'is_ctldir':'bool',
            'user':'typing.Optional[str]',
            'group':'typing.Optional[str]',
            'acl':'bool',
    })
    Permissions = typing.TypedDict('Permissions', {
            'read':'typing.Optional[bool]',
            'write':'typing.Optional[bool]',
            'execute':'typing.Optional[bool]',
    })
    Perms = typing.TypedDict('Perms', {
            'READ_DATA':'bool',
            'WRITE_DATA':'bool',
            'APPEND_DATA':'bool',
            'READ_NAMED_ATTRS':'bool',
            'WRITE_NAMED_ATTRS':'bool',
            'EXECUTE':'bool',
            'DELETE_CHILD':'bool',
            'READ_ATTRIBUTES':'bool',
            'WRITE_ATTRIBUTES':'bool',
            'DELETE':'bool',
            'READ_ACL':'bool',
            'WRITE_ACL':'bool',
            'WRITE_OWNER':'bool',
            'SYNCHRONIZE':'bool',
            'BASIC':'BASIC',
    })
    Perms_ = typing.TypedDict('Perms_', {
            'READ':'bool',
            'WRITE':'bool',
            'EXECUTE':'bool',
    })
    Posix1eAce = typing.TypedDict('Posix1eAce', {
            'default':'bool',
            'tag':'Tag_',
            'id':'int',
            'perms':'Perms_',
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
    SetDosmode = typing.TypedDict('SetDosmode', {
            'path':'str',
            'dosmode':'Dosmode',
    })
    class ShareType(str,Enum):
        NONE = 'NONE'
        SMB = 'SMB'
        NFS = 'NFS'
        ...
    class Tag(str,Enum):
        Owner = 'owner@'
        Group = 'group@'
        Everyone = 'everyone@'
        USER = 'USER'
        GROUP = 'GROUP'
        ...
    class Tag_(str,Enum):
        USEROBJ = 'USER_OBJ'
        GROUPOBJ = 'GROUP_OBJ'
        USER = 'USER'
        GROUP = 'GROUP'
        OTHER = 'OTHER'
        MASK = 'MASK'
        ...
    TruenasAcl = typing.TypedDict('TruenasAcl', {
            'path':'str',
            'trivial':'bool',
            'acltype':'typing.Optional[str]',
            'acl':'typing.Union[list[Nfs4Ace], list[Posix1eAce]]',
    })
    class Type(str,Enum):
        ALLOW = 'ALLOW'
        DENY = 'DENY'
        ...
    class Type_(str,Enum):
        DIRECTORY = 'DIRECTORY'
        FILE = 'FILE'
        SYMLINK = 'SYMLINK'
        OTHER = 'OTHER'
        ...
