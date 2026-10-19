# Connection

The JSON-RPC 2.0 transport to the middleware. `TrueNASWSConnection` is what
`client.conn` returns; it is rarely constructed directly, since
`TrueNASClient` opens and authenticates one for you.

::: pytruenas.connection
    options:
      members:
        - TrueNASWSConnection
        - Subscription
        - Event
        - dumps
        - loads

## Errors

Every error pytruenas raises derives from one base, `TrueNASError`; all of them
are defined in `pytruenas.exceptions` and exported from the package root.

::: pytruenas.exceptions
