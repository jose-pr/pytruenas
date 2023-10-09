
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class FilesystemAcltemplate(
    Namespace
    ):
    _namespace:typing.Literal['filesystem.acltemplate']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def by_path(self, 
        acltemplate_by_path:'AcltemplateByPath'={},
    /) -> 'list[AcltemplateEntry]': 
        """
        Retrieve list of available ACL templates for a given `path`.
        
        Supports `query-filters` and `query-options`.
        `format-options` gives additional options to alter the results of
        the template query:
        
        `canonicalize` - place ACL entries for NFSv4 ACLs in Microsoft canonical order.
        `ensure_builtins` - ensure all results contain entries for `builtin_users` and `builtin_administrators`
        groups.
        `resolve_names` - convert ids in ACL entries into names.

        Parameters
        ----------
        acltemplate_by_path:
            acltemplate_by_path
        Returns
        -------
        list[AcltemplateEntry]:
            templates
        """
        ...
    @typing.overload
    def create(self, 
        acltemplate_create:'AcltemplateCreate'={},
    /) -> 'FilesystemAcltemplateCreateReturns': 
        """
        Create a new filesystem ACL template.

        Parameters
        ----------
        acltemplate_create:
            acltemplate_create
        Returns
        -------
        FilesystemAcltemplateCreateReturns:
            filesystem_acltemplate_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        

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
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions_'={},
    /) -> 'typing.Union[list[AcltemplateEntry_], AcltemplateEntry__, int, AcltemplateEntry___]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[AcltemplateEntry_], AcltemplateEntry__, int, AcltemplateEntry___]:
            
        """
        ...
    @typing.overload
    def update(self, 
        id:'int',
        acltemplate_update:'AcltemplateUpdate'={},
    /) -> 'FilesystemAcltemplateUpdateReturns': 
        """
        update filesystem ACL template with `id`.

        Parameters
        ----------
        id:
            id
        acltemplate_update:
            acltemplate_update
        Returns
        -------
        FilesystemAcltemplateUpdateReturns:
            filesystem_acltemplate_update_returns
        """
        ...
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
