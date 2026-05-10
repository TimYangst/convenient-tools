"""grb: rebase the current branch on top of an updated base branch (default main)."""

import argparse
import sys

from . import _git


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="grb",
        description="Update the base branch and rebase the current branch on top of it.",
    )
    parser.add_argument(
        "-b", "--base", default="main", help="base branch to rebase onto (default: main)"
    )
    args = parser.parse_args()

    _git.require_clean()

    base = args.base
    cur = _git.current_branch()
    if cur == base:
        sys.stderr.write(f"error: already on '{base}'; nothing to rebase.\n")
        sys.exit(1)

    _git.run("git", "checkout", base)
    _git.run("git", "pull", "--ff-only")
    _git.run("git", "checkout", cur)
    _git.run("git", "rebase", base)
