from pytruenas import Namespace as _NS 
class Alert(_NS):
    
    def dismiss(
        uuid,
    ) -> AlertDismiss:
        """Dismiss `id` alert."""
        ...
    def list(
    ) -> AlertList:
        """List all types of alerts including active/dismissed currently in the system."""
        ...
    def list_categories(
    ) -> AlertList_categories:
        """List all types of alerts which the system can issue."""
        ...
    def list_policies(
    ) -> AlertList_policies:
        """List all alert policies which indicate the frequency of the alerts."""
        ...
    def restore(
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