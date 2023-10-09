
from pytruenas.base import Namespace

import typing
from enum import Enum

class PoolDataset(Namespace):
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
    ChecksumChoices = typing.TypedDict('ChecksumChoices', {
            'ON':'ON',
            'FLETCHER2':'FLETCHER2',
            'FLETCHER4':'FLETCHER4',
            'SHA256':'SHA256',
            'SHA512':'SHA512',
            'SKEIN':'SKEIN',
            'EDONR':'EDONR',
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
    class Object(str,Enum):
        INHERIT = 'INHERIT'
        ...
    class Sync(str,Enum):
        STANDARD = 'STANDARD'
        ALWAYS = 'ALWAYS'
        DISABLED = 'DISABLED'
        ...
    class Snapdev(str,Enum):
        HIDDEN = 'HIDDEN'
        VISIBLE = 'VISIBLE'
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
        ...
    class Atime(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        ...
    class Exec(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        ...
    class Snapdir(str,Enum):
        VISIBLE = 'VISIBLE'
        HIDDEN = 'HIDDEN'
        ...
    class Deduplication(str,Enum):
        ON = 'ON'
        VERIFY = 'VERIFY'
        OFF = 'OFF'
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
        ...
    class Readonly(str,Enum):
        ON = 'ON'
        OFF = 'OFF'
        ...
    class Casesensitivity(str,Enum):
        SENSITIVE = 'SENSITIVE'
        INSENSITIVE = 'INSENSITIVE'
        ...
    class Aclmode(str,Enum):
        PASSTHROUGH = 'PASSTHROUGH'
        RESTRICTED = 'RESTRICTED'
        DISCARD = 'DISCARD'
        ...
    class Acltype(str,Enum):
        OFF = 'OFF'
        NFSV4 = 'NFSV4'
        POSIX = 'POSIX'
        ...
    class ShareType(str,Enum):
        GENERIC = 'GENERIC'
        SMB = 'SMB'
        APPS = 'APPS'
        ...
    class Xattr(str,Enum):
        ON = 'ON'
        SA = 'SA'
        ...
    class Algorithm(str,Enum):
        AES128CCM = 'AES-128-CCM'
        AES192CCM = 'AES-192-CCM'
        AES256CCM = 'AES-256-CCM'
        AES128GCM = 'AES-128-GCM'
        AES192GCM = 'AES-192-GCM'
        AES256GCM = 'AES-256-GCM'
        ...
    EncryptionOptions = typing.TypedDict('EncryptionOptions', {
            'generate_key':'bool',
            'pbkdf2iters':'int',
            'algorithm':'Algorithm',
            'passphrase':'typing.Optional[str]',
            'key':'typing.Optional[str]',
    })
    UserProperty = typing.TypedDict('UserProperty', {
            'key':'str',
            'value':'str',
    })
    PoolDatasetCreate = typing.TypedDict('PoolDatasetCreate', {
            'name':'str',
            'type':'Type',
            'volsize':'int',
            'volblocksize':'Volblocksize',
            'sparse':'bool',
            'force_size':'bool',
            'comments':'typing.Union[str, Object]',
            'sync':'typing.Union[str, Object]',
            'snapdev':'typing.Union[str, Object]',
            'compression':'typing.Union[str, Object]',
            'atime':'typing.Union[str, Object]',
            'exec':'typing.Union[str, Object]',
            'managedby':'typing.Union[str, Object]',
            'quota':'typing.Optional[int]',
            'quota_warning':'typing.Union[int, Object]',
            'quota_critical':'typing.Union[int, Object]',
            'refquota':'typing.Optional[int]',
            'refquota_warning':'typing.Union[int, Object]',
            'refquota_critical':'typing.Union[int, Object]',
            'reservation':'int',
            'refreservation':'int',
            'special_small_block_size':'typing.Union[int, Object]',
            'copies':'typing.Union[int, Object]',
            'snapdir':'typing.Union[str, Object]',
            'deduplication':'typing.Union[str, Object]',
            'checksum':'typing.Union[str, Object]',
            'readonly':'typing.Union[str, Object]',
            'recordsize':'typing.Union[str, Object]',
            'casesensitivity':'typing.Union[str, Object]',
            'aclmode':'typing.Union[str, Object]',
            'acltype':'typing.Union[str, Object]',
            'share_type':'ShareType',
            'xattr':'typing.Union[str, Object]',
            'encryption_options':'EncryptionOptions',
            'encryption':'bool',
            'inherit_encryption':'bool',
            'user_properties':'list[UserProperty]',
            'create_ancestors':'bool',
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
    DatasetDelete = typing.TypedDict('DatasetDelete', {
            'recursive':'bool',
            'force':'bool',
    })
    SnapshotSpec = typing.TypedDict('SnapshotSpec', {
            'start':'str',
            'end':'str',
    })
    Snapshots = typing.TypedDict('Snapshots', {
            'all':'bool',
            'recursive':'bool',
            'snapshots':'list[typing.Union[SnapshotSpec, str]]',
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
    EncryptionAlgorithmChoices = typing.TypedDict('EncryptionAlgorithmChoices', {
            'AES-128-CCM':'AES128CCM',
            'AES-192-CCM':'AES192CCM',
            'AES-256-CCM':'AES256CCM',
            'AES-128-GCM':'AES128GCM',
            'AES-192-GCM':'AES192GCM',
            'AES-256-GCM':'AES256GCM',
    })
    Dataset = typing.TypedDict('Dataset', {
            'force':'bool',
            'name':'str',
            'key':'str',
            'passphrase':'str',
    })
    EncryptionRootSummaryOptions = typing.TypedDict('EncryptionRootSummaryOptions', {
            'key_file':'bool',
            'force':'bool',
            'datasets':'list[Dataset]',
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
    class BASIC(str,Enum):
        FULLCONTROL = 'FULL_CONTROL'
        MODIFY = 'MODIFY'
        READ = 'READ'
        TRAVERSE = 'TRAVERSE'
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
    class BASIC_(str,Enum):
        INHERIT = 'INHERIT'
        NOINHERIT = 'NOINHERIT'
        ...
    Flags = typing.TypedDict('Flags', {
            'FILE_INHERIT':'bool',
            'DIRECTORY_INHERIT':'bool',
            'NO_PROPAGATE_INHERIT':'bool',
            'INHERIT_ONLY':'bool',
            'INHERITED':'bool',
            'BASIC':'BASIC_',
    })
    Nfs4Ace = typing.TypedDict('Nfs4Ace', {
            'tag':'Tag',
            'id':'typing.Optional[int]',
            'type':'Type_',
            'perms':'Perms',
            'flags':'Flags',
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
    Posix1eAce = typing.TypedDict('Posix1eAce', {
            'default':'bool',
            'tag':'Tag_',
            'id':'int',
            'perms':'Perms_',
    })
    Options = typing.TypedDict('Options', {
            'set_default_acl':'bool',
            'stripacl':'bool',
            'recursive':'bool',
            'traverse':'bool',
    })
    PoolDatasetPermission = typing.TypedDict('PoolDatasetPermission', {
            'user':'str',
            'group':'str',
            'mode':'typing.Optional[str]',
            'acl':'typing.Union[list[Nfs4Ace], list[Posix1eAce]]',
            'options':'Options',
    })
    Nfs4Ace_ = typing.TypedDict('Nfs4Ace_', {
            'tag':'Tag',
            'id':'typing.Optional[int]',
            'type':'Type_',
            'perms':'Perms',
            'flags':'Flags',
    })
    PoolDatasetPermission_ = typing.TypedDict('PoolDatasetPermission_', {
            'user':'str',
            'group':'str',
            'mode':'typing.Optional[str]',
            'acl':'typing.Union[list[Nfs4Ace_], list[Posix1eAce]]',
            'options':'Options',
    })
    Process = typing.TypedDict('Process', {
            'pid':'int',
            'name':'str',
            'service':'str',
            'cmdline':'str',
    })
    QueryOptions_ = typing.TypedDict('QueryOptions_', {
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
    Comments_ = typing.TypedDict('Comments_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaWarning_ = typing.TypedDict('QuotaWarning_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaCritical_ = typing.TypedDict('QuotaCritical_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaWarning_ = typing.TypedDict('RefquotaWarning_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaCritical_ = typing.TypedDict('RefquotaCritical_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Managedby_ = typing.TypedDict('Managedby_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Deduplication__ = typing.TypedDict('Deduplication__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Aclmode__ = typing.TypedDict('Aclmode__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Acltype__ = typing.TypedDict('Acltype__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Xattr__ = typing.TypedDict('Xattr__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Atime__ = typing.TypedDict('Atime__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Casesensitivity__ = typing.TypedDict('Casesensitivity__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Checksum__ = typing.TypedDict('Checksum__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Exec__ = typing.TypedDict('Exec__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sync__ = typing.TypedDict('Sync__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compression__ = typing.TypedDict('Compression__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compressratio_ = typing.TypedDict('Compressratio_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Origin_ = typing.TypedDict('Origin_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Quota_ = typing.TypedDict('Quota_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refquota_ = typing.TypedDict('Refquota_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Reservation_ = typing.TypedDict('Reservation_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refreservation_ = typing.TypedDict('Refreservation_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Copies_ = typing.TypedDict('Copies_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdir__ = typing.TypedDict('Snapdir__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Readonly__ = typing.TypedDict('Readonly__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Recordsize_ = typing.TypedDict('Recordsize_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sparse_ = typing.TypedDict('Sparse_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volsize_ = typing.TypedDict('Volsize_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volblocksize__ = typing.TypedDict('Volblocksize__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    KeyFormat_ = typing.TypedDict('KeyFormat_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    EncryptionAlgorithm_ = typing.TypedDict('EncryptionAlgorithm_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Used_ = typing.TypedDict('Used_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbychildren_ = typing.TypedDict('Usedbychildren_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbydataset_ = typing.TypedDict('Usedbydataset_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbyrefreservation_ = typing.TypedDict('Usedbyrefreservation_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbysnapshots_ = typing.TypedDict('Usedbysnapshots_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Available_ = typing.TypedDict('Available_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    SpecialSmallBlockSize_ = typing.TypedDict('SpecialSmallBlockSize_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Pbkdf2iters_ = typing.TypedDict('Pbkdf2iters_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Creation_ = typing.TypedDict('Creation_', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdev__ = typing.TypedDict('Snapdev__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
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
            'comments':'Comments_',
            'quota_warning':'QuotaWarning_',
            'quota_critical':'QuotaCritical_',
            'refquota_warning':'RefquotaWarning_',
            'refquota_critical':'RefquotaCritical_',
            'managedby':'Managedby_',
            'deduplication':'Deduplication__',
            'aclmode':'Aclmode__',
            'acltype':'Acltype__',
            'xattr':'Xattr__',
            'atime':'Atime__',
            'casesensitivity':'Casesensitivity__',
            'checksum':'Checksum__',
            'exec':'Exec__',
            'sync':'Sync__',
            'compression':'Compression__',
            'compressratio':'Compressratio_',
            'origin':'Origin_',
            'quota':'Quota_',
            'refquota':'Refquota_',
            'reservation':'Reservation_',
            'refreservation':'Refreservation_',
            'copies':'Copies_',
            'snapdir':'Snapdir__',
            'readonly':'Readonly__',
            'recordsize':'Recordsize_',
            'sparse':'Sparse_',
            'volsize':'Volsize_',
            'volblocksize':'Volblocksize__',
            'key_format':'KeyFormat_',
            'encryption_algorithm':'EncryptionAlgorithm_',
            'used':'Used_',
            'usedbychildren':'Usedbychildren_',
            'usedbydataset':'Usedbydataset_',
            'usedbyrefreservation':'Usedbyrefreservation_',
            'usedbysnapshots':'Usedbysnapshots_',
            'available':'Available_',
            'special_small_block_size':'SpecialSmallBlockSize_',
            'pbkdf2iters':'Pbkdf2iters_',
            'creation':'Creation_',
            'snapdev':'Snapdev__',
            'mountpoint':'typing.Optional[str]',
    })
    Comments__ = typing.TypedDict('Comments__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaWarning__ = typing.TypedDict('QuotaWarning__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaCritical__ = typing.TypedDict('QuotaCritical__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaWarning__ = typing.TypedDict('RefquotaWarning__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaCritical__ = typing.TypedDict('RefquotaCritical__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Managedby__ = typing.TypedDict('Managedby__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Deduplication___ = typing.TypedDict('Deduplication___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Aclmode___ = typing.TypedDict('Aclmode___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Acltype___ = typing.TypedDict('Acltype___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Xattr___ = typing.TypedDict('Xattr___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Atime___ = typing.TypedDict('Atime___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Casesensitivity___ = typing.TypedDict('Casesensitivity___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Checksum___ = typing.TypedDict('Checksum___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Exec___ = typing.TypedDict('Exec___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sync___ = typing.TypedDict('Sync___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compression___ = typing.TypedDict('Compression___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compressratio__ = typing.TypedDict('Compressratio__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Origin__ = typing.TypedDict('Origin__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Quota__ = typing.TypedDict('Quota__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refquota__ = typing.TypedDict('Refquota__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Reservation__ = typing.TypedDict('Reservation__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refreservation__ = typing.TypedDict('Refreservation__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Copies__ = typing.TypedDict('Copies__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdir___ = typing.TypedDict('Snapdir___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Readonly___ = typing.TypedDict('Readonly___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Recordsize__ = typing.TypedDict('Recordsize__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sparse__ = typing.TypedDict('Sparse__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volsize__ = typing.TypedDict('Volsize__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volblocksize___ = typing.TypedDict('Volblocksize___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    KeyFormat__ = typing.TypedDict('KeyFormat__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    EncryptionAlgorithm__ = typing.TypedDict('EncryptionAlgorithm__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Used__ = typing.TypedDict('Used__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbychildren__ = typing.TypedDict('Usedbychildren__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbydataset__ = typing.TypedDict('Usedbydataset__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbyrefreservation__ = typing.TypedDict('Usedbyrefreservation__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbysnapshots__ = typing.TypedDict('Usedbysnapshots__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Available__ = typing.TypedDict('Available__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    SpecialSmallBlockSize__ = typing.TypedDict('SpecialSmallBlockSize__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Pbkdf2iters__ = typing.TypedDict('Pbkdf2iters__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Creation__ = typing.TypedDict('Creation__', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdev___ = typing.TypedDict('Snapdev___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    PoolDatasetEntry_ = typing.TypedDict('PoolDatasetEntry_', {
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
            'comments':'Comments__',
            'quota_warning':'QuotaWarning__',
            'quota_critical':'QuotaCritical__',
            'refquota_warning':'RefquotaWarning__',
            'refquota_critical':'RefquotaCritical__',
            'managedby':'Managedby__',
            'deduplication':'Deduplication___',
            'aclmode':'Aclmode___',
            'acltype':'Acltype___',
            'xattr':'Xattr___',
            'atime':'Atime___',
            'casesensitivity':'Casesensitivity___',
            'checksum':'Checksum___',
            'exec':'Exec___',
            'sync':'Sync___',
            'compression':'Compression___',
            'compressratio':'Compressratio__',
            'origin':'Origin__',
            'quota':'Quota__',
            'refquota':'Refquota__',
            'reservation':'Reservation__',
            'refreservation':'Refreservation__',
            'copies':'Copies__',
            'snapdir':'Snapdir___',
            'readonly':'Readonly___',
            'recordsize':'Recordsize__',
            'sparse':'Sparse__',
            'volsize':'Volsize__',
            'volblocksize':'Volblocksize___',
            'key_format':'KeyFormat__',
            'encryption_algorithm':'EncryptionAlgorithm__',
            'used':'Used__',
            'usedbychildren':'Usedbychildren__',
            'usedbydataset':'Usedbydataset__',
            'usedbyrefreservation':'Usedbyrefreservation__',
            'usedbysnapshots':'Usedbysnapshots__',
            'available':'Available__',
            'special_small_block_size':'SpecialSmallBlockSize__',
            'pbkdf2iters':'Pbkdf2iters__',
            'creation':'Creation__',
            'snapdev':'Snapdev___',
            'mountpoint':'typing.Optional[str]',
    })
    Comments___ = typing.TypedDict('Comments___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaWarning___ = typing.TypedDict('QuotaWarning___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaCritical___ = typing.TypedDict('QuotaCritical___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaWarning___ = typing.TypedDict('RefquotaWarning___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaCritical___ = typing.TypedDict('RefquotaCritical___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Managedby___ = typing.TypedDict('Managedby___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Deduplication____ = typing.TypedDict('Deduplication____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Aclmode____ = typing.TypedDict('Aclmode____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Acltype____ = typing.TypedDict('Acltype____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Xattr____ = typing.TypedDict('Xattr____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Atime____ = typing.TypedDict('Atime____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Casesensitivity____ = typing.TypedDict('Casesensitivity____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Checksum____ = typing.TypedDict('Checksum____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Exec____ = typing.TypedDict('Exec____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sync____ = typing.TypedDict('Sync____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compression____ = typing.TypedDict('Compression____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compressratio___ = typing.TypedDict('Compressratio___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Origin___ = typing.TypedDict('Origin___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Quota___ = typing.TypedDict('Quota___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refquota___ = typing.TypedDict('Refquota___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Reservation___ = typing.TypedDict('Reservation___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refreservation___ = typing.TypedDict('Refreservation___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Copies___ = typing.TypedDict('Copies___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdir____ = typing.TypedDict('Snapdir____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Readonly____ = typing.TypedDict('Readonly____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Recordsize___ = typing.TypedDict('Recordsize___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sparse___ = typing.TypedDict('Sparse___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volsize___ = typing.TypedDict('Volsize___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volblocksize____ = typing.TypedDict('Volblocksize____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    KeyFormat___ = typing.TypedDict('KeyFormat___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    EncryptionAlgorithm___ = typing.TypedDict('EncryptionAlgorithm___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Used___ = typing.TypedDict('Used___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbychildren___ = typing.TypedDict('Usedbychildren___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbydataset___ = typing.TypedDict('Usedbydataset___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbyrefreservation___ = typing.TypedDict('Usedbyrefreservation___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbysnapshots___ = typing.TypedDict('Usedbysnapshots___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Available___ = typing.TypedDict('Available___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    SpecialSmallBlockSize___ = typing.TypedDict('SpecialSmallBlockSize___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Pbkdf2iters___ = typing.TypedDict('Pbkdf2iters___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Creation___ = typing.TypedDict('Creation___', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdev____ = typing.TypedDict('Snapdev____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    PoolDatasetEntry__ = typing.TypedDict('PoolDatasetEntry__', {
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
            'comments':'Comments___',
            'quota_warning':'QuotaWarning___',
            'quota_critical':'QuotaCritical___',
            'refquota_warning':'RefquotaWarning___',
            'refquota_critical':'RefquotaCritical___',
            'managedby':'Managedby___',
            'deduplication':'Deduplication____',
            'aclmode':'Aclmode____',
            'acltype':'Acltype____',
            'xattr':'Xattr____',
            'atime':'Atime____',
            'casesensitivity':'Casesensitivity____',
            'checksum':'Checksum____',
            'exec':'Exec____',
            'sync':'Sync____',
            'compression':'Compression____',
            'compressratio':'Compressratio___',
            'origin':'Origin___',
            'quota':'Quota___',
            'refquota':'Refquota___',
            'reservation':'Reservation___',
            'refreservation':'Refreservation___',
            'copies':'Copies___',
            'snapdir':'Snapdir____',
            'readonly':'Readonly____',
            'recordsize':'Recordsize___',
            'sparse':'Sparse___',
            'volsize':'Volsize___',
            'volblocksize':'Volblocksize____',
            'key_format':'KeyFormat___',
            'encryption_algorithm':'EncryptionAlgorithm___',
            'used':'Used___',
            'usedbychildren':'Usedbychildren___',
            'usedbydataset':'Usedbydataset___',
            'usedbyrefreservation':'Usedbyrefreservation___',
            'usedbysnapshots':'Usedbysnapshots___',
            'available':'Available___',
            'special_small_block_size':'SpecialSmallBlockSize___',
            'pbkdf2iters':'Pbkdf2iters___',
            'creation':'Creation___',
            'snapdev':'Snapdev____',
            'mountpoint':'typing.Optional[str]',
    })
    class QuotaType_(str,Enum):
        DATASET = 'DATASET'
        USER = 'USER'
        USEROBJ = 'USEROBJ'
        GROUP = 'GROUP'
        GROUPOBJ = 'GROUPOBJ'
        ...
    QuotaEntry = typing.TypedDict('QuotaEntry', {
            'quota_type':'QuotaType_',
            'id':'str',
            'quota_value':'typing.Optional[int]',
    })
    Dataset_ = typing.TypedDict('Dataset_', {
            'force':'bool',
            'name':'str',
            'key':'str',
            'passphrase':'str',
            'recursive':'bool',
    })
    UnlockOptions = typing.TypedDict('UnlockOptions', {
            'force':'bool',
            'key_file':'bool',
            'recursive':'bool',
            'toggle_attachments':'bool',
            'datasets':'list[Dataset_]',
    })
    Unlock = typing.TypedDict('Unlock', {
            'unlocked':'list[str]',
            'failed':'dict[str]',
    })
    UserProperty_ = typing.TypedDict('UserProperty_', {
            'key':'str',
            'value':'str',
            'remove':'bool',
    })
    PoolDatasetUpdate = typing.TypedDict('PoolDatasetUpdate', {
            'volsize':'int',
            'force_size':'bool',
            'comments':'typing.Union[str, Object]',
            'sync':'typing.Union[str, Object]',
            'snapdev':'typing.Union[str, Object]',
            'compression':'typing.Union[str, Object]',
            'atime':'typing.Union[str, Object]',
            'exec':'typing.Union[str, Object]',
            'managedby':'typing.Union[str, Object]',
            'quota':'typing.Optional[int]',
            'quota_warning':'typing.Union[int, Object]',
            'quota_critical':'typing.Union[int, Object]',
            'refquota':'typing.Optional[int]',
            'refquota_warning':'typing.Union[int, Object]',
            'refquota_critical':'typing.Union[int, Object]',
            'reservation':'int',
            'refreservation':'int',
            'special_small_block_size':'typing.Union[int, Object]',
            'copies':'typing.Union[int, Object]',
            'snapdir':'typing.Union[str, Object]',
            'deduplication':'typing.Union[str, Object]',
            'checksum':'typing.Union[str, Object]',
            'readonly':'typing.Union[str, Object]',
            'recordsize':'typing.Union[str, Object]',
            'aclmode':'typing.Union[str, Object]',
            'acltype':'typing.Union[str, Object]',
            'xattr':'typing.Union[str, Object]',
            'user_properties':'list[UserProperty]',
            'create_ancestors':'bool',
            'user_properties_update':'list[UserProperty_]',
    })
    Comments____ = typing.TypedDict('Comments____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaWarning____ = typing.TypedDict('QuotaWarning____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    QuotaCritical____ = typing.TypedDict('QuotaCritical____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaWarning____ = typing.TypedDict('RefquotaWarning____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    RefquotaCritical____ = typing.TypedDict('RefquotaCritical____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Managedby____ = typing.TypedDict('Managedby____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Deduplication_____ = typing.TypedDict('Deduplication_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Aclmode_____ = typing.TypedDict('Aclmode_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Acltype_____ = typing.TypedDict('Acltype_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Xattr_____ = typing.TypedDict('Xattr_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Atime_____ = typing.TypedDict('Atime_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Casesensitivity_____ = typing.TypedDict('Casesensitivity_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Checksum_____ = typing.TypedDict('Checksum_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Exec_____ = typing.TypedDict('Exec_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sync_____ = typing.TypedDict('Sync_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compression_____ = typing.TypedDict('Compression_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Compressratio____ = typing.TypedDict('Compressratio____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Origin____ = typing.TypedDict('Origin____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Quota____ = typing.TypedDict('Quota____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refquota____ = typing.TypedDict('Refquota____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Reservation____ = typing.TypedDict('Reservation____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Refreservation____ = typing.TypedDict('Refreservation____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Copies____ = typing.TypedDict('Copies____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdir_____ = typing.TypedDict('Snapdir_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Readonly_____ = typing.TypedDict('Readonly_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Recordsize____ = typing.TypedDict('Recordsize____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Sparse____ = typing.TypedDict('Sparse____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volsize____ = typing.TypedDict('Volsize____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Volblocksize_____ = typing.TypedDict('Volblocksize_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    KeyFormat____ = typing.TypedDict('KeyFormat____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    EncryptionAlgorithm____ = typing.TypedDict('EncryptionAlgorithm____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Used____ = typing.TypedDict('Used____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbychildren____ = typing.TypedDict('Usedbychildren____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbydataset____ = typing.TypedDict('Usedbydataset____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbyrefreservation____ = typing.TypedDict('Usedbyrefreservation____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Usedbysnapshots____ = typing.TypedDict('Usedbysnapshots____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Available____ = typing.TypedDict('Available____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    SpecialSmallBlockSize____ = typing.TypedDict('SpecialSmallBlockSize____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Pbkdf2iters____ = typing.TypedDict('Pbkdf2iters____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Creation____ = typing.TypedDict('Creation____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
    })
    Snapdev_____ = typing.TypedDict('Snapdev_____', {
            'parsed':'typing.Union[str, int, bool, dict[str], list]',
            'rawvalue':'typing.Optional[str]',
            'value':'typing.Optional[str]',
            'source':'typing.Optional[str]',
            'source_info':'typing.Union[str, int, bool, dict[str], list]',
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
            'comments':'Comments____',
            'quota_warning':'QuotaWarning____',
            'quota_critical':'QuotaCritical____',
            'refquota_warning':'RefquotaWarning____',
            'refquota_critical':'RefquotaCritical____',
            'managedby':'Managedby____',
            'deduplication':'Deduplication_____',
            'aclmode':'Aclmode_____',
            'acltype':'Acltype_____',
            'xattr':'Xattr_____',
            'atime':'Atime_____',
            'casesensitivity':'Casesensitivity_____',
            'checksum':'Checksum_____',
            'exec':'Exec_____',
            'sync':'Sync_____',
            'compression':'Compression_____',
            'compressratio':'Compressratio____',
            'origin':'Origin____',
            'quota':'Quota____',
            'refquota':'Refquota____',
            'reservation':'Reservation____',
            'refreservation':'Refreservation____',
            'copies':'Copies____',
            'snapdir':'Snapdir_____',
            'readonly':'Readonly_____',
            'recordsize':'Recordsize____',
            'sparse':'Sparse____',
            'volsize':'Volsize____',
            'volblocksize':'Volblocksize_____',
            'key_format':'KeyFormat____',
            'encryption_algorithm':'EncryptionAlgorithm____',
            'used':'Used____',
            'usedbychildren':'Usedbychildren____',
            'usedbydataset':'Usedbydataset____',
            'usedbyrefreservation':'Usedbyrefreservation____',
            'usedbysnapshots':'Usedbysnapshots____',
            'available':'Available____',
            'special_small_block_size':'SpecialSmallBlockSize____',
            'pbkdf2iters':'Pbkdf2iters____',
            'creation':'Creation____',
            'snapdev':'Snapdev_____',
            'mountpoint':'typing.Optional[str]',
    })
