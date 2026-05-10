#!/usr/bin/env bash
# Symlink every skill in .agents/skills/ into a user-level agent skills directory
# so the skills maintained in this repo are globally available to AI coding agents.
#
# Usage:
#   bash .agents/setup_agent.sh [agent_name]
#
# Examples:
#   bash .agents/setup_agent.sh           # defaults to "claude" -> ~/.claude/skills/
#   bash .agents/setup_agent.sh claude
#
# Re-running is safe: correct symlinks are left alone, mismatches are reported,
# and missing links are created.

set -euo pipefail

AGENT_NAME="${1:-claude}"

case "$AGENT_NAME" in
    claude) TARGET_DIR="$HOME/.claude/skills" ;;
    *)
        echo "ERROR: unknown agent '$AGENT_NAME'. Supported: claude" >&2
        echo "To add another agent, extend the case statement in $(basename "$0")." >&2
        exit 1
        ;;
esac

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SKILLS_SRC="${REPO_ROOT}/.agents/skills"

if [[ ! -d "$SKILLS_SRC" ]]; then
    echo "ERROR: no skills directory at $SKILLS_SRC" >&2
    exit 1
fi

mkdir -p "$TARGET_DIR"

linked=()
ok=()
conflict=()

for skill_dir in "$SKILLS_SRC"/*/; do
    [[ -d "$skill_dir" ]] || continue
    skill_dir="${skill_dir%/}"
    skill_name="$(basename "$skill_dir")"
    target="$TARGET_DIR/$skill_name"

    if [[ -L "$target" ]]; then
        current="$(readlink "$target")"
        if [[ "$current" == "$skill_dir" ]]; then
            ok+=("$skill_name")
            continue
        fi
        conflict+=("$skill_name -> $current (expected $skill_dir)")
        continue
    elif [[ -e "$target" ]]; then
        conflict+=("$skill_name (exists, not a symlink)")
        continue
    fi

    ln -s "$skill_dir" "$target"
    linked+=("$skill_name")
done

echo "Agent:  $AGENT_NAME"
echo "Target: $TARGET_DIR"
echo "Source: $SKILLS_SRC"
if [[ ${#linked[@]} -gt 0 ]]; then
    echo "Linked:"
    printf '  + %s\n' "${linked[@]}"
fi
if [[ ${#ok[@]} -gt 0 ]]; then
    echo "Already linked:"
    printf '  = %s\n' "${ok[@]}"
fi
if [[ ${#conflict[@]} -gt 0 ]]; then
    echo "Conflicts (skipped, resolve manually):"
    printf '  ! %s\n' "${conflict[@]}"
    exit 1
fi
exit 0
