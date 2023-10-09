<%
%>
from pytruenas import Namespace
import typing
class ${ns.classname}(Namespace):
    def __init__(self, client) -> None:
        super().__init__(client, '${ns.dotname}')

    %for name, obj in ns.objects.items():
    ${name} = typing.TypedDict('${name}', {
    %for pname, ty in obj.properties.items():
            '${pname}':'${ty.python()}',
    %endfor
    })
    %endfor