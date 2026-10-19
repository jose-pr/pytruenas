# Host

`TrueNASClient` is a [hostctl](https://github.com/jose-pr/hostctl) `PosixHost`:
`run`, `path`, `spawn`, `info`, `close`, `shell`, `capabilities`, and
`last_selection` are inherited, and it adds the TrueNAS surface (`api`,
`conn`, `connect` (the API connection only), `login`, `upload`, `download`,
`dump_api`, `install_sshcreds`).

`TrueNASConfig` is the matching `HostConfig`. It accepts every connection string
`TrueNASClient` does and normalizes to a `truenas+*` scheme, so
`HostConfig("truenas+wss://nas")` resolves through hostctl's own registry.

::: pytruenas.host

## Providers

::: pytruenas.providers

## Web shell

::: pytruenas.webshell
