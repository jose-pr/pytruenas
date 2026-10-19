# Generating typings

`generate-typings` turns a host's live API definition into a package of `.pyi`
stubs, so editors and type checkers understand
`client.api.<namespace>.<method>(...)` calls — argument names, types, and return
shapes.

```bash
pip install pytruenas
pytruenas generate-typings --path truenasapi_typings/current nas.example.com
```

Options:

- `--path PATH` — output directory for the stub package (default
  `truenasapi_typings/current`). A previous output (it carries a
  `.pytruenas-typings` marker) is replaced; any other directory that is not
  empty is refused rather than emptied — hand-written stubs included.
- `--api-version VERSION` — target a specific API version (e.g. `v26.0.0`);
  defaults to the newest version in the dump.
- `--from FILE` — read the API definition from a dump file instead of the
  host: `pytruenas dump-api` output, or a gzipped file from
  `$PYTRUENAS_CACHE`. Nothing connects. Without it, the definition comes
  from `client.dump_api()`, which caches it per host and API version.

The generator dumps the whole API and writes one `.pyi` per namespace (about
129 files for a TrueNAS 26.0 host). The test suite generates stubs from a small
fixture dump and from a set of unusual schema shapes, compiles them, and
type-checks them and calls against them with pyright and mypy; it does not run
against a full live dump.

The root module of the generated package exports `Current`, an alias for the
version class it generated (`V2600` for v26.0.0), which is what makes the documented
annotation resolve:

```python
from truenasapi_typings.current import Current

from pytruenas import TrueNASClient

client: TrueNASClient[Current] = TrueNASClient("nas.example.com", credentials=api_key)
client.api.user.query()   # completed and checked from the stubs
```

Optional keys use `NotRequired` (and an array that admits no items is
`list[Never]`), which `typing` only has from Python 3.11, so the stubs import
them from `typing_extensions` below that. Install it in the environment you
type-check in if your target is older than 3.11. The output is the same
whichever Python version runs the generator.

!!! note
    Generated stubs are **not** shipped in the package — they are produced on
    demand for your target's exact API version. Generate them inside your
    project (the default `--path` does) so that pyright or mypy, run from the
    project root, resolves `truenasapi_typings.current`.
