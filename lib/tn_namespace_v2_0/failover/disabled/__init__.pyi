
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class FailoverDisabled(Namespace):
    _namespace:_ty.Literal['failover.disabled']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def reasons(self, 
    /) -> 'list': 
        """
        Returns a list of reasons why failover is not enabled/functional.
        
        NO_VOLUME - There are no pools configured.
        NO_VIP - There are no interfaces configured with Virtual IP.
        NO_SYSTEM_READY - Other storage controller has not finished booting.
        NO_PONG - Other storage controller is not communicable.
        NO_FAILOVER - Failover is administratively disabled.
        NO_LICENSE - Other storage controller has no license.
        DISAGREE_VIP - Nodes Virtual IP states do not agree.
        MISMATCH_DISKS - The storage controllers do not have the same quantity of disks.
        MISMATCH_VERSIONS - TrueNAS software versions do not match between storage controllers.
        NO_CRITICAL_INTERFACES - No network interfaces are marked critical for failover.
        NO_FENCED - Zpools are imported but fenced isn't running.
        LOC_FAILOVER_ONGOING - This node is currently processing a failover event.
        REM_FAILOVER_ONGOING - Other node is currently processing a failover event.
        NO_HEARTBEAT_IFACE - Local heartbeat interface does not exist.
        NO_CARRIER_ON_HEARTBEAT - Local heartbeat interface is down.

        Parameters
        ----------
        Returns
        -------
        list:
            reasons
        """
        ...
