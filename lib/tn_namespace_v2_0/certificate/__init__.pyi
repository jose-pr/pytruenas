
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Certificate(Namespace):
    _namespace:_ty.Literal['certificate']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def acme_server_choices(self, 
    /) -> 'dict[str]': 
        """
        Dictionary of popular ACME Servers with their directory URI endpoints which we display automatically
        in UI

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            acme_server_choices
        """
        ...
    @_ty.overload
    def certificate_signing_requests_profiles(self, 
    /) -> 'dict[str]': 
        """
        Returns a dictionary of predefined options for specific use cases i.e openvpn client/server
        configurations which can be used for creating certificate signing requests.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            Example(s):
            ```
            {
                "HTTPS RSA Certificate": {
                    "cert_extensions": {
                        "BasicConstraints": {
                            "enabled": true,
                            "ca": false,
                            "extension_critical": true
                        },
                        "ExtendedKeyUsage": {
                            "enabled": true,
                            "extension_critical": true,
                            "usages": [
                                "SERVER_AUTH",
                                "CLIENT_AUTH"
                            ]
                        },
                        "KeyUsage": {
                            "enabled": true,
                            "extension_critical": true,
                            "digital_signature": true,
                            "key_encipherment": true,
                            "key_agreement": true
                        }
                    },
                    "key_length": 2048,
                    "key_type": "RSA",
                    "lifetime": 397,
                    "digest_algorithm": "SHA256"
                },
                "HTTPS ECC Certificate": {
                    "cert_extensions": {
                        "BasicConstraints": {
                            "enabled": true,
                            "ca": false,
                            "extension_critical": true
                        },
                        "ExtendedKeyUsage": {
                            "enabled": true,
                            "extension_critical": true,
                            "usages": [
                                "SERVER_AUTH",
                                "CLIENT_AUTH"
                            ]
                        },
                        "KeyUsage": {
                            "enabled": true,
                            "extension_critical": true,
                            "digital_signature": true
                        }
                    },
                    "ec_curve": "SECP384R1",
                    "key_type": "EC",
                    "lifetime": 397,
                    "digest_algorithm": "SHA256"
                }
            }
            ```
        """
        ...
    @_ty.overload
    def country_choices(self, 
    /) -> 'dict[str]': 
        """
        Returns country choices for creating a certificate/csr.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            country_choices
        """
        ...
    @_ty.overload
    def create(self, 
        certificate_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create a new Certificate
        
        Certificates are classified under following types and the necessary keywords to be passed
        for `create_type` attribute to create the respective type of certificate
        
        1) Internal Certificate                 -  CERTIFICATE_CREATE_INTERNAL
        
        2) Imported Certificate                 -  CERTIFICATE_CREATE_IMPORTED
        
        3) Certificate Signing Request          -  CERTIFICATE_CREATE_CSR
        
        4) Imported Certificate Signing Request -  CERTIFICATE_CREATE_IMPORTED_CSR
        
        5) ACME Certificate                     -  CERTIFICATE_CREATE_ACME
        
        By default, created certs use RSA keys. If an Elliptic Curve Key is desired, it can be specified with the
        `key_type` attribute. If the `ec_curve` attribute is not specified for the Elliptic Curve Key, then default to
        using "SECP384R1" curve.
        
        A type is selected by the Certificate Service based on `create_type`. The rest of the values in `data` are
        validated accordingly and finally a certificate is made based on the selected type.
        
        `cert_extensions` can be specified to set X509v3 extensions.

        Parameters
        ----------
        certificate_create:
            certificate_create
        Returns
        -------
        dict[str]:
            certificate_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
        force:'bool'=False,
    /) -> 'bool': 
        """
        Delete certificate of `id`.
        
        If the certificate is an ACME based certificate, certificate service will try to
        revoke the certificate by updating it's status with the ACME server, if it fails an exception is raised
        and the certificate is not deleted from the system. However, if `force` is set to True, certificate is deleted
        from the system even if some error occurred while revoking the certificate with the ACME Server

        Parameters
        ----------
        id:
            Delete certificate of `id`.
        force:
            If the certificate is an ACME based certificate, certificate service will try to
            revoke the certificate by updating it's status with the ACME server, if it fails an exception is raised
            and the certificate is not deleted from the system. However, if `force` is set to True, certificate is deleted
            from the system even if some error occurred while revoking the certificate with the ACME Server
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
        """
        ...
    @_ty.overload
    def ec_curve_choices(self, 
    /) -> 'dict[str]': 
        """
        Dictionary of supported EC curves.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            ec_curve_choices
        """
        ...
    @_ty.overload
    def extended_key_usage_choices(self, 
    /) -> 'dict[str]': 
        """
        Dictionary of choices for `ExtendedKeyUsage` extension which can be passed over to `usages` attribute.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            extended_key_usage_choices
        """
        ...
    @_ty.overload
    def get_instance(self, 
        id:'str|int|bool|dict[str]|list',
        query_options_get_instance:'dict[str]'={},
    /) -> None: 
        """
        Returns instance matching `id`. If `id` is not found, Validation error is raised.
        
        Please see `query` method documentation for `options`.

        Parameters
        ----------
        id:
            Returns instance matching `id`. If `id` is not found, Validation error is raised.
        query_options_get_instance:
            query-options-get_instance
        Returns
        -------
        """
        ...
    @_ty.overload
    def key_type_choices(self, 
    /) -> 'dict[str]': 
        """
        Dictionary of supported key types for certificates.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            private_key_type_choices
        """
        ...
    @_ty.overload
    def profiles(self, 
    /) -> 'dict[str]': 
        """
        Returns a dictionary of predefined options for specific use cases i.e openvpn client/server
        configurations which can be used for creating certificates.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            certificate_profiles
        """
        ...
    @_ty.overload
    def query(self, 
        query_filters:'list'=[],
        query_options:'dict[str]'={},
    /) -> 'list|dict[str]|int|dict[str]': 
        """
        

        Parameters
        ----------
        query_filters:
            query-filters
        query_options:
            query-options
        Returns
        -------
        list:
            
        dict[str]:
            
        int:
            
        dict[str]:
            
        """
        ...
    @_ty.overload
    def update(self, 
        id:'int',
        certificate_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update certificate of `id`
        
        Only name and revoked attribute can be updated.
        
        When `revoked` is enabled, the specified cert `id` is revoked and if it belongs to a CA chain which
        exists on this system, its serial number is added to the CA's certificate revocation list.

        Parameters
        ----------
        id:
            Update certificate of `id`
            When `revoked` is enabled, the specified cert `id` is revoked and if it belongs to a CA chain which
            exists on this system, its serial number is added to the CA's certificate revocation list.
        certificate_update:
            certificate_update
        Returns
        -------
        dict[str]:
            certificate_update_returns
        """
        ...
