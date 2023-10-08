
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class SystemGeneral(Namespace):
    _namespace:_ty.Literal['system.general']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def checkin(self, 
    /) -> None: 
        """
        After UI settings are saved with `rollback_timeout` this method needs to be called within that timeout limit
        to prevent reverting the changes.
        
        This is to ensure user verifies the changes went as planned and its working.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @_ty.overload
    def checkin_waiting(self, 
    /) -> 'int|None': 
        """
        Determines whether or not we are waiting user to check-in the applied UI settings changes before they are rolled
        back. Returns a number of seconds before the automatic rollback or null if there are no changes pending.

        Parameters
        ----------
        Returns
        -------
        int:
            remaining_seconds
        None:
            remaining_seconds
        """
        ...
    @_ty.overload
    def config(self, 
    /) -> 'dict[str]': 
        """
        

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            system_general_entry
        """
        ...
    @_ty.overload
    def country_choices(self, 
    /) -> 'dict[str]': 
        """
        Returns country choices.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            country_choices
        """
        ...
    @_ty.overload
    def kbdmap_choices(self, 
    /) -> 'dict[str]': 
        """
        Returns kbdmap choices.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            kbdmap_choices
        """
        ...
    @_ty.overload
    def language_choices(self, 
    /) -> 'dict[str]': 
        """
        Returns language choices.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            System Language Choices
        """
        ...
    @_ty.overload
    def local_url(self, 
    /) -> 'str': 
        """
        Returns configured local url in the format of protocol://host:port

        Parameters
        ----------
        Returns
        -------
        str:
            local_url
        """
        ...
    @_ty.overload
    def timezone_choices(self, 
    /) -> 'dict[str]': 
        """
        Returns available timezones

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            System Timezone Choices
        """
        ...
    @_ty.overload
    def ui_address_choices(self, 
    /) -> 'dict[str]': 
        """
        Returns UI ipv4 address choices.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            Available UI IPv4 Address Choices
        """
        ...
    @_ty.overload
    def ui_certificate_choices(self, 
    /) -> 'dict[str]': 
        """
        Return choices of certificates which can be used for `ui_certificate`.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            UI Certificate Choices
        """
        ...
    @_ty.overload
    def ui_httpsprotocols_choices(self, 
    /) -> 'dict[str]': 
        """
        Returns available HTTPS protocols.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            UI HTTPS Protocol Choices
        """
        ...
    @_ty.overload
    def ui_restart(self, 
        delay:'int'=3,
    /) -> None: 
        """
        Restart HTTP server to use latest UI settings.
        
        HTTP server will be restarted after `delay` seconds.

        Parameters
        ----------
        delay:
            delay
        Returns
        -------
        """
        ...
    @_ty.overload
    def ui_v6address_choices(self, 
    /) -> 'dict[str]': 
        """
        Returns UI ipv6 address choices.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            Available UI IPv6 Address Choices
        """
        ...
    @_ty.overload
    def update(self, 
        general_settings:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update System General Service Configuration.
        
        `ui_certificate` is used to enable HTTPS access to the system. If `ui_certificate` is not configured on boot,
        it is automatically created by the system.
        
        `ui_httpsredirect` when set, makes sure that all HTTP requests are converted to HTTPS requests to better
        enhance security.
        
        `ui_address` and `ui_v6address` are a list of valid ipv4/ipv6 addresses respectively which the system will
        listen on.
        
        `ui_allowlist` is a list of IP addresses and networks that are allow to use API and UI. If this list is empty,
        then all IP addresses are allowed to use API and UI.
        
        `ds_auth` controls whether configured Directory Service users that are granted with Privileges are allowed to
        log in to the Web UI or use TrueNAS API.
        
        UI configuration is not applied automatically. Call `system.general.ui_restart` to apply new UI settings (all
        HTTP connections will be aborted) or specify `ui_restart_delay` (in seconds) to automatically apply them after
        some small amount of time necessary you might need to receive the response for your settings update request.
        
        If incorrect UI configuration is applied, you might loss API connectivity and won't be able to fix the settings.
        To avoid that, specify `rollback_timeout` (in seconds). It will automatically roll back UI configuration to the
        previously working settings after `rollback_timeout` passes unless you call `system.general.checkin` in case
        the new settings were correct and no rollback is necessary.

        Parameters
        ----------
        general_settings:
            general_settings
        Returns
        -------
        dict[str]:
            system_general_update_returns
        """
        ...
