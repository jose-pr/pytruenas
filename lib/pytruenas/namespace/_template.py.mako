<%
%>
from pytruenas import Namespace
class ${exportas}(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, '${ns['config']['namespace']}')

