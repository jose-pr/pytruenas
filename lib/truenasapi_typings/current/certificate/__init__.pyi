from pytruenas import Namespace as _NS 
class Certificate(_NS):
    
    def acme_server_choices(
    ) -> CertificateAcme_server_choices:
        """Dictionary of popular ACME Servers with their directory URI endpoints which we display automatically in the UI"""
        ...
    def country_choices(
    ) -> CertificateCountry_choices:
        """Returns country choices for creating a certificate/csr."""
        ...
    def ec_curve_choices(
    ) -> CertificateEc_curve_choices:
        """Dictionary of supported EC curves."""
        ...
    def extended_key_usage_choices(
    ) -> CertificateExtended_key_usage_choices:
        """Dictionary of names that can be used in the ExtendedKeyUsage attribute of a certificate request."""
        ...
class CertificateAcme_server_choices:
    ...
class CertificateCountry_choices:
    ...
class CertificateEc_curve_choices:
    ...
class CertificateExtended_key_usage_choices:
    ... 