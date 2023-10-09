
from pytruenas import Namespace, TrueNASClient
import typing
class IscsiTarget(Namespace):
    _namespace:typing.Literal['iscsi.target']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def create(self, 
        iscsi_target_create:'IscsiTargetCreate'={},
    /) -> 'dict[str]': 
        """
        Create an iSCSI Target.
        
        `groups` is a list of group dictionaries which provide information related to using a `portal`, `initiator`,
        `authmethod` and `auth` with this target. `auth` represents a valid iSCSI Authorized Access and defaults to
        null.
        
        `auth_networks` is a list of IP/CIDR addresses which are allowed to use this initiator. If all networks are
        to be allowed, this field should be left empty.

        Parameters
        ----------
        iscsi_target_create:
            iscsi_target_create
        Returns
        -------
        dict[str]:
            iscsi_target_create_returns
        """
        ...
    Group = typing.TypedDict('Group', {
            'portal':'int',
            'initiator':'typing.Optional[int]',
            'authmethod':'str',
            'auth':'typing.Optional[int]',
    })
    IscsiTargetCreate = typing.TypedDict('IscsiTargetCreate', {
            'name':'str',
            'alias':'typing.Optional[str]',
            'mode':'str',
            'groups':'list[Group]',
            'auth_networks':'list[str]',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
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
    Group_ = typing.TypedDict('Group_', {
            'portal':'int',
            'initiator':'typing.Optional[int]',
            'authmethod':'str',
            'auth':'typing.Optional[int]',
    })
    IscsiTargetUpdate = typing.TypedDict('IscsiTargetUpdate', {
            'name':'str',
            'alias':'typing.Optional[str]',
            'mode':'str',
            'groups':'list[Group_]',
            'auth_networks':'list[str]',
    })
    @typing.overload
    def delete(self, 
        id:'int',
        force:'bool'=False,
    /) -> 'bool': 
        """
        Delete iSCSI Target of `id`.
        
        Deleting an iSCSI Target makes sure we delete all Associated Targets which use `id` iSCSI Target.

        Parameters
        ----------
        id:
            Delete iSCSI Target of `id`.
        force:
            force
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    Group = typing.TypedDict('Group', {
            'portal':'int',
            'initiator':'typing.Optional[int]',
            'authmethod':'str',
            'auth':'typing.Optional[int]',
    })
    IscsiTargetCreate = typing.TypedDict('IscsiTargetCreate', {
            'name':'str',
            'alias':'typing.Optional[str]',
            'mode':'str',
            'groups':'list[Group]',
            'auth_networks':'list[str]',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
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
    Group_ = typing.TypedDict('Group_', {
            'portal':'int',
            'initiator':'typing.Optional[int]',
            'authmethod':'str',
            'auth':'typing.Optional[int]',
    })
    IscsiTargetUpdate = typing.TypedDict('IscsiTargetUpdate', {
            'name':'str',
            'alias':'typing.Optional[str]',
            'mode':'str',
            'groups':'list[Group_]',
            'auth_networks':'list[str]',
    })
    @typing.overload
    def get_instance(self, 
        id:'typing.Union[str, int, bool, dict[str], list]',
        query_options_get_instance:'QueryOptionsGetInstance'={},
    /) -> None: 
        """
        Returns instance matching `id`. If `id` is not found, Validation error is raised.
        
        Please see `query` method documentation for `options`.

        Parameters
        ----------
        id:
            Returns instance matching `id`. If `id` is not found, Validation error is raised.
        query_options_get_instance:
            query-options-get_instance
        Returns
        -------
        """
        ...
    Group = typing.TypedDict('Group', {
            'portal':'int',
            'initiator':'typing.Optional[int]',
            'authmethod':'str',
            'auth':'typing.Optional[int]',
    })
    IscsiTargetCreate = typing.TypedDict('IscsiTargetCreate', {
            'name':'str',
            'alias':'typing.Optional[str]',
            'mode':'str',
            'groups':'list[Group]',
            'auth_networks':'list[str]',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
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
    Group_ = typing.TypedDict('Group_', {
            'portal':'int',
            'initiator':'typing.Optional[int]',
            'authmethod':'str',
            'auth':'typing.Optional[int]',
    })
    IscsiTargetUpdate = typing.TypedDict('IscsiTargetUpdate', {
            'name':'str',
            'alias':'typing.Optional[str]',
            'mode':'str',
            'groups':'list[Group_]',
            'auth_networks':'list[str]',
    })
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[list[dict[str]], dict[str], int]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[dict[str]], dict[str], int]:
            
        """
        ...
    Group = typing.TypedDict('Group', {
            'portal':'int',
            'initiator':'typing.Optional[int]',
            'authmethod':'str',
            'auth':'typing.Optional[int]',
    })
    IscsiTargetCreate = typing.TypedDict('IscsiTargetCreate', {
            'name':'str',
            'alias':'typing.Optional[str]',
            'mode':'str',
            'groups':'list[Group]',
            'auth_networks':'list[str]',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
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
    Group_ = typing.TypedDict('Group_', {
            'portal':'int',
            'initiator':'typing.Optional[int]',
            'authmethod':'str',
            'auth':'typing.Optional[int]',
    })
    IscsiTargetUpdate = typing.TypedDict('IscsiTargetUpdate', {
            'name':'str',
            'alias':'typing.Optional[str]',
            'mode':'str',
            'groups':'list[Group_]',
            'auth_networks':'list[str]',
    })
    @typing.overload
    def update(self, 
        id:'int',
        iscsi_target_update:'IscsiTargetUpdate'={},
    /) -> 'dict[str]': 
        """
        Update iSCSI Target of `id`.

        Parameters
        ----------
        id:
            Update iSCSI Target of `id`.
            Create an iSCSI Target.
        iscsi_target_update:
            iscsi_target_update
        Returns
        -------
        dict[str]:
            iscsi_target_update_returns
        """
        ...
    Group = typing.TypedDict('Group', {
            'portal':'int',
            'initiator':'typing.Optional[int]',
            'authmethod':'str',
            'auth':'typing.Optional[int]',
    })
    IscsiTargetCreate = typing.TypedDict('IscsiTargetCreate', {
            'name':'str',
            'alias':'typing.Optional[str]',
            'mode':'str',
            'groups':'list[Group]',
            'auth_networks':'list[str]',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
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
    Group_ = typing.TypedDict('Group_', {
            'portal':'int',
            'initiator':'typing.Optional[int]',
            'authmethod':'str',
            'auth':'typing.Optional[int]',
    })
    IscsiTargetUpdate = typing.TypedDict('IscsiTargetUpdate', {
            'name':'str',
            'alias':'typing.Optional[str]',
            'mode':'str',
            'groups':'list[Group_]',
            'auth_networks':'list[str]',
    })
    @typing.overload
    def validate_name(self, 
        name:'str',
        existing_id:'typing.Optional[int]'=None,
    /) -> None: 
        """
        Returns validation error for iSCSI target name
        :param name: name to be validated
        :param existing_id: id of an existing iSCSI target that will receive this name (or `None` if a new target
                            is being created)
        :return: error message (or `None` if there is no error)

        Parameters
        ----------
        name:
            name
        existing_id:
            existing_id
        Returns
        -------
        """
        ...
    Group = typing.TypedDict('Group', {
            'portal':'int',
            'initiator':'typing.Optional[int]',
            'authmethod':'str',
            'auth':'typing.Optional[int]',
    })
    IscsiTargetCreate = typing.TypedDict('IscsiTargetCreate', {
            'name':'str',
            'alias':'typing.Optional[str]',
            'mode':'str',
            'groups':'list[Group]',
            'auth_networks':'list[str]',
    })
    QueryOptionsGetInstance = typing.TypedDict('QueryOptionsGetInstance', {
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
    Group_ = typing.TypedDict('Group_', {
            'portal':'int',
            'initiator':'typing.Optional[int]',
            'authmethod':'str',
            'auth':'typing.Optional[int]',
    })
    IscsiTargetUpdate = typing.TypedDict('IscsiTargetUpdate', {
            'name':'str',
            'alias':'typing.Optional[str]',
            'mode':'str',
            'groups':'list[Group_]',
            'auth_networks':'list[str]',
    })

