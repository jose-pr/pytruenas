
from pytruenas.base import Namespace
from pytruenas.mixins import TableExtMixin

import typing
from enum import Enum

class PoolDataset(TableExtMixin, Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'pool.dataset')

    Attachment = typing.TypedDict('Attachment', {
            'type':'str',
            'service':'typing.Optional[str]',
            'attachments':'list[str]',
    })
    ChangeKeyOptions = typing.TypedDict('ChangeKeyOptions', {
            'generate_key':'bool',
            'key_file':'bool',
            'pbkdf2iters':'int',
            'passphrase':'typing.Optional[str]',
            'key':'typing.Optional[str]',
    })
    ChecksumChoices = typing.TypedDict('ChecksumChoices', {
            'ON':'ON',
            'FLETCHER2':'FLETCHER2',
            'FLETCHER4':'FLETCHER4',
            'SHA256':'SHA256',
            'SHA512':'SHA512',
            'SKEIN':'SKEIN',
            'EDONR':'EDONR',
    })
    class ON(str,Enum):
        ON = 'ON'
        ...
    class FLETCHER2(str,Enum):
        FLETCHER2 = 'FLETCHER2'
        ...
    class FLETCHER4(str,Enum):
        FLETCHER4 = 'FLETCHER4'
        ...
    class SHA256(str,Enum):
        SHA256 = 'SHA256'
        ...
    class SHA512(str,Enum):
        SHA512 = 'SHA512'
        ...
    class SKEIN(str,Enum):
        SKEIN = 'SKEIN'
        ...
    class EDONR(str,Enum):
        EDONR = 'EDONR'
        ...
    CompressionChoices = typing.TypedDict('CompressionChoices', {
            'OFF':'OFF',
            'LZ4':'LZ4',
            'GZIP':'GZIP',
            'GZIP-1':'GZIP1',
            'GZIP-9':'GZIP9',
            'ZSTD':'ZSTD',
            'ZSTD-FAST':'ZSTDFAST',
            'ZLE':'ZLE',
            'LZJB':'LZJB',
            'ZSTD-1':'ZSTD1',
            'ZSTD-2':'ZSTD2',
            'ZSTD-3':'ZSTD3',
            'ZSTD-4':'ZSTD4',
            'ZSTD-5':'ZSTD5',
            'ZSTD-6':'ZSTD6',
            'ZSTD-7':'ZSTD7',
            'ZSTD-8':'ZSTD8',
            'ZSTD-9':'ZSTD9',
            'ZSTD-10':'ZSTD10',
            'ZSTD-11':'ZSTD11',
            'ZSTD-12':'ZSTD12',
            'ZSTD-13':'ZSTD13',
            'ZSTD-14':'ZSTD14',
            'ZSTD-15':'ZSTD15',
            'ZSTD-16':'ZSTD16',
            'ZSTD-17':'ZSTD17',
            'ZSTD-18':'ZSTD18',
            'ZSTD-19':'ZSTD19',
            'ZSTD-FAST-1':'ZSTDFAST1',
            'ZSTD-FAST-2':'ZSTDFAST2',
            'ZSTD-FAST-3':'ZSTDFAST3',
            'ZSTD-FAST-4':'ZSTDFAST4',
            'ZSTD-FAST-5':'ZSTDFAST5',
            'ZSTD-FAST-6':'ZSTDFAST6',
            'ZSTD-FAST-7':'ZSTDFAST7',
            'ZSTD-FAST-8':'ZSTDFAST8',
            'ZSTD-FAST-9':'ZSTDFAST9',
            'ZSTD-FAST-10':'ZSTDFAST10',
            'ZSTD-FAST-20':'ZSTDFAST20',
            'ZSTD-FAST-30':'ZSTDFAST30',
            'ZSTD-FAST-40':'ZSTDFAST40',
            'ZSTD-FAST-50':'ZSTDFAST50',
            'ZSTD-FAST-60':'ZSTDFAST60',
            'ZSTD-FAST-70':'ZSTDFAST70',
            'ZSTD-FAST-80':'ZSTDFAST80',
            'ZSTD-FAST-90':'ZSTDFAST90',
            'ZSTD-FAST-100':'ZSTDFAST100',
            'ZSTD-FAST-500':'ZSTDFAST500',
            'ZSTD-FAST-1000':'ZSTDFAST1000',
    })
    class OFF(str,Enum):
        OFF = 'OFF'
        ...
    class LZ4(str,Enum):
        LZ4 = 'LZ4'
        ...
    class GZIP(str,Enum):
        GZIP = 'GZIP'
        ...
    class GZIP1(str,Enum):
        GZIP1 = 'GZIP-1'
        ...
    class GZIP9(str,Enum):
        GZIP9 = 'GZIP-9'
        ...
    class ZSTD(str,Enum):
        ZSTD = 'ZSTD'
        ...
    class ZSTDFAST(str,Enum):
        ZSTDFAST = 'ZSTD-FAST'
        ...
    class ZLE(str,Enum):
        ZLE = 'ZLE'
        ...
    class LZJB(str,Enum):
        LZJB = 'LZJB'
        ...
    class ZSTD1(str,Enum):
        ZSTD1 = 'ZSTD-1'
        ...
    class ZSTD2(str,Enum):
        ZSTD2 = 'ZSTD-2'
        ...
    class ZSTD3(str,Enum):
        ZSTD3 = 'ZSTD-3'
        ...
    class ZSTD4(str,Enum):
        ZSTD4 = 'ZSTD-4'
        ...
    class ZSTD5(str,Enum):
        ZSTD5 = 'ZSTD-5'
        ...
    class ZSTD6(str,Enum):
        ZSTD6 = 'ZSTD-6'
        ...
    class ZSTD7(str,Enum):
        ZSTD7 = 'ZSTD-7'
        ...
    class ZSTD8(str,Enum):
        ZSTD8 = 'ZSTD-8'
        ...
    class ZSTD9(str,Enum):
        ZSTD9 = 'ZSTD-9'
        ...
    class ZSTD10(str,Enum):
        ZSTD10 = 'ZSTD-10'
        ...
    class ZSTD11(str,Enum):
        ZSTD11 = 'ZSTD-11'
        ...
    class ZSTD12(str,Enum):
        ZSTD12 = 'ZSTD-12'
        ...
    class ZSTD13(str,Enum):
        ZSTD13 = 'ZSTD-13'
        ...
    class ZSTD14(str,Enum):
        ZSTD14 = 'ZSTD-14'
        ...
    class ZSTD15(str,Enum):
        ZSTD15 = 'ZSTD-15'
        ...
    class ZSTD16(str,Enum):
        ZSTD16 = 'ZSTD-16'
        ...
    class ZSTD17(str,Enum):
        ZSTD17 = 'ZSTD-17'
        ...
    class ZSTD18(str,Enum):
        ZSTD18 = 'ZSTD-18'
        ...
    class ZSTD19(str,Enum):
        ZSTD19 = 'ZSTD-19'
        ...
    class ZSTDFAST1(str,Enum):
        ZSTDFAST1 = 'ZSTD-FAST-1'
        ...
    class ZSTDFAST2(str,Enum):
        ZSTDFAST2 = 'ZSTD-FAST-2'
        ...
    class ZSTDFAST3(str,Enum):
        ZSTDFAST3 = 'ZSTD-FAST-3'
        ...
    class ZSTDFAST4(str,Enum):
        ZSTDFAST4 = 'ZSTD-FAST-4'
        ...
    class ZSTDFAST5(str,Enum):
        ZSTDFAST5 = 'ZSTD-FAST-5'
        ...
    class ZSTDFAST6(str,Enum):
        ZSTDFAST6 = 'ZSTD-FAST-6'
        ...
    class ZSTDFAST7(str,Enum):
        ZSTDFAST7 = 'ZSTD-FAST-7'
        ...
    class ZSTDFAST8(str,Enum):
        ZSTDFAST8 = 'ZSTD-FAST-8'
        ...
    class ZSTDFAST9(str,Enum):
        ZSTDFAST9 = 'ZSTD-FAST-9'
        ...
    class ZSTDFAST10(str,Enum):
        ZSTDFAST10 = 'ZSTD-FAST-10'
        ...
    class ZSTDFAST20(str,Enum):
        ZSTDFAST20 = 'ZSTD-FAST-20'
        ...
    class ZSTDFAST30(str,Enum):
        ZSTDFAST30 = 'ZSTD-FAST-30'
        ...
    class ZSTDFAST40(str,Enum):
        ZSTDFAST40 = 'ZSTD-FAST-40'
        ...
    class ZSTDFAST50(str,Enum):
        ZSTDFAST50 = 'ZSTD-FAST-50'
        ...
    class ZSTDFAST60(str,Enum):
        ZSTDFAST60 = 'ZSTD-FAST-60'
        ...
    class ZSTDFAST70(str,Enum):
        ZSTDFAST70 = 'ZSTD-FAST-70'
        ...
    class ZSTDFAST80(str,Enum):
        ZSTDFAST80 = 'ZSTD-FAST-80'
        ...
    class ZSTDFAST90(str,Enum):
        ZSTDFAST90 = 'ZSTD-FAST-90'
        ...
    class ZSTDFAST100(str,Enum):
        ZSTDFAST100 = 'ZSTD-FAST-100'
        ...
    class ZSTDFAST500(str,Enum):
        ZSTDFAST500 = 'ZSTD-FAST-500'
        ...
    class ZSTDFAST1000(str,Enum):
        ZSTDFAST1000 = 'ZSTD-FAST-1000'
        ...
    PoolDatasetCreate = typing.TypedDict('PoolDatasetCreate', {
            'name':'str',
            'type':'Type',
            'volsize':'int',
            'volblocksize':'Volblocksize',
            'sparse':'bool',
            'force_size':'bool',
            'comments':'typing.Union[str, Choices]',
            'sync':'Sync',
            'snapdev':'Snapdev',
            'compression':'Compression',
            'atime':'Atime',
            'exec':'Exec',
            'managedby':'typing.Union[str, Choices]',
            'quota':'typing.Optional[int]',
            'quota_warning':'typing.Union[int, Choices]',
            'quota_critical':'typing.Union[int, Choices]',
            'refquota':'typing.Optional[int]',
            'refquota_warning':'typing.Union[int, Choices]',
            'refquota_critical':'typing.Union[int, Choices]',
            'reservation':'int',
            'refreservation':'int',
            'special_small_block_size':'typing.Union[int, Choices]',
            'copies':'typing.Union[int, Choices]',
            'snapdir':'Snapdir',
            'deduplication':'Deduplication',
            'checksum':'Checksum',
            'readonly':'Readonly',
            'recordsize':'typing.Union[str, Choices]',
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
    class Type(str,Enum):
        FILESYSTEM = 'FILESYSTEM'
        VOLUME = 'VOLUME'
        ...
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
    class Choices(str,Enum):
        INHERIT = 'INHERIT'
        ...
    class Sync(str,Enum):
        STANDARD = 'STANDARD'
        ALWAYS = 'ALWAYS'
        DISABLED = 'DISABLED'
        INHERIT = 'INHERIT'
        ...
    class Snapdev(str,Enum):
        HIDDEN = 'HIDDEN'
        VISIBLE = 'VISIBLE'
        INHERIT = 'INHERIT'
        ...
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
    class Atime(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        INHERIT = 'INHERIT'
        ...
    class Exec(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        INHERIT = 'INHERIT'
        ...
    class Snapdir(str,Enum):
        VISIBLE = 'VISIBLE'
        HIDDEN = 'HIDDEN'
        INHERIT = 'INHERIT'
        ...
    class Deduplication(str,Enum):
        ON = 'ON'
        VERIFY = 'VERIFY'
        OFF = 'OFF'
        INHERIT = 'INHERIT'
        ...
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
    class Readonly(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        INHERIT = 'INHERIT'
        ...
    class Casesensitivity(str,Enum):
        SENSITIVE = 'SENSITIVE'
        INSENSITIVE = 'INSENSITIVE'
        INHERIT = 'INHERIT'
        ...
    class Aclmode(str,Enum):
        PASSTHROUGH = 'PASSTHROUGH'
        RESTRICTED = 'RESTRICTED'
        DISCARD = 'DISCARD'
        INHERIT = 'INHERIT'
        ...
    class Acltype(str,Enum):
        OFF = 'OFF'
        NFSV4 = 'NFSV4'
        POSIX = 'POSIX'
        INHERIT = 'INHERIT'
        ...
    class ShareType(str,Enum):
        GENERIC = 'GENERIC'
        SMB = 'SMB'
        APPS = 'APPS'
        ...
    class Xattr(str,Enum):
        ON = 'ON'
        SA = 'SA'
        INHERIT = 'INHERIT'
        ...
    EncryptionOptions = typing.TypedDict('EncryptionOptions', {
            'generate_key':'bool',
            'pbkdf2iters':'int',
            'algorithm':'Algorithm',
            'passphrase':'typing.Optional[str]',
            'key':'typing.Optional[str]',
    })
    class Algorithm(str,Enum):
        AES128CCM = 'AES-128-CCM'
        AES192CCM = 'AES-192-CCM'
        AES256CCM = 'AES-256-CCM'
        AES128GCM = 'AES-128-GCM'
        AES192GCM = 'AES-192-GCM'
        AES256GCM = 'AES-256-GCM'
        ...
    UserProperty = typing.TypedDict('UserProperty', {
            'key':'str',
            'value':'str',
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
    Comments = typing.TypedDict('Comments', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaWarning = typing.TypedDict('QuotaWarning', {
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
    RefquotaWarning = typing.TypedDict('RefquotaWarning', {
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
    Managedby = typing.TypedDict('Managedby', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Deduplication_ = typing.TypedDict('Deduplication_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Aclmode_ = typing.TypedDict('Aclmode_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Acltype_ = typing.TypedDict('Acltype_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Xattr_ = typing.TypedDict('Xattr_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Atime_ = typing.TypedDict('Atime_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Casesensitivity_ = typing.TypedDict('Casesensitivity_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Checksum_ = typing.TypedDict('Checksum_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Exec_ = typing.TypedDict('Exec_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sync_ = typing.TypedDict('Sync_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
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
    Origin = typing.TypedDict('Origin', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Quota = typing.TypedDict('Quota', {
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
    Reservation = typing.TypedDict('Reservation', {
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
    Copies = typing.TypedDict('Copies', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdir_ = typing.TypedDict('Snapdir_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
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
    Sparse = typing.TypedDict('Sparse', {
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
    Volblocksize_ = typing.TypedDict('Volblocksize_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    KeyFormat = typing.TypedDict('KeyFormat', {
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
    Available = typing.TypedDict('Available', {
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
    Pbkdf2iters = typing.TypedDict('Pbkdf2iters', {
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
    Snapdev_ = typing.TypedDict('Snapdev_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    DatasetDelete = typing.TypedDict('DatasetDelete', {
            'recursive':'bool',
            'force':'bool',
    })
    Snapshots = typing.TypedDict('Snapshots', {
            'all':'bool',
            'recursive':'bool',
            'snapshots':'list[SnapshotSpec]',
    })
    SnapshotSpec = typing.TypedDict('SnapshotSpec', {
            'start':'str',
            'end':'str',
    })
    EncryptionAlgorithmChoices = typing.TypedDict('EncryptionAlgorithmChoices', {
            'AES-128-CCM':'AES128CCM',
            'AES-192-CCM':'AES192CCM',
            'AES-256-CCM':'AES256CCM',
            'AES-128-GCM':'AES128GCM',
            'AES-192-GCM':'AES192GCM',
            'AES-256-GCM':'AES256GCM',
    })
    class AES128CCM(str,Enum):
        AES128CCM = 'AES-128-CCM'
        ...
    class AES192CCM(str,Enum):
        AES192CCM = 'AES-192-CCM'
        ...
    class AES256CCM(str,Enum):
        AES256CCM = 'AES-256-CCM'
        ...
    class AES128GCM(str,Enum):
        AES128GCM = 'AES-128-GCM'
        ...
    class AES192GCM(str,Enum):
        AES192GCM = 'AES-192-GCM'
        ...
    class AES256GCM(str,Enum):
        AES256GCM = 'AES-256-GCM'
        ...
    EncryptionRootSummaryOptions = typing.TypedDict('EncryptionRootSummaryOptions', {
            'key_file':'bool',
            'force':'bool',
            'datasets':'list[Dataset]',
    })
    Dataset = typing.TypedDict('Dataset', {
            'force':'bool',
            'name':'str',
            'key':'str',
            'passphrase':'str',
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
    class QuotaType(str,Enum):
        USER = 'USER'
        GROUP = 'GROUP'
        DATASET = 'DATASET'
        PROJECT = 'PROJECT'
        ...
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
    LockOptions = typing.TypedDict('LockOptions', {
            'force_umount':'bool',
    })
    PoolDatasetPermission = typing.TypedDict('PoolDatasetPermission', {
            'user':'str',
            'group':'str',
            'mode':'typing.Optional[str]',
            'acl':'typing.Union[list[Nfs4Ace], list[Posix1eAce]]',
            'options':'Options',
    })
    Nfs4Ace = typing.TypedDict('Nfs4Ace', {
            'tag':'Tag',
            'id':'typing.Optional[int]',
            'type':'Type_',
            'perms':'Perms',
            'flags':'Flags',
    })
    class Tag(str,Enum):
        Owner = 'owner@'
        Group = 'group@'
        Everyone = 'everyone@'
        USER = 'USER'
        GROUP = 'GROUP'
        ...
    class Type_(str,Enum):
        ALLOW = 'ALLOW'
        DENY = 'DENY'
        ...
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
    class BASIC(str,Enum):
        FULLCONTROL = 'FULL_CONTROL'
        MODIFY = 'MODIFY'
        READ = 'READ'
        TRAVERSE = 'TRAVERSE'
        ...
    Flags = typing.TypedDict('Flags', {
            'FILE_INHERIT':'bool',
            'DIRECTORY_INHERIT':'bool',
            'NO_PROPAGATE_INHERIT':'bool',
            'INHERIT_ONLY':'bool',
            'INHERITED':'bool',
            'BASIC':'BASIC_',
    })
    class BASIC_(str,Enum):
        INHERIT = 'INHERIT'
        NOINHERIT = 'NOINHERIT'
        ...
    Posix1eAce = typing.TypedDict('Posix1eAce', {
            'default':'bool',
            'tag':'Tag_',
            'id':'int',
            'perms':'Perms_',
    })
    class Tag_(str,Enum):
        USEROBJ = 'USER_OBJ'
        GROUPOBJ = 'GROUP_OBJ'
        USER = 'USER'
        GROUP = 'GROUP'
        OTHER = 'OTHER'
        MASK = 'MASK'
        ...
    Perms_ = typing.TypedDict('Perms_', {
            'READ':'bool',
            'WRITE':'bool',
            'EXECUTE':'bool',
    })
    Options = typing.TypedDict('Options', {
            'set_default_acl':'bool',
            'stripacl':'bool',
            'recursive':'bool',
            'traverse':'bool',
    })
    Process = typing.TypedDict('Process', {
            'pid':'int',
            'name':'str',
            'service':'str',
            'cmdline':'str',
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
    QuotaEntry = typing.TypedDict('QuotaEntry', {
            'quota_type':'QuotaType_',
            'id':'str',
            'quota_value':'typing.Optional[int]',
    })
    class QuotaType_(str,Enum):
        DATASET = 'DATASET'
        USER = 'USER'
        USEROBJ = 'USEROBJ'
        GROUP = 'GROUP'
        GROUPOBJ = 'GROUPOBJ'
        ...
    UnlockOptions = typing.TypedDict('UnlockOptions', {
            'force':'bool',
            'key_file':'bool',
            'recursive':'bool',
            'toggle_attachments':'bool',
            'datasets':'list[Dataset_]',
    })
    Dataset_ = typing.TypedDict('Dataset_', {
            'force':'bool',
            'name':'str',
            'key':'str',
            'passphrase':'str',
            'recursive':'bool',
    })
    Unlock = typing.TypedDict('Unlock', {
            'unlocked':'list[str]',
            'failed':'dict[str]',
    })
    PoolDatasetUpdate = typing.TypedDict('PoolDatasetUpdate', {
            'volsize':'int',
            'force_size':'bool',
            'comments':'typing.Union[str, Choices]',
            'sync':'Sync',
            'snapdev':'Snapdev',
            'compression':'Compression',
            'atime':'Atime',
            'exec':'Exec',
            'managedby':'typing.Union[str, Choices]',
            'quota':'typing.Optional[int]',
            'quota_warning':'typing.Union[int, Choices]',
            'quota_critical':'typing.Union[int, Choices]',
            'refquota':'typing.Optional[int]',
            'refquota_warning':'typing.Union[int, Choices]',
            'refquota_critical':'typing.Union[int, Choices]',
            'reservation':'int',
            'refreservation':'int',
            'special_small_block_size':'typing.Union[int, Choices]',
            'copies':'typing.Union[int, Choices]',
            'snapdir':'Snapdir',
            'deduplication':'Deduplication',
            'checksum':'Checksum',
            'readonly':'Readonly',
            'recordsize':'typing.Union[str, Choices]',
            'aclmode':'Aclmode',
            'acltype':'Acltype',
            'xattr':'Xattr',
            'user_properties':'list[UserProperty]',
            'create_ancestors':'bool',
            'user_properties_update':'list[UserProperty_]',
    })
    UserProperty_ = typing.TypedDict('UserProperty_', {
            'key':'str',
            'value':'str',
            'remove':'bool',
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
