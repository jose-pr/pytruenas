from pytruenas import Namespace as _NS 
class FilesystemAcltemplate(_NS):
    
    def by_path(self,
        filesystem_acl,
    ) -> FilesystemAcltemplateBy_path:
        """Retrieve list of available ACL templates for a given `path`.

Supports `query-filters` and `query-options`. `format-options` gives additional options to alter the results of the template query:

`canonicalize` - place ACL entries for NFSv4 ACLs in Microsoft canonical order. `ensure_builtins` - ensure all results contain entries for `builtin_users` and `builtin_administrators` groups. `resolve_names` - convert ids in ACL entries into names."""
        ...
    def create(self,
        acltemplate_create,
    ) -> FilesystemAcltemplateCreate:
        """Create a new filesystem ACL template."""
        ...
    def delete(self,
        id,
    ) -> FilesystemAcltemplateDelete:
        """"""
        ...
    def get_instance(self,
        id,
        options,
    ) -> FilesystemAcltemplateGet_instance:
        """Returns instance matching `id`. If `id` is not found, Validation error is raised.

Please see `query` method documentation for `options`."""
        ...
    def query(self,
        filters,
        options,
    ) -> FilesystemAcltemplateQuery:
        """"""
        ...
    def update(self,
        id,
        acltemplate_update,
    ) -> FilesystemAcltemplateUpdate:
        """update filesystem ACL template with `id`."""
        ...
class FilesystemAcltemplateBy_path:
    ...
class FilesystemAcltemplateCreate:
    ...
class FilesystemAcltemplateDelete:
    ...
class FilesystemAcltemplateGet_instance:
    ...
class FilesystemAcltemplateQuery:
    ...
class FilesystemAcltemplateUpdate:
    ... 