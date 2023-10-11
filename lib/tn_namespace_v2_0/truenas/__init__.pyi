
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from enum import Enum
import typing
class Truenas(
    Namespace
    ):
    _namespace:typing.Literal['truenas']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def accept_eula(self, 
    /) -> None: 
        """
        Accept TrueNAS EULA.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def get_chassis_hardware(self, 
    /) -> 'str': 
        """
        Returns what type of hardware this is, detected from dmidecode.

        Parameters
        ----------
        Returns
        -------
        str:
            system_chassis_hardware
        """
        ...
    @typing.overload
    def get_customer_information(self, 
    /) -> None: 
        """
        Returns stored customer information.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def get_eula(self, 
    /) -> 'typing.Optional[str]': 
        """
        Returns the TrueNAS End-User License Agreement (EULA).

        Parameters
        ----------
        Returns
        -------
        typing.Optional[str]:
            eula
        """
        ...
    @typing.overload
    def is_eula_accepted(self, 
    /) -> 'bool': 
        """
        Returns whether the EULA is accepted or not.

        Parameters
        ----------
        Returns
        -------
        bool:
            system_eula_accepted
        """
        ...
    @typing.overload
    def is_production(self, 
    /) -> 'bool': 
        """
        Returns if system is marked as production.

        Parameters
        ----------
        Returns
        -------
        bool:
            is_production_system
        """
        ...
    @typing.overload
    def set_production(self, 
        production:'bool',
        attach_debug:'bool',
    /) -> 'SetProduction': 
        """
        Sets system production state and optionally sends initial debug.

        Parameters
        ----------
        production:
            production
        attach_debug:
            attach_debug
        Returns
        -------
        SetProduction:
            set_production
        """
        ...
    @typing.overload
    def update_customer_information(self, 
        customer_information_update:'CustomerInformationUpdate',
    /) -> None: 
        """
        Updates customer information.

        Parameters
        ----------
        customer_information_update:
            customer_information_update
        Returns
        -------
        """
        ...
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
    CustomerInformationUpdate = typing.TypedDict('CustomerInformationUpdate', {
            'company':'str',
            'administrative_user':'AdministrativeUser',
            'technical_user':'TechnicalUser',
            'reseller':'Reseller',
            'physical_location':'PhysicalLocation',
            'primary_use_case':'str',
            'other_primary_use_case':'str',
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
    Reseller = typing.TypedDict('Reseller', {
            'company':'str',
            'first_name':'str',
            'last_name':'str',
            'title':'str',
            'office_phone':'str',
            'mobile_phone':'str',
    })
    SetProduction = typing.TypedDict('SetProduction', {
            'ticket':'typing.Optional[int]',
            'url':'typing.Optional[str]',
            'has_debug':'bool',
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
