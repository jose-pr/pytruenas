from pytruenas import Namespace as _NS 
class Nfs(_NS):
    
    def bindip_choices(self,
    ) -> NfsBindip_choices:
        """Returns ip choices for NFS service to use"""
        ...
    def config(self,
    ) -> NfsConfig:
        """"""
        ...
    def update(self,
        nfs_update,
    ) -> NfsUpdate:
        """Update NFS Service Configuration.

`servers` - Represents number of servers to create. By default, the number of nfsd is determined by the capabilities of the system. To specify the number of nfsd, set a value between 1 and 256. 'Unset' the field to return to default. This field will always report the number of nfsd to start.

            INPUT: 1 .. 256 or 'unset' where unset will enable the automatic determination and 1 ..256 will set the number of nfsd Default: Number of nfsd is automatically determined and will be no less than 1 and no more than 32

            The number of mountd will be 1/4 the number of reported nfsd.

`allow_nonroot` - If 'enabled' it allows non-root mount requests to be served.

                INPUT: enable/disable (True/False) Default: disabled

`bindip` -  Limit the server IP addresses available for NFS By default, NFS will listen on all IP addresses that are active on the server. To specify the server interface or a set of interfaces provide a list of IP's. If the field is unset/empty, NFS listens on all available server addresses.

            INPUT: list of IP addresses available configured on the server Default: Use all available addresses (empty list)

`protocols` - enable/disable NFSv3, NFSv4 Both can be enabled or NFSv4 or NFSv4 by themselves.  At least one must be enabled. Note:  The 'showmount' command is available only if NFSv3 is enabled.

            INPUT: Select NFSv3 or NFSv4 or NFSv3,NFSv4 Default: NFSv3,NFSv4

`v4_krb` -  Force Kerberos authentication on NFS shares If enabled, NFS shares will fail if the Kerberos ticket is unavilable

            INPUT: enable/disable Default: disabled

`v4_domain` -   Specify a DNS domain (NFSv4 only) If set, the value will be used to override the default DNS domain name for NFSv4. Specifies the 'Domain' idmapd.conf setting.

            INPUT: a string Default: unset, i.e. an empty string.

`mountd_port` - mountd port binding The value set specifies the port mountd(8) binds to.

            INPUT: unset or an integer between 1 .. 65535 Default: unset

`rpcstatd_port` - statd port binding The value set specifies the port rpc.statd(8) binds to.

            INPUT: unset or an integer between 1 .. 65535 Default: unset

`rpclockd_port` - lockd port binding The value set specifies the port rpclockd_port(8) binds to.

            INPUT: unset or an integer between 1 .. 65535 Default: unset

`rdma` -    Enable/Disable NFS over RDMA support Available on supported platforms and requires an installed and RDMA capable NIC. NFS over RDMA uses port 20040.

            INPUT: Enable/Disable Default: Disable"""
        ...
class NfsBindip_choices:
    ...
class NfsConfig:
    ...
class NfsUpdate:
    ... 