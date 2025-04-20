from pytruenas import Namespace as _NS

from .image import AppImage

from .ix_volume import AppIx_volume

from .registry import AppRegistry
 
class App(_NS):
    
    def available(
        
    ) -> AppAvailable:
        ...
    
    def available_space(
        
    ) -> AppAvailable_space:
        ...
    
    def categories(
        
    ) -> AppCategories:
        ...
    
    def certificate_authority_choices(
        
    ) -> AppCertificate_authority_choices:
        ...
    
    def certificate_choices(
        
    ) -> AppCertificate_choices:
        ...
    
    def config(
        
    ) -> AppConfig:
        ...
    
    def container_console_choices(
        
    ) -> AppContainer_console_choices:
        ...
    
    def container_ids(
        
    ) -> AppContainer_ids:
        ...
    
    def convert_to_custom(
        
    ) -> AppConvert_to_custom:
        ...
    
    def create(
        
    ) -> AppCreate:
        ...
    
    def delete(
        
    ) -> AppDelete:
        ...
    
    def get_instance(
        
    ) -> AppGet_instance:
        ...
    
    def gpu_choices(
        
    ) -> AppGpu_choices:
        ...
    
    def ip_choices(
        
    ) -> AppIp_choices:
        ...
    
    def latest(
        
    ) -> AppLatest:
        ...
    
    def outdated_docker_images(
        
    ) -> AppOutdated_docker_images:
        ...
    
    def pull_images(
        
    ) -> AppPull_images:
        ...
    
    def query(
        
    ) -> AppQuery:
        ...
    
    def redeploy(
        
    ) -> AppRedeploy:
        ...
    
    def rollback(
        
    ) -> AppRollback:
        ...
    
    def rollback_versions(
        
    ) -> AppRollback_versions:
        ...
    
    def similar(
        
    ) -> AppSimilar:
        ...
    
    def start(
        
    ) -> AppStart:
        ...
    
    def stop(
        
    ) -> AppStop:
        ...
    
    def update(
        
    ) -> AppUpdate:
        ...
    
    def upgrade(
        
    ) -> AppUpgrade:
        ...
    
    def upgrade_summary(
        
    ) -> AppUpgrade_summary:
        ...
    
    def used_ports(
        
    ) -> AppUsed_ports:
        ...
     
    
    image: AppImage
    
    ix_volume: AppIx_volume
    
    registry: AppRegistry
     



class AppAvailable:
    ...

class AppAvailable_space:
    ...

class AppCategories:
    ...

class AppCertificate_authority_choices:
    ...

class AppCertificate_choices:
    ...

class AppConfig:
    ...

class AppContainer_console_choices:
    ...

class AppContainer_ids:
    ...

class AppConvert_to_custom:
    ...

class AppCreate:
    ...

class AppDelete:
    ...

class AppGet_instance:
    ...

class AppGpu_choices:
    ...

class AppIp_choices:
    ...

class AppLatest:
    ...

class AppOutdated_docker_images:
    ...

class AppPull_images:
    ...

class AppQuery:
    ...

class AppRedeploy:
    ...

class AppRollback:
    ...

class AppRollback_versions:
    ...

class AppSimilar:
    ...

class AppStart:
    ...

class AppStop:
    ...

class AppUpdate:
    ...

class AppUpgrade:
    ...

class AppUpgrade_summary:
    ...

class AppUsed_ports:
    ...
 