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
        %if not param.get('required', True):
=${param.get('default',None)}\
        %endif
,
    % endfor
    /): 
        """${method['description'] or ''}
        """
        ...
% endfor
