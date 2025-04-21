from pytruenas import Namespace as _NS 
class Core(_NS):
    
    def ping(
    ) -> CorePing:
        """Utility method which just returns "pong". Can be used to keep connection/authtoken alive instead of using "ping" protocol message."""
        ...
    def set_options(
        options,
    ) -> CoreSet_options:
        """"""
        ...
    def subscribe(
        event,
    ) -> CoreSubscribe:
        """"""
        ...
    def unsubscribe(
        id_,
    ) -> CoreUnsubscribe:
        """"""
        ...
class CorePing:
    ...
class CoreSet_options:
    ...
class CoreSubscribe:
    ...
class CoreUnsubscribe:
    ... 