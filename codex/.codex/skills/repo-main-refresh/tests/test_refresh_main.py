import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "refresh_main.py"


def run(command, cwd, check=True):
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if check and result.returncode != 0:
        raise AssertionError(
            f"{command} failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def git(cwd, *args, check=True):
    return run(["git", *args], cwd, check=check)


def script(cwd, *args):
    return run(["uv", "run", str(SCRIPT), "--cwd", str(cwd), *args], cwd, check=False)


class RepoMainRefreshTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.remote = self.root / "remote.git"
        self.seed = self.root / "seed"
        self.main = self.root / "repo"
        git(self.root, "init", "--bare", "--initial-branch=main", str(self.remote))
        git(self.root, "clone", str(self.remote), str(self.seed))
        self.configure_repo(self.seed)
        (self.seed / "file.txt").write_text("base\n")
        git(self.seed, "add", "file.txt")
        git(self.seed, "commit", "-m", "base")
        git(self.seed, "push", "-u", "origin", "main")
        git(self.root, "clone", str(self.remote), str(self.main))
        self.configure_repo(self.main)

    def tearDown(self):
        self.tmp.cleanup()

    @staticmethod
    def configure_repo(path):
        git(path, "config", "user.email", "test@example.com")
        git(path, "config", "user.name", "Test User")

    def push_remote_commit(self, filename="remote.txt", content="remote\n"):
        (self.seed / filename).write_text(content)
        git(self.seed, "add", filename)
        git(self.seed, "commit", "-m", f"add {filename}")
        git(self.seed, "push", "origin", "main")

    def test_fast_forwards_clean_behind_main(self):
        old = git(self.main, "rev-parse", "HEAD").stdout.strip()
        self.push_remote_commit()
        result = script(self.main)
        new = git(self.main, "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertNotEqual(old, new)
        self.assertIn("SAFE: local main is ready for a new worktree.", result.stdout)
        self.assertIn("Result: fast-forwarded", result.stdout)

    def test_check_only_does_not_fast_forward(self):
        old = git(self.main, "rev-parse", "HEAD").stdout.strip()
        self.push_remote_commit()
        result = script(self.main, "--check-only")
        new = git(self.main, "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(old, new)
        self.assertIn("check-only mode found local main behind", result.stdout)

    def test_dirty_main_blocks(self):
        (self.main / "dirty.txt").write_text("dirty\n")
        self.push_remote_commit()
        result = script(self.main)
        self.assertEqual(result.returncode, 1)
        self.assertIn("clean the main checkout", result.stdout)
        self.assertIn("?? dirty.txt", result.stdout)

    def test_ahead_only_blocks(self):
        (self.main / "local.txt").write_text("local\n")
        git(self.main, "add", "local.txt")
        git(self.main, "commit", "-m", "local")
        result = script(self.main)
        self.assertEqual(result.returncode, 1)
        self.assertIn("local main is ahead", result.stdout)

    def test_diverged_blocks(self):
        (self.main / "local.txt").write_text("local\n")
        git(self.main, "add", "local.txt")
        git(self.main, "commit", "-m", "local")
        self.push_remote_commit()
        result = script(self.main)
        self.assertEqual(result.returncode, 1)
        self.assertIn("have diverged", result.stdout)

    def test_missing_main_checkout_blocks(self):
        feature = self.root / "feature"
        git(self.main, "worktree", "add", "-b", "feature", str(feature), "main")
        git(feature, "config", "user.email", "test@example.com")
        git(feature, "config", "user.name", "Test User")
        git(self.main, "checkout", "--detach")
        result = script(feature)
        self.assertEqual(result.returncode, 1)
        self.assertIn("no worktree has local main checked out", result.stderr)

    def test_reports_non_main_dirty_worktree_without_blocking(self):
        feature = self.root / "feature"
        git(self.main, "worktree", "add", "-b", "feature", str(feature), "main")
        (feature / "scratch.txt").write_text("scratch\n")
        result = script(feature)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("Non-main dirty worktrees:", result.stdout)
        self.assertIn("scratch.txt", result.stdout)
        self.assertIn("SAFE: local main is ready for a new worktree.", result.stdout)

    def test_requires_origin_main_upstream(self):
        git(self.main, "branch", "--unset-upstream", "main")
        result = script(self.main)
        self.assertEqual(result.returncode, 1)
        self.assertIn("must track origin/main", result.stderr)


if __name__ == "__main__":
    os.environ.setdefault("UV_CACHE_DIR", str(Path.cwd() / ".uv-cache"))
    unittest.main()
