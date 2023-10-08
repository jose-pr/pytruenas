
from pytruenas import Namespace
class IpmiSensors(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, 'ipmi.sensors')

