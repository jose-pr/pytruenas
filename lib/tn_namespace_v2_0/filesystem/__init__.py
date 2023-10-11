
from pytruenas.base import Namespace

import typing
from enum import Enum

class Filesystem(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'filesystem')

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
