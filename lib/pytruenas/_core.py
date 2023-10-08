from typing import TypedDict
from . import _utils


class ServiceConfig(TypedDict):
    datastore: str
    datastore_prefix: str
    datastore_extend: None
    datastore_extend_context: None
    datastore_primary_key: str
    datastore_primary_key_type: str
    event_register: bool
    event_send: bool
    service: None
    service_verb: str
    service_verb_syn: bool
    namespace: str
    namespace_alias: str
    private: bool
    cli_namespace: str
    cli_private: bool
    cli_description: str
    role_prefix: str
    role_separate_delete: bool
    verbose_name: str


class NamespaceInfo(TypedDict):
    config: ServiceConfig
    type: str
    methods: "Method"


class Parameter(TypedDict):
    name: str
    title: str
    required: bool
    type: "str|list[str]"
    description: str

    def _normalize(self) -> "Parameter":
        # type: ignore
        if self:
            self = {k.strip("_"): v for k, v in self.items()}
            _ty = self.get("type", _utils.MISSING)
            match _ty:
                case _utils.MISSING:
                    if "type" not in self:
                        if "anyOf" in self:
                            k = "anyOf"
                        else:
                            pass
                        self[k] = [Parameter._normalize(v) for v in self[k]]
            for k in ["items"]:
                if k in self:
                    self[k] = [Parameter._normalize(v) for v in self[k]]
        return self


class Method(TypedDict):
    description: str
    cli_description: str
    examples: dict
    item_method: bool
    no_auth_required: bool
    filterable: bool
    filterable_schema: None
    pass_application: bool
    extra_methods: None
    require_websocket: bool
    job: bool
    downloadable: bool
    uploadable: bool
    check_pipes: list
    accepts: Parameter
    returns: Parameter | None

    def _normalize(self):
        # type: ignore
        returns = self["returns"]
        if returns is None:
            returns = []
        self["accepts"] = [Parameter._normalize(v) for v in self["accepts"]]
        self["returns"] = [Parameter._normalize(v) for v in returns]
        return self


class Event(TypedDict):
    description: str
    wildcard_subscription: bool
    accepts: list[Parameter]
    returns: dict
