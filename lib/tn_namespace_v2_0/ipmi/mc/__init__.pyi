
from pytruenas import Namespace, TrueNASClient
import typing
class IpmiMc(Namespace):
    _namespace:typing.Literal['ipmi.mc']
    def __init__(self, client:TrueNASClient) -> None: ...
    @typing.overload
    def info(self, 
    /) -> 'dict[str]': 
        """
        Return looks like:
        {
            'auxiliary_firmware_revision_information': '00000006h',
            'bridge': 'unsupported',
            'chassis_device': 'supported',
            'device_available': 'yes (normal operation)',
            'device_id': '32',
            'device_revision': '1',
            'device_sdrs': 'unsupported',
            'firmware_revision': '6.71',
            'fru_inventory_device': 'supported',
            'ipmb_event_generator': 'supported',
            'ipmb_event_receiver': 'supported',
            'ipmi_version': '2.0',
            'manufacturer_id': 'Super Micro Computer Inc. (10876)',
            'product_id': '2327',
            'sdr_repository_device': 'supported',
            'sel_device': 'supported',
            'sensor_device': 'supported'
        }

        Parameters
        ----------
        Returns
        -------
        dict[str]:
            mc_info
        """
        ...

