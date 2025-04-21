from pytruenas import Namespace as _NS 
class PoolResilver(_NS):
    
    def config(
    ) -> PoolResilverConfig:
        """"""
        ...
    def update(
        data,
    ) -> PoolResilverUpdate:
        """Configure Pool Resilver Priority.

If `begin` time is greater than `end` time it means it will rollover the day, e.g. begin = "19:00", end = "05:00" will increase pool resilver priority from 19:00 of one day until 05:00 of the next day.

`weekday` follows crontab(5) values 0-7 (0 or 7 is Sun)."""
        ...
class PoolResilverConfig:
    ...
class PoolResilverUpdate:
    ... 