"""gac: git add -A && git commit (forwards extra args, e.g. -m "msg")."""
import subprocess
import sys


def main() -> None:
    add = subprocess.run(["git", "add", "-A"])
    if add.returncode != 0:
        sys.exit(add.returncode)
    commit = subprocess.run(["git", "commit", *sys.argv[1:]])
    sys.exit(commit.returncode)
