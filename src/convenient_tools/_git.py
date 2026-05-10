"""Shared git helpers for convenient_tools."""
import subprocess
import sys


def capture(*args: str) -> str:
    r = subprocess.run(list(args), capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        sys.exit(r.returncode)
    return r.stdout.strip()


def current_branch() -> str:
    return capture("git", "rev-parse", "--abbrev-ref", "HEAD")


def is_dirty() -> bool:
    r = subprocess.run(
        ["git", "status", "--porcelain"], capture_output=True, text=True
    )
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        sys.exit(r.returncode)
    return bool(r.stdout.strip())


def require_clean() -> None:
    if is_dirty():
        sys.stderr.write(
            "error: working tree has uncommitted changes; commit or stash first.\n"
        )
        sys.exit(1)


def run(*args: str) -> None:
    """Run a git command, exiting with its returncode on failure."""
    r = subprocess.run(list(args))
    if r.returncode != 0:
        sys.exit(r.returncode)
