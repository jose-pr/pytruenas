from pytruenas import Namespace as _NS
import typing as _ty 
class Certificate(_NS):
    
    def acme_server_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CertificateAcme_server_choices:
        """Dictionary of popular ACME Servers with their directory URI endpoints which we display automatically in the UI"""
        ...
    def country_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CertificateCountry_choices:
        """Returns country choices for creating a certificate/csr."""
        ...
    def ec_curve_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CertificateEc_curve_choices:
        """Dictionary of supported EC curves."""
        ...
    def extended_key_usage_choices(self,
        _method:str|None=None,
        _ioerror:bool=False,
        _filetransfer:bool|bytes=False,
    ) -> CertificateExtended_key_usage_choices:
        """Dictionary of names that can be used in the ExtendedKeyUsage attribute of a certificate request."""
        ...
class CertificateAcme_server_choices(_ty.TypedDict):
    ...
class CertificateCountry_choices(_ty.TypedDict):
    ...
class CertificateEc_curve_choices(_ty.TypedDict):
    ...
class CertificateExtended_key_usage_choices(_ty.TypedDict):
    ... 