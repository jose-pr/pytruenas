from pytruenas import Namespace as _NS
import typing as _ty 
class SharingSmb(_NS):
    
    def getacl(self,
        smb_getacl,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SharingSmbGetacl:
        """"""
        ...
    def presets(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SharingSmbPresets:
        """Retrieve pre-defined configuration sets for specific use-cases. These parameter combinations are often non-obvious, but beneficial in these scenarios."""
        ...
    def setacl(self,
        smb_setacl,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SharingSmbSetacl:
        """Set an ACL on `share_name`. This only impacts access through the SMB protocol.

`share_name` the name of the share

`share_acl` a list of ACL entries (dictionaries) with the following keys:

`ae_who_sid` who the ACL entry applies to expressed as a Windows SID

`ae_who_id` Unix ID information for user or group to which the ACL entry applies.

`ae_perm` string representation of the permissions granted to the user or group. FULL - grants read, write, execute, delete, write acl, and change owner. CHANGE - grants read, write, execute, and delete. READ - grants read and execute.

`ae_type` can be ALLOWED or DENIED."""
        ...
class SharingSmbGetacl(_ty.TypedDict):
    ...
class SharingSmbPresets(_ty.TypedDict):
    ...
class SharingSmbSetacl(_ty.TypedDict):
    ... 