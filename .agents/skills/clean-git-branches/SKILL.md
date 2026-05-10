---
name: clean-git-branches
description: List local git branches in the current repo whose last commit is older than a threshold (default 2 weeks) as cleanup candidates, then delete the ones the user confirms. Optional argument sets the threshold (e.g., "1month", "30d", "2026-01-01").
---

# Clean stale local git branches

Goal: surface local branches that have gone quiet in the current repo and delete the ones the user confirms. Never touches remotes, the working tree, or remote-tracking refs.

## Input

The skill arg, if any, is the inactivity threshold. Normalize it to a git-compatible relative spec:

- `2w`, `2weeks`, `2 weeks` → `2.weeks.ago`
- `30d`, `30days` → `30.days.ago`
- `1m`, `1month` → `1.month.ago`
- ISO date like `2026-01-01` → keep as-is, compare with `git log -1 --format=%cI`
- Empty arg → default `2.weeks.ago`

## Procedure

1. **Verify repo.** Run `git rev-parse --is-inside-work-tree`. If it fails, stop and tell the user the current directory is not a git repo.

2. **Identify protected names.** Always exclude:
   - `main`, `master`, `develop` (and the current `HEAD` branch — git refuses to delete it anyway)
   - Anything the user has listed as protected in this repo's `CLAUDE.md` or `.agents/skills/clean-git-branches/protected.txt` if present

3. **Collect candidates.** Run:
   ```bash
   git for-each-ref --sort=committerdate refs/heads/ \
     --format='%(refname:short)|%(committerdate:iso8601)|%(committerdate:relative)|%(authorname)|%(subject)'
   ```
   Keep only rows whose `committerdate` is **strictly older** than the cutoff, and whose name is not protected.

4. **Annotate merged status (this drives delete safety).** Pick a base ref: prefer `main`, fall back to `master`, then `develop`. Run `git branch --merged <base> --format='%(refname:short)'` and mark each candidate as `merged` or `unmerged`. This classification — not git's built-in `-d` heuristic — is what step 7 trusts when deciding whether a delete is safe. Surface the chosen base in the list header so the user knows what "merged" means.

5. **Present the list.** Show a compact table:
   ```
   branch                last commit       author     merged?  subject
   feat/old-thing        3 months ago      alice      merged   add foo
   wip/spike             5 weeks ago       bob        unmerged try bar
   ```
   If there are zero candidates, say so and stop.

6. **Ask which to delete.** Use `AskUserQuestion`:
   - "Delete all merged candidates" — only the `merged` ones
   - "Pick which to delete" — follow up with multi-select question(s), 4 options per question, listing candidates
   - "Cancel" — stop, delete nothing

7. **Delete by category.** Use the step-4 classification as authoritative — it answers the only safety question that matters (is the branch tip reachable from `<base>`?). Do **not** rely on `git branch -d`'s safety check, which consults the current `HEAD`/upstream and will reject branches that are merged into `<base>` but not into `HEAD`.
   - **For branches marked `merged` (into `<base>`):** run `git branch -D <name>` directly. We've already verified the tip is in `<base>`, so no commits are lost.
   - **For branches marked `unmerged`:** try `git branch -d <name>` first (it occasionally succeeds when the branch is merged into `HEAD` even if not into `<base>`). If it fails, surface that branch back to the user and ask explicitly: "X is unmerged into `<base>`. Force-delete with `git branch -D`?" Only run `-D` after a per-branch yes. Never batch-force unmerged branches.

8. **Report.** Print:
   - Deleted: `<name> (merged | safe-d | forced)` — `merged` = deleted via `-D` after step-4 verified it's in `<base>`; `safe-d` = unmerged candidate whose `-d` happened to succeed; `forced` = unmerged candidate the user explicitly approved for `-D`.
   - Skipped: `<name> (reason)`

## Hard rules

- Local branches only. Do not run `git push :<branch>`, `git push --delete`, or touch `refs/remotes/`.
- Do not switch branches, stash, reset, or modify the working tree.
- Do not auto-force-delete. Unmerged deletion always needs explicit per-branch confirmation.
- If `git status --porcelain` shows changes, that's fine — branch deletion does not touch files. Proceed.
- Do not delete a branch that another worktree has checked out. If `git branch -d` reports "checked out at", surface that and skip.
