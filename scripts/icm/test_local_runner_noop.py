from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from local_runner import RunnerError, changed_paths, current_sha, require_candidate_progress


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return completed.stdout.strip()


class NoopCandidateGuardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "icm-test@example.invalid")
        git(self.repo, "config", "user.name", "ICM Test")
        (self.repo / "tracked.txt").write_text("base\n", encoding="utf-8")
        git(self.repo, "add", "tracked.txt")
        git(self.repo, "commit", "-q", "-m", "base")
        self.base = current_sha(self.repo)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_unchanged_head_is_rejected(self) -> None:
        with self.assertRaisesRegex(RunnerError, "unchanged candidate HEAD"):
            require_candidate_progress(self.repo, self.base, changed_paths(self.repo, self.base))

    def test_empty_commit_is_rejected(self) -> None:
        git(self.repo, "commit", "--allow-empty", "-q", "-m", "empty")
        self.assertNotEqual(current_sha(self.repo), self.base)
        self.assertEqual(changed_paths(self.repo, self.base), [])
        with self.assertRaisesRegex(RunnerError, "no changed paths"):
            require_candidate_progress(self.repo, self.base, [])

    def test_real_commit_passes(self) -> None:
        (self.repo / "tracked.txt").write_text("changed\n", encoding="utf-8")
        git(self.repo, "add", "tracked.txt")
        git(self.repo, "commit", "-q", "-m", "real change")
        changes = changed_paths(self.repo, self.base)
        candidate = require_candidate_progress(self.repo, self.base, changes)
        self.assertNotEqual(candidate, self.base)
        self.assertEqual(changes, ["tracked.txt"])


if __name__ == "__main__":
    unittest.main()
