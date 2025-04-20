from pytruenas import Namespace as _NS
 
class AppImage(_NS):
    
    def delete(
        
    ) -> AppImageDelete:
        ...
    
    def dockerhub_rate_limit(
        
    ) -> AppImageDockerhub_rate_limit:
        ...
    
    def get_instance(
        
    ) -> AppImageGet_instance:
        ...
    
    def pull(
        
    ) -> AppImagePull:
        ...
    
    def query(
        
    ) -> AppImageQuery:
        ...
     
     



class AppImageDelete:
    ...

class AppImageDockerhub_rate_limit:
    ...

class AppImageGet_instance:
    ...

class AppImagePull:
    ...

class AppImageQuery:
    ...
 