<%
%>
from pytruenas import Namespace
class ${ns.classname}(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, '${ns.dotname}')

