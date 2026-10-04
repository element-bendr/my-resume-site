from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Protocol

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
TASK_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,127}$")


class CandidatePublishError(RuntimeError):
    pass


class RefReader(Protocol):
    def read_ref(self, ref: str) -> str | None: ...


def candidate_ref(task_id: str) -> str:
    if not TASK_ID_RE.fullmatch(task_id):
        raise CandidatePublishError(f"invalid task id: {task_id!r}")
    return f"refs/heads/icm/candidates/{task_id}"


def _git(repo_root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        capture_output=True,
        text=True,
    )
    if check and completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "git command failed").strip()
        raise CandidatePublishError(detail)
    return completed


def _remote_repository(url: str) -> str | None:
    value = url.strip()
    prefixes = (
        "https://github.com/",
        "ssh://git@github.com/",
        "git@github.com:",
    )
    path = None
    for prefix in prefixes:
        if value.startswith(prefix):
            path = value[len(prefix):]
            break
    if path is None:
        return None
    path = path.rstrip("/")
    if path.endswith(".git"):
        path = path[:-4]
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", path):
        return None
    return path


def _verify_remote(repo_root: Path, remote: str, repository: str) -> None:
    if not remote or remote.startswith("-") or any(ch.isspace() for ch in remote):
        raise CandidatePublishError(f"unsafe candidate remote name: {remote!r}")
    fetch_url = _git(repo_root, "remote", "get-url", remote).stdout.strip()
    resolved = _remote_repository(fetch_url)
    if resolved != repository:
        raise CandidatePublishError(
            f"candidate remote repository mismatch: remote={resolved!r} expected={repository!r}"
        )


def publish_candidate(
    repo_root: Path,
    control_plane: RefReader,
    *,
    repository: str,
    task_id: str,
    base_sha: str,
    candidate_sha: str,
    remote: str = "origin",
) -> str:
    repo_root = Path(repo_root).resolve()
    if not SHA_RE.fullmatch(base_sha):
        raise CandidatePublishError("base SHA must be 40 lowercase hex characters")
    if not SHA_RE.fullmatch(candidate_sha):
        raise CandidatePublishError("candidate SHA must be 40 lowercase hex characters")

    _git(repo_root, "cat-file", "-e", f"{base_sha}^{{commit}}")
    _git(repo_root, "cat-file", "-e", f"{candidate_sha}^{{commit}}")
    ancestor = _git(
        repo_root,
        "merge-base",
        "--is-ancestor",
        base_sha,
        candidate_sha,
        check=False,
    )
    if ancestor.returncode != 0:
        raise CandidatePublishError("candidate is not descended from the exact task base SHA")

    _verify_remote(repo_root, remote, repository)
    ref = candidate_ref(task_id)
    existing = control_plane.read_ref(ref)
    if existing is not None:
        if existing == candidate_sha:
            return ref
        raise CandidatePublishError(
            f"candidate ref already exists with different SHA: {ref}={existing}"
        )

    completed = _git(
        repo_root,
        "push",
        "--porcelain",
        f"--force-with-lease={ref}:",
        remote,
        f"{candidate_sha}:{ref}",
        check=False,
    )
    if completed.returncode != 0:
        current = control_plane.read_ref(ref)
        if current == candidate_sha:
            return ref
        detail = (completed.stderr or completed.stdout or "candidate push failed").strip()
        raise CandidatePublishError(detail)

    resolved = control_plane.read_ref(ref)
    if resolved != candidate_sha:
        raise CandidatePublishError(
            f"candidate publication verification failed: {ref}={resolved!r}"
        )
    return ref
