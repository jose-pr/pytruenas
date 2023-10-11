
from pytruenas.base import Namespace

import typing
from enum import Enum

class Keychaincredential(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'keychaincredential')

    KeychainCredentialCreate = typing.TypedDict('KeychainCredentialCreate', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
    })
    KeychaincredentialCreateReturns = typing.TypedDict('KeychaincredentialCreateReturns', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'id':'int',
    })
    Options = typing.TypedDict('Options', {
            'cascade':'bool',
    })
    SshKeyPair = typing.TypedDict('SshKeyPair', {
            'private_key':'str',
            'public_key':'str',
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
    KeychainCredentialEntry = typing.TypedDict('KeychainCredentialEntry', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'id':'int',
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
    SetupSshConnection = typing.TypedDict('SetupSshConnection', {
            'private_key':'PrivateKey',
            'connection_name':'str',
            'setup_type':'SetupType',
            'semi_automatic_setup':'SemiAutomaticSetup',
            'manual_setup':'dict[str]',
    })
    PrivateKey = typing.TypedDict('PrivateKey', {
            'generate_key':'bool',
            'existing_key_id':'int',
            'name':'str',
    })
    class SetupType(str,Enum):
        SEMIAUTOMATIC = 'SEMI-AUTOMATIC'
        MANUAL = 'MANUAL'
        ...
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
    KeychainCredentialUpdate = typing.TypedDict('KeychainCredentialUpdate', {
            'name':'str',
            'attributes':'dict[str]',
    })
    KeychaincredentialUpdateReturns = typing.TypedDict('KeychaincredentialUpdateReturns', {
            'name':'str',
            'type':'str',
            'attributes':'dict[str]',
            'id':'int',
    })
    CredentialResult = typing.TypedDict('CredentialResult', {
            'title':'str',
            'unbind_method':'str',
    })
