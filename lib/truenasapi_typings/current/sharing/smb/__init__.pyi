from pytruenas import Namespace as _NS 
class SharingSmb(_NS):
    
    def getacl(
        smb_getacl,
    ) -> SharingSmbGetacl:
        """"""
        ...
    def presets(
    ) -> SharingSmbPresets:
        """Retrieve pre-defined configuration sets for specific use-cases. These parameter combinations are often non-obvious, but beneficial in these scenarios."""
        ...
    def setacl(
        smb_setacl,
    ) -> SharingSmbSetacl:
        """Set an ACL on `share_name`. This only impacts access through the SMB protocol.

`share_name` the name of the share

`share_acl` a list of ACL entries (dictionaries) with the following keys:

`ae_who_sid` who the ACL entry applies to expressed as a Windows SID

`ae_who_id` Unix ID information for user or group to which the ACL entry applies.

`ae_perm` string representation of the permissions granted to the user or group. FULL - grants read, write, execute, delete, write acl, and change owner. CHANGE - grants read, write, execute, and delete. READ - grants read and execute.

`ae_type` can be ALLOWED or DENIED."""
        ...
class SharingSmbGetacl:
    ...
class SharingSmbPresets:
    ...
class SharingSmbSetacl:
    ... 