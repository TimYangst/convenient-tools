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

After that every script declared in `[project.scripts]` is on your `PATH` (uv drops them in `~/.local/bin`). On zsh/bash that directory is already wired up by `~/.local/bin/env`, which `uv` adds to your shell rc the first time it's used — no further config needed.

To pick up later changes, re-run with `--force`:

```bash
uv tool install --editable . --force
```

## Available tools

All git tools below operate on the current repo's working tree.

### `gac` — git add + commit

`git add -A`, then `git commit`. Any extra arguments are forwarded to `git commit`, so all the usual flags work.

```bash
gac -m "fix: handle empty payload"
gac --amend --no-edit
gac                              # opens $EDITOR for the commit message
```

### `grb` — rebase the current branch onto an updated base

Steps:

1. Refuses to run if the working tree has uncommitted changes.
2. Checks out the base branch and runs `git pull --ff-only` (no surprise merge commits).
3. Checks out the original branch and runs `git rebase <base>`.

```bash
grb                              # rebase current branch onto main
grb -b develop                   # use a different base branch
```

### `gpo` — push the current branch

Pushes the current branch to a remote, always with `-u`, so the upstream is recorded on the first push and `git pull` / `git push` both work bare afterwards.

```bash
gpo                              # git push -u origin <current-branch>
gpo -r upstream                  # push to a different remote
```

Refuses to run if the working tree has uncommitted changes.

## Adding a new tool

1. Create a module under `src/convenient_tools/`, e.g. `src/convenient_tools/foo.py`, exposing a `main()` callable. For git tools, reuse helpers from `src/convenient_tools/_git.py` (`current_branch`, `is_dirty`, `require_clean`, `run`, `capture`).
2. Register it in `pyproject.toml`:

   ```toml
   [project.scripts]
   foo = "convenient_tools.foo:main"
   ```

3. Re-run `uv tool install --editable . --force` (or `uv sync` for dev use) to pick up the new entry point.

## Project layout

```
src/convenient_tools/
├── __init__.py          # placeholder entry point (`convenient-tools`)
├── _git.py              # shared git helpers
├── gac.py               # gac: add + commit
├── grb.py               # grb: rebase onto base
└── gpo.py               # gpo: push current branch
```
