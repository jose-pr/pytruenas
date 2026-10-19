# API Reference

Generated from docstrings, organized by module:

- **[Client](client.md)** — `TrueNASClient`: connection, `api`, `path`, `run`,
  `upload`/`download`.
- **[Namespace](namespace.md)** — the dynamic API proxy and the
  `_get`/`_query`/`_create`/`_update`/`_upsert` helpers.
- **[Connection](connection.md)** — the lean middleware client, extended-JSON
  (`dumps`/`loads`), and the errors: `TrueNASError` and its subclasses.
- **[Auth](auth.md)** — `Credentials` and the credential types.
- **[Filesystem](fs.md)** — `TnasWsPath`, the websocket leg of `client.path()`.
- **[Host](host.md)** — `TrueNASClient`'s hostctl half and `TrueNASConfig`, the transport
  providers, and the web-shell executor.
