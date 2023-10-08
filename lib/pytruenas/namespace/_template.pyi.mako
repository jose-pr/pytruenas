<%
%>
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class ${ns.classname}(Namespace):
    _namespace:_ty.Literal['${ns.dotname}']
    def __init__(self, client:TrueNASClient) -> None: ...
% for name, signatures in ns.methods.items():
% for method in signatures:
    @_ty.overload
    def ${name}(self, 
    % for pname, param in method.arguments.items():
        ${pname}\
        %if param.type:
:'${'|'.join([t.python() for t in param.type])}'\
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
%for p in method.returns:
${'|'.join([t.python() for t in p.type])}\
 %endfor
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
% for t in param.type:
        ${t.python()}:
            ${(param.description or '').strip().replace('\n', '\n            ')}
%endfor
%endfor
        """
        ...
% endfor
% endfor
