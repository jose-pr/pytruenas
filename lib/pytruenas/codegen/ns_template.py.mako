<%
    from pytruenas.api import Object, Enum
    from pytruenas import _utils
%>
from ${str(ns.baseclass.__module__)} import ${str(ns.baseclass.__name__)}
% for mixin in ns.mixins:
from ${str(mixin.__module__)} import ${str(mixin.__name__)}
% endfor

import typing
from enum import Enum

class ${ns.classname}(\
% for mixin in ns.mixins:
${str(mixin.__name__)}, \
% endfor
${str(ns.baseclass.__name__)}):
    def __init__(self, client) -> None:
        super().__init__(client, '${ns.dotname}')

    %for obj in ns.objects:
    %if isinstance(obj, Object):
    ${obj.name} = typing.TypedDict('${obj.name}', {
    %for pname, ty in obj.properties.items():
            '${pname}':'${ty.python()}',
    %endfor
    })
    %elif isinstance(obj, Enum):
    class ${obj.name}(${obj.type.python()},Enum):
    %for val in obj.options:
    %if val is None:
        NONE = None
    %else:
        ${_utils.classname(val)} = '${val}'
    %endif
    %endfor
        ...
    %endif
    %endfor