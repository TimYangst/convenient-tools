"""gpo: push the current branch to a remote (default origin)."""
import argparse

from . import _git


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="gpo",
        description="Push the current branch to the given remote (default: origin).",
    )
    parser.add_argument(
        "-r", "--remote", default="origin", help="remote name (default: origin)"
    )
    args = parser.parse_args()

    _git.require_clean()
    branch = _git.current_branch()
    _git.run("git", "push", "-u", args.remote, branch)
