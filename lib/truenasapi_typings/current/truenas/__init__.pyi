from pytruenas import Namespace as _NS
 
class Truenas(_NS):
    
    def accept_eula(
        
    ) -> TruenasAccept_eula:
        ...
    
    def get_chassis_hardware(
        
    ) -> TruenasGet_chassis_hardware:
        ...
    
    def get_eula(
        
    ) -> TruenasGet_eula:
        ...
    
    def is_eula_accepted(
        
    ) -> TruenasIs_eula_accepted:
        ...
    
    def is_ix_hardware(
        
    ) -> TruenasIs_ix_hardware:
        ...
    
    def is_production(
        
    ) -> TruenasIs_production:
        ...
    
    def managed_by_truecommand(
        
    ) -> TruenasManaged_by_truecommand:
        ...
    
    def set_production(
        
    ) -> TruenasSet_production:
        ...
     
     



class TruenasAccept_eula:
    ...

class TruenasGet_chassis_hardware:
    ...

class TruenasGet_eula:
    ...

class TruenasIs_eula_accepted:
    ...

class TruenasIs_ix_hardware:
    ...

class TruenasIs_production:
    ...

class TruenasManaged_by_truecommand:
    ...

class TruenasSet_production:
    ...
 