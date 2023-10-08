
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class FilesystemAcltemplate(Namespace):
    _namespace:_ty.Literal['filesystem.acltemplate']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def by_path(self, 
        acltemplate_by_path:'dict[str]'={},
    /) -> 'list': 
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
        list:
            templates
        """
        ...
    @_ty.overload
    def create(self, 
        acltemplate_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create a new filesystem ACL template.

        Parameters
        ----------
        acltemplate_create:
            acltemplate_create
        Returns
        -------
        dict[str]:
            filesystem_acltemplate_create_returns
        """
        ...
    @_ty.overload
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
    @_ty.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'dict[str]'={},
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
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
    def update(self, 
        id:'int',
        acltemplate_update:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            filesystem_acltemplate_update_returns
        """
        ...
