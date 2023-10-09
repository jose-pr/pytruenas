
from pytruenas import TrueNASClient
from pytruenas.base import Namespace
from pytruenas.mixins import ConfigMixin
from enum import Enum
import typing
class Kmip(
    ConfigMixin,
    Namespace
    ):
    _namespace:typing.Literal['kmip']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def clear_sync_pending_keys(self, 
    /) -> None: 
        """
        Clear all keys which are pending to be synced between KMIP server and TN database.
        
        For ZFS/SED keys, we remove the UID from local database with which we are able to retrieve ZFS/SED keys.
        It should be used with caution.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def config(self, 
    /) -> 'KmipEntry': 
        """
        

        Parameters
        ----------
        Returns
        -------
        KmipEntry:
            kmip_entry
        """
        ...
    @typing.overload
    def kmip_sync_pending(self, 
    /) -> 'bool': 
        """
        Returns true or false based on if there are keys which are to be synced from local database to remote KMIP
        server or vice versa.

        Parameters
        ----------
        Returns
        -------
        bool:
            pending_kmip_sync
        """
        ...
    @typing.overload
    def ssl_version_choices(self, 
    /) -> 'SslVersionChoices': 
        """
        Retrieve valid SSL version choices to be used when configuring kmip service.

        Parameters
        ----------
        Returns
        -------
        SslVersionChoices:
            ssl_version_choices
        """
        ...
    @typing.overload
    def sync_keys(self, 
    /) -> None: 
        """
        Sync ZFS/SED keys between KMIP Server and TN database.

        Parameters
        ----------
        Returns
        -------
        """
        ...
    @typing.overload
    def update(self, 
        kmip_update:'KmipUpdate'={},
    /) -> 'KmipUpdateReturns': 
        """
        Update KMIP Server Configuration.
        
        System currently authenticates connection with remote KMIP Server with a TLS handshake. `certificate` and
        `certificate_authority` determine the certs which will be used to initiate the TLS handshake with `server`.
        
        `validate` is enabled by default. When enabled, system will test connection to `server` making sure
        it's reachable.
        
        `manage_zfs_keys`/`manage_sed_disks` when enabled will sync keys from local database to remote KMIP server.
        When disabled, if there are any keys left to be retrieved from the KMIP server,
        it will sync them back to local database.
        
        `enabled` if true, cannot be set to disabled if there are existing keys pending to be synced. However users
        can still perform this action by enabling `force_clear`.
        
        `ssl_version` can be specified to match the ssl configuration being used by KMIP server.
        
        `change_server` is a boolean field which allows users to migrate data between two KMIP servers. System
        will first migrate keys from old KMIP server to local database and then migrate the keys from local database
        to new KMIP server. If it is unable to retrieve all the keys from old server, this will fail. Users can bypass
        this by enabling `force_clear`.
        
        `force_clear` is a boolean option which when enabled will in this case remove all
        pending keys to be synced from database. It should be used with extreme caution as users may end up with
        not having ZFS dataset or SED disks keys leaving them locked forever. It is disabled by default.

        Parameters
        ----------
        kmip_update:
            kmip_update
        Returns
        -------
        KmipUpdateReturns:
            kmip_update_returns
        """
        ...
    class SslVersion(str,Enum):
        PROTOCOLTLSv1 = 'PROTOCOL_TLSv1'
        PROTOCOLTLSv11 = 'PROTOCOL_TLSv1_1'
        PROTOCOLTLSv12 = 'PROTOCOL_TLSv1_2'
        ...
    KmipEntry = typing.TypedDict('KmipEntry', {
            'id':'int',
            'enabled':'bool',
            'manage_sed_disks':'bool',
            'manage_zfs_keys':'bool',
            'certificate':'typing.Optional[int]',
            'certificate_authority':'typing.Optional[int]',
            'port':'int',
            'server':'typing.Optional[str]',
            'ssl_version':'SslVersion',
    })
    class PROTOCOLTLSv1(str,Enum):
        PROTOCOLTLSv1 = 'PROTOCOL_TLSv1'
        ...
    class PROTOCOLTLSv11(str,Enum):
        PROTOCOLTLSv11 = 'PROTOCOL_TLSv1_1'
        ...
    class PROTOCOLTLSv12(str,Enum):
        PROTOCOLTLSv12 = 'PROTOCOL_TLSv1_2'
        ...
    SslVersionChoices = typing.TypedDict('SslVersionChoices', {
            'PROTOCOL_TLSv1':'PROTOCOLTLSv1',
            'PROTOCOL_TLSv1_1':'PROTOCOLTLSv11',
            'PROTOCOL_TLSv1_2':'PROTOCOLTLSv12',
    })
    KmipUpdate = typing.TypedDict('KmipUpdate', {
            'enabled':'bool',
            'manage_sed_disks':'bool',
            'manage_zfs_keys':'bool',
            'certificate':'typing.Optional[int]',
            'certificate_authority':'typing.Optional[int]',
            'port':'int',
            'server':'typing.Optional[str]',
            'ssl_version':'SslVersion',
            'force_clear':'bool',
            'change_server':'bool',
            'validate':'bool',
    })
    KmipUpdateReturns = typing.TypedDict('KmipUpdateReturns', {
            'id':'int',
            'enabled':'bool',
            'manage_sed_disks':'bool',
            'manage_zfs_keys':'bool',
            'certificate':'typing.Optional[int]',
            'certificate_authority':'typing.Optional[int]',
            'port':'int',
            'server':'typing.Optional[str]',
            'ssl_version':'SslVersion',
    })
