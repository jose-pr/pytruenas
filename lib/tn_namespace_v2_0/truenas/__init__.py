
from pytruenas import Namespace
import typing
class Truenas(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'truenas')

    SetProduction = typing.TypedDict('SetProduction', {
            'ticket':'typing.Optional[int]',
            'url':'typing.Optional[str]',
            'has_debug':'bool',
    })
    AdministrativeUser = typing.TypedDict('AdministrativeUser', {
            'first_name':'str',
            'last_name':'str',
            'title':'str',
            'office_phone':'str',
            'mobile_phone':'str',
            'primary_email':'str',
            'secondary_email':'str',
            'address':'str',
            'city':'str',
            'state':'str',
            'zip':'str',
            'country':'str',
    })
    TechnicalUser = typing.TypedDict('TechnicalUser', {
            'first_name':'str',
            'last_name':'str',
            'title':'str',
            'office_phone':'str',
            'mobile_phone':'str',
            'primary_email':'str',
            'secondary_email':'str',
            'address':'str',
            'city':'str',
            'state':'str',
            'zip':'str',
            'country':'str',
    })
    Reseller = typing.TypedDict('Reseller', {
            'company':'str',
            'first_name':'str',
            'last_name':'str',
            'title':'str',
            'office_phone':'str',
            'mobile_phone':'str',
    })
    PhysicalLocation = typing.TypedDict('PhysicalLocation', {
            'address':'str',
            'city':'str',
            'state':'str',
            'zip':'str',
            'country':'str',
            'contact_name':'str',
            'contact_phone_number':'str',
            'contact_email':'str',
    })
    CustomerInformationUpdate = typing.TypedDict('CustomerInformationUpdate', {
            'company':'str',
            'administrative_user':'AdministrativeUser',
            'technical_user':'TechnicalUser',
            'reseller':'Reseller',
            'physical_location':'PhysicalLocation',
            'primary_use_case':'str',
            'other_primary_use_case':'str',
    })
