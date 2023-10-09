
from pytruenas.base import Namespace

import typing
from enum import Enum

class Update(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'update')

    UpdateCheckAvailable = typing.TypedDict('UpdateCheckAvailable', {
            'train':'str',
    })
    Updatefile = typing.TypedDict('Updatefile', {
            'resume':'bool',
            'destination':'typing.Optional[str]',
    })
    Options = typing.TypedDict('Options', {
            'dataset_name':'typing.Optional[str]',
            'resume':'bool',
            'cleanup':'bool',
    })
    Update = typing.TypedDict('Update', {
            'dataset_name':'typing.Optional[str]',
            'resume':'bool',
            'train':'typing.Optional[str]',
            'reboot':'bool',
    })
