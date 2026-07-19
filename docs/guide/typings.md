# Generating typings

`generate-typings` turns a host's live API definition into a package of `.pyi`
stubs, so editors and type checkers understand
`client.api.<namespace>.<method>(...)` calls — argument names, types, and return
shapes.

```bash
pip install pytruenas[codegen]
pytruenas generate-typings -t nas.example.com --path truenasapi_typings/current
```

Options:

- `--path PATH` — output directory for the stub package.
- `--api-version VERSION` — target a specific API version (e.g. `v26.0.0`);
  defaults to the host's current version.
- `--api-cache FILE` — read/write a cached API dump instead of hitting the host.

The generator dumps the whole API and writes one `.pyi` per namespace. On a real
TrueNAS 26.0 host this produces ~129 stub files covering every namespace; all
output is valid Python that parses cleanly.

!!! note
    Generated stubs are **not** shipped in the package — they are produced on
    demand for your target's exact API version. `src/truenasapi_typings/` is an
    empty namespace package that your generated `current/` (or versioned)
    stubs drop into.
