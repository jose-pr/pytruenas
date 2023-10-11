
from pytruenas.base import Namespace

import typing
from enum import Enum

class PoolDataset(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'pool.dataset')

    class Aclmode(str,Enum):
        PASSTHROUGH = 'PASSTHROUGH'
        RESTRICTED = 'RESTRICTED'
        DISCARD = 'DISCARD'
        INHERIT = 'INHERIT'
        ...
    Aclmode_ = typing.TypedDict('Aclmode_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class Acltype(str,Enum):
        OFF = 'OFF'
        NFSV4 = 'NFSV4'
        POSIX = 'POSIX'
        INHERIT = 'INHERIT'
        ...
    Acltype_ = typing.TypedDict('Acltype_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class Algorithm(str,Enum):
        AES128CCM = 'AES-128-CCM'
        AES192CCM = 'AES-192-CCM'
        AES256CCM = 'AES-256-CCM'
        AES128GCM = 'AES-128-GCM'
        AES192GCM = 'AES-192-GCM'
        AES256GCM = 'AES-256-GCM'
        ...
    class Atime(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        INHERIT = 'INHERIT'
        ...
    Atime_ = typing.TypedDict('Atime_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Attachment = typing.TypedDict('Attachment', {
            'type':'str',
            'service':'typing.Optional[str]',
            'attachments':'list[str]',
    })
    Available = typing.TypedDict('Available', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class BASIC(str,Enum):
        FULLCONTROL = 'FULL_CONTROL'
        MODIFY = 'MODIFY'
        READ = 'READ'
        TRAVERSE = 'TRAVERSE'
        ...
    class BASIC_(str,Enum):
        INHERIT = 'INHERIT'
        NOINHERIT = 'NOINHERIT'
        ...
    class Casesensitivity(str,Enum):
        SENSITIVE = 'SENSITIVE'
        INSENSITIVE = 'INSENSITIVE'
        INHERIT = 'INHERIT'
        ...
    Casesensitivity_ = typing.TypedDict('Casesensitivity_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    ChangeKeyOptions = typing.TypedDict('ChangeKeyOptions', {
            'generate_key':'bool',
            'key_file':'bool',
            'pbkdf2iters':'int',
            'passphrase':'typing.Optional[str]',
            'key':'typing.Optional[str]',
    })
    class Checksum(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        FLETCHER2 = 'FLETCHER2'
        FLETCHER4 = 'FLETCHER4'
        SHA256 = 'SHA256'
        SHA512 = 'SHA512'
        SKEIN = 'SKEIN'
        EDONR = 'EDONR'
        INHERIT = 'INHERIT'
        ...
    ChecksumChoices = typing.TypedDict('ChecksumChoices', {
            'ON':'typing.Literal["ON"]',
            'FLETCHER2':'typing.Literal["FLETCHER2"]',
            'FLETCHER4':'typing.Literal["FLETCHER4"]',
            'SHA256':'typing.Literal["SHA256"]',
            'SHA512':'typing.Literal["SHA512"]',
            'SKEIN':'typing.Literal["SKEIN"]',
            'EDONR':'typing.Literal["EDONR"]',
    })
    Checksum_ = typing.TypedDict('Checksum_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Comments = typing.TypedDict('Comments', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class Compression(str,Enum):
        OFF = 'OFF'
        LZ4 = 'LZ4'
        GZIP = 'GZIP'
        GZIP1 = 'GZIP-1'
        GZIP9 = 'GZIP-9'
        ZSTD = 'ZSTD'
        ZSTDFAST = 'ZSTD-FAST'
        ZLE = 'ZLE'
        LZJB = 'LZJB'
        ZSTD1 = 'ZSTD-1'
        ZSTD2 = 'ZSTD-2'
        ZSTD3 = 'ZSTD-3'
        ZSTD4 = 'ZSTD-4'
        ZSTD5 = 'ZSTD-5'
        ZSTD6 = 'ZSTD-6'
        ZSTD7 = 'ZSTD-7'
        ZSTD8 = 'ZSTD-8'
        ZSTD9 = 'ZSTD-9'
        ZSTD10 = 'ZSTD-10'
        ZSTD11 = 'ZSTD-11'
        ZSTD12 = 'ZSTD-12'
        ZSTD13 = 'ZSTD-13'
        ZSTD14 = 'ZSTD-14'
        ZSTD15 = 'ZSTD-15'
        ZSTD16 = 'ZSTD-16'
        ZSTD17 = 'ZSTD-17'
        ZSTD18 = 'ZSTD-18'
        ZSTD19 = 'ZSTD-19'
        ZSTDFAST1 = 'ZSTD-FAST-1'
        ZSTDFAST2 = 'ZSTD-FAST-2'
        ZSTDFAST3 = 'ZSTD-FAST-3'
        ZSTDFAST4 = 'ZSTD-FAST-4'
        ZSTDFAST5 = 'ZSTD-FAST-5'
        ZSTDFAST6 = 'ZSTD-FAST-6'
        ZSTDFAST7 = 'ZSTD-FAST-7'
        ZSTDFAST8 = 'ZSTD-FAST-8'
        ZSTDFAST9 = 'ZSTD-FAST-9'
        ZSTDFAST10 = 'ZSTD-FAST-10'
        ZSTDFAST20 = 'ZSTD-FAST-20'
        ZSTDFAST30 = 'ZSTD-FAST-30'
        ZSTDFAST40 = 'ZSTD-FAST-40'
        ZSTDFAST50 = 'ZSTD-FAST-50'
        ZSTDFAST60 = 'ZSTD-FAST-60'
        ZSTDFAST70 = 'ZSTD-FAST-70'
        ZSTDFAST80 = 'ZSTD-FAST-80'
        ZSTDFAST90 = 'ZSTD-FAST-90'
        ZSTDFAST100 = 'ZSTD-FAST-100'
        ZSTDFAST500 = 'ZSTD-FAST-500'
        ZSTDFAST1000 = 'ZSTD-FAST-1000'
        INHERIT = 'INHERIT'
        ...
    CompressionChoices = typing.TypedDict('CompressionChoices', {
            'OFF':'typing.Literal["OFF"]',
            'LZ4':'typing.Literal["LZ4"]',
            'GZIP':'typing.Literal["GZIP"]',
            'GZIP-1':'typing.Literal["GZIP-1"]',
            'GZIP-9':'typing.Literal["GZIP-9"]',
            'ZSTD':'typing.Literal["ZSTD"]',
            'ZSTD-FAST':'typing.Literal["ZSTD-FAST"]',
            'ZLE':'typing.Literal["ZLE"]',
            'LZJB':'typing.Literal["LZJB"]',
            'ZSTD-1':'typing.Literal["ZSTD-1"]',
            'ZSTD-2':'typing.Literal["ZSTD-2"]',
            'ZSTD-3':'typing.Literal["ZSTD-3"]',
            'ZSTD-4':'typing.Literal["ZSTD-4"]',
            'ZSTD-5':'typing.Literal["ZSTD-5"]',
            'ZSTD-6':'typing.Literal["ZSTD-6"]',
            'ZSTD-7':'typing.Literal["ZSTD-7"]',
            'ZSTD-8':'typing.Literal["ZSTD-8"]',
            'ZSTD-9':'typing.Literal["ZSTD-9"]',
            'ZSTD-10':'typing.Literal["ZSTD-10"]',
            'ZSTD-11':'typing.Literal["ZSTD-11"]',
            'ZSTD-12':'typing.Literal["ZSTD-12"]',
            'ZSTD-13':'typing.Literal["ZSTD-13"]',
            'ZSTD-14':'typing.Literal["ZSTD-14"]',
            'ZSTD-15':'typing.Literal["ZSTD-15"]',
            'ZSTD-16':'typing.Literal["ZSTD-16"]',
            'ZSTD-17':'typing.Literal["ZSTD-17"]',
            'ZSTD-18':'typing.Literal["ZSTD-18"]',
            'ZSTD-19':'typing.Literal["ZSTD-19"]',
            'ZSTD-FAST-1':'typing.Literal["ZSTD-FAST-1"]',
            'ZSTD-FAST-2':'typing.Literal["ZSTD-FAST-2"]',
            'ZSTD-FAST-3':'typing.Literal["ZSTD-FAST-3"]',
            'ZSTD-FAST-4':'typing.Literal["ZSTD-FAST-4"]',
            'ZSTD-FAST-5':'typing.Literal["ZSTD-FAST-5"]',
            'ZSTD-FAST-6':'typing.Literal["ZSTD-FAST-6"]',
            'ZSTD-FAST-7':'typing.Literal["ZSTD-FAST-7"]',
            'ZSTD-FAST-8':'typing.Literal["ZSTD-FAST-8"]',
            'ZSTD-FAST-9':'typing.Literal["ZSTD-FAST-9"]',
            'ZSTD-FAST-10':'typing.Literal["ZSTD-FAST-10"]',
            'ZSTD-FAST-20':'typing.Literal["ZSTD-FAST-20"]',
            'ZSTD-FAST-30':'typing.Literal["ZSTD-FAST-30"]',
            'ZSTD-FAST-40':'typing.Literal["ZSTD-FAST-40"]',
            'ZSTD-FAST-50':'typing.Literal["ZSTD-FAST-50"]',
            'ZSTD-FAST-60':'typing.Literal["ZSTD-FAST-60"]',
            'ZSTD-FAST-70':'typing.Literal["ZSTD-FAST-70"]',
            'ZSTD-FAST-80':'typing.Literal["ZSTD-FAST-80"]',
            'ZSTD-FAST-90':'typing.Literal["ZSTD-FAST-90"]',
            'ZSTD-FAST-100':'typing.Literal["ZSTD-FAST-100"]',
            'ZSTD-FAST-500':'typing.Literal["ZSTD-FAST-500"]',
            'ZSTD-FAST-1000':'typing.Literal["ZSTD-FAST-1000"]',
    })
    Compression_ = typing.TypedDict('Compression_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compressratio = typing.TypedDict('Compressratio', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Copies = typing.TypedDict('Copies', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Creation = typing.TypedDict('Creation', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Dataset = typing.TypedDict('Dataset', {
            'force':'bool',
            'name':'str',
            'key':'str',
            'passphrase':'str',
    })
    DatasetDelete = typing.TypedDict('DatasetDelete', {
            'recursive':'bool',
            'force':'bool',
    })
    DatasetEncryptionSummary = typing.TypedDict('DatasetEncryptionSummary', {
            'name':'str',
            'key_format':'str',
            'key_present_in_database':'bool',
            'valid_key':'bool',
            'locked':'bool',
            'unlock_error':'typing.Optional[str]',
            'unlock_successful':'bool',
    })
    Dataset_ = typing.TypedDict('Dataset_', {
            'force':'bool',
            'name':'str',
            'key':'str',
            'passphrase':'str',
            'recursive':'bool',
    })
    class Deduplication(str,Enum):
        ON = 'ON'
        VERIFY = 'VERIFY'
        OFF = 'OFF'
        INHERIT = 'INHERIT'
        ...
    Deduplication_ = typing.TypedDict('Deduplication_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    EncryptionAlgorithm = typing.TypedDict('EncryptionAlgorithm', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    EncryptionAlgorithmChoices = typing.TypedDict('EncryptionAlgorithmChoices', {
            'AES-128-CCM':'typing.Literal["AES-128-CCM"]',
            'AES-192-CCM':'typing.Literal["AES-192-CCM"]',
            'AES-256-CCM':'typing.Literal["AES-256-CCM"]',
            'AES-128-GCM':'typing.Literal["AES-128-GCM"]',
            'AES-192-GCM':'typing.Literal["AES-192-GCM"]',
            'AES-256-GCM':'typing.Literal["AES-256-GCM"]',
    })
    EncryptionOptions = typing.TypedDict('EncryptionOptions', {
            'generate_key':'bool',
            'pbkdf2iters':'int',
            'algorithm':'Algorithm',
            'passphrase':'typing.Optional[str]',
            'key':'typing.Optional[str]',
    })
    EncryptionRootSummaryOptions = typing.TypedDict('EncryptionRootSummaryOptions', {
            'key_file':'bool',
            'force':'bool',
            'datasets':'list[Dataset]',
    })
    class Exec(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        INHERIT = 'INHERIT'
        ...
    Exec_ = typing.TypedDict('Exec_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Flags = typing.TypedDict('Flags', {
            'FILE_INHERIT':'bool',
            'DIRECTORY_INHERIT':'bool',
            'NO_PROPAGATE_INHERIT':'bool',
            'INHERIT_ONLY':'bool',
            'INHERITED':'bool',
            'BASIC':'BASIC_',
    })
    KeyFormat = typing.TypedDict('KeyFormat', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    LockOptions = typing.TypedDict('LockOptions', {
            'force_umount':'bool',
    })
    Managedby = typing.TypedDict('Managedby', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Nfs4Ace = typing.TypedDict('Nfs4Ace', {
            'tag':'Tag',
            'id':'typing.Optional[int]',
            'type':'Type_',
            'perms':'Perms',
            'flags':'Flags',
    })
    Options = typing.TypedDict('Options', {
            'set_default_acl':'bool',
            'stripacl':'bool',
            'recursive':'bool',
            'traverse':'bool',
    })
    Origin = typing.TypedDict('Origin', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Pbkdf2iters = typing.TypedDict('Pbkdf2iters', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Perms = typing.TypedDict('Perms', {
            'READ_DATA':'bool',
            'WRITE_DATA':'bool',
            'APPEND_DATA':'bool',
            'READ_NAMED_ATTRS':'bool',
            'WRITE_NAMED_ATTRS':'bool',
            'EXECUTE':'bool',
            'DELETE_CHILD':'bool',
            'READ_ATTRIBUTES':'bool',
            'WRITE_ATTRIBUTES':'bool',
            'DELETE':'bool',
            'READ_ACL':'bool',
            'WRITE_ACL':'bool',
            'WRITE_OWNER':'bool',
            'SYNCHRONIZE':'bool',
            'BASIC':'BASIC',
    })
    Perms_ = typing.TypedDict('Perms_', {
            'READ':'bool',
            'WRITE':'bool',
            'EXECUTE':'bool',
    })
    PoolDatasetCreate = typing.TypedDict('PoolDatasetCreate', {
            'name':'str',
            'type':'Type',
            'volsize':'int',
            'volblocksize':'Volblocksize',
            'sparse':'bool',
            'force_size':'bool',
            'comments':'typing.Union[str, typing.Literal["INHERIT"]]',
            'sync':'Sync',
            'snapdev':'Snapdev',
            'compression':'Compression',
            'atime':'Atime',
            'exec':'Exec',
            'managedby':'typing.Union[str, typing.Literal["INHERIT"]]',
            'quota':'typing.Optional[int]',
            'quota_warning':'typing.Union[int, typing.Literal["INHERIT"]]',
            'quota_critical':'typing.Union[int, typing.Literal["INHERIT"]]',
            'refquota':'typing.Optional[int]',
            'refquota_warning':'typing.Union[int, typing.Literal["INHERIT"]]',
            'refquota_critical':'typing.Union[int, typing.Literal["INHERIT"]]',
            'reservation':'int',
            'refreservation':'int',
            'special_small_block_size':'typing.Union[int, typing.Literal["INHERIT"]]',
            'copies':'typing.Union[int, typing.Literal["INHERIT"]]',
            'snapdir':'Snapdir',
            'deduplication':'Deduplication',
            'checksum':'Checksum',
            'readonly':'Readonly',
            'recordsize':'typing.Union[str, typing.Literal["INHERIT"]]',
            'casesensitivity':'Casesensitivity',
            'aclmode':'Aclmode',
            'acltype':'Acltype',
            'share_type':'ShareType',
            'xattr':'Xattr',
            'encryption_options':'EncryptionOptions',
            'encryption':'bool',
            'inherit_encryption':'bool',
            'user_properties':'list[UserProperty]',
            'create_ancestors':'bool',
    })
    PoolDatasetCreateReturns = typing.TypedDict('PoolDatasetCreateReturns', {
            'id':'str',
            'type':'str',
            'name':'str',
            'pool':'str',
            'encrypted':'bool',
            'encryption_root':'typing.Optional[str]',
            'key_loaded':'typing.Optional[bool]',
            'children':'list',
            'user_properties':'dict[str]',
            'locked':'bool',
            'comments':'Comments',
            'quota_warning':'QuotaWarning',
            'quota_critical':'QuotaCritical',
            'refquota_warning':'RefquotaWarning',
            'refquota_critical':'RefquotaCritical',
            'managedby':'Managedby',
            'deduplication':'Deduplication_',
            'aclmode':'Aclmode_',
            'acltype':'Acltype_',
            'xattr':'Xattr_',
            'atime':'Atime_',
            'casesensitivity':'Casesensitivity_',
            'checksum':'Checksum_',
            'exec':'Exec_',
            'sync':'Sync_',
            'compression':'Compression_',
            'compressratio':'Compressratio',
            'origin':'Origin',
            'quota':'Quota',
            'refquota':'Refquota',
            'reservation':'Reservation',
            'refreservation':'Refreservation',
            'copies':'Copies',
            'snapdir':'Snapdir_',
            'readonly':'Readonly_',
            'recordsize':'Recordsize',
            'sparse':'Sparse',
            'volsize':'Volsize',
            'volblocksize':'Volblocksize_',
            'key_format':'KeyFormat',
            'encryption_algorithm':'EncryptionAlgorithm',
            'used':'Used',
            'usedbychildren':'Usedbychildren',
            'usedbydataset':'Usedbydataset',
            'usedbyrefreservation':'Usedbyrefreservation',
            'usedbysnapshots':'Usedbysnapshots',
            'available':'Available',
            'special_small_block_size':'SpecialSmallBlockSize',
            'pbkdf2iters':'Pbkdf2iters',
            'creation':'Creation',
            'snapdev':'Snapdev_',
            'mountpoint':'typing.Optional[str]',
    })
    PoolDatasetEntry = typing.TypedDict('PoolDatasetEntry', {
            'id':'str',
            'type':'str',
            'name':'str',
            'pool':'str',
            'encrypted':'bool',
            'encryption_root':'typing.Optional[str]',
            'key_loaded':'typing.Optional[bool]',
            'children':'list',
            'user_properties':'dict[str]',
            'locked':'bool',
            'comments':'Comments',
            'quota_warning':'QuotaWarning',
            'quota_critical':'QuotaCritical',
            'refquota_warning':'RefquotaWarning',
            'refquota_critical':'RefquotaCritical',
            'managedby':'Managedby',
            'deduplication':'Deduplication_',
            'aclmode':'Aclmode_',
            'acltype':'Acltype_',
            'xattr':'Xattr_',
            'atime':'Atime_',
            'casesensitivity':'Casesensitivity_',
            'checksum':'Checksum_',
            'exec':'Exec_',
            'sync':'Sync_',
            'compression':'Compression_',
            'compressratio':'Compressratio',
            'origin':'Origin',
            'quota':'Quota',
            'refquota':'Refquota',
            'reservation':'Reservation',
            'refreservation':'Refreservation',
            'copies':'Copies',
            'snapdir':'Snapdir_',
            'readonly':'Readonly_',
            'recordsize':'Recordsize',
            'sparse':'Sparse',
            'volsize':'Volsize',
            'volblocksize':'Volblocksize_',
            'key_format':'KeyFormat',
            'encryption_algorithm':'EncryptionAlgorithm',
            'used':'Used',
            'usedbychildren':'Usedbychildren',
            'usedbydataset':'Usedbydataset',
            'usedbyrefreservation':'Usedbyrefreservation',
            'usedbysnapshots':'Usedbysnapshots',
            'available':'Available',
            'special_small_block_size':'SpecialSmallBlockSize',
            'pbkdf2iters':'Pbkdf2iters',
            'creation':'Creation',
            'snapdev':'Snapdev_',
            'mountpoint':'typing.Optional[str]',
    })
    PoolDatasetPermission = typing.TypedDict('PoolDatasetPermission', {
            'user':'str',
            'group':'str',
            'mode':'typing.Optional[str]',
            'acl':'typing.Union[list[Nfs4Ace], list[Posix1eAce]]',
            'options':'Options',
    })
    PoolDatasetUpdate = typing.TypedDict('PoolDatasetUpdate', {
            'volsize':'int',
            'force_size':'bool',
            'comments':'typing.Union[str, typing.Literal["INHERIT"]]',
            'sync':'Sync',
            'snapdev':'Snapdev',
            'compression':'Compression',
            'atime':'Atime',
            'exec':'Exec',
            'managedby':'typing.Union[str, typing.Literal["INHERIT"]]',
            'quota':'typing.Optional[int]',
            'quota_warning':'typing.Union[int, typing.Literal["INHERIT"]]',
            'quota_critical':'typing.Union[int, typing.Literal["INHERIT"]]',
            'refquota':'typing.Optional[int]',
            'refquota_warning':'typing.Union[int, typing.Literal["INHERIT"]]',
            'refquota_critical':'typing.Union[int, typing.Literal["INHERIT"]]',
            'reservation':'int',
            'refreservation':'int',
            'special_small_block_size':'typing.Union[int, typing.Literal["INHERIT"]]',
            'copies':'typing.Union[int, typing.Literal["INHERIT"]]',
            'snapdir':'Snapdir',
            'deduplication':'Deduplication',
            'checksum':'Checksum',
            'readonly':'Readonly',
            'recordsize':'typing.Union[str, typing.Literal["INHERIT"]]',
            'aclmode':'Aclmode',
            'acltype':'Acltype',
            'xattr':'Xattr',
            'user_properties':'list[UserProperty]',
            'create_ancestors':'bool',
            'user_properties_update':'list[UserProperty_]',
    })
    PoolDatasetUpdateReturns = typing.TypedDict('PoolDatasetUpdateReturns', {
            'id':'str',
            'type':'str',
            'name':'str',
            'pool':'str',
            'encrypted':'bool',
            'encryption_root':'typing.Optional[str]',
            'key_loaded':'typing.Optional[bool]',
            'children':'list',
            'user_properties':'dict[str]',
            'locked':'bool',
            'comments':'Comments',
            'quota_warning':'QuotaWarning',
            'quota_critical':'QuotaCritical',
            'refquota_warning':'RefquotaWarning',
            'refquota_critical':'RefquotaCritical',
            'managedby':'Managedby',
            'deduplication':'Deduplication_',
            'aclmode':'Aclmode_',
            'acltype':'Acltype_',
            'xattr':'Xattr_',
            'atime':'Atime_',
            'casesensitivity':'Casesensitivity_',
            'checksum':'Checksum_',
            'exec':'Exec_',
            'sync':'Sync_',
            'compression':'Compression_',
            'compressratio':'Compressratio',
            'origin':'Origin',
            'quota':'Quota',
            'refquota':'Refquota',
            'reservation':'Reservation',
            'refreservation':'Refreservation',
            'copies':'Copies',
            'snapdir':'Snapdir_',
            'readonly':'Readonly_',
            'recordsize':'Recordsize',
            'sparse':'Sparse',
            'volsize':'Volsize',
            'volblocksize':'Volblocksize_',
            'key_format':'KeyFormat',
            'encryption_algorithm':'EncryptionAlgorithm',
            'used':'Used',
            'usedbychildren':'Usedbychildren',
            'usedbydataset':'Usedbydataset',
            'usedbyrefreservation':'Usedbyrefreservation',
            'usedbysnapshots':'Usedbysnapshots',
            'available':'Available',
            'special_small_block_size':'SpecialSmallBlockSize',
            'pbkdf2iters':'Pbkdf2iters',
            'creation':'Creation',
            'snapdev':'Snapdev_',
            'mountpoint':'typing.Optional[str]',
    })
    Posix1eAce = typing.TypedDict('Posix1eAce', {
            'default':'bool',
            'tag':'Tag_',
            'id':'int',
            'perms':'Perms_',
    })
    Process = typing.TypedDict('Process', {
            'pid':'int',
            'name':'str',
            'service':'str',
            'cmdline':'str',
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
    Quota = typing.TypedDict('Quota', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaCritical = typing.TypedDict('QuotaCritical', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaEntry = typing.TypedDict('QuotaEntry', {
            'quota_type':'QuotaType_',
            'id':'str',
            'quota_value':'typing.Optional[int]',
    })
    class QuotaType(str,Enum):
        USER = 'USER'
        GROUP = 'GROUP'
        DATASET = 'DATASET'
        PROJECT = 'PROJECT'
        ...
    class QuotaType_(str,Enum):
        DATASET = 'DATASET'
        USER = 'USER'
        USEROBJ = 'USEROBJ'
        GROUP = 'GROUP'
        GROUPOBJ = 'GROUPOBJ'
        ...
    QuotaWarning = typing.TypedDict('QuotaWarning', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class Readonly(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        INHERIT = 'INHERIT'
        ...
    Readonly_ = typing.TypedDict('Readonly_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Recordsize = typing.TypedDict('Recordsize', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refquota = typing.TypedDict('Refquota', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaCritical = typing.TypedDict('RefquotaCritical', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaWarning = typing.TypedDict('RefquotaWarning', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refreservation = typing.TypedDict('Refreservation', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Reservation = typing.TypedDict('Reservation', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class ShareType(str,Enum):
        GENERIC = 'GENERIC'
        SMB = 'SMB'
        APPS = 'APPS'
        ...
    class Snapdev(str,Enum):
        HIDDEN = 'HIDDEN'
        VISIBLE = 'VISIBLE'
        INHERIT = 'INHERIT'
        ...
    Snapdev_ = typing.TypedDict('Snapdev_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class Snapdir(str,Enum):
        VISIBLE = 'VISIBLE'
        HIDDEN = 'HIDDEN'
        INHERIT = 'INHERIT'
        ...
    Snapdir_ = typing.TypedDict('Snapdir_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    SnapshotSpec = typing.TypedDict('SnapshotSpec', {
            'start':'str',
            'end':'str',
    })
    Snapshots = typing.TypedDict('Snapshots', {
            'all':'bool',
            'recursive':'bool',
            'snapshots':'list[SnapshotSpec]',
    })
    Sparse = typing.TypedDict('Sparse', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    SpecialSmallBlockSize = typing.TypedDict('SpecialSmallBlockSize', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class Sync(str,Enum):
        STANDARD = 'STANDARD'
        ALWAYS = 'ALWAYS'
        DISABLED = 'DISABLED'
        INHERIT = 'INHERIT'
        ...
    Sync_ = typing.TypedDict('Sync_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class Tag(str,Enum):
        Owner = 'owner@'
        Group = 'group@'
        Everyone = 'everyone@'
        USER = 'USER'
        GROUP = 'GROUP'
        ...
    class Tag_(str,Enum):
        USEROBJ = 'USER_OBJ'
        GROUPOBJ = 'GROUP_OBJ'
        USER = 'USER'
        GROUP = 'GROUP'
        OTHER = 'OTHER'
        MASK = 'MASK'
        ...
    class Type(str,Enum):
        FILESYSTEM = 'FILESYSTEM'
        VOLUME = 'VOLUME'
        ...
    class Type_(str,Enum):
        ALLOW = 'ALLOW'
        DENY = 'DENY'
        ...
    Unlock = typing.TypedDict('Unlock', {
            'unlocked':'list[str]',
            'failed':'dict[str]',
    })
    UnlockOptions = typing.TypedDict('UnlockOptions', {
            'force':'bool',
            'key_file':'bool',
            'recursive':'bool',
            'toggle_attachments':'bool',
            'datasets':'list[Dataset_]',
    })
    Used = typing.TypedDict('Used', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbychildren = typing.TypedDict('Usedbychildren', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbydataset = typing.TypedDict('Usedbydataset', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbyrefreservation = typing.TypedDict('Usedbyrefreservation', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbysnapshots = typing.TypedDict('Usedbysnapshots', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    UserProperty = typing.TypedDict('UserProperty', {
            'key':'str',
            'value':'str',
    })
    UserProperty_ = typing.TypedDict('UserProperty_', {
            'key':'str',
            'value':'str',
            'remove':'bool',
    })
    class Volblocksize(str,Enum):
        _512 = '512'
        _512B = '512B'
        _1K = '1K'
        _2K = '2K'
        _4K = '4K'
        _8K = '8K'
        _16K = '16K'
        _32K = '32K'
        _64K = '64K'
        _128K = '128K'
        ...
    Volblocksize_ = typing.TypedDict('Volblocksize_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volsize = typing.TypedDict('Volsize', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    class Xattr(str,Enum):
        ON = 'ON'
        SA = 'SA'
        INHERIT = 'INHERIT'
        ...
    Xattr_ = typing.TypedDict('Xattr_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
