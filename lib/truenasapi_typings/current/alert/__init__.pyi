from pytruenas import Namespace as _NS
 
class Alert(_NS):
    
    def dismiss(
        
    ) -> AlertDismiss:
        ...
    
    def list(
        
    ) -> AlertList:
        ...
    
    def list_categories(
        
    ) -> AlertList_categories:
        ...
    
    def list_policies(
        
    ) -> AlertList_policies:
        ...
    
    def restore(
        
    ) -> AlertRestore:
        ...
     
     



class AlertDismiss:
    ...

class AlertList:
    ...

class AlertList_categories:
    ...

class AlertList_policies:
    ...

class AlertRestore:
    ...
 