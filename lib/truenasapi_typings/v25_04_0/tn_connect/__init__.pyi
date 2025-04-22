from pytruenas import Namespace as _NS 
class Tn_connect(_NS):
    
    def config(self,
    ) -> Tn_connectConfig:
        """"""
        ...
    def generate_claim_token(self,
    ) -> Tn_connectGenerate_claim_token:
        """Generate a claim token for TrueNAS Connect.

This is used to claim the system with TrueNAS Connect. When this endpoint will be called, a token will be generated which will be used to assist with initial setup with truenas connect."""
        ...
    def get_registration_uri(self,
    ) -> Tn_connectGet_registration_uri:
        """Return the registration URI for TrueNAS Connect.

Before this endpoint is called, tn_connect must be enabled and a claim token must be generated - based off which this endpoint will return the registration URI for TrueNAS Connect."""
        ...
    def ip_choices(self,
    ) -> Tn_connectIp_choices:
        """Returns IP choices which can be used with TrueNAS Connect."""
        ...
    def update(self,
        tn_connect_update,
    ) -> Tn_connectUpdate:
        """Update TrueNAS Connect configuration."""
        ...
class Tn_connectConfig:
    ...
class Tn_connectGenerate_claim_token:
    ...
class Tn_connectGet_registration_uri:
    ...
class Tn_connectIp_choices:
    ...
class Tn_connectUpdate:
    ... 