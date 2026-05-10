# convenient-tools

A personal collection of command-line utilities, packaged together so they install with one `uv tool install`.

## Install (editable, for development)

```bash
uv sync
uv run convenient-tools          # runs the placeholder entry point
```

## Install globally on your machine

```bash
uv tool install --editable .
```

After that every script declared in `[project.scripts]` is on your `PATH`.

## Adding a new tool

1. Create a module under `src/convenient_tools/`, e.g. `src/convenient_tools/gac.py`, exposing a `main()` callable.
2. Register it in `pyproject.toml`:

   ```toml
   [project.scripts]
   gac = "convenient_tools.gac:main"
   ```

3. Re-run `uv tool install --editable . --force` (or `uv sync` for dev use) to pick up the new entry point.
