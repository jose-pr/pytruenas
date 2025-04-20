from pytruenas import Namespace as _NS
 
class Catalog(_NS):
    
    def apps(
        
    ) -> CatalogApps:
        ...
    
    def config(
        
    ) -> CatalogConfig:
        ...
    
    def get_app_details(
        
    ) -> CatalogGet_app_details:
        ...
    
    def sync(
        
    ) -> CatalogSync:
        ...
    
    def trains(
        
    ) -> CatalogTrains:
        ...
    
    def update(
        
    ) -> CatalogUpdate:
        ...
     
     



class CatalogApps:
    ...

class CatalogConfig:
    ...

class CatalogGet_app_details:
    ...

class CatalogSync:
    ...

class CatalogTrains:
    ...

class CatalogUpdate:
    ...
 