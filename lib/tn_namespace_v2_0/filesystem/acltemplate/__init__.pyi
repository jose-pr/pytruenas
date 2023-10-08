
from pytruenas import Namespace, TrueNASClient
import typing
class FilesystemAcltemplate(Namespace):
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
        id:'str|int|bool|dict[str]|list',
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
        query_options:'QueryOptions'={},
    /) -> 'list[AcltemplateEntry]|AcltemplateEntry|int|AcltemplateEntry': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list[AcltemplateEntry]:
            
        AcltemplateEntry:
            
        int:
            
        AcltemplateEntry:
            
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

class AcltemplateByPath(typing.TypedDict):
        path:'str'
        query-filters:'list[list]'
        query-options:'QueryOptions'
        format-options:'FormatOptions'
        ...
class QueryOptions(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class FormatOptions(typing.TypedDict):
        canonicalize:'bool'
        ensure_builtins:'bool'
        resolve_names:'bool'
        ...
class AcltemplateEntry(typing.TypedDict):
        name:'str'
        acltype:'str'
        comment:'str'
        acl:'typing.Union[list[Nfs4Ace], list[Posix1eAce]]'
        id:'int'
        builtin:'bool'
        ...
class Nfs4Ace(typing.TypedDict):
        tag:'str'
        id:'typing.Optional[int]'
        type:'str'
        perms:'Perms'
        flags:'Flags'
        ...
class Perms(typing.TypedDict):
        READ_DATA:'bool'
        WRITE_DATA:'bool'
        APPEND_DATA:'bool'
        READ_NAMED_ATTRS:'bool'
        WRITE_NAMED_ATTRS:'bool'
        EXECUTE:'bool'
        DELETE_CHILD:'bool'
        READ_ATTRIBUTES:'bool'
        WRITE_ATTRIBUTES:'bool'
        DELETE:'bool'
        READ_ACL:'bool'
        WRITE_ACL:'bool'
        WRITE_OWNER:'bool'
        SYNCHRONIZE:'bool'
        BASIC:'str'
        ...
class Flags(typing.TypedDict):
        FILE_INHERIT:'bool'
        DIRECTORY_INHERIT:'bool'
        NO_PROPAGATE_INHERIT:'bool'
        INHERIT_ONLY:'bool'
        INHERITED:'bool'
        BASIC:'str'
        ...
class Posix1eAce(typing.TypedDict):
        default:'bool'
        tag:'str'
        id:'int'
        perms:'Perms'
        ...
class Perms_(typing.TypedDict):
        READ:'bool'
        WRITE:'bool'
        EXECUTE:'bool'
        ...
class AcltemplateCreate(typing.TypedDict):
        name:'str'
        acltype:'str'
        comment:'str'
        acl:'typing.Union[list[Nfs4Ace], list[Posix1eAce]]'
        ...
class FilesystemAcltemplateCreateReturns(typing.TypedDict):
        name:'str'
        acltype:'str'
        comment:'str'
        acl:'typing.Union[list[Nfs4Ace], list[Posix1eAce]]'
        id:'int'
        builtin:'bool'
        ...
class QueryOptionsGetInstance(typing.TypedDict):
        relationships:'bool'
        extend:'typing.Optional[str]'
        extend_context:'typing.Optional[str]'
        prefix:'typing.Optional[str]'
        extra:'dict[str]'
        order_by:'list'
        select:'list'
        count:'bool'
        get:'bool'
        offset:'int'
        limit:'int'
        force_sql_filters:'bool'
        ...
class AcltemplateUpdate(typing.TypedDict):
        name:'str'
        acltype:'str'
        comment:'str'
        acl:'typing.Union[list[Nfs4Ace], list[Posix1eAce]]'
        ...
class FilesystemAcltemplateUpdateReturns(typing.TypedDict):
        name:'str'
        acltype:'str'
        comment:'str'
        acl:'typing.Union[list[Nfs4Ace], list[Posix1eAce]]'
        id:'int'
        builtin:'bool'
        ...
