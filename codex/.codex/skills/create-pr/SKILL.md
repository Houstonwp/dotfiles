---
name: create-pr
description: Create pull requests following project conventions. Use when opening PRs, writing PR descriptions, or preparing changes for review.
---

# Create Pull Request

Create pull requests following project engineering practices.

**Requires**: GitHub CLI (`gh`) authenticated and available.

## Prerequisites

Before creating a PR, ensure all changes are committed. If there are uncommitted changes, run the `commit` skill first to commit them properly.

```bash
# Check for uncommitted changes
git status --porcelain
```

If the output shows any uncommitted changes (modified, added, or untracked files that should be included), invoke the `commit` skill before proceeding.

## Process

### Step 1: Verify Branch State

```bash
# Detect the default branch
BASE=$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name')

# Check current branch and status
git status
git log $BASE..HEAD --oneline
```

Ensure:
- All changes are committed
- Branch is up to date with remote
- Changes are rebased on the base branch if needed

### Step 2: Analyze Changes

Review what will be included in the PR:

```bash
# See all commits that will be in the PR
git log $BASE..HEAD

# See the full diff
git diff $BASE...HEAD
```

Understand the scope and purpose of all changes before writing the description.

### Step 3: Write the PR Description

First, check if the repository has a PR template:

```bash
# Fetch PR template from GitHub
gh repo view --json pullRequestTemplates --jq '.pullRequestTemplates[0].body'
```

If a PR template exists, follow its structure and fill in all required sections. Otherwise, follow this structure:

```markdown
<brief description of what the PR does>

<why these changes are being made - the motivation>

<alternative approaches considered, if any>

<any additional context reviewers need>
```

**Formatting rules (avoid broken Markdown):**
- Use real newlines (not `\n` escapes).
- Leave a blank line between paragraphs and between sections.
- Prefer `--body-file` when creating or updating PRs to preserve formatting.

**Do NOT include:**
- "Test plan" sections
- Checkbox lists of testing steps
- Redundant summaries of the diff

**Do include:**
- Clear explanation of what and why
- Links to relevant issues or tickets
- Context that isn't obvious from the code
- Notes on specific areas that need careful review

### Step 4: Create the PR

Create a temporary PR body file to preserve formatting:

```bash
cat <<'EOF' > /tmp/pr-body.md
<description body here>
EOF
```

```bash
gh pr create --title "<type>(<scope>): <description>" --body-file /tmp/pr-body.md
```

**Title format** follows commit conventions:
- `feat(scope): Add new feature`
- `fix(scope): Fix the bug`
- `ref: Refactor something`

## PR Description Examples

### Feature PR

```markdown
Add Slack thread replies for alert notifications

When an alert is updated or resolved, we now post a reply to the original
Slack thread instead of creating a new message. This keeps related
notifications grouped and reduces channel noise.

Previously considered posting edits to the original message, but threading
better preserves the timeline of events and works when the original message
is older than Slack's edit window.

Refs #1234
```

### Bug Fix PR

```markdown
Handle null response in user API endpoint

The user endpoint could return null for soft-deleted accounts, causing
dashboard crashes when accessing user properties. This adds a null check
and returns a proper 404 response.

Found while investigating #5678.

Fixes #5678
```

### Refactor PR

```markdown
Extract validation logic to shared module

Moves duplicate validation code from the alerts, issues, and projects
endpoints into a shared validator class. No behavior change.

This prepares for adding new validation rules in #9999 without
duplicating logic across endpoints.
```

## Issue References

Reference issues in the PR body:

| Syntax | Effect |
|--------|--------|
| `Fixes #1234` | Closes GitHub issue on merge |
| `Fixes #1234` | Closes GitHub issue on merge |
| `Refs #1234` | Links without closing |

## Guidelines

- **One PR per feature/fix** - Don't bundle unrelated changes
- **Keep PRs reviewable** - Smaller PRs get faster, better reviews
- **Explain the why** - Code shows what; description explains why
- **Mark WIP early** - Use draft PRs for early feedback

## Editing Existing PRs

If you need to update a PR after creation, use `gh api` instead of `gh pr edit`:

```bash
# Update PR description (preserve Markdown formatting)
cat <<'EOF' > /tmp/pr-body.md
Updated description here
EOF
gh api -X PATCH repos/{owner}/{repo}/pulls/PR_NUMBER -F body=@/tmp/pr-body.md

# Update PR title
gh api -X PATCH repos/{owner}/{repo}/pulls/PR_NUMBER -f title='new: Title here'

# Update both
cat <<'EOF' > /tmp/pr-body.md
New description
EOF
gh api -X PATCH repos/{owner}/{repo}/pulls/PR_NUMBER \
  -f title='new: Title' \
  -F body=@/tmp/pr-body.md
```

Note: `gh pr edit` is currently broken due to GitHub's Projects (classic) deprecation.

## References

- [GitHub Pull Request best practices](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests)
