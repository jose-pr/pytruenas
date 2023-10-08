
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class ContainerImage(Namespace):
    _namespace:_ty.Literal['container.image']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
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
    @_ty.overload
    def get_chart_releases_consuming_image(self, 
        image_tags:'list'=[],
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
    def pull(self, 
        image_pull:'dict[str]'={},
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
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
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
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
