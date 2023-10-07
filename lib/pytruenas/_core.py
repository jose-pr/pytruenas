
from typing import TypedDict


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
    service_verb_syn:bool
    namespace: str
    namespace_alias: str
    private: bool
    cli_namespace: str
    cli_private: bool
    cli_description: str
    role_prefix: str
    role_separate_delete: bool
    verbose_name: str

class Service(TypedDict):
    config: ServiceConfig
    type: str


class ServiceMethodVars(TypedDict):
    _name_: str
    title: str
    _required_: bool
    type: 'str|list[str]'
    description: str

class ServiceMethod(TypedDict):
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
  accepts: ServiceMethodVars
  returns: ServiceMethodVars | None

class Event(TypedDict):
    description: str
    wildcard_subscription: bool
    accepts: list[ServiceMethodVars]
    returns: dict

