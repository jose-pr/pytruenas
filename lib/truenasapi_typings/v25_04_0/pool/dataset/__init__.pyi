from pytruenas import Namespace as _NS 
class PoolDataset(_NS):
    
    def details(
    ) -> PoolDatasetDetails:
        """Retrieve all dataset(s) details outlining any services/tasks which might be consuming them."""
        ...
    def snapshot_count(
        dataset,
    ) -> PoolDatasetSnapshot_count:
        """Returns snapshot count for specified `dataset`."""
        ...
class PoolDatasetDetails:
    ...
class PoolDatasetSnapshot_count:
    ... 