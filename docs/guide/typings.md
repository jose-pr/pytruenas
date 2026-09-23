# Generating typings

`generate-typings` turns a host's live API definition into a package of `.pyi`
stubs, so editors and type checkers understand
`client.api.<namespace>.<method>(...)` calls — argument names, types, and return
shapes.

```bash
pip install pytruenas[codegen]
pytruenas generate-typings --path truenasapi_typings/current nas.example.com
```

Options:

- `--path PATH` — output directory for the stub package. A previous output is
  replaced; a directory holding anything other than stubs is refused rather
  than emptied.
- `--api-version VERSION` — target a specific API version (e.g. `v26.0.0`);
  defaults to the host's current version.
- `--api-cache FILE` — read/write a cached API dump instead of hitting the host.

The generator dumps the whole API and writes one `.pyi` per namespace. On a real
TrueNAS 26.0 host this produces ~129 stub files covering every namespace; all
output is valid Python that parses cleanly.

The root module of the generated package exports `Current`, an alias for the
version class it generated (`V26000`), which is what makes the documented
annotation resolve:

```python
from truenasapi_typings.current import Current

from pytruenas import TrueNASClient

client: TrueNASClient[Current] = TrueNASClient("nas.example.com", api_key)
client.api.user.query()   # completed and checked from the stubs
```

Optional keys use `NotRequired`, which `typing` only has from Python 3.11, so
the stubs import it from `typing_extensions` below that. Install it in the
environment you type-check in if your target is older than 3.11.

!!! note
    Generated stubs are **not** shipped in the package — they are produced on
    demand for your target's exact API version. `src/truenasapi_typings/` is an
    empty namespace package that your generated `current/` (or versioned)
    stubs drop into.
