
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class ChartRelease(
    Namespace
    ):
    _namespace:typing.Literal['chart.release']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def certificate_authority_choices(self, 
    /) -> 'list[CertificateauthorityEntry]': 
        """
        Returns certificate authorities which can be used by applications.

        Parameters
        ----------
        Returns
        -------
        list[CertificateauthorityEntry]:
            certificate_authority_choices
        """
        ...
    @typing.overload
    def certificate_choices(self, 
    /) -> 'list[CertificateEntry]': 
        """
        Returns certificates which can be used by applications.

        Parameters
        ----------
        Returns
        -------
        list[CertificateEntry]:
            certificate_choices
        """
        ...
    @typing.overload
    def create(self, 
        _chart_release_create:'ChartReleaseCreate',
    /) -> 'ChartReleaseCreateReturns': 
        """
        Create a chart release for a catalog item.
        
        `release_name` is the name which will be used to identify the created chart release.
        
        `catalog` is a valid catalog id where system will look for catalog `item` details.
        
        `train` is which train to look for under `catalog` i.e stable / testing etc.
        
        `version` specifies the catalog `item` version.
        
        `values` is configuration specified for the catalog item version in question which will be used to
        create the chart release.

        Parameters
        ----------
        chart_release_create:
            chart_release_create
        Returns
        -------
        ChartReleaseCreateReturns:
            chart_release_create_returns
        """
        ...
    @typing.overload
    def delete(self, 
        _release_name:'str',
        _options:'Options',
    /) -> 'bool': 
        """
        Delete existing chart release.
        
        This will delete the chart release from the kubernetes cluster and also remove any associated volumes / data.
        To clarify, host path volumes will not be deleted which live outside the chart release dataset.

        Parameters
        ----------
        release_name:
            release_name
        options:
            options
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    @typing.overload
    def events(self, 
        _release_name:'str',
    /) -> 'list[Event]': 
        """
        Returns kubernetes events for `release_name` Chart Release.

        Parameters
        ----------
        release_name:
            release_name
        Returns
        -------
        list[Event]:
            events
        """
        ...
    @typing.overload
    def get_chart_releases_using_chart_release_images(self, 
        _chart_release_name:'str',
    /) -> 'dict[str]': 
        """
        Retrieve chart releases which are consuming any images in use by `chart_release_name`.

        Parameters
        ----------
        chart_release_name:
            chart_release_name
        Returns
        -------
        dict[str]:
            Example(s):
            ```
            {
                "minio2": [
                    "minio/minio:RELEASE.2022-03-05T06-32-39Z"
                ]
            }
            ```
        """
        ...
    @typing.overload
    def get_instance(self, 
        _id:'typing.Union[str, int, bool, dict[str], list]',
        _query_options_get_instance:'QueryOptionsGetInstance',
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
    @typing.overload
    def nic_choices(self, 
    /) -> 'dict[str]': 
        """
        Available choices for NIC which can be added to a pod in a chart release.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            nic_choices
        """
        ...
    @typing.overload
    def pod_console_choices(self, 
        _release_name:'str',
    /) -> 'dict[str]': 
        """
        Returns choices for console access to a chart release.
        
        Output is a dictionary with names of pods as keys and containing names of containers which the pod
        comprises of.

        Parameters
        ----------
        release_name:
            release_name
        Returns
        -------
        dict[str]:
            Example(s):
            ```
            {
                "plex-d4559844b-zcgq9": [
                    "plex"
                ]
            }
            ```
        """
        ...
    @typing.overload
    def pod_logs(self, 
        _release_name:'str',
        _options:'Options_',
    /) -> None: 
        """
        Export logs of `options.container_name` container in `options.pod_name` pod in `release_name` chart release.
        
        `options.tail_lines` is an option to select how many lines of logs to retrieve for the said container. It
        defaults to 500. If set to `null`, it will retrieve complete logs of the container.
        
        `options.limit_bytes` is an option to select how many bytes to retrieve from the tail lines selected. If set
        to null ( which is the default ), it will not limit the bytes returned. To clarify, `options.tail_lines`
        is applied first and the required number of lines are retrieved and then `options.limit_bytes` is applied.
        
        Please refer to websocket documentation for downloading the file.

        Parameters
        ----------
        release_name:
            Export logs of `options.container_name` container in `options.pod_name` pod in `release_name` chart release.
        options:
            options
        Returns
        -------
        """
        ...
    @typing.overload
    def pod_logs_choices(self, 
        _release_name:'str',
    /) -> 'dict[str]': 
        """
        Returns choices for accessing logs of any container in any pod in a chart release.

        Parameters
        ----------
        release_name:
            release_name
        Returns
        -------
        dict[str]:
            Example(s):
            ```
            {
                "plex-d4559844b-zcgq9": [
                    "plex"
                ]
            }
            ```
        """
        ...
    @typing.overload
    def pod_status(self, 
        _release_name:'str',
    /) -> 'PodStatus_': 
        """
        Retrieve available/desired pods status for a chart release and it's current state.

        Parameters
        ----------
        release_name:
            release_name
        Returns
        -------
        PodStatus_:
            pod_status
        """
        ...
    @typing.overload
    def pull_container_images(self, 
        _release_name:'str',
        _pull_container_images_options:'PullContainerImagesOptions',
    /) -> 'dict[str]': 
        """
        Update container images being used by `release_name` chart release.
        
        `redeploy` when set will redeploy pods which will result in chart release using newer updated versions of
        the container images.

        Parameters
        ----------
        release_name:
            Update container images being used by `release_name` chart release.
        pull_container_images_options:
            pull_container_images_options
        Returns
        -------
        dict[str]:
            Dictionary of container image(s) with container image tag as key and update status as value
            
            Example(s):
            ```
            {
                "plexinc/pms-docker:1.23.2.4656-85f0adf5b": "Updated image"
            }
            ```
        """
        ...
    @typing.overload
    def query(self, 
        _query_filters:'list[list]',
        _query_options:'QueryOptions',
    /) -> 'typing.Union[list[ChartReleaseEntry], ChartReleaseEntry, int]': 
        """
        Query available chart releases.
        
        `query-options.extra.retrieve_resources` is a boolean when set will retrieve existing kubernetes resources
        in the chart namespace.
        
        `query-options.extra.history` is a boolean when set will retrieve all chart version upgrades
        for a chart release.
        
        `query-options.extra.include_chart_schema` is a boolean when set will retrieve the schema being used by
        the chart release in question.
        
        `query-options.extra.resource_events` is a boolean when set will retrieve individual events of each resource.
        This only has effect if `query-options.extra.retrieve_resources` is set.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[ChartReleaseEntry], ChartReleaseEntry, int]:
            
        """
        ...
    @typing.overload
    def redeploy(self, 
        _release_name:'str',
    /) -> 'ChartReleaseEntry': 
        """
        Redeploy will initiate a new rollout of the Helm chart according to upgrade strategy defined by the chart
        release workloads. A good example for redeploying is updating kubernetes pods with an updated container image.

        Parameters
        ----------
        release_name:
            release_name
        Returns
        -------
        ChartReleaseEntry:
            chart_release_entry
        """
        ...
    @typing.overload
    def remove_ix_volume(self, 
        _release_name:'str',
        _volume_name:'str',
    /) -> None: 
        """
        Remove `volume_name` ix_volume from `release_name` chart release.

        Parameters
        ----------
        release_name:
            release_name
        volume_name:
            volume_name
        Returns
        -------
        """
        ...
    @typing.overload
    def rollback(self, 
        _release_name:'str',
        _rollback_options:'RollbackOptions',
    /) -> 'ChartReleaseEntry': 
        """
        Rollback a chart release to a previous chart version.
        
        `item_version` is version which we want to rollback a chart release to.
        
        `rollback_snapshot` is a boolean value which when set will rollback snapshots of any PVC's or ix volumes being
        consumed by the chart release.
        
        `force_rollback` is a boolean which when set will force rollback operation to move forward even if no
        snapshots are found. This is only useful when `rollback_snapshot` is set.
        
        `recreate_resources` is a boolean which will delete and then create the kubernetes resources on rollback
        of chart release. This should be used with caution as if chart release is consuming immutable objects like
        a PVC, the rollback operation can't be performed and will fail as helm tries to do a 3 way patch for rollback.
        
        Rollback is functional for the actual configuration of the release at the `item_version` specified and
        any associated `ix_volumes` with any PVC's which were consuming chart release storage class.

        Parameters
        ----------
        release_name:
            release_name
        rollback_options:
            rollback_options
        Returns
        -------
        ChartReleaseEntry:
            chart_release_entry
        """
        ...
    @typing.overload
    def scale(self, 
        _release_name:'str',
        _scale_options:'ScaleOptions',
    /) -> 'ScaleChartRelease': 
        """
        Scale a `release_name` chart release to `scale_options.replica_count` specified.
        
        This will scale deployments/statefulset to replica count specified.

        Parameters
        ----------
        release_name:
            Scale a `release_name` chart release to `scale_options.replica_count` specified.
        scale_options:
            scale_options
        Returns
        -------
        ScaleChartRelease:
            scale_chart_release
        """
        ...
    @typing.overload
    def scale_workloads(self, 
        _release_name:'str',
        _workloads:'list[ScaleWorkload]',
    /) -> None: 
        """
        Scale workloads in a chart release to specified `replica_count`.

        Parameters
        ----------
        release_name:
            release_name
        workloads:
            workloads
        Returns
        -------
        """
        ...
    @typing.overload
    def scaleable_resources(self, 
    /) -> 'ScaleableResources': 
        """
        Returns choices for types of workloads which can be scaled up/down.

        Parameters
        ----------
        Returns
        -------
        ScaleableResources:
            scaleable_resources
        """
        ...
    @typing.overload
    def update(self, 
        _chart_release:'str',
        _chart_release_update:'ChartReleaseUpdate',
    /) -> 'ChartReleaseUpdateReturns': 
        """
        Update an existing chart release.
        
        `values` is configuration specified for the catalog item version in question which will be used to
        create the chart release.

        Parameters
        ----------
        chart_release:
            chart_release
        chart_release_update:
            chart_release_update
        Returns
        -------
        ChartReleaseUpdateReturns:
            chart_release_update_returns
        """
        ...
    @typing.overload
    def upgrade(self, 
        _release_name:'str',
        _upgrade_options:'UpgradeOptions',
    /) -> 'ChartReleaseEntry': 
        """
        Upgrade `release_name` chart release.
        
        `upgrade_options.item_version` specifies to which item version chart release should be upgraded to.
        
        System will update container images being used by `release_name` chart release as a chart release
        upgrade is not considered complete until the images in use have also been updated to latest versions.
        
        During upgrade, `upgrade_options.values` can be specified to apply configuration changes for configuration
        changes for the chart release in question.
        
        When chart version is upgraded, system will automatically take a snapshot of `ix_volumes` in question
        which can be used to rollback later on.

        Parameters
        ----------
        release_name:
            Upgrade `release_name` chart release.
            System will update container images being used by `release_name` chart release as a chart release
            upgrade is not considered complete until the images in use have also been updated to latest versions.
        upgrade_options:
            upgrade_options
        Returns
        -------
        ChartReleaseEntry:
            chart_release_entry
        """
        ...
    @typing.overload
    def upgrade_summary(self, 
        _release_name:'str',
        _options:'Options__',
    /) -> 'UpgradeSummary': 
        """
        Retrieve upgrade summary for `release_name` which will include which container images will be updated
        and changelog for `options.item_version` chart version specified if applicable. If only container images
        need to be updated, changelog will be `null`.
        
        If chart release `release_name` does not require an upgrade, an error will be raised.

        Parameters
        ----------
        release_name:
            Retrieve upgrade summary for `release_name` which will include which container images will be updated
            and changelog for `options.item_version` chart version specified if applicable. If only container images
            need to be updated, changelog will be `null`.
        options:
            options
        Returns
        -------
        UpgradeSummary:
            upgrade_summary
        """
        ...
    @typing.overload
    def used_ports(self, 
    /) -> 'list[int]': 
        """
        Returns ports in use by applications.

        Parameters
        ----------
        Returns
        -------
        list[int]:
            used_ports
        """
        ...
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
