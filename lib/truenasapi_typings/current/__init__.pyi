from pytruenas import Namespace as _NS
from pytruenas.models import jsonschema as _jsonschema
import typing as _ty
from .acme import Acme
from .alert import Alert
from .alertclasses import Alertclasses
from .alertservice import Alertservice
from .api_key import ApiKey
from .app import App
from .auth import Auth
from .boot import Boot
from .catalog import Catalog
from .certificate import Certificate
from .cloud_backup import CloudBackup
from .cloudsync import Cloudsync
from .config import Config
from .core import Core
from .cronjob import Cronjob
from .device import Device
from .disk import Disk
from .docker import Docker
from .enclosure import Enclosure
from .failover import Failover
from .filesystem import Filesystem
from .ftp import Ftp
from .group import Group
from .initshutdownscript import Initshutdownscript
from .ipmi import Ipmi
from .iscsi import Iscsi
from .k8s_to_docker import K8sToDocker
from .keychaincredential import Keychaincredential
from .nfs import Nfs
from .pool import Pool
from .privilege import Privilege
from .reporting import Reporting
from .sharing import Sharing
from .smb import Smb
from .snmp import Snmp
from .staticroute import Staticroute
from .system import System
from .tn_connect import TnConnect
from .truenas import Truenas
from .user import User
from .virt import Virt 
class Current(_NS):
    
    acme: Acme
    alert: Alert
    alertclasses: Alertclasses
    alertservice: Alertservice
    api_key: ApiKey
    app: App
    auth: Auth
    boot: Boot
    catalog: Catalog
    certificate: Certificate
    cloud_backup: CloudBackup
    cloudsync: Cloudsync
    config: Config
    core: Core
    cronjob: Cronjob
    device: Device
    disk: Disk
    docker: Docker
    enclosure: Enclosure
    failover: Failover
    filesystem: Filesystem
    ftp: Ftp
    group: Group
    initshutdownscript: Initshutdownscript
    ipmi: Ipmi
    iscsi: Iscsi
    k8s_to_docker: K8sToDocker
    keychaincredential: Keychaincredential
    nfs: Nfs
    pool: Pool
    privilege: Privilege
    reporting: Reporting
    sharing: Sharing
    smb: Smb
    snmp: Snmp
    staticroute: Staticroute
    system: System
    tn_connect: TnConnect
    truenas: Truenas
    user: User
    virt: Virt