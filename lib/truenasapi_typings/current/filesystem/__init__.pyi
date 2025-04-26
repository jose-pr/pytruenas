from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .acltemplate import Acltemplate 
class Filesystem(_NS):
    
    def chown(self,
        filesystem_chown:ChownFilesystemChown,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Change owner or group of file at `path`.

`uid` and `gid` specify new owner of the file. If either key is absent or None, then existing value on the file is not changed.

`user` and `group` alternatively allow specifying a uid gid by user name or group name.

`recursive` performs action recursively, but does not traverse filesystem mount points.

If `traverse` and `recursive` are specified, then the chown operation will traverse filesystem mount points."""
        ...
    def get(self,
        path:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Job to get contents of `path`."""
        ...
    def get_zfs_attributes(self,
        path:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GetZfsAttributesReturn:
        """Get the current ZFS attributes for the file at the given path"""
        ...
    def getacl(self,
        path:str,
        simplified:bool=True,
        resolve_ids:bool=False,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GetaclNFS4ACLResult|GetaclPOSIXACLResult|GetaclDISABLEDACLResult:
        """Return ACL of a given path. This may return a POSIX1e ACL or a NFSv4 ACL. The acl type is indicated by the `acltype` key.

`simplified` - effect of this depends on ACL type on underlying filesystem. In the case of NFSv4 ACLs simplified permissions and flags are returned for ACL entries where applicable. NFSv4 errata below. In the case of POSIX1E ACls, this setting has no impact on returned ACL.

`resolve_ids` - adds additional `who` key to each ACL entry, that converts the numeric id to a user name or group name. In the case of owner@ and group@ (NFSv4) or USER_OBJ and GROUP_OBJ (POSIX1E), st_uid or st_gid will be converted from stat() return for file. In the case of MASK (POSIX1E), OTHER (POSIX1E), everyone@ (NFSv4), key `who` will be included, but set to null. In case of failure to resolve the id to a name, `who` will be set to null. This option should only be used if resolving ids to names is required.

Errata about ACLType NFSv4:

`simplified` returns a shortened form of the ACL permset and flags where applicable. If permissions have been simplified, then the `perms` object will contain only a single `BASIC` key with a string describing the underlying permissions set.

`TRAVERSE` sufficient rights to traverse a directory, but not read contents.

`READ` sufficient rights to traverse a directory, and read file contents.

`MODIFIY` sufficient rights to traverse, read, write, and modify a file.

`FULL_CONTROL` all permissions.

If the permisssions do not fit within one of the pre-defined simplified permissions types, then the full ACL entry will be returned."""
        ...
    def listdir(self,
        path:str,
        query_filters:_jsonschema.JsonArray=[],
        query_options:ListdirQueryOptions={'relationships': True, 'extend': None, 'extend_context': None, 'prefix': None, 'extra': {}, 'order_by': [], 'select': [], 'count': False, 'get': False, 'offset': 0, 'limit': 0, 'force_sql_filters': False},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> list[ListdirFilesystemDirQueryResultItem]|ListdirFilesystemDirQueryResultItem|int:
        """Get the contents of a directory.

The select option may be used to optimize listdir performance. Metadata-related fields that are not selected will not be retrieved from the filesystem.

For example {"select": ["path", "type"]} will avoid querying an xattr list and ZFS attributes for files in a directory.

NOTE: an empty list for select (default) is treated as requesting all information.

Each entry of the list consists of: name(str): name of the file path(str): absolute path of the entry realpath(str): absolute real path of the entry (if SYMLINK) type(str): DIRECTORY | FILE | SYMLINK | OTHER size(int): size of the entry allocation_size(int): on-disk size of entry mode(int): file mode/permission uid(int): user id of entry owner gid(int): group id of entry owner acl(bool): extended ACL is present on file is_mountpoint(bool): path is a mountpoint is_ctldir(bool): path is within special .zfs directory attributes(list): list of statx file attributes that apply to the file. See statx(2) manpage for more details. xattrs(list): list of extended attribute names. zfs_attrs(list): list of ZFS file attributes on file"""
        ...
    def mkdir(self,
        filesystem_mkdir:MkdirFilesystemMkdir,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> MkdirReturn:
        """Create a directory at the specified path.

The following options are supported:

`mode` - specify the permissions to set on the new directory (0o755 is default). `raise_chmod_error` - choose whether to raise an exception if the attempt to set mode fails. In this case, the newly created directory will be removed to prevent use with unintended permissions.

NOTE: if chmod error is skipped, the resulting `mode` key in mkdir response will indicate the current permissions on the directory and not the permissions specified in the mkdir payload"""
        ...
    def put(self,
        path:str,
        options:PutOptions={'append': False, 'mode': None},
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> bool:
        """Job to put contents to `path`."""
        ...
    def set_zfs_attributes(self,
        set_zfs_file_attributes:SetZfsAttributesSetZfsFileAttributes,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SetZfsAttributesReturn:
        """Set special ZFS-related file flags on the specified path

`readonly` - this maps to READONLY MS-DOS attribute. When set, file may not be written to (toggling does not impact existing file opens).

`hidden` - this maps to HIDDEN MS-DOS attribute. When set, the SMB HIDDEN flag is set and file is "hidden" from the perspective of SMB clients.

`system` - this maps to SYSTEM MS-DOS attribute. Is presented to SMB clients, but has no impact on local filesystem.

`archive` - this maps to ARCHIVE MS-DOS attribute. Value is reset to True whenever file is modified.

`immutable` - file may not be altered or deleted. Also appears as IMMUTABLE in attributes in `filesystem.stat` output and as STATX_ATTR_IMMUTABLE in statx() response.

`nounlink` - file may be altered but not deleted.

`appendonly` - file may only be opened with O_APPEND flag. Also appears as APPEND in attributes in `filesystem.stat` output and as STATX_ATTR_APPEND in statx() response.

`offline` - this maps to OFFLINE MS-DOS attribute. Is presented to SMB clients, but has no impact on local filesystem.

`sparse` - maps to SPARSE MS-DOS attribute. Is presented to SMB clients, but has no impact on local filesystem."""
        ...
    def setacl(self,
        filesystem_acl:SetaclFilesystemAcl,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SetaclNFS4ACLResult|SetaclPOSIXACLResult|SetaclDISABLEDACLResult:
        """Set ACL of a given path. Takes the following parameters: `path` full path to directory or file.

`dacl` ACL entries. Formatting depends on the underlying `acltype`. NFS4ACL requires NFSv4 entries. POSIX1e requires POSIX1e entries.

`uid` the desired UID of the file user. If set to None (the default), then user is not changed.

`user` the desired username for the file user. If set to None, then user is not changed.

Note about interaction between `uid` and `user`: One and only one of these parameters should be set, and _only_ if the API consumer wishes to change the owner on the file / directory.

`gid` the desired GID of the file group. If set to None (the default), then group is not changed.

`group` the desired groupname for the file group. If set to None (the default), then group is not changed.

Note about interaction between `gid` and `group`: One and only one of these parameters should be set, and _only_ if the API consumer wishes to change the owner on the file / directory.

WARNING: if user, uid, group, or gid is specified in a recursive operation then the owning user, group, or both for _all_ files will be changed.

`recursive` apply the ACL recursively

`traverse` traverse filestem boundaries (ZFS datasets)

`strip` convert ACL to trivial. ACL is trivial if it can be expressed as a file mode without losing any access rules.

`canonicalize` reorder ACL entries so that they are in concanical form as described in the Microsoft documentation MS-DTYP 2.4.5 (ACL). This only applies to NFSv4 ACLs.

The following notes about ACL entries are necessarily terse. If more detail is requried please consult relevant TrueNAS documentation.

Notes about NFSv4 ACL entry fields:

`tag` refers to the type of principal to whom the ACL entries applies. USER and GROUP have conventional meanings. `owner@` refers to the owning user of the file, `group@` refers to the owning group of the file, and `everyone@` refers to ALL users (including the owning user and group)..

`id` refers to the numeric user id or group id associatiated with USER or GROUP entries.

`who` a user or group name may be specified in lieu of numeric ID for USER or GROUP entries

`type` may be ALLOW or DENY. Deny entries take precedence over allow when the ACL is evaluated.

`perms` permissions allowed or denied by the entry. May be set as a simlified BASIC type or more complex type detailing specific permissions.

`flags` inheritance flags determine how this entry will be presented (if at all) on newly-created files or directories within the specified path. Only valid for directories.

Notes about posix1e ACL entry fields:

`default` the ACL entry is in the posix default ACL (will be copied to new files and directories) created within the directory where it is set. These are _NOT_ evaluated when determining access for the file on which they're set. If default is false then the entry applies to the posix access ACL, which is used to determine access to the directory, but is not inherited on new files / directories.

`tag` the type of principal to whom the ACL entry apples. USER and GROUP have conventional meanings USER_OBJ refers to the owning user of the file and is also denoted by "user" in conventional POSIX UGO permissions. GROUP_OBJ refers to the owning group of the file and is denoted by "group" in the same. OTHER refers to POSIX other, which applies to all users and groups who are not USER_OBJ or GROUP_OBJ. MASK sets maximum permissions granted to all USER and GROUP entries. A valid POSIX1 ACL entry contains precisely one USER_OBJ, GROUP_OBJ, OTHER, and MASK entry for the default and access list.

`id` refers to the numeric user id or group id associatiated with USER or GROUP entries.

`who` a user or group name may be specified in lieu of numeric ID for USER or GROUP entries

`perms` - object containing posix permissions."""
        ...
    def setperm(self,
        filesystem_setperm:SetpermFilesystemSetperm,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> None:
        """Set unix permissions on given `path`.

If `mode` is specified then the mode will be applied to the path and files and subdirectories depending on which `options` are selected. Mode should be formatted as string representation of octal permissions bits.

`uid` the desired UID of the file user. If set to None (the default), then user is not changed.

`gid` the desired GID of the file group. If set to None (the default), then group is not changed.

`user` and `group` alternatively allow specifying the owner by name.

WARNING: `uid`, `gid, `user`, and `group` _should_ remain unset _unless_ the administrator wishes to change the owner or group of files.

`stripacl` setperm will fail if an extended ACL is present on `path`, unless `stripacl` is set to True.

`recursive` remove ACLs recursively, but do not traverse dataset boundaries.

`traverse` remove ACLs from child datasets.

If no `mode` is set, and `stripacl` is True, then non-trivial ACLs will be converted to trivial ACLs. An ACL is trivial if it can be expressed as a file mode without losing any access rules."""
        ...
    def stat(self,
        path:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> StatReturn:
        """Return filesystem information for a given path.

`realpath(str)`: absolute real path of the entry (if SYMLINK)

`type(str)`: DIRECTORY | FILE | SYMLINK | OTHER

`size(int)`: size of the entry

`allocation_size(int)`: on-disk size of entry

`mode(int)`: file mode/permission

`uid(int)`: user id of file owner

`gid(int)`: group id of file owner

`atime(float)`: timestamp for when file was last accessed. NOTE: this timestamp may be changed from userspace.

`mtime(float)`: timestamp for when file data was last modified NOTE: this timestamp may be changed from userspace.

`ctime(float)`: timestamp for when file was last changed.

`btime(float)`: timestamp for when file was initially created. NOTE: depending on platform this may be changed from userspace.

`dev(int)`: device id of the device containing the file. In the context of the TrueNAS API, this is sufficient to uniquely identify a given dataset.

`mount_id(int)`: the mount id for the filesystem underlying the given path. Bind mounts will have same device id, but different mount IDs. This value is sufficient to uniquely identify the particular mount which can be used to identify children of the given mountpoint.

`inode(int)`: inode number of the file. This number uniquely identifies the file on the given device, but once a file is deleted its inode number may be reused.

`nlink(int)`: number of hard lnks to the file.

`acl(bool)`: extended ACL is present on file

`is_mountpoint(bool)`: path is a mountpoint

`is_ctldir(bool)`: path is within special .zfs directory

`attributes(list)`: list of statx file attributes that apply to the file. See statx(2) manpage for more details."""
        ...
    def statfs(self,
        path:str,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> StatfsReturn:
        """Return stats from the filesystem of a given path.

Raises: CallError(ENOENT) - Path not found"""
        ...
    acltemplate: Acltemplate
ChownFilesystemChown = _ty.TypedDict('ChownFilesystemChown', {
    'path': str,
    'uid': _ty.NotRequired[int|None],
    'user': _ty.NotRequired[str|None],
    'gid': _ty.NotRequired[int|None],
    'group': _ty.NotRequired[str|None],
    'options': _ty.NotRequired[_jsonschema.JsonValue], 
})
GetZfsAttributesReturn = _ty.TypedDict('GetZfsAttributesReturn', {
    'readonly': _ty.NotRequired[bool|None],
    'hidden': _ty.NotRequired[bool|None],
    'system': _ty.NotRequired[bool|None],
    'archive': _ty.NotRequired[bool|None],
    'immutable': _ty.NotRequired[bool|None],
    'nounlink': _ty.NotRequired[bool|None],
    'appendonly': _ty.NotRequired[bool|None],
    'offline': _ty.NotRequired[bool|None],
    'sparse': _ty.NotRequired[bool|None], 
})
GetaclNFS4ACLResult = _ty.TypedDict('GetaclNFS4ACLResult', {
    'path': str,
    'user': str|None,
    'group': str|None,
    'uid': int|None,
    'gid': int|None,
    'acltype': str,
    'acl': _jsonschema.JsonArray,
    'aclflags': _jsonschema.JsonValue,
    'trivial': bool, 
})
GetaclPOSIXACLResult = _ty.TypedDict('GetaclPOSIXACLResult', {
    'path': str,
    'user': str|None,
    'group': str|None,
    'uid': int|None,
    'gid': int|None,
    'acltype': str,
    'acl': _jsonschema.JsonArray,
    'trivial': bool, 
})
GetaclDISABLEDACLResult = _ty.TypedDict('GetaclDISABLEDACLResult', {
    'path': str,
    'user': str|None,
    'group': str|None,
    'uid': int|None,
    'gid': int|None,
    'acltype': str,
    'acl': None,
    'trivial': bool, 
})
ListdirQueryOptions = _ty.TypedDict('ListdirQueryOptions', {
    'relationships': _ty.NotRequired[bool],
    'extend': _ty.NotRequired[str|None],
    'extend_context': _ty.NotRequired[str|None],
    'prefix': _ty.NotRequired[str|None],
    'extra': _ty.NotRequired[_jsonschema.JsonObject],
    'order_by': _ty.NotRequired[list[str]],
    'select': _ty.NotRequired[list[str|_jsonschema.JsonArray]],
    'count': _ty.NotRequired[bool],
    'get': _ty.NotRequired[bool],
    'offset': _ty.NotRequired[int],
    'limit': _ty.NotRequired[int],
    'force_sql_filters': _ty.NotRequired[bool], 
})
ListdirFilesystemDirQueryResultItem = _ty.TypedDict('ListdirFilesystemDirQueryResultItem', {
    'name': _ty.NotRequired[str],
    'path': _ty.NotRequired[str],
    'realpath': _ty.NotRequired[str],
    'type': _ty.NotRequired[str],
    'size': _ty.NotRequired[int],
    'allocation_size': _ty.NotRequired[int],
    'mode': _ty.NotRequired[int],
    'mount_id': _ty.NotRequired[int],
    'acl': _ty.NotRequired[bool],
    'uid': _ty.NotRequired[int],
    'gid': _ty.NotRequired[int],
    'is_mountpoint': _ty.NotRequired[bool],
    'is_ctldir': _ty.NotRequired[bool],
    'attributes': _ty.NotRequired[list[str]],
    'xattrs': _ty.NotRequired[list[str]],
    'zfs_attrs': _ty.NotRequired[list[str]|None], 
})
MkdirFilesystemMkdir = _ty.TypedDict('MkdirFilesystemMkdir', {
    'path': str,
    'options': _ty.NotRequired[_jsonschema.JsonValue], 
})
MkdirReturn = _ty.TypedDict('MkdirReturn', {
    'name': str,
    'path': str,
    'realpath': str,
    'type': str,
    'size': int,
    'allocation_size': int,
    'mode': int,
    'mount_id': int,
    'acl': bool,
    'uid': int,
    'gid': int,
    'is_mountpoint': bool,
    'is_ctldir': bool,
    'attributes': list[str],
    'xattrs': list[str],
    'zfs_attrs': list[str]|None, 
})
PutOptions = _ty.TypedDict('PutOptions', {
    'append': _ty.NotRequired[bool],
    'mode': _ty.NotRequired[int|None], 
})
SetZfsAttributesSetZfsFileAttributes = _ty.TypedDict('SetZfsAttributesSetZfsFileAttributes', {
    'path': str,
    'zfs_file_attributes': _jsonschema.JsonValue, 
})
SetZfsAttributesReturn = _ty.TypedDict('SetZfsAttributesReturn', {
    'readonly': _ty.NotRequired[bool|None],
    'hidden': _ty.NotRequired[bool|None],
    'system': _ty.NotRequired[bool|None],
    'archive': _ty.NotRequired[bool|None],
    'immutable': _ty.NotRequired[bool|None],
    'nounlink': _ty.NotRequired[bool|None],
    'appendonly': _ty.NotRequired[bool|None],
    'offline': _ty.NotRequired[bool|None],
    'sparse': _ty.NotRequired[bool|None], 
})
SetaclFilesystemAcl = _ty.TypedDict('SetaclFilesystemAcl', {
    'path': str,
    'dacl': _jsonschema.JsonArray|_jsonschema.JsonArray,
    'options': _ty.NotRequired[_jsonschema.JsonValue],
    'nfs41_flags': _ty.NotRequired[_jsonschema.JsonValue],
    'uid': _ty.NotRequired[int|None],
    'user': _ty.NotRequired[str|None],
    'gid': _ty.NotRequired[int|None],
    'group': _ty.NotRequired[str|None],
    'acltype': _ty.NotRequired[str|None], 
})
SetaclNFS4ACLResult = _ty.TypedDict('SetaclNFS4ACLResult', {
    'path': str,
    'user': str|None,
    'group': str|None,
    'uid': int|None,
    'gid': int|None,
    'acltype': str,
    'acl': _jsonschema.JsonArray,
    'aclflags': _jsonschema.JsonValue,
    'trivial': bool, 
})
SetaclPOSIXACLResult = _ty.TypedDict('SetaclPOSIXACLResult', {
    'path': str,
    'user': str|None,
    'group': str|None,
    'uid': int|None,
    'gid': int|None,
    'acltype': str,
    'acl': _jsonschema.JsonArray,
    'trivial': bool, 
})
SetaclDISABLEDACLResult = _ty.TypedDict('SetaclDISABLEDACLResult', {
    'path': str,
    'user': str|None,
    'group': str|None,
    'uid': int|None,
    'gid': int|None,
    'acltype': str,
    'acl': None,
    'trivial': bool, 
})
SetpermFilesystemSetperm = _ty.TypedDict('SetpermFilesystemSetperm', {
    'path': str,
    'uid': _ty.NotRequired[int|None],
    'user': _ty.NotRequired[str|None],
    'gid': _ty.NotRequired[int|None],
    'group': _ty.NotRequired[str|None],
    'mode': _ty.NotRequired[str|None],
    'options': _ty.NotRequired[_jsonschema.JsonValue], 
})
StatReturn = _ty.TypedDict('StatReturn', {
    'realpath': str,
    'type': str,
    'size': int,
    'allocation_size': int,
    'mode': int,
    'mount_id': int,
    'uid': int,
    'gid': int,
    'atime': _jsonschema.JsonNumber,
    'mtime': _jsonschema.JsonNumber,
    'ctime': _jsonschema.JsonNumber,
    'btime': _jsonschema.JsonNumber,
    'dev': int,
    'inode': int,
    'nlink': int,
    'acl': bool,
    'is_mountpoint': bool,
    'is_ctldir': bool,
    'attributes': list[str],
    'user': str|None,
    'group': str|None, 
})
StatfsReturn = _ty.TypedDict('StatfsReturn', {
    'flags': list[str|_jsonschema.JsonValue],
    'fsid': str,
    'fstype': str|_jsonschema.JsonValue,
    'source': str,
    'dest': str,
    'blocksize': int,
    'total_blocks': int,
    'free_blocks': int,
    'avail_blocks': int,
    'total_blocks_str': str,
    'free_blocks_str': str,
    'avail_blocks_str': str,
    'files': int,
    'free_files': int,
    'name_max': int,
    'total_bytes': int,
    'free_bytes': int,
    'avail_bytes': int,
    'total_bytes_str': str,
    'free_bytes_str': str,
    'avail_bytes_str': str, 
})