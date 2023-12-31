
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin
from enum import Enum
import typing
class SystemGeneral(
    ConfigMixin,
    Namespace
    ):
    _namespace:typing.Literal['system.general']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
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
    @typing.overload
    def checkin_waiting(self, 
    /) -> 'typing.Optional[int]': 
        """
        Determines whether or not we are waiting user to check-in the applied UI settings changes before they are rolled
        back. Returns a number of seconds before the automatic rollback or null if there are no changes pending.

        Parameters
        ----------
        Returns
        -------
        typing.Optional[int]:
            remaining_seconds
        """
        ...
    @typing.overload
    def config(self, 
    /) -> 'SystemGeneralEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        SystemGeneralEntry:
            system_general_entry
        """
        ...
    @typing.overload
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
    @typing.overload
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
    @typing.overload
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
    @typing.overload
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
    @typing.overload
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
    @typing.overload
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
    @typing.overload
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
    @typing.overload
    def ui_httpsprotocols_choices(self, 
    /) -> 'UiHttpsProtocols': 
        """
        Returns available HTTPS protocols.

        Parameters
        ----------
        Returns
        -------
        UiHttpsProtocols:
            UI HTTPS Protocol Choices
        """
        ...
    @typing.overload
    def ui_restart(self, 
        _delay:'int',
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
    @typing.overload
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
    @typing.overload
    def update(self, 
        _general_settings:'GeneralSettings',
    /) -> 'SystemGeneralUpdateReturns': 
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
        SystemGeneralUpdateReturns:
            system_general_update_returns
        """
        ...
    GeneralSettings = typing.TypedDict('GeneralSettings', {
            'ui_httpsport':'int',
            'ui_httpsredirect':'bool',
            'ui_httpsprotocols':'list[Protocol]',
            'ui_port':'int',
            'ui_address':'list[str]',
            'ui_v6address':'list[str]',
            'ui_allowlist':'list[str]',
            'ui_consolemsg':'bool',
            'ui_x_frame_options':'UiXFrameOptions',
            'kbdmap':'str',
            'language':'str',
            'timezone':'str',
            'usage_collection':'typing.Optional[bool]',
            'birthday':'str',
            'ds_auth':'bool',
            'ui_certificate':'typing.Optional[int]',
            'rollback_timeout':'typing.Optional[int]',
            'ui_restart_delay':'typing.Optional[int]',
    })
    class Protocol(str,Enum):
        TLSv1 = 'TLSv1'
        TLSv11 = 'TLSv1.1'
        TLSv12 = 'TLSv1.2'
        TLSv13 = 'TLSv1.3'
        ...
    SystemGeneralEntry = typing.TypedDict('SystemGeneralEntry', {
            'ui_certificate':'UiCertificate',
            'ui_httpsport':'int',
            'ui_httpsredirect':'bool',
            'ui_httpsprotocols':'list[Protocol]',
            'ui_port':'int',
            'ui_address':'list[str]',
            'ui_v6address':'list[str]',
            'ui_allowlist':'list[str]',
            'ui_consolemsg':'bool',
            'ui_x_frame_options':'UiXFrameOptions',
            'kbdmap':'str',
            'language':'str',
            'timezone':'str',
            'usage_collection':'typing.Optional[bool]',
            'birthday':'str',
            'wizardshown':'bool',
            'usage_collection_is_set':'bool',
            'ds_auth':'bool',
            'id':'int',
    })
    SystemGeneralUpdateReturns = typing.TypedDict('SystemGeneralUpdateReturns', {
            'ui_certificate':'UiCertificate',
            'ui_httpsport':'int',
            'ui_httpsredirect':'bool',
            'ui_httpsprotocols':'list[Protocol]',
            'ui_port':'int',
            'ui_address':'list[str]',
            'ui_v6address':'list[str]',
            'ui_allowlist':'list[str]',
            'ui_consolemsg':'bool',
            'ui_x_frame_options':'UiXFrameOptions',
            'kbdmap':'str',
            'language':'str',
            'timezone':'str',
            'usage_collection':'typing.Optional[bool]',
            'birthday':'str',
            'wizardshown':'bool',
            'usage_collection_is_set':'bool',
            'ds_auth':'bool',
            'id':'int',
    })
    UiCertificate = typing.TypedDict('UiCertificate', {
            'id':'int',
            'type':'int',
            'name':'str',
            'certificate':'typing.Optional[str]',
            'privatekey':'typing.Optional[str]',
            'CSR':'typing.Optional[str]',
            'acme_uri':'typing.Optional[str]',
            'domains_authenticators':'dict[str]',
            'renew_days':'int',
            'revoked_date':'typing.Optional[str]',
            'signedby':'dict[str]',
            'root_path':'str',
            'acme':'dict[str]',
            'certificate_path':'typing.Optional[str]',
            'privatekey_path':'typing.Optional[str]',
            'csr_path':'typing.Optional[str]',
            'cert_type':'str',
            'revoked':'bool',
            'expired':'typing.Optional[bool]',
            'issuer':'typing.Union[str, NoneType, dict[str]]',
            'chain_list':'list[str]',
            'country':'typing.Optional[str]',
            'state':'typing.Optional[str]',
            'city':'typing.Optional[str]',
            'organization':'typing.Optional[str]',
            'organizational_unit':'typing.Optional[str]',
            'san':'typing.Optional[list]',
            'email':'typing.Optional[str]',
            'DN':'typing.Optional[str]',
            'subject_name_hash':'typing.Optional[str]',
            'digest_algorithm':'typing.Optional[str]',
            'from':'typing.Optional[str]',
            'common':'typing.Optional[str]',
            'until':'typing.Optional[str]',
            'fingerprint':'typing.Optional[str]',
            'key_type':'typing.Optional[str]',
            'internal':'typing.Optional[str]',
            'lifetime':'typing.Optional[int]',
            'serial':'typing.Optional[int]',
            'key_length':'typing.Optional[int]',
            'chain':'typing.Optional[bool]',
            'CA_type_existing':'bool',
            'CA_type_internal':'bool',
            'CA_type_intermediate':'bool',
            'cert_type_existing':'bool',
            'cert_type_internal':'bool',
            'cert_type_CSR':'bool',
            'parsed':'bool',
            'can_be_revoked':'bool',
            'extensions':'dict[str]',
            'revoked_certs':'list',
            'crl_path':'str',
            'signed_certificates':'int',
    })
    UiHttpsProtocols = typing.TypedDict('UiHttpsProtocols', {
            'TLSv1':'typing.Literal["TLSv1"]',
            'TLSv1.1':'typing.Literal["TLSv1.1"]',
            'TLSv1.2':'typing.Literal["TLSv1.2"]',
            'TLSv1.3':'typing.Literal["TLSv1.3"]',
    })
    class UiXFrameOptions(str,Enum):
        SAMEORIGIN = 'SAMEORIGIN'
        DENY = 'DENY'
        ALLOWALL = 'ALLOW_ALL'
        ...
