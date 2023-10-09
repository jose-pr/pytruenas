<%
%>
from ${str(ns.baseclass.__module__)} import ${str(ns.baseclass.__name__)}
% for mixin in ns.mixins:
from ${str(mixin.__module__)} import ${str(mixin.__name__)}
% endfor

import typing
class ${ns.classname}(\
% for mixin in ns.mixins:
${str(mixin.__name__)}, \
% endfor
${str(ns.baseclass.__name__)}):
    def __init__(self, client) -> None:
        super().__init__(client, '${ns.dotname}')

    %for name, obj in ns.objects.items():
    ${name} = typing.TypedDict('${name}', {
    %for pname, ty in obj.properties.items():
            '${pname}':'${ty.python()}',
    %endfor
    })
    %endfor