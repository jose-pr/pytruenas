from pytruenas import Namespace as _NS

from .auth import IscsiAuth

from .extent import IscsiExtent

from .global_ import IscsiGlobal

from .initiator import IscsiInitiator

from .portal import IscsiPortal

from .target import IscsiTarget

from .targetextent import IscsiTargetextent
 
class Iscsi(_NS):
     
    
    auth: IscsiAuth
    
    extent: IscsiExtent
    
    global_: IscsiGlobal
    
    initiator: IscsiInitiator
    
    portal: IscsiPortal
    
    target: IscsiTarget
    
    targetextent: IscsiTargetextent
     


 