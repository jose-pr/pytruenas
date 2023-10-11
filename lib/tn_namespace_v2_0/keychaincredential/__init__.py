
from pytruenas.base import Namespace

import typing
from enum import Enum

class Keychaincredential(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'keychaincredential')

    CredentialResult = typing.TypedDict('CredentialResult', {
            'title':'str',
            'unbind_method':'str',
    })
    KeychainCredentialCreate = typing.TypedDict('KeychainCredentialCreate', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
    })
    KeychainCredentialEntry = typing.TypedDict('KeychainCredentialEntry', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'id':'int',
    })
    KeychainCredentialUpdate = typing.TypedDict('KeychainCredentialUpdate', {
            'name':'str',
            'attributes':'dict[str]',
    })
    KeychainRemoteSshHostKeyScan = typing.TypedDict('KeychainRemoteSshHostKeyScan', {
            'host':'str',
            'port':'str',
            'connect_timeout':'int',
    })
    KeychainRemoteSshSemiautomaticSetup = typing.TypedDict('KeychainRemoteSshSemiautomaticSetup', {
            'name':'str',
            'url':'str',
            'token':'str',
            'admin_username':'str',
            'password':'str',
            'otp_token':'str',
            'username':'str',
            'private_key':'int',
            'connect_timeout':'int',
            'sudo':'bool',
    })
    KeychaincredentialCreateReturns = typing.TypedDict('KeychaincredentialCreateReturns', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'id':'int',
    })
    KeychaincredentialUpdateReturns = typing.TypedDict('KeychaincredentialUpdateReturns', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'id':'int',
    })
    Options = typing.TypedDict('Options', {
            'cascade':'bool',
    })
    PrivateKey = typing.TypedDict('PrivateKey', {
            'generate_key':'bool',
            'existing_key_id':'int',
            'name':'str',
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
    SemiAutomaticSetup = typing.TypedDict('SemiAutomaticSetup', {
            'url':'str',
            'token':'str',
            'admin_username':'str',
            'password':'str',
            'otp_token':'str',
            'username':'str',
            'connect_timeout':'int',
            'sudo':'bool',
    })
    SetupSshConnection = typing.TypedDict('SetupSshConnection', {
            'private_key':'PrivateKey',
            'connection_name':'str',
            'setup_type':'SetupType',
            'semi_automatic_setup':'SemiAutomaticSetup',
            'manual_setup':'dict[str]',
    })
    class SetupType(str,Enum):
        SEMIAUTOMATIC = 'SEMI-AUTOMATIC'
        MANUAL = 'MANUAL'
        ...
    SshKeyPair = typing.TypedDict('SshKeyPair', {
            'private_key':'str',
            'public_key':'str',
    })
