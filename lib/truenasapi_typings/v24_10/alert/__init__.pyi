from pytruenas import Namespace as _NS 
class Alert(_NS):
    
    def dismiss(self,
        uuid,
    ) -> AlertDismiss:
        """Dismiss `id` alert."""
        ...
    def list(self,
    ) -> AlertList:
        """List all types of alerts including active/dismissed currently in the system."""
        ...
    def list_categories(self,
    ) -> AlertList_categories:
        """List all types of alerts which the system can issue."""
        ...
    def list_policies(self,
    ) -> AlertList_policies:
        """List all alert policies which indicate the frequency of the alerts."""
        ...
    def restore(self,
        uuid,
    ) -> AlertRestore:
        """Restore `id` alert which had been dismissed."""
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