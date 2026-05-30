---
name: repo-main-refresh
description: Check a Git repo before creating new worktrees, safely refresh local main from origin/main, and report dirty worktrees. Use when Codex is asked to inspect repo freshness, compare main with its remote, check for untracked or uncommitted work, or before creating a new worktree from main.
---

# Repo Main Refresh

## Workflow

Run this before creating a new worktree from `main`, or when asked to check where `main` is relative to the remote:

```bash
uv run /Users/houstonp/.codex/skills/repo-main-refresh/scripts/refresh_main.py
```

Use `--check-only` only for an audit that must not fast-forward local `main`:

```bash
uv run /Users/houstonp/.codex/skills/repo-main-refresh/scripts/refresh_main.py --check-only
```

The helper fetches with `git fetch --prune origin`, requires local `main` to track `origin/main`, finds the worktree where `main` is checked out, and fast-forwards only when the `main` checkout is clean and local `main` is behind-only.

## Stop Conditions

Stop and ask the user what to do when the helper exits `1`. Do not create a new worktree from `main` unless the report includes:

```text
SAFE: local main is ready for a new worktree.
```

Expected blockers include:

- No Git repo at the current path.
- No checked-out `main` worktree.
- Local `main` does not track `origin/main`.
- `origin/main` is missing after fetch.
- The `main` checkout has tracked modifications or normal untracked files.
- Local `main` is ahead of `origin/main`.
- Local `main` has diverged from `origin/main`.
- `--check-only` finds that local `main` is behind and would need a fast-forward.

Ignored files do not block or report by default.

## Report Handling

Read the compact report and carry its state forward:

- Use the listed main checkout path as the source of truth for `main`.
- Mention whether `main` was already current or fast-forwarded.
- Surface dirty non-`main` worktrees as context, but do not treat them as blockers.
- After a safe report, create the requested worktree from updated local `main` using the repo's normal branch and path conventions.

Exit codes:

- `0`: `main` is current or was safely fast-forwarded.
- `1`: Git state needs user choice before proceeding.
- `2`: Script misuse or unexpected runtime failure.
