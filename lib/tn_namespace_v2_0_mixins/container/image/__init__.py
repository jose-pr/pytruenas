
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class ContainerImage(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'container.image')

    Authentication = typing.TypedDict('Authentication', {
            'username':'str',
            'password':'str',
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
    ImagePull = typing.TypedDict('ImagePull', {
            'authentication':'Authentication',
            'from_image':'str',
            'tag':'typing.Optional[str]',
    })
    ParsedRepoTag = typing.TypedDict('ParsedRepoTag', {
            'image':'str',
            'tag':'str',
            'registry':'str',
            'complete_tag':'str',
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
