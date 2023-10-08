
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Truenas(Namespace):
    _namespace:_ty.Literal['truenas']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
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
    @_ty.overload
    def set_production(self, 
        production:'bool',
        attach_debug:'bool'=False,
    /) -> 'dict[str]': 
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
        dict[str]:
            set_production
        """
        ...
    @_ty.overload
    def update_customer_information(self, 
        customer_information_update:'dict[str]'={},
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
