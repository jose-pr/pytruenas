
from pytruenas.base import Namespace

import typing
from enum import Enum

class FilesystemAcltemplate(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'filesystem.acltemplate')

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
    FormatOptions = typing.TypedDict('FormatOptions', {
            'canonicalize':'bool',
            'ensure_builtins':'bool',
            'resolve_names':'bool',
    })
    AcltemplateByPath = typing.TypedDict('AcltemplateByPath', {
            'path':'str',
            'query-filters':'list[list]',
            'query-options':'QueryOptions',
            'format-options':'FormatOptions',
    })
    class Acltype(str,Enum):
        NFS4 = 'NFS4'
        POSIX1E = 'POSIX1E'
        ...
    class Tag(str,Enum):
        Owner = 'owner@'
        Group = 'group@'
        Everyone = 'everyone@'
        USER = 'USER'
        GROUP = 'GROUP'
        ...
    class Type(str,Enum):
        ALLOW = 'ALLOW'
        DENY = 'DENY'
        ...
    class BASIC(str,Enum):
        FULLCONTROL = 'FULL_CONTROL'
        MODIFY = 'MODIFY'
        READ = 'READ'
        TRAVERSE = 'TRAVERSE'
        ...
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
    class BASIC_(str,Enum):
        INHERIT = 'INHERIT'
        NOINHERIT = 'NOINHERIT'
        ...
    Flags = typing.TypedDict('Flags', {
            'FILE_INHERIT':'bool',
            'DIRECTORY_INHERIT':'bool',
            'NO_PROPAGATE_INHERIT':'bool',
            'INHERIT_ONLY':'bool',
            'INHERITED':'bool',
            'BASIC':'BASIC_',
    })
    Nfs4Ace = typing.TypedDict('Nfs4Ace', {
            'tag':'Tag',
            'id':'typing.Optional[int]',
            'type':'Type',
            'perms':'Perms',
            'flags':'Flags',
    })
    class Tag_(str,Enum):
        USEROBJ = 'USER_OBJ'
        GROUPOBJ = 'GROUP_OBJ'
        USER = 'USER'
        GROUP = 'GROUP'
        OTHER = 'OTHER'
        MASK = 'MASK'
        ...
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
    AcltemplateEntry = typing.TypedDict('AcltemplateEntry', {
            'name':'str',
            'acltype':'Acltype',
            'comment':'str',
            'acl':'typing.Union[list[Nfs4Ace], list[Posix1eAce]]',
            'id':'int',
            'builtin':'bool',
    })
    Nfs4Ace_ = typing.TypedDict('Nfs4Ace_', {
            'tag':'Tag',
            'id':'typing.Optional[int]',
            'type':'Type',
            'perms':'Perms',
            'flags':'Flags',
    })
    AcltemplateCreate = typing.TypedDict('AcltemplateCreate', {
            'name':'str',
            'acltype':'Acltype',
            'comment':'str',
            'acl':'typing.Union[list[Nfs4Ace_], list[Posix1eAce]]',
    })
    Nfs4Ace__ = typing.TypedDict('Nfs4Ace__', {
            'tag':'Tag',
            'id':'typing.Optional[int]',
            'type':'Type',
            'perms':'Perms',
            'flags':'Flags',
    })
    FilesystemAcltemplateCreateReturns = typing.TypedDict('FilesystemAcltemplateCreateReturns', {
            'name':'str',
            'acltype':'Acltype',
            'comment':'str',
            'acl':'typing.Union[list[Nfs4Ace__], list[Posix1eAce]]',
            'id':'int',
            'builtin':'bool',
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
    QueryOptions_ = typing.TypedDict('QueryOptions_', {
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
    Nfs4Ace___ = typing.TypedDict('Nfs4Ace___', {
            'tag':'Tag',
            'id':'typing.Optional[int]',
            'type':'Type',
            'perms':'Perms',
            'flags':'Flags',
    })
    AcltemplateEntry_ = typing.TypedDict('AcltemplateEntry_', {
            'name':'str',
            'acltype':'Acltype',
            'comment':'str',
            'acl':'typing.Union[list[Nfs4Ace___], list[Posix1eAce]]',
            'id':'int',
            'builtin':'bool',
    })
    Nfs4Ace____ = typing.TypedDict('Nfs4Ace____', {
            'tag':'Tag',
            'id':'typing.Optional[int]',
            'type':'Type',
            'perms':'Perms',
            'flags':'Flags',
    })
    AcltemplateEntry__ = typing.TypedDict('AcltemplateEntry__', {
            'name':'str',
            'acltype':'Acltype',
            'comment':'str',
            'acl':'typing.Union[list[Nfs4Ace____], list[Posix1eAce]]',
            'id':'int',
            'builtin':'bool',
    })
    Nfs4Ace_____ = typing.TypedDict('Nfs4Ace_____', {
            'tag':'Tag',
            'id':'typing.Optional[int]',
            'type':'Type',
            'perms':'Perms',
            'flags':'Flags',
    })
    AcltemplateEntry___ = typing.TypedDict('AcltemplateEntry___', {
            'name':'str',
            'acltype':'Acltype',
            'comment':'str',
            'acl':'typing.Union[list[Nfs4Ace_____], list[Posix1eAce]]',
            'id':'int',
            'builtin':'bool',
    })
    Nfs4Ace______ = typing.TypedDict('Nfs4Ace______', {
            'tag':'Tag',
            'id':'typing.Optional[int]',
            'type':'Type',
            'perms':'Perms',
            'flags':'Flags',
    })
    AcltemplateUpdate = typing.TypedDict('AcltemplateUpdate', {
            'name':'str',
            'acltype':'Acltype',
            'comment':'str',
            'acl':'typing.Union[list[Nfs4Ace______], list[Posix1eAce]]',
    })
    Nfs4Ace_______ = typing.TypedDict('Nfs4Ace_______', {
            'tag':'Tag',
            'id':'typing.Optional[int]',
            'type':'Type',
            'perms':'Perms',
            'flags':'Flags',
    })
    FilesystemAcltemplateUpdateReturns = typing.TypedDict('FilesystemAcltemplateUpdateReturns', {
            'name':'str',
            'acltype':'Acltype',
            'comment':'str',
            'acl':'typing.Union[list[Nfs4Ace_______], list[Posix1eAce]]',
            'id':'int',
            'builtin':'bool',
    })
