from enum import Enum as _Enum
from typing import (
    TYPE_CHECKING as _TYPING,
    TypedDict as _Dict,
)
from ._base import Config as _Config


class Certificate(_Dict):
    id: int
    type: int
    name: str
    certificate: str
    privatekey: str
    CSR: str
    acme_uri: str
    domains_authenticators: dict
    renew_days: int
    revoked_date: str
    signedby: dict
    root_path: str
    acme: dict
    certificate_path: str
    privatekey_path: str
    csr_path: str
    cert_type: str
    revoked: bool
    expired: bool
    issuer: str | dict
    chain_list: list[str]
    country: str
    state: str
    city: str
    organization: str
    organizational_unit: str
    san: list[str]
    email: str
    DN: str
    subject_name_hash: str
    digest_algorithm: str
    #'from': str
    common: str
    until: str
    fingerprint: str
    key_type: str
    internal: str
    lifetime: int
    serial: int
    key_length: int
    chain: bool
    CA_type_existing: bool
    CA_type_internal: bool
    CA_type_intermediate: bool
    cert_type_existing: bool
    cert_type_internal: bool
    cert_type_CSR: bool
    parsed: bool
    can_be_revoked: bool
    extensions: dict
    revoked_certs: list
    crl_path: str
    signed_certificates: int


class TLSProtocol(str, _Enum):
    TLSv1 = "TLSv1"
    TLSv1_1 = "TLSv1.1"
    TLSv1_2 = "TLSv1.2"
    TLSv1_3 = "TLSv1.3"


class XFrameOptions(str, _Enum):
    SameOrigin = "SAMEORIGIN"
    Deny = "DENY"
    AllowAll = "ALLOW_ALL"


class SystemGeneralConfig(_Dict):
    ui_certificate: Certificate
    ui_httpsport: int
    ui_httpsredirect: bool
    ui_httpsprotocols: list[TLSProtocol]
    ui_port: int
    ui_address: list[str]
    ui_v6address: list[str]
    ui_allowlist: list[str]
    ui_consolemsg: bool
    ui_x_frame_options: list[XFrameOptions]
    kbdmap: str
    language: str
    timezone: str
    usage_collection: bool
    birthday: str
    wizardshown: bool
    usage_collection_is_set: bool
    ds_auth: bool
    id: int


_NS = _Config[SystemGeneralConfig]
_Choices = dict[str,str]
if _TYPING:

    class _NS(_Config[SystemGeneralConfig]):
        def checkin(self) -> None:
            ...

        def checkin_waiting(self) -> int | None:
            ...

        def country_choices(self) -> _Choices:
            ...

        def kbdmap_choices(self) -> _Choices:
            ...

        def language_choices(self) -> _Choices:
            ...

        def local_url(self) -> str:
            ...

        def timezone_choices(self) -> _Choices:
            ...

        def ui_address_choices(self) -> _Choices:
            ...

        def ui_certificate_choices(self) -> _Choices:
            ...

        def ui_httpsprotocols_choices(self) -> dict[TLSProtocol]:
            ...

        def ui_restart(self) -> int:
            ...

        def ui_v6address_choices(self) -> _Choices:
            ...


class SystemGeneral(_NS):
    ...
