
from pytruenas.base import Namespace

import typing
from enum import Enum

class ChartRelease(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'chart.release')

    AfterScale = typing.TypedDict('AfterScale', {
            'deployments':'dict[str]',
            'statefulsets':'dict[str]',
    })
    BeforeScale = typing.TypedDict('BeforeScale', {
            'deployments':'dict[str]',
            'statefulsets':'dict[str]',
    })
    CertificateEntry = typing.TypedDict('CertificateEntry', {
            'id':'int',
            'type':'int',
            'name':'str',
            'certificate':'typing.Optional[str]',
            'privatekey':'typing.Optional[str]',
            'CSR':'typing.Optional[str]',
            'acme_uri':'typing.Optional[str]',
            'domains_authenticators':'dict[str]',
            'renew_days':'int',
            'revoked_date':'typing.Optional[str]',
            'signedby':'dict[str]',
            'root_path':'str',
            'acme':'dict[str]',
            'certificate_path':'typing.Optional[str]',
            'privatekey_path':'typing.Optional[str]',
            'csr_path':'typing.Optional[str]',
            'cert_type':'str',
            'revoked':'bool',
            'expired':'typing.Optional[bool]',
            'issuer':'typing.Union[str, NoneType, dict[str]]',
            'chain_list':'list[str]',
            'country':'typing.Optional[str]',
            'state':'typing.Optional[str]',
            'city':'typing.Optional[str]',
            'organization':'typing.Optional[str]',
            'organizational_unit':'typing.Optional[str]',
            'san':'typing.Optional[list]',
            'email':'typing.Optional[str]',
            'DN':'typing.Optional[str]',
            'subject_name_hash':'typing.Optional[str]',
            'digest_algorithm':'typing.Optional[str]',
            'from':'typing.Optional[str]',
            'common':'typing.Optional[str]',
            'until':'typing.Optional[str]',
            'fingerprint':'typing.Optional[str]',
            'key_type':'typing.Optional[str]',
            'internal':'typing.Optional[str]',
            'lifetime':'typing.Optional[int]',
            'serial':'typing.Optional[int]',
            'key_length':'typing.Optional[int]',
            'chain':'typing.Optional[bool]',
            'CA_type_existing':'bool',
            'CA_type_internal':'bool',
            'CA_type_intermediate':'bool',
            'cert_type_existing':'bool',
            'cert_type_internal':'bool',
            'cert_type_CSR':'bool',
            'parsed':'bool',
            'can_be_revoked':'bool',
            'extensions':'dict[str]',
            'revoked_certs':'list',
            'crl_path':'str',
            'signed_certificates':'int',
    })
    CertificateauthorityEntry = typing.TypedDict('CertificateauthorityEntry', {
            'id':'int',
            'type':'int',
            'name':'str',
            'certificate':'typing.Optional[str]',
            'privatekey':'typing.Optional[str]',
            'CSR':'typing.Optional[str]',
            'acme_uri':'typing.Optional[str]',
            'domains_authenticators':'dict[str]',
            'renew_days':'int',
            'revoked_date':'typing.Optional[str]',
            'signedby':'dict[str]',
            'root_path':'str',
            'acme':'dict[str]',
            'certificate_path':'typing.Optional[str]',
            'privatekey_path':'typing.Optional[str]',
            'csr_path':'typing.Optional[str]',
            'cert_type':'str',
            'revoked':'bool',
            'expired':'typing.Optional[bool]',
            'issuer':'typing.Union[str, NoneType, dict[str]]',
            'chain_list':'list[str]',
            'country':'typing.Optional[str]',
            'state':'typing.Optional[str]',
            'city':'typing.Optional[str]',
            'organization':'typing.Optional[str]',
            'organizational_unit':'typing.Optional[str]',
            'san':'typing.Optional[list]',
            'email':'typing.Optional[str]',
            'DN':'typing.Optional[str]',
            'subject_name_hash':'typing.Optional[str]',
            'digest_algorithm':'typing.Optional[str]',
            'from':'typing.Optional[str]',
            'common':'typing.Optional[str]',
            'until':'typing.Optional[str]',
            'fingerprint':'typing.Optional[str]',
            'key_type':'typing.Optional[str]',
            'internal':'typing.Optional[str]',
            'lifetime':'typing.Optional[int]',
            'serial':'typing.Optional[int]',
            'key_length':'typing.Optional[int]',
            'chain':'typing.Optional[bool]',
            'CA_type_existing':'bool',
            'CA_type_internal':'bool',
            'CA_type_intermediate':'bool',
            'cert_type_existing':'bool',
            'cert_type_internal':'bool',
            'cert_type_CSR':'bool',
            'parsed':'bool',
            'can_be_revoked':'bool',
            'extensions':'dict[str]',
            'revoked_certs':'list',
            'crl_path':'str',
            'signed_certificates':'int',
            'add_to_trusted_store':'bool',
    })
    ChartMetadata = typing.TypedDict('ChartMetadata', {
            'name':'str',
            'version':'str',
            'latest_chart_version':'str',
    })
    ChartReleaseCreate = typing.TypedDict('ChartReleaseCreate', {
            'values':'dict[str]',
            'catalog':'str',
            'item':'str',
            'release_name':'str',
            'train':'str',
            'version':'str',
    })
    ChartReleaseCreateReturns = typing.TypedDict('ChartReleaseCreateReturns', {
            'name':'str',
            'info':'dict[str]',
            'config':'dict[str]',
            'hooks':'list',
            'version':'int',
            'namespace':'str',
            'chart_metadata':'ChartMetadata',
            'id':'str',
            'catalog':'str',
            'catalog_train':'str',
            'path':'str',
            'dataset':'str',
            'status':'str',
            'used_ports':'list[Port]',
            'pod_status':'PodStatus',
            'update_available':'bool',
            'human_version':'str',
            'human_latest_version':'str',
            'container_images_update_available':'bool',
            'portals':'dict[str]',
            'chart_schema':'dict[str]',
            'history':'dict[str]',
            'resources':'Resources',
    })
    ChartReleaseEntry = typing.TypedDict('ChartReleaseEntry', {
            'name':'str',
            'info':'dict[str]',
            'config':'dict[str]',
            'hooks':'list',
            'version':'int',
            'namespace':'str',
            'chart_metadata':'ChartMetadata',
            'id':'str',
            'catalog':'str',
            'catalog_train':'str',
            'path':'str',
            'dataset':'str',
            'status':'str',
            'used_ports':'list[Port]',
            'pod_status':'PodStatus',
            'update_available':'bool',
            'human_version':'str',
            'human_latest_version':'str',
            'container_images_update_available':'bool',
            'portals':'dict[str]',
            'chart_schema':'dict[str]',
            'history':'dict[str]',
            'resources':'Resources',
    })
    ChartReleaseUpdate = typing.TypedDict('ChartReleaseUpdate', {
            'values':'dict[str]',
    })
    ChartReleaseUpdateReturns = typing.TypedDict('ChartReleaseUpdateReturns', {
            'name':'str',
            'info':'dict[str]',
            'config':'dict[str]',
            'hooks':'list',
            'version':'int',
            'namespace':'str',
            'chart_metadata':'ChartMetadata',
            'id':'str',
            'catalog':'str',
            'catalog_train':'str',
            'path':'str',
            'dataset':'str',
            'status':'str',
            'used_ports':'list[Port]',
            'pod_status':'PodStatus',
            'update_available':'bool',
            'human_version':'str',
            'human_latest_version':'str',
            'container_images_update_available':'bool',
            'portals':'dict[str]',
            'chart_schema':'dict[str]',
            'history':'dict[str]',
            'resources':'Resources',
    })
    Event = typing.TypedDict('Event', {
            'involvedObject':'InvolvedObject',
            'metadata':'Metadata',
    })
    InvolvedObject = typing.TypedDict('InvolvedObject', {
            'kind':'str',
            'name':'str',
            'namespace':'str',
    })
    Metadata = typing.TypedDict('Metadata', {
            'namespace':'str',
            'uid':'str',
            'name':'str',
    })
    Options = typing.TypedDict('Options', {
            'delete_unused_images':'bool',
    })
    Options_ = typing.TypedDict('Options_', {
            'limit_bytes':'typing.Optional[int]',
            'tail_lines':'typing.Optional[int]',
            'pod_name':'str',
            'container_name':'str',
    })
    Options__ = typing.TypedDict('Options__', {
            'item_version':'str',
    })
    PodStatus = typing.TypedDict('PodStatus', {
            'available':'int',
            'desired':'int',
    })
    PodStatus_ = typing.TypedDict('PodStatus_', {
            'available':'int',
            'desired':'int',
            'status':'Status',
    })
    Port = typing.TypedDict('Port', {
            'port':'int',
            'protocol':'str',
    })
    PullContainerImagesOptions = typing.TypedDict('PullContainerImagesOptions', {
            'redeploy':'bool',
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
    Resources = typing.TypedDict('Resources', {
            'storage_class':'dict[str]',
            'persistent_volumes':'list',
            'host_path_volumes':'list',
            'locked_host_paths':'list',
            'container_images':'dict[str]',
            'truenas_certificates':'list[int]',
            'truenas_certificate_authorities':'list[int]',
            'cronjobs':'list',
            'deployments':'list',
            'jobs':'list',
            'persistent_volume_claims':'list',
            'pods':'list',
            'statefulsets':'list',
    })
    RollbackOptions = typing.TypedDict('RollbackOptions', {
            'force_rollback':'bool',
            'recreate_resources':'bool',
            'rollback_snapshot':'bool',
            'item_version':'str',
    })
    ScaleChartRelease = typing.TypedDict('ScaleChartRelease', {
            'before_scale':'BeforeScale',
            'after_scale':'AfterScale',
    })
    ScaleOptions = typing.TypedDict('ScaleOptions', {
            'replica_count':'int',
    })
    ScaleWorkload = typing.TypedDict('ScaleWorkload', {
            'replica_count':'int',
            'type':'Type',
            'name':'str',
    })
    ScaleableResources = typing.TypedDict('ScaleableResources', {
            'DEPLOYMENT':'typing.Literal["DEPLOYMENT"]',
            'STATEFULSET':'typing.Literal["STATEFULSET"]',
    })
    class Status(str,Enum):
        ACTIVE = 'ACTIVE'
        DEPLOYING = 'DEPLOYING'
        STOPPED = 'STOPPED'
        ...
    class Type(str,Enum):
        DEPLOYMENT = 'DEPLOYMENT'
        STATEFULSET = 'STATEFULSET'
        ...
    UpgradeOptions = typing.TypedDict('UpgradeOptions', {
            'values':'dict[str]',
            'item_version':'str',
    })
    UpgradeSummary = typing.TypedDict('UpgradeSummary', {
            'image_update_available':'bool',
            'item_update_available':'bool',
            'container_images_to_update':'dict[str]',
            'latest_version':'str',
            'latest_human_version':'str',
            'upgrade_version':'str',
            'upgrade_human_version':'str',
            'changelog':'typing.Optional[str]',
            'available_versions_for_upgrade':'list[VersionInfo]',
    })
    VersionInfo = typing.TypedDict('VersionInfo', {
            'version':'str',
            'human_version':'str',
    })
