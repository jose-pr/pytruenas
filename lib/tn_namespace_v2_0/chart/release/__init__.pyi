
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class ChartRelease(Namespace):
    _namespace:_ty.Literal['chart.release']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def certificate_authority_choices(self, 
    /) -> 'list': 
        """
        Returns certificate authorities which can be used by applications.

        Parameters
        ----------
        Returns
        -------
        list:
            certificate_authority_choices
        """
        ...
    @_ty.overload
    def certificate_choices(self, 
    /) -> 'list': 
        """
        Returns certificates which can be used by applications.

        Parameters
        ----------
        Returns
        -------
        list:
            certificate_choices
        """
        ...
    @_ty.overload
    def create(self, 
        chart_release_create:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            chart_release_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        release_name:'str',
        options:'dict[str]'={},
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
    @_ty.overload
    def events(self, 
        release_name:'str',
    /) -> 'list': 
        """
        Returns kubernetes events for `release_name` Chart Release.

        Parameters
        ----------
        release_name:
            release_name
        Returns
        -------
        list:
            events
        """
        ...
    @_ty.overload
    def get_chart_releases_using_chart_release_images(self, 
        chart_release_name:'str',
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
    @_ty.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'dict[str]'={},
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
    @_ty.overload
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
    @_ty.overload
    def pod_console_choices(self, 
        release_name:'str',
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
    @_ty.overload
    def pod_logs(self, 
        release_name:'str',
        options:'dict[str]'={},
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
    @_ty.overload
    def pod_logs_choices(self, 
        release_name:'str',
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
    @_ty.overload
    def pod_status(self, 
        release_name:'str',
    /) -> 'dict[str]': 
        """
        Retrieve available/desired pods status for a chart release and it's current state.

        Parameters
        ----------
        release_name:
            release_name
        Returns
        -------
        dict[str]:
            pod_status
        """
        ...
    @_ty.overload
    def pull_container_images(self, 
        release_name:'str',
        pull_container_images_options:'dict[str]'={},
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
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
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
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
    def redeploy(self, 
        release_name:'str',
    /) -> 'dict[str]': 
        """
        Redeploy will initiate a new rollout of the Helm chart according to upgrade strategy defined by the chart
        release workloads. A good example for redeploying is updating kubernetes pods with an updated container image.

        Parameters
        ----------
        release_name:
            release_name
        Returns
        -------
        dict[str]:
            chart_release_entry
        """
        ...
    @_ty.overload
    def remove_ix_volume(self, 
        release_name:'str',
        volume_name:'str',
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
    @_ty.overload
    def rollback(self, 
        release_name:'str',
        rollback_options:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            chart_release_entry
        """
        ...
    @_ty.overload
    def scale(self, 
        release_name:'str',
        scale_options:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            scale_chart_release
        """
        ...
    @_ty.overload
    def scale_workloads(self, 
        release_name:'str',
        workloads:'list'=[],
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
    @_ty.overload
    def scaleable_resources(self, 
    /) -> 'dict[str]': 
        """
        Returns choices for types of workloads which can be scaled up/down.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            scaleable_resources
        """
        ...
    @_ty.overload
    def update(self, 
        chart_release:'str',
        chart_release_update:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            chart_release_update_returns
        """
        ...
    @_ty.overload
    def upgrade(self, 
        release_name:'str',
        upgrade_options:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            chart_release_entry
        """
        ...
    @_ty.overload
    def upgrade_summary(self, 
        release_name:'str',
        options:'dict[str]'={},
    /) -> 'dict[str]': 
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
        dict[str]:
            upgrade_summary
        """
        ...
    @_ty.overload
    def used_ports(self, 
    /) -> 'list': 
        """
        Returns ports in use by applications.

        Parameters
        ----------
        Returns
        -------
        list:
            used_ports
        """
        ...
