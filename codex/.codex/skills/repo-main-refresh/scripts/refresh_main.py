import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


STATUS_LIMIT = 20


class GitError(Exception):
    def __init__(self, message, returncode=2):
        super().__init__(message)
        self.returncode = returncode


@dataclass
class Worktree:
    path: str
    branch: str | None
    head: str | None


def run_git(args, cwd, check=True):
    result = subprocess.run(
        ["git", "-C", str(cwd), *args],
        text=True,
        capture_output=True,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise GitError(f"git {' '.join(args)} failed: {detail}")
    return result


def git_output(args, cwd, check=True):
    return run_git(args, cwd, check=check).stdout.strip()


def find_repo_root(cwd):
    result = run_git(["rev-parse", "--show-toplevel"], cwd, check=False)
    if result.returncode != 0:
        raise GitError("BLOCKED: current directory is not inside a Git worktree.", 1)
    return Path(result.stdout.strip())


def parse_worktrees(text):
    worktrees = []
    current = {}
    for line in text.splitlines():
        if not line:
            if current:
                worktrees.append(
                    Worktree(
                        path=current.get("worktree", ""),
                        branch=current.get("branch"),
                        head=current.get("HEAD"),
                    )
                )
                current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value
    if current:
        worktrees.append(
            Worktree(
                path=current.get("worktree", ""),
                branch=current.get("branch"),
                head=current.get("HEAD"),
            )
        )
    return worktrees


def list_worktrees(repo_root):
    text = git_output(["worktree", "list", "--porcelain"], repo_root)
    return parse_worktrees(text)


def branch_label(worktree):
    if worktree.branch is None:
        return "detached"
    prefix = "refs/heads/"
    if worktree.branch.startswith(prefix):
        return worktree.branch[len(prefix) :]
    return worktree.branch


def find_main_worktree(worktrees):
    matches = [wt for wt in worktrees if wt.branch == "refs/heads/main"]
    if not matches:
        raise GitError("BLOCKED: no worktree has local main checked out.", 1)
    if len(matches) > 1:
        paths = ", ".join(wt.path for wt in matches)
        raise GitError(f"BLOCKED: multiple worktrees report local main: {paths}", 1)
    return matches[0]


def status_short(path):
    result = run_git(["status", "--short", "--untracked-files=normal"], path, check=False)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        return [f"! status unavailable: {detail}"]
    if not result.stdout.strip():
        return []
    return result.stdout.rstrip().splitlines()


def ensure_origin_main_tracking(repo_root):
    upstream = git_output(
        ["for-each-ref", "--format=%(upstream:short)", "refs/heads/main"],
        repo_root,
    )
    if upstream != "origin/main":
        shown = upstream if upstream else "no upstream"
        raise GitError(f"BLOCKED: local main must track origin/main; found {shown}.", 1)

    origin_main = run_git(["rev-parse", "--verify", "refs/remotes/origin/main"], repo_root, check=False)
    if origin_main.returncode != 0:
        raise GitError("BLOCKED: origin/main is missing after fetch.", 1)


def ahead_behind(repo_root):
    counts = git_output(
        ["rev-list", "--left-right", "--count", "refs/heads/main...refs/remotes/origin/main"],
        repo_root,
    )
    ahead_text, behind_text = counts.split()
    return int(ahead_text), int(behind_text)


def short_sha(repo_root, ref):
    return git_output(["rev-parse", "--short", ref], repo_root)


def commit_subjects(repo_root, rev_range, limit=5):
    result = run_git(
        ["log", "--oneline", f"-n{limit}", rev_range],
        repo_root,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return []
    return result.stdout.rstrip().splitlines()


def format_status_block(title, entries):
    lines = [title]
    for entry in entries[:STATUS_LIMIT]:
        lines.append(f"  {entry}")
    if len(entries) > STATUS_LIMIT:
        lines.append(f"  ... {len(entries) - STATUS_LIMIT} more entries")
    return lines


def dirty_non_main_worktrees(worktrees, main_path):
    dirty = []
    for worktree in worktrees:
        if Path(worktree.path) == main_path:
            continue
        entries = status_short(worktree.path)
        if entries:
            dirty.append((worktree, entries))
    return dirty


def print_report(lines):
    for line in lines:
        print(line)


def block_report(message, report_lines):
    print_report([message, *report_lines])
    return 1


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Safely refresh local main from origin/main before creating worktrees."
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Fetch and report only; do not fast-forward local main.",
    )
    parser.add_argument(
        "--cwd",
        default=".",
        help="Path inside the repository to inspect. Defaults to the current directory.",
    )
    args = parser.parse_args(argv)

    try:
        repo_root = find_repo_root(Path(args.cwd).resolve())
        worktrees = list_worktrees(repo_root)
        main_worktree = find_main_worktree(worktrees)
        main_path = Path(main_worktree.path)

        fetch = run_git(["fetch", "--prune", "origin"], repo_root, check=False)
        if fetch.returncode != 0:
            detail = fetch.stderr.strip() or fetch.stdout.strip()
            raise GitError(f"BLOCKED: git fetch --prune origin failed: {detail}", 1)

        ensure_origin_main_tracking(repo_root)
        old_sha = short_sha(repo_root, "refs/heads/main")
        remote_sha = short_sha(repo_root, "refs/remotes/origin/main")

        report = [
            f"Main checkout: {main_path}",
            f"Local main: {old_sha}",
            f"origin/main: {remote_sha}",
        ]

        main_status = status_short(main_path)
        if main_status:
            report.extend(format_status_block("Main checkout is not clean:", main_status))
            return block_report("BLOCKED: clean the main checkout before refreshing.", report)

        ahead, behind = ahead_behind(repo_root)
        report.append(f"Relation: main is {ahead} ahead, {behind} behind origin/main")

        if ahead and behind:
            report.extend(format_status_block("Local-only commits:", commit_subjects(repo_root, "origin/main..main")))
            report.extend(format_status_block("Remote-only commits:", commit_subjects(repo_root, "main..origin/main")))
            return block_report("BLOCKED: local main and origin/main have diverged. Ask the user what to do.", report)

        if ahead:
            report.extend(format_status_block("Local-only commits:", commit_subjects(repo_root, "origin/main..main")))
            return block_report("BLOCKED: local main is ahead of origin/main. Ask the user what to do.", report)

        if behind and args.check_only:
            report.extend(format_status_block("Remote-only commits:", commit_subjects(repo_root, "main..origin/main")))
            return block_report("BLOCKED: check-only mode found local main behind origin/main. Rerun without --check-only to fast-forward.", report)

        action = "already current"
        if behind:
            merge = run_git(["merge", "--ff-only", "origin/main"], main_path, check=False)
            if merge.returncode != 0:
                detail = merge.stderr.strip() or merge.stdout.strip()
                return block_report(f"BLOCKED: fast-forward failed: {detail}", report)
            new_sha = short_sha(repo_root, "refs/heads/main")
            action = f"fast-forwarded {old_sha} -> {new_sha}"
            report[1] = f"Local main: {new_sha}"

        dirty_elsewhere = dirty_non_main_worktrees(worktrees, main_path)
        if dirty_elsewhere:
            report.append("Non-main dirty worktrees:")
            for worktree, entries in dirty_elsewhere:
                report.append(f"- {worktree.path} ({branch_label(worktree)})")
                for entry in entries[:STATUS_LIMIT]:
                    report.append(f"  {entry}")
                if len(entries) > STATUS_LIMIT:
                    report.append(f"  ... {len(entries) - STATUS_LIMIT} more entries")
        else:
            report.append("Non-main dirty worktrees: none")

        report.append(f"Result: {action}")
        report.append("SAFE: local main is ready for a new worktree.")
        report.append("Next: create the requested worktree from local main using the repo's normal path and branch naming.")
        print_report(report)
        return 0
    except GitError as exc:
        print(str(exc), file=sys.stderr)
        return exc.returncode
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
