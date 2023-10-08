
from pytruenas import Namespace, TrueNASClient
import typing
class Truenas(Namespace):
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
    /) -> 'str|None': 
        """
        Returns the TrueNAS End-User License Agreement (EULA).

        Parameters
        ----------
        Returns
        -------
        str:
            eula
        None:
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
        attach_debug:'bool'=False,
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
        customer_information_update:'CustomerInformationUpdate'={},
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

class SetProduction(typing.TypedDict):
        ticket:'typing.Optional[int]'
        url:'typing.Optional[str]'
        has_debug:'bool'
        ...
class CustomerInformationUpdate(typing.TypedDict):
        company:'str'
        administrative_user:'AdministrativeUser'
        technical_user:'TechnicalUser'
        reseller:'Reseller'
        physical_location:'PhysicalLocation'
        primary_use_case:'str'
        other_primary_use_case:'str'
        ...
class AdministrativeUser(typing.TypedDict):
        first_name:'str'
        last_name:'str'
        title:'str'
        office_phone:'str'
        mobile_phone:'str'
        primary_email:'str'
        secondary_email:'str'
        address:'str'
        city:'str'
        state:'str'
        zip:'str'
        country:'str'
        ...
class TechnicalUser(typing.TypedDict):
        first_name:'str'
        last_name:'str'
        title:'str'
        office_phone:'str'
        mobile_phone:'str'
        primary_email:'str'
        secondary_email:'str'
        address:'str'
        city:'str'
        state:'str'
        zip:'str'
        country:'str'
        ...
class Reseller(typing.TypedDict):
        company:'str'
        first_name:'str'
        last_name:'str'
        title:'str'
        office_phone:'str'
        mobile_phone:'str'
        ...
class PhysicalLocation(typing.TypedDict):
        address:'str'
        city:'str'
        state:'str'
        zip:'str'
        country:'str'
        contact_name:'str'
        contact_phone_number:'str'
        contact_email:'str'
        ...
