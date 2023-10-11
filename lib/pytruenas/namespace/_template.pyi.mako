<%
        from pytruenas.api import Object, Enum
        from pytruenas import _utils
%>
from pytruenas import TrueNASClient
from ${str(ns.baseclass.__module__)} import ${str(ns.baseclass.__name__)}
% for mixin in ns.mixins:
from ${str(mixin.__module__)} import ${str(mixin.__name__)}
% endfor
from enum import Enum
import typing
class ${ns.classname}(
% for mixin in ns.mixins:
    ${str(mixin.__name__)},
% endfor
    ${str(ns.baseclass.__name__)}
    ):
    _namespace:typing.Literal['${ns.dotname}']
    def __init__(self, client:TrueNASClient) -> None: ...
% for method in ns.methods:
    @typing.overload
    def ${method.name}(self, 
    % for pname, param in method.arguments.items():
        ${pname}\
        %if param.type:
:'${param.type.python()}'\
        %endif
        %if not param.required and param.default != MISSING:
=${param.default}\
        %endif
,
    % endfor
    /)\
%if not method.returns:
 -> None\
%else:
 -> '\
${'|'.join([p.type.python() for p in method.returns])}\
'\
%endif
: 
        """
        ${(method.description or '').strip().replace('\n', '\n        ')}

        Parameters
        ----------
% for pname, param in method.arguments.items():
        ${pname}:
            ${(param.description or '').strip().replace('\n', '\n            ')}
%endfor
        Returns
        -------
% for param in method.returns:
        ${param.type.python()}:
            ${(param.description or '').strip().replace('\n', '\n            ')}
%endfor
        """
        ...
% endfor
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
