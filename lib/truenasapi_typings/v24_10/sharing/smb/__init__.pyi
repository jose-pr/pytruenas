from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty 
class Smb(_NS):
    
    def getacl(self,
        smb_getacl:GetaclSmbGetacl,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> GetaclReturn:
        """"""
        ...
    def presets(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> _jsonschema.JsonObject:
        """Retrieve pre-defined configuration sets for specific use-cases. These parameter combinations are often non-obvious, but beneficial in these scenarios."""
        ...
    def setacl(self,
        smb_setacl:SetaclSmbSetacl,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> SetaclReturn:
        """Set an ACL on `share_name`. This only impacts access through the SMB protocol.

`share_name` the name of the share

`share_acl` a list of ACL entries (dictionaries) with the following keys:

`ae_who_sid` who the ACL entry applies to expressed as a Windows SID

`ae_who_id` Unix ID information for user or group to which the ACL entry applies.

`ae_perm` string representation of the permissions granted to the user or group. FULL - grants read, write, execute, delete, write acl, and change owner. CHANGE - grants read, write, execute, and delete. READ - grants read and execute.

`ae_type` can be ALLOWED or DENIED."""
        ...
GetaclSmbGetacl = _ty.TypedDict('GetaclSmbGetacl', {
    'share_name': str, 
})
GetaclReturn = _ty.TypedDict('GetaclReturn', {
    'share_name': str,
    'share_acl': _ty.NotRequired[_jsonschema.JsonArray], 
})
SetaclSmbSetacl = _ty.TypedDict('SetaclSmbSetacl', {
    'share_name': str,
    'share_acl': _ty.NotRequired[_jsonschema.JsonArray], 
})
SetaclReturn = _ty.TypedDict('SetaclReturn', {
    'share_name': str,
    'share_acl': _ty.NotRequired[_jsonschema.JsonArray], 
})