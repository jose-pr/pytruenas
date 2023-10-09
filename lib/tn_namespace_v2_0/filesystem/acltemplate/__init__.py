
from pytruenas import Namespace
import typing
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
            'BASIC':'str',
    })
    Flags = typing.TypedDict('Flags', {
            'FILE_INHERIT':'bool',
            'DIRECTORY_INHERIT':'bool',
            'NO_PROPAGATE_INHERIT':'bool',
            'INHERIT_ONLY':'bool',
            'INHERITED':'bool',
            'BASIC':'str',
    })
    Nfs4Ace = typing.TypedDict('Nfs4Ace', {
            'tag':'str',
            'id':'typing.Optional[int]',
            'type':'str',
            'perms':'Perms',
            'flags':'Flags',
    })
    Perms_ = typing.TypedDict('Perms_', {
            'READ':'bool',
            'WRITE':'bool',
            'EXECUTE':'bool',
    })
    Posix1eAce = typing.TypedDict('Posix1eAce', {
            'default':'bool',
            'tag':'str',
            'id':'int',
            'perms':'Perms_',
    })
    AcltemplateEntry = typing.TypedDict('AcltemplateEntry', {
            'name':'str',
            'acltype':'str',
            'comment':'str',
            'acl':'typing.Union[list[Nfs4Ace], list[Posix1eAce]]',
            'id':'int',
            'builtin':'bool',
    })
    Perms__ = typing.TypedDict('Perms__', {
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
            'BASIC':'str',
    })
    Flags_ = typing.TypedDict('Flags_', {
            'FILE_INHERIT':'bool',
            'DIRECTORY_INHERIT':'bool',
            'NO_PROPAGATE_INHERIT':'bool',
            'INHERIT_ONLY':'bool',
            'INHERITED':'bool',
            'BASIC':'str',
    })
    Nfs4Ace_ = typing.TypedDict('Nfs4Ace_', {
            'tag':'str',
            'id':'typing.Optional[int]',
            'type':'str',
            'perms':'Perms__',
            'flags':'Flags_',
    })
    Perms___ = typing.TypedDict('Perms___', {
            'READ':'bool',
            'WRITE':'bool',
            'EXECUTE':'bool',
    })
    Posix1eAce_ = typing.TypedDict('Posix1eAce_', {
            'default':'bool',
            'tag':'str',
            'id':'int',
            'perms':'Perms___',
    })
    AcltemplateCreate = typing.TypedDict('AcltemplateCreate', {
            'name':'str',
            'acltype':'str',
            'comment':'str',
            'acl':'typing.Union[list[Nfs4Ace_], list[Posix1eAce_]]',
    })
    Perms____ = typing.TypedDict('Perms____', {
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
            'BASIC':'str',
    })
    Flags__ = typing.TypedDict('Flags__', {
            'FILE_INHERIT':'bool',
            'DIRECTORY_INHERIT':'bool',
            'NO_PROPAGATE_INHERIT':'bool',
            'INHERIT_ONLY':'bool',
            'INHERITED':'bool',
            'BASIC':'str',
    })
    Nfs4Ace__ = typing.TypedDict('Nfs4Ace__', {
            'tag':'str',
            'id':'typing.Optional[int]',
            'type':'str',
            'perms':'Perms____',
            'flags':'Flags__',
    })
    Perms_____ = typing.TypedDict('Perms_____', {
            'READ':'bool',
            'WRITE':'bool',
            'EXECUTE':'bool',
    })
    Posix1eAce__ = typing.TypedDict('Posix1eAce__', {
            'default':'bool',
            'tag':'str',
            'id':'int',
            'perms':'Perms_____',
    })
    FilesystemAcltemplateCreateReturns = typing.TypedDict('FilesystemAcltemplateCreateReturns', {
            'name':'str',
            'acltype':'str',
            'comment':'str',
            'acl':'typing.Union[list[Nfs4Ace__], list[Posix1eAce__]]',
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
    Perms______ = typing.TypedDict('Perms______', {
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
            'BASIC':'str',
    })
    Flags___ = typing.TypedDict('Flags___', {
            'FILE_INHERIT':'bool',
            'DIRECTORY_INHERIT':'bool',
            'NO_PROPAGATE_INHERIT':'bool',
            'INHERIT_ONLY':'bool',
            'INHERITED':'bool',
            'BASIC':'str',
    })
    Nfs4Ace___ = typing.TypedDict('Nfs4Ace___', {
            'tag':'str',
            'id':'typing.Optional[int]',
            'type':'str',
            'perms':'Perms______',
            'flags':'Flags___',
    })
    Perms_______ = typing.TypedDict('Perms_______', {
            'READ':'bool',
            'WRITE':'bool',
            'EXECUTE':'bool',
    })
    Posix1eAce___ = typing.TypedDict('Posix1eAce___', {
            'default':'bool',
            'tag':'str',
            'id':'int',
            'perms':'Perms_______',
    })
    AcltemplateEntry_ = typing.TypedDict('AcltemplateEntry_', {
            'name':'str',
            'acltype':'str',
            'comment':'str',
            'acl':'typing.Union[list[Nfs4Ace___], list[Posix1eAce___]]',
            'id':'int',
            'builtin':'bool',
    })
    Perms________ = typing.TypedDict('Perms________', {
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
            'BASIC':'str',
    })
    Flags____ = typing.TypedDict('Flags____', {
            'FILE_INHERIT':'bool',
            'DIRECTORY_INHERIT':'bool',
            'NO_PROPAGATE_INHERIT':'bool',
            'INHERIT_ONLY':'bool',
            'INHERITED':'bool',
            'BASIC':'str',
    })
    Nfs4Ace____ = typing.TypedDict('Nfs4Ace____', {
            'tag':'str',
            'id':'typing.Optional[int]',
            'type':'str',
            'perms':'Perms________',
            'flags':'Flags____',
    })
    Perms_________ = typing.TypedDict('Perms_________', {
            'READ':'bool',
            'WRITE':'bool',
            'EXECUTE':'bool',
    })
    Posix1eAce____ = typing.TypedDict('Posix1eAce____', {
            'default':'bool',
            'tag':'str',
            'id':'int',
            'perms':'Perms_________',
    })
    AcltemplateEntry__ = typing.TypedDict('AcltemplateEntry__', {
            'name':'str',
            'acltype':'str',
            'comment':'str',
            'acl':'typing.Union[list[Nfs4Ace____], list[Posix1eAce____]]',
            'id':'int',
            'builtin':'bool',
    })
    Perms__________ = typing.TypedDict('Perms__________', {
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
            'BASIC':'str',
    })
    Flags_____ = typing.TypedDict('Flags_____', {
            'FILE_INHERIT':'bool',
            'DIRECTORY_INHERIT':'bool',
            'NO_PROPAGATE_INHERIT':'bool',
            'INHERIT_ONLY':'bool',
            'INHERITED':'bool',
            'BASIC':'str',
    })
    Nfs4Ace_____ = typing.TypedDict('Nfs4Ace_____', {
            'tag':'str',
            'id':'typing.Optional[int]',
            'type':'str',
            'perms':'Perms__________',
            'flags':'Flags_____',
    })
    Perms___________ = typing.TypedDict('Perms___________', {
            'READ':'bool',
            'WRITE':'bool',
            'EXECUTE':'bool',
    })
    Posix1eAce_____ = typing.TypedDict('Posix1eAce_____', {
            'default':'bool',
            'tag':'str',
            'id':'int',
            'perms':'Perms___________',
    })
    AcltemplateEntry___ = typing.TypedDict('AcltemplateEntry___', {
            'name':'str',
            'acltype':'str',
            'comment':'str',
            'acl':'typing.Union[list[Nfs4Ace_____], list[Posix1eAce_____]]',
            'id':'int',
            'builtin':'bool',
    })
    Perms____________ = typing.TypedDict('Perms____________', {
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
            'BASIC':'str',
    })
    Flags______ = typing.TypedDict('Flags______', {
            'FILE_INHERIT':'bool',
            'DIRECTORY_INHERIT':'bool',
            'NO_PROPAGATE_INHERIT':'bool',
            'INHERIT_ONLY':'bool',
            'INHERITED':'bool',
            'BASIC':'str',
    })
    Nfs4Ace______ = typing.TypedDict('Nfs4Ace______', {
            'tag':'str',
            'id':'typing.Optional[int]',
            'type':'str',
            'perms':'Perms____________',
            'flags':'Flags______',
    })
    Perms_____________ = typing.TypedDict('Perms_____________', {
            'READ':'bool',
            'WRITE':'bool',
            'EXECUTE':'bool',
    })
    Posix1eAce______ = typing.TypedDict('Posix1eAce______', {
            'default':'bool',
            'tag':'str',
            'id':'int',
            'perms':'Perms_____________',
    })
    AcltemplateUpdate = typing.TypedDict('AcltemplateUpdate', {
            'name':'str',
            'acltype':'str',
            'comment':'str',
            'acl':'typing.Union[list[Nfs4Ace______], list[Posix1eAce______]]',
    })
    Perms______________ = typing.TypedDict('Perms______________', {
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
            'BASIC':'str',
    })
    Flags_______ = typing.TypedDict('Flags_______', {
            'FILE_INHERIT':'bool',
            'DIRECTORY_INHERIT':'bool',
            'NO_PROPAGATE_INHERIT':'bool',
            'INHERIT_ONLY':'bool',
            'INHERITED':'bool',
            'BASIC':'str',
    })
    Nfs4Ace_______ = typing.TypedDict('Nfs4Ace_______', {
            'tag':'str',
            'id':'typing.Optional[int]',
            'type':'str',
            'perms':'Perms______________',
            'flags':'Flags_______',
    })
    Perms_______________ = typing.TypedDict('Perms_______________', {
            'READ':'bool',
            'WRITE':'bool',
            'EXECUTE':'bool',
    })
    Posix1eAce_______ = typing.TypedDict('Posix1eAce_______', {
            'default':'bool',
            'tag':'str',
            'id':'int',
            'perms':'Perms_______________',
    })
    FilesystemAcltemplateUpdateReturns = typing.TypedDict('FilesystemAcltemplateUpdateReturns', {
            'name':'str',
            'acltype':'str',
            'comment':'str',
            'acl':'typing.Union[list[Nfs4Ace_______], list[Posix1eAce_______]]',
            'id':'int',
            'builtin':'bool',
    })
