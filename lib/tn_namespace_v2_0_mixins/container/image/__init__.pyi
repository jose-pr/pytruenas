
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
class ContainerImage(
    TableExtMixin,
    Namespace
    ):
    _namespace:typing.Literal['container.image']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def delete(self, 
        id:'str',
    /) -> None: 
        """
        `options.force` should be used to force delete an image even if it's in use by a stopped container.

        Parameters
        ----------
        id:
            id
        Returns
        -------
        """
        ...
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
    Authentication = typing.TypedDict('Authentication', {
            'username':'str',
            'password':'str',
    })
    ImagePull = typing.TypedDict('ImagePull', {
            'authentication':'Authentication',
            'from_image':'str',
            'tag':'typing.Optional[str]',
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
    ParsedRepoTag = typing.TypedDict('ParsedRepoTag', {
            'image':'str',
            'tag':'str',
            'registry':'str',
            'complete_tag':'str',
    })
    ContainerImageEntry = typing.TypedDict('ContainerImageEntry', {
            'id':'str',
            'repo_tags':'list[str]',
            'repo_digests':'list[str]',
            'size':'int',
            'dangling':'bool',
            'update_available':'bool',
            'system_image':'bool',
            'parsed_repo_tags':'list[ParsedRepoTag]',
            'complete_tags':'list[str]',
    })
    ContainerImageEntry_ = typing.TypedDict('ContainerImageEntry_', {
            'id':'str',
            'repo_tags':'list[str]',
            'repo_digests':'list[str]',
            'size':'int',
            'dangling':'bool',
            'update_available':'bool',
            'system_image':'bool',
            'parsed_repo_tags':'list[ParsedRepoTag]',
            'complete_tags':'list[str]',
    })
    ContainerImageEntry__ = typing.TypedDict('ContainerImageEntry__', {
            'id':'str',
            'repo_tags':'list[str]',
            'repo_digests':'list[str]',
            'size':'int',
            'dangling':'bool',
            'update_available':'bool',
            'system_image':'bool',
            'parsed_repo_tags':'list[ParsedRepoTag]',
            'complete_tags':'list[str]',
    })
    @typing.overload
    def get_chart_releases_consuming_image(self, 
        image_tags:'list[str]'=[],
    /) -> 'list': 
        """
        Retrieve chart releases consuming `image_tag` image.

        Parameters
        ----------
        image_tags:
            image_tags
        Returns
        -------
        list:
            get_chart_releases_consuming_image
        """
        ...
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
    Authentication = typing.TypedDict('Authentication', {
            'username':'str',
            'password':'str',
    })
    ImagePull = typing.TypedDict('ImagePull', {
            'authentication':'Authentication',
            'from_image':'str',
            'tag':'typing.Optional[str]',
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
    ParsedRepoTag = typing.TypedDict('ParsedRepoTag', {
            'image':'str',
            'tag':'str',
            'registry':'str',
            'complete_tag':'str',
    })
    ContainerImageEntry = typing.TypedDict('ContainerImageEntry', {
            'id':'str',
            'repo_tags':'list[str]',
            'repo_digests':'list[str]',
            'size':'int',
            'dangling':'bool',
            'update_available':'bool',
            'system_image':'bool',
            'parsed_repo_tags':'list[ParsedRepoTag]',
            'complete_tags':'list[str]',
    })
    ContainerImageEntry_ = typing.TypedDict('ContainerImageEntry_', {
            'id':'str',
            'repo_tags':'list[str]',
            'repo_digests':'list[str]',
            'size':'int',
            'dangling':'bool',
            'update_available':'bool',
            'system_image':'bool',
            'parsed_repo_tags':'list[ParsedRepoTag]',
            'complete_tags':'list[str]',
    })
    ContainerImageEntry__ = typing.TypedDict('ContainerImageEntry__', {
            'id':'str',
            'repo_tags':'list[str]',
            'repo_digests':'list[str]',
            'size':'int',
            'dangling':'bool',
            'update_available':'bool',
            'system_image':'bool',
            'parsed_repo_tags':'list[ParsedRepoTag]',
            'complete_tags':'list[str]',
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
    Authentication = typing.TypedDict('Authentication', {
            'username':'str',
            'password':'str',
    })
    ImagePull = typing.TypedDict('ImagePull', {
            'authentication':'Authentication',
            'from_image':'str',
            'tag':'typing.Optional[str]',
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
    ParsedRepoTag = typing.TypedDict('ParsedRepoTag', {
            'image':'str',
            'tag':'str',
            'registry':'str',
            'complete_tag':'str',
    })
    ContainerImageEntry = typing.TypedDict('ContainerImageEntry', {
            'id':'str',
            'repo_tags':'list[str]',
            'repo_digests':'list[str]',
            'size':'int',
            'dangling':'bool',
            'update_available':'bool',
            'system_image':'bool',
            'parsed_repo_tags':'list[ParsedRepoTag]',
            'complete_tags':'list[str]',
    })
    ContainerImageEntry_ = typing.TypedDict('ContainerImageEntry_', {
            'id':'str',
            'repo_tags':'list[str]',
            'repo_digests':'list[str]',
            'size':'int',
            'dangling':'bool',
            'update_available':'bool',
            'system_image':'bool',
            'parsed_repo_tags':'list[ParsedRepoTag]',
            'complete_tags':'list[str]',
    })
    ContainerImageEntry__ = typing.TypedDict('ContainerImageEntry__', {
            'id':'str',
            'repo_tags':'list[str]',
            'repo_digests':'list[str]',
            'size':'int',
            'dangling':'bool',
            'update_available':'bool',
            'system_image':'bool',
            'parsed_repo_tags':'list[ParsedRepoTag]',
            'complete_tags':'list[str]',
    })
    @typing.overload
    def pull(self, 
        image_pull:'ImagePull'={},
    /) -> None: 
        """
        `from_image` is the name of the image to pull. Format for the name is "registry/repo/image" where
        registry may be omitted and it will default to docker registry in this case.
        
        `tag` specifies tag of the image and defaults to `null`. In case of `null` it will retrieve all the tags
        of the image.
        
        `authentication` should be specified if image to be retrieved is under a private repository.

        Parameters
        ----------
        image_pull:
            image_pull
        Returns
        -------
        """
        ...
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
    Authentication = typing.TypedDict('Authentication', {
            'username':'str',
            'password':'str',
    })
    ImagePull = typing.TypedDict('ImagePull', {
            'authentication':'Authentication',
            'from_image':'str',
            'tag':'typing.Optional[str]',
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
    ParsedRepoTag = typing.TypedDict('ParsedRepoTag', {
            'image':'str',
            'tag':'str',
            'registry':'str',
            'complete_tag':'str',
    })
    ContainerImageEntry = typing.TypedDict('ContainerImageEntry', {
            'id':'str',
            'repo_tags':'list[str]',
            'repo_digests':'list[str]',
            'size':'int',
            'dangling':'bool',
            'update_available':'bool',
            'system_image':'bool',
            'parsed_repo_tags':'list[ParsedRepoTag]',
            'complete_tags':'list[str]',
    })
    ContainerImageEntry_ = typing.TypedDict('ContainerImageEntry_', {
            'id':'str',
            'repo_tags':'list[str]',
            'repo_digests':'list[str]',
            'size':'int',
            'dangling':'bool',
            'update_available':'bool',
            'system_image':'bool',
            'parsed_repo_tags':'list[ParsedRepoTag]',
            'complete_tags':'list[str]',
    })
    ContainerImageEntry__ = typing.TypedDict('ContainerImageEntry__', {
            'id':'str',
            'repo_tags':'list[str]',
            'repo_digests':'list[str]',
            'size':'int',
            'dangling':'bool',
            'update_available':'bool',
            'system_image':'bool',
            'parsed_repo_tags':'list[ParsedRepoTag]',
            'complete_tags':'list[str]',
    })
    @typing.overload
    def query(self, 
        query_filters:'list[list]'=[],
        query_options:'QueryOptions'={},
    /) -> 'typing.Union[list[ContainerImageEntry], ForwardRef(ContainerImageEntry_), int, ForwardRef(ContainerImageEntry__)]': 
        """
        Retrieve container images present in the system.
        
        `query-options.extra.parse_tags` is a boolean which when set will have normalized tags to be retrieved
        for container images.

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        typing.Union[list[ContainerImageEntry], ForwardRef(ContainerImageEntry_), int, ForwardRef(ContainerImageEntry__)]:
            
        """
        ...
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
    Authentication = typing.TypedDict('Authentication', {
            'username':'str',
            'password':'str',
    })
    ImagePull = typing.TypedDict('ImagePull', {
            'authentication':'Authentication',
            'from_image':'str',
            'tag':'typing.Optional[str]',
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
    ParsedRepoTag = typing.TypedDict('ParsedRepoTag', {
            'image':'str',
            'tag':'str',
            'registry':'str',
            'complete_tag':'str',
    })
    ContainerImageEntry = typing.TypedDict('ContainerImageEntry', {
            'id':'str',
            'repo_tags':'list[str]',
            'repo_digests':'list[str]',
            'size':'int',
            'dangling':'bool',
            'update_available':'bool',
            'system_image':'bool',
            'parsed_repo_tags':'list[ParsedRepoTag]',
            'complete_tags':'list[str]',
    })
    ContainerImageEntry_ = typing.TypedDict('ContainerImageEntry_', {
            'id':'str',
            'repo_tags':'list[str]',
            'repo_digests':'list[str]',
            'size':'int',
            'dangling':'bool',
            'update_available':'bool',
            'system_image':'bool',
            'parsed_repo_tags':'list[ParsedRepoTag]',
            'complete_tags':'list[str]',
    })
    ContainerImageEntry__ = typing.TypedDict('ContainerImageEntry__', {
            'id':'str',
            'repo_tags':'list[str]',
            'repo_digests':'list[str]',
            'size':'int',
            'dangling':'bool',
            'update_available':'bool',
            'system_image':'bool',
            'parsed_repo_tags':'list[ParsedRepoTag]',
            'complete_tags':'list[str]',
    })
