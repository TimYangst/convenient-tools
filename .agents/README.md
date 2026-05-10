# .agents/ — Shared Agent Skills

Reusable skills for AI coding agents (Claude Code, Codex, Cursor, …) working in this repo. Follows the [Agent Skills](https://agentskills.io) open standard.

## Structure

```
.agents/
└── skills/
    └── <skill-name>/
        └── SKILL.md   # frontmatter (name, description) + instructions
```

## Linking skills to user-level Claude Code

Skills live in this repo so they version with the code, but they're symlinked into `~/.claude/skills/` so they're available in every directory.

Run once (and re-run after adding a new skill — it's idempotent):

```bash
bash .agents/setup_agent.sh claude
```

The script symlinks every `.agents/skills/<name>/` into `~/.claude/skills/<name>`, leaves existing correct links alone, and exits non-zero if it finds a conflicting file or mismatched link.

Invoke from chat with `/<skill-name>` once linked.

## Skills

| Skill | What it does |
|-------|--------------|
| `clean-git-branches` | List local branches whose last commit is older than a threshold (default 2 weeks) and delete the ones you confirm. |
