from pytruenas import Namespace as _NS

from .acltemplate import FilesystemAcltemplate
 
class Filesystem(_NS):
    
    def chown(
        
    ) -> FilesystemChown:
        ...
    
    def get(
        
    ) -> FilesystemGet:
        ...
    
    def get_zfs_attributes(
        
    ) -> FilesystemGet_zfs_attributes:
        ...
    
    def getacl(
        
    ) -> FilesystemGetacl:
        ...
    
    def listdir(
        
    ) -> FilesystemListdir:
        ...
    
    def mkdir(
        
    ) -> FilesystemMkdir:
        ...
    
    def put(
        
    ) -> FilesystemPut:
        ...
    
    def set_zfs_attributes(
        
    ) -> FilesystemSet_zfs_attributes:
        ...
    
    def setacl(
        
    ) -> FilesystemSetacl:
        ...
    
    def setperm(
        
    ) -> FilesystemSetperm:
        ...
    
    def stat(
        
    ) -> FilesystemStat:
        ...
    
    def statfs(
        
    ) -> FilesystemStatfs:
        ...
     
    
    acltemplate: FilesystemAcltemplate
     



class FilesystemChown:
    ...

class FilesystemGet:
    ...

class FilesystemGet_zfs_attributes:
    ...

class FilesystemGetacl:
    ...

class FilesystemListdir:
    ...

class FilesystemMkdir:
    ...

class FilesystemPut:
    ...

class FilesystemSet_zfs_attributes:
    ...

class FilesystemSetacl:
    ...

class FilesystemSetperm:
    ...

class FilesystemStat:
    ...

class FilesystemStatfs:
    ...
 