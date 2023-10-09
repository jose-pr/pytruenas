
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin

import typing
from enum import Enum

class Kubernetes(ConfigMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'kubernetes')

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
    Metadata = typing.TypedDict('Metadata', {
            'name':'str',
    })
    Event = typing.TypedDict('Event', {
            'metadata':'Metadata',
            'message':'str',
    })
    Options = typing.TypedDict('Options', {
            'wait_for_csi':'bool',
    })
    class Status(str,Enum):
        PENDING = 'PENDING'
        RUNNING = 'RUNNING'
        INITIALIZING = 'INITIALIZING'
        STOPPING = 'STOPPING'
        STOPPED = 'STOPPED'
        UNCONFIGURED = 'UNCONFIGURED'
        FAILED = 'FAILED'
        ...
    Status_ = typing.TypedDict('Status_', {
            'status':'Status',
            'description':'str',
    })
    MigrationOptions = typing.TypedDict('MigrationOptions', {
            'passphrase':'str',
    })
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
