
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class Certificateauthority(Namespace):
    _namespace:_ty.Literal['certificateauthority']
    def __init__(self, client:TrueNASClient) -> None: ...
    @_ty.overload
    def ca_sign_csr(self, 
        ca_sign_csr:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Sign CSR by Certificate Authority of `ca_id`
        
        Sign CSR's and generate a certificate from it. `ca_id` provides which CA is to be used for signing
        a CSR of `csr_cert_id` which exists in the system
        
        `cert_extensions` can be specified if specific extensions are to be set in the newly signed certificate.

        Parameters
        ----------
        ca_sign_csr:
            ca_sign_csr
        Returns
        -------
        dict[str]:
            certificate_entry
        """
        ...
    @_ty.overload
    def create(self, 
        ca_create:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Create a new Certificate Authority
        
        Certificate Authorities are classified under following types with the necessary keywords to be passed
        for `create_type` attribute to create the respective type of certificate authority
        
        1) Internal Certificate Authority       -  CA_CREATE_INTERNAL
        
        2) Imported Certificate Authority       -  CA_CREATE_IMPORTED
        
        3) Intermediate Certificate Authority   -  CA_CREATE_INTERMEDIATE
        
        Created certificate authorities use RSA keys by default. If an Elliptic Curve Key is desired, then it can be
        specified with the `key_type` attribute. If the `ec_curve` attribute is not specified for the Elliptic
        Curve Key, default to using "SECP384R1" curve.
        
        A type is selected by the Certificate Authority Service based on `create_type`. The rest of the values
        are validated accordingly and finally a certificate is made based on the selected type.
        
        `cert_extensions` can be specified to set X509v3 extensions.

        Parameters
        ----------
        ca_create:
            ca_create
        Returns
        -------
        dict[str]:
            certificateauthority_create_returns
        """
        ...
    @_ty.overload
    def delete(self, 
        id:'int',
    /) -> 'bool': 
        """
        Delete a Certificate Authority of `id`

        Parameters
        ----------
        id:
            Delete a Certificate Authority of `id`
        Returns
        -------
        bool:
            Will return `true` if `id` is deleted successfully
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
    def profiles(self, 
    /) -> 'dict[str]': 
        """
        Returns a dictionary of predefined options for specific use cases i.e OpenVPN certificate authority
        configurations which can be used for creating certificate authorities.

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            certificate_authority_profiles
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
        ca_update:'dict[str]'={},
    /) -> 'dict[str]': 
        """
        Update Certificate Authority of `id`
        
        Only `name` and `revoked` attribute can be updated.
        
        If `revoked` is enabled, the CA and its complete chain is marked as revoked and added to the CA's
        certificate revocation list.

        Parameters
        ----------
        id:
            Update Certificate Authority of `id`
        ca_update:
            ca_update
        Returns
        -------
        dict[str]:
            certificateauthority_update_returns
        """
        ...
