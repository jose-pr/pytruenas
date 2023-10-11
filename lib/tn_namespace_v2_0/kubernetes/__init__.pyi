
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Kubernetes(
    Namespace
    ):
    _namespace:typing.Literal['kubernetes']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def backup_chart_releases(self, 
        backup_name:'typing.Optional[str]',
    /) -> 'str': 
        """
        Create a backup of existing chart releases.
        
        The backup will save helm configuration with history for each chart release and then take a
        snapshot of `ix-applications` dataset.

        Parameters
        ----------
        backup_name:
            backup_name
        Returns
        -------
        str:
            backup_name
        """
        ...
    @typing.overload
    def bindip_choices(self, 
    /) -> 'dict[str]': 
        """
        Returns ip choices for Kubernetes service to use.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            kubernetes_bind_ip_choices
        """
        ...
    @typing.overload
    def config(self, 
    /) -> 'KubernetesEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        KubernetesEntry:
            kubernetes_entry
        """
        ...
    @typing.overload
    def delete_backup(self, 
        backup_name:'str',
    /) -> None: 
        """
        Delete `backup_name` chart releases backup.

        Parameters
        ----------
        backup_name:
            backup_name
        Returns
        -------
        """
        ...
    @typing.overload
    def events(self, 
    /) -> 'list[Event]': 
        """
        Returns events for kubernetes node.

        Parameters
        ----------
        Returns
        -------
        list[Event]:
            kubernetes_node_events
        """
        ...
    @typing.overload
    def list_backups(self, 
    /) -> 'dict[str]': 
        """
        List existing chart releases backups.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            backups
        """
        ...
    @typing.overload
    def node_ip(self, 
    /) -> 'typing.Optional[str]': 
        """
        Returns IP used by kubernetes which kubernetes uses to allow incoming connections.

        Parameters
        ----------
        Returns
        -------
        typing.Optional[str]:
            kubernetes_node_ip
        """
        ...
    @typing.overload
    def restore_backup(self, 
        backup_name:'str',
        options:'Options',
    /) -> None: 
        """
        Restore `backup_name` chart releases backup.
        
        It should be noted that a rollback will be initiated which will destroy any newer snapshots/clones
        of `ix-applications` dataset then the snapshot in question of `backup_name`.

        Parameters
        ----------
        backup_name:
            Restore `backup_name` chart releases backup.
        options:
            options
        Returns
        -------
        """
        ...
    @typing.overload
    def route_interface_choices(self, 
    /) -> 'dict[str]': 
        """
        Returns Interface choices for Kubernetes service to use for ipv4 connections.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            route_interface_choices
        """
        ...
    @typing.overload
    def status(self, 
    /) -> 'Status': 
        """
        Returns the status of the Kubernetes service.

        Parameters
        ----------
        Returns
        -------
        Status:
            status
        """
        ...
    @typing.overload
    def update(self, 
        kubernetes_update:'KubernetesUpdate',
    /) -> 'KubernetesUpdateReturns': 
        """
        `pool` must be a valid ZFS pool configured in the system. Kubernetes service will initialise the pool by
        creating datasets under `pool_name/ix-applications`.
        
        `configure_gpus` is a boolean to enable or disable to prevent automatically loading any GPU Support
        into kubernetes. This includes not loading any daemonsets for Intel and NVIDIA support.
        
        `servicelb` is a boolean to enable or disable the integrated k3s Service Loadbalancer called "Klipper".
        This can be set to disabled to enable the user to run another LoadBalancer or no LoadBalancer at all.
        
        `cluster_cidr` is the CIDR to be used for default NAT network between workloads.
        
        `service_cidr` is the CIDR to be used for kubernetes services which are an abstraction and refer to a
        logically set of kubernetes pods.
        
        `cluster_dns_ip` is the IP of the DNS server running for the kubernetes cluster. It must be in the range
        of `service_cidr`.
        
        Specifying values for `cluster_cidr`, `service_cidr` and `cluster_dns_ip` are permanent and a subsequent change
        requires re-initialisation of the applications. To clarify, system will destroy old `ix-applications` dataset
        and any data within it when any of the values for the above configuration change.
        
        `node_ip` is the IP address which the kubernetes cluster will assign to the TrueNAS node. It defaults to
        0.0.0.0 and the cluster in this case will automatically manage which IP address to use for managing traffic
        for default NAT network.
        
        By default kubernetes pods will be using default gateway of the system for outward traffic. This might
        not be desirable for certain users who want to separate NAT traffic over a specific interface / route. System
        will create a L3 network which will be routing the traffic towards default gateway for NAT.
        
        If users want to restrict traffic over a certain gateway / interface, they can specify a default route
        for the NAT traffic. `route_v4_interface` and `route_v4_gateway` will set a default route for the kubernetes
        cluster IPv4 traffic. Similarly `route_v6_interface` and 'route_v6_gateway` can be used to specify default
        route for IPv6 traffic.
        
        In case user is switching pools and the new desired pool has not been configured for kubernetes before, it
        is possible to replicate data from old pool to new pool with setting `migrate_applications` attribute. This
        will replicate contents of old pool's ix-applications dataset to the new pool.
        
        `force` is a boolean which can be set to bypass validation which does not allow users to select a pool which
        is potentially corrupt by having a partially initialized ix-applications dataset. In that case the cluster
        would be re-initialized and user would still be able to select such a pool.
        
        `metrics_server` is a boolean to enable or disable the integrated k3s Metrics Server. This can be set
        to enabled to enable the user to use of Kubernetes Horizontal/Vertical Pod Autoscalers.

        Parameters
        ----------
        kubernetes_update:
            kubernetes_update
        Returns
        -------
        KubernetesUpdateReturns:
            kubernetes_update_returns
        """
        ...
    KubernetesEntry = typing.TypedDict('KubernetesEntry', {
            'servicelb':'bool',
            'configure_gpus':'bool',
            'metrics_server':'bool',
            'passthrough_mode':'bool',
            'pool':'typing.Optional[str]',
            'cluster_cidr':'str',
            'service_cidr':'str',
            'cluster_dns_ip':'str',
            'node_ip':'str',
            'route_v4_interface':'typing.Optional[str]',
            'route_v4_gateway':'typing.Optional[str]',
            'route_v6_interface':'typing.Optional[str]',
            'route_v6_gateway':'typing.Optional[str]',
            'dataset':'typing.Optional[str]',
            'id':'int',
    })
    Event = typing.TypedDict('Event', {
            'metadata':'Metadata',
            'message':'str',
    })
    Metadata = typing.TypedDict('Metadata', {
            'name':'str',
    })
    Options = typing.TypedDict('Options', {
            'wait_for_csi':'bool',
    })
    Status = typing.TypedDict('Status', {
            'status':'Status_',
            'description':'str',
    })
    class Status_(str,Enum):
        PENDING = 'PENDING'
        RUNNING = 'RUNNING'
        INITIALIZING = 'INITIALIZING'
        STOPPING = 'STOPPING'
        STOPPED = 'STOPPED'
        UNCONFIGURED = 'UNCONFIGURED'
        FAILED = 'FAILED'
        ...
    KubernetesUpdate = typing.TypedDict('KubernetesUpdate', {
            'servicelb':'bool',
            'configure_gpus':'bool',
            'metrics_server':'bool',
            'passthrough_mode':'bool',
            'pool':'typing.Optional[str]',
            'cluster_cidr':'str',
            'service_cidr':'str',
            'cluster_dns_ip':'str',
            'node_ip':'str',
            'route_v4_interface':'typing.Optional[str]',
            'route_v4_gateway':'typing.Optional[str]',
            'route_v6_interface':'typing.Optional[str]',
            'route_v6_gateway':'typing.Optional[str]',
            'migrate_applications':'bool',
            'force':'bool',
            'migration_options':'MigrationOptions',
    })
    MigrationOptions = typing.TypedDict('MigrationOptions', {
            'passphrase':'str',
    })
    KubernetesUpdateReturns = typing.TypedDict('KubernetesUpdateReturns', {
            'servicelb':'bool',
            'configure_gpus':'bool',
            'metrics_server':'bool',
            'passthrough_mode':'bool',
            'pool':'typing.Optional[str]',
            'cluster_cidr':'str',
            'service_cidr':'str',
            'cluster_dns_ip':'str',
            'node_ip':'str',
            'route_v4_interface':'typing.Optional[str]',
            'route_v4_gateway':'typing.Optional[str]',
            'route_v6_interface':'typing.Optional[str]',
            'route_v6_gateway':'typing.Optional[str]',
            'dataset':'typing.Optional[str]',
            'id':'int',
    })
