<%
%>
from pytruenas import Namespace, TrueNASClient
import typing as _ty
class ${exportas}(Namespace):
    _namespace:_ty.Literal['${ns['config']['namespace']}']
    def __init__(self, client:TrueNASClient) -> None: ...
% for name, method in ns['methods'].items():
    def ${name}(self, 
    % for param in method['accepts']:
        ${param['name']}\
        %if 'type' in param:
:${'|'.join([str(t) for t in param['type']])}\
        %endif
        %if not param.get('required', True):
=${param.get('default',None)}\
        %endif
,
    % endfor
    /)\
%if not method['returns']:
 -> None\
%else:
 -> ${'|'.join([str(t) for t in method['_returns']])}\
%endif
: 
        """${method['description'] or ''}
        """
        ...
% endfor
