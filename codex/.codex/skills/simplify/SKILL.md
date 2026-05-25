---
name: simplify
description: Review and clean changed code by launching three parallel review agents for reuse, quality, and efficiency, then directly fixing accepted findings. Use when the user asks to simplify, clean up, review, de-hack, refactor lightly, or improve changed files, commits, PR diffs, staged/unstaged work, or untracked changes.
---

# Simplify

Run a focused cleanup review over a selected change set, aggregate three independent review passes, and edit the code immediately after aggregation.

## Change Set

Select the reviewed changes from the user's request and local context:

- If the user names a PR, commit, branch, range, patch, staged changes, unstaged changes, working tree, or untracked files, use that exact scope.
- If the scope is a PR or branch, diff against the appropriate base or merge-base for the repository.
- If the scope is a commit, use that commit's patch.
- If the scope is the current working tree, include staged, unstaged, and relevant untracked files when the request implies all local changes.
- If no scope is clear, inspect repository status and ask the user what to review.
- If the selected scope has no changes, stop and ask; do not silently substitute recently modified files.

Capture the full patch for tracked changes. For untracked files, include their full content when small enough, otherwise include a concise file summary plus the important sections.

## Language References

Before launching reviewers, load the reference files for languages or frameworks present in the change set:

- Rust: `references/rust.md`
- Python: `references/python.md`

If a changed language has no reference file, continue with general review judgment and note that no language-specific reference existed.

## Parallel Reviews

Launch three review agents concurrently, preferably in one agent-tool message when the environment supports it. Pass each agent the same full change-set context and any loaded language references. Do not run the three passes serially. If the environment cannot launch three agents concurrently, stop and tell the user the skill cannot run as required.

Each agent should return findings with file paths, line references when possible, severity, rationale, and a concrete fix recommendation. Ask agents to avoid praise and focus only on actionable issues.

### Agent 1: Code Reuse

Find changed code that should reuse existing utilities, helpers, types, modules, or framework patterns. Search adjacent files, shared utility modules, and existing call sites before flagging duplication.

Focus on:

- New functions duplicating existing behavior.
- Inline path, string, environment, parsing, validation, or type-checking logic that should use a project or standard helper.
- Local abstractions that conflict with established repository patterns.

### Agent 2: Code Quality

Find hacky, brittle, or over-complicated changes.

Focus on:

- Redundant state or cached values that should be derived.
- Parameter sprawl instead of restructuring an API.
- Copy-paste with slight variation.
- Leaky abstractions or boundary violations.
- Stringly typed values where constants, enums, unions, or domain types exist.
- Unnecessary UI/JSX wrappers when component props can express layout directly.
- Deep nested conditionals that should be flattened.
- Comments explaining what changed or what obvious code does; keep only non-obvious why.

### Agent 3: Efficiency

Find unnecessary work, avoidable overhead, and missed concurrency.

Focus on:

- Redundant computations, file reads, API calls, or N+1 patterns.
- Independent operations that can run concurrently.
- New hot-path work in startup, request, render, loop, or per-item paths.
- Store/state updates that fire when nothing changed.
- Existence pre-checks before file/resource operations; prefer direct operation and error handling.
- Unbounded collections, leaks, missing cleanup, and overly broad reads or loads.

## Fix Pass

Wait for all three agents. Aggregate findings by root cause, deduplicate overlap, and edit the code directly for findings that are correct and worth addressing.

When a finding is a false positive or not worth addressing, skip it without debating it. Track the skip reason for the final report.

Keep fixes scoped to the selected change set unless a small adjacent edit is required to use an existing helper or preserve consistency.

## Verification

Run the narrowest credible verification for the edits, following repository instructions first:

- Read local agent/project instructions when present.
- Use the repository's package manager and command surface.
- Prefer format, lint/typecheck, and targeted tests affected by the cleanup.
- If verification is expensive or unavailable, run the highest-signal subset and report what was not run.

## Final Report

Report:

- Change scope reviewed.
- Issues fixed.
- Findings skipped as false positives or not worth changing, with short reasons.
- Verification commands run and their outcomes.
- Any verification not run.
