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
        - ClientException
        - ValidationErrors
        - CallTimeout
        - ConnectionClosed
        - JobFailed

## Errors

Every error above, and `pytruenas.auth.AuthenticationError`, derives from one
base, exported from the package root with them:

::: pytruenas.exceptions
    options:
      members:
        - TrueNASError
