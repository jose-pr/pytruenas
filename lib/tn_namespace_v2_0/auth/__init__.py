
from pytruenas import Namespace
import typing
class Auth(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'auth')

    CurrentUserInformation = typing.TypedDict('CurrentUserInformation', {
            'pw_name':'str',
            'pw_gecos':'str',
            'pw_dir':'str',
            'pw_shell':'str',
            'pw_uid':'int',
            'pw_gid':'int',
            'grouplist':'list',
            'sid_info':'dict[str]',
            'attributes':'dict[str]',
    })
    QueryOptions = typing.TypedDict('QueryOptions', {
            'relationships':'bool',
            'extend':'typing.Optional[str]',
            'extend_context':'typing.Optional[str]',
            'prefix':'typing.Optional[str]',
            'extra':'dict[str]',
            'order_by':'list',
            'select':'list',
            'count':'bool',
            'get':'bool',
            'offset':'int',
            'limit':'int',
            'force_sql_filters':'bool',
    })
    Session = typing.TypedDict('Session', {
            'id':'str',
            'current':'bool',
            'internal':'bool',
            'origin':'str',
            'credentials':'str',
            'created_at':'str',
    })
