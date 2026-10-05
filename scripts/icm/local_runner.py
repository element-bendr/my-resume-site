from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from task_validate import (
    TaskValidationError,
    changed_refs,
    load_json_object,
    require_valid_task,
    snapshot_refs,
    validate_changed_paths,
)

try:
    from icm_io import atomic_write_text
except ImportError:
    # Running this file directly places scripts/icm on sys.path, not scripts/.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from icm_io import atomic_write_text

ZERO_SHA = "0" * 40
MAX_CAPTURE_CHARS = 20_000


class RunnerError(RuntimeError):
    pass


class ClaimConflict(RunnerError):
    pass


class LocalLockConflict(RunnerError):
    pass


@dataclass(frozen=True)
class CommandResult:
    argv: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str

    @property
    def passed(self) -> bool:
        return self.returncode == 0


@dataclass(frozen=True)
class RunnerPolicy:
    repository: str
    trusted_control_refs: frozenset[str]
    executor_commands: dict[str, tuple[str, ...]]
    validation_commands: dict[str, tuple[str, ...]]
    worktree_root: Path
    state_root: Path
    command_timeout_seconds: int = 900
    environment_allowlist: frozenset[str] = frozenset()
    candidate_remote: str = "origin"

    @classmethod
    def from_dict(cls, data: dict[str, Any], *, base_dir: Path) -> "RunnerPolicy":
        required = {
            "repository",
            "trusted_control_refs",
            "executor_commands",
            "validation_commands",
            "worktree_root",
            "state_root",
        }
        extra = set(data) - (
            required | {"command_timeout_seconds", "environment_allowlist", "candidate_remote"}
        )
        missing = required - set(data)
        if missing:
            raise RunnerError(f"policy missing fields: {', '.join(sorted(missing))}")
        if extra:
            raise RunnerError(f"policy has unsupported fields: {', '.join(sorted(extra))}")
        if not isinstance(data["repository"], str) or not data["repository"]:
            raise RunnerError("policy.repository must be non-empty")
        refs = data["trusted_control_refs"]
        if not isinstance(refs, list) or not refs or not all(isinstance(item, str) and item for item in refs):
            raise RunnerError("policy.trusted_control_refs must be a non-empty string list")

        def commands(name: str) -> dict[str, tuple[str, ...]]:
            raw = data[name]
            if not isinstance(raw, dict):
                raise RunnerError(f"policy.{name} must be an object")
            result: dict[str, tuple[str, ...]] = {}
            for key, value in raw.items():
                if not isinstance(key, str) or not key:
                    raise RunnerError(f"policy.{name} keys must be non-empty strings")
                if not isinstance(value, list) or not value or not all(isinstance(part, str) and part for part in value):
                    raise RunnerError(f"policy.{name}.{key} must be a non-empty argv list")
                result[key] = tuple(value)
            return result

        raw_allowlist = data.get("environment_allowlist", [])
        if not isinstance(raw_allowlist, list) or not all(isinstance(item, str) and item for item in raw_allowlist):
            raise RunnerError("policy.environment_allowlist must be a string list")

        timeout = data.get("command_timeout_seconds", 900)
        if not isinstance(timeout, int) or timeout <= 0 or timeout > 7200:
            raise RunnerError("policy.command_timeout_seconds must be 1..7200")

        candidate_remote = data.get("candidate_remote", "origin")
        if (
            not isinstance(candidate_remote, str)
            or not candidate_remote
            or candidate_remote.startswith("-")
            or any(ch.isspace() for ch in candidate_remote)
        ):
            raise RunnerError("policy.candidate_remote must be a safe non-empty Git remote name")

        def resolve_local_path(value: Any, field: str) -> Path:
            if not isinstance(value, str) or not value:
                raise RunnerError(f"policy.{field} must be a non-empty path string")
            path = Path(value)
            return path if path.is_absolute() else (base_dir / path).resolve()

        return cls(
            repository=data["repository"],
            trusted_control_refs=frozenset(refs),
            executor_commands=commands("executor_commands"),
            validation_commands=commands("validation_commands"),
            worktree_root=resolve_local_path(data["worktree_root"], "worktree_root"),
            state_root=resolve_local_path(data["state_root"], "state_root"),
            command_timeout_seconds=timeout,
            environment_allowlist=frozenset(raw_allowlist),
            candidate_remote=candidate_remote,
        )


class GitRefClaimStore:
    """Create-only Git ref claims for a trusted control repository.

    `git update-ref <ref> <new> 000...0` is compare-and-swap creation: it fails
    if the ref already exists. A remote GitHub implementation is supplied by the
    Stage 04 control-plane adapter; the runner depends only on these semantics.
    """

    def __init__(self, repo: Path):
        self.repo = Path(repo).resolve()

    def claim_ref(self, task_id: str) -> str:
        return f"refs/heads/icm/claims/{task_id}"

    def read(self, task_id: str) -> str | None:
        ref = self.claim_ref(task_id)
        result = subprocess.run(
            ["git", "-C", str(self.repo), "rev-parse", "--verify", ref],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return None
        return result.stdout.strip() or None

    def create(self, task_id: str, base_sha: str) -> str:
        ref = self.claim_ref(task_id)
        result = subprocess.run(
            ["git", "-C", str(self.repo), "update-ref", ref, base_sha, ZERO_SHA],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            current = self.read(task_id)
            raise ClaimConflict(f"task already claimed: {task_id}; current={current or 'unknown'}")
        resolved = self.read(task_id)
        if resolved != base_sha:
            raise RunnerError(f"claim verification failed for {task_id}: {resolved!r}")
        return ref


class LocalTaskLock:
    def __init__(self, lock_path: Path, owner: str):
        self.lock_path = Path(lock_path)
        self.owner = owner
        self.fd: int | None = None

    def __enter__(self) -> "LocalTaskLock":
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        try:
            self.fd = os.open(self.lock_path, flags, 0o600)
        except FileExistsError as exc:
            raise LocalLockConflict(f"local execution lock already exists: {self.lock_path}") from exc
        os.write(self.fd, (self.owner + "\n").encode("utf-8"))
        os.fsync(self.fd)
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
        self.lock_path.unlink(missing_ok=True)


def git(root: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout or "git command failed").strip()
        raise RunnerError(detail)
    return result.stdout.strip()


def current_sha(root: Path) -> str:
    value = git(root, "rev-parse", "HEAD")
    if len(value) != 40:
        raise RunnerError(f"invalid HEAD SHA: {value!r}")
    return value


def _branch_for(task_id: str) -> str:
    return f"icm/run/{task_id}"


def prepare_worktree(repo_root: Path, worktree_root: Path, task_id: str, base_sha: str) -> Path:
    repo_root = Path(repo_root).resolve()
    worktree_root = Path(worktree_root).resolve()
    worktree_root.mkdir(parents=True, exist_ok=True)
    target = worktree_root / task_id
    branch = _branch_for(task_id)

    if target.exists():
        if not (target / ".git").exists():
            raise RunnerError(f"existing worktree path is not a Git worktree: {target}")
        actual_branch = git(target, "branch", "--show-current")
        if actual_branch != branch:
            raise RunnerError(f"worktree branch mismatch: {actual_branch!r} != {branch!r}")
        if git(target, "status", "--porcelain", "--untracked-files=all"):
            raise RunnerError(f"existing worktree is dirty: {target}")
        if current_sha(target) != base_sha:
            raise RunnerError(f"existing clean worktree is not at task base SHA: {target}")
        return target

    branch_exists = subprocess.run(
        ["git", "-C", str(repo_root), "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
    ).returncode == 0
    args = ["worktree", "add"]
    if branch_exists:
        args.extend([str(target), branch])
    else:
        args.extend(["-b", branch, str(target), base_sha])
    git(repo_root, *args)
    if current_sha(target) != base_sha:
        raise RunnerError("new worktree did not resolve to exact task base SHA")
    return target


def _bounded(text: str) -> str:
    if len(text) <= MAX_CAPTURE_CHARS:
        return text
    return text[:MAX_CAPTURE_CHARS] + "\n...[truncated]"


def run_command(
    argv: tuple[str, ...],
    *,
    cwd: Path,
    timeout_seconds: int,
    env: dict[str, str] | None = None,
) -> CommandResult:
    if not argv:
        raise RunnerError("empty command argv")
    try:
        completed = subprocess.run(
            list(argv),
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            shell=False,
            env=env,
        )
    except subprocess.TimeoutExpired as exc:
        raise RunnerError(f"command timed out after {timeout_seconds}s: {argv[0]}") from exc
    return CommandResult(
        argv=argv,
        returncode=completed.returncode,
        stdout=_bounded(completed.stdout),
        stderr=_bounded(completed.stderr),
    )


def render_command(argv: tuple[str, ...], context: dict[str, str]) -> tuple[str, ...]:
    allowed = {f"{{{key}}}": value for key, value in context.items()}
    return tuple(allowed.get(part, part) for part in argv)


def write_task_context(policy: RunnerPolicy, task: dict[str, Any], worktree: Path) -> Path:
    path = policy.state_root / "tasks" / f"{task['task_id']}.json"
    payload = {
        "schema_version": 1,
        "task": task,
        "execution": {
            "worktree": str(worktree),
            "branch": _branch_for(task["task_id"]),
        },
    }
    atomic_write_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")
    try:
        path.chmod(0o600)
    except OSError:
        pass
    return path


def changed_paths(worktree: Path, base_sha: str) -> list[str]:
    committed = git(worktree, "diff", "--name-only", f"{base_sha}..HEAD").splitlines()
    dirty = git(worktree, "status", "--porcelain=v1", "--untracked-files=all").splitlines()
    paths = set(committed)
    for line in dirty:
        if not line:
            continue
        value = line[3:] if len(line) >= 4 else ""
        if " -> " in value:
            value = value.split(" -> ", 1)[1]
        if value:
            paths.add(value.strip('"'))
    return sorted(paths)


def command_environment(policy: RunnerPolicy) -> dict[str, str]:
    safe_defaults = {"PATH", "HOME", "TMPDIR", "LANG", "LC_ALL"}
    allowed = safe_defaults | set(policy.environment_allowlist)
    return {key: value for key, value in os.environ.items() if key in allowed}


def require_candidate_progress(worktree: Path, base_sha: str, changes: list[str]) -> str:
    candidate_sha = current_sha(worktree)
    if candidate_sha == base_sha:
        raise RunnerError(
            "executor produced unchanged candidate HEAD; no-op candidates cannot be published"
        )
    if not changes:
        raise RunnerError(
            "executor produced no changed paths; empty commits/no-op candidates cannot be published"
        )
    return candidate_sha


def execute_task(
    repo_root: Path,
    task: dict[str, Any],
    policy: RunnerPolicy,
    *,
    trusted_ref_sha: str,
    claim_store: GitRefClaimStore | None = None,
) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    require_valid_task(
        repo_root,
        task,
        expected_repository=policy.repository,
        trusted_control_refs=set(policy.trusted_control_refs),
        allowed_validation_ids=set(policy.validation_commands),
        trusted_ref_sha=trusted_ref_sha,
    )

    executor = policy.executor_commands.get(task["executor_profile"])
    if executor is None:
        raise RunnerError(f"executor profile is not configured: {task['executor_profile']}")

    claim_store = claim_store or GitRefClaimStore(repo_root)
    lock_path = policy.state_root / "locks" / f"{task['task_id']}.lock"
    with LocalTaskLock(lock_path, owner=f"pid={os.getpid()}"):
        claim_ref = claim_store.create(task["task_id"], task["base_sha"])
        worktree = prepare_worktree(
            repo_root,
            policy.worktree_root,
            task["task_id"],
            task["base_sha"],
        )
        protected_ref_state = snapshot_refs(repo_root, task["protected_refs"])
        task_file = write_task_context(policy, task, worktree)
        command_context = {
            "task_file": str(task_file),
            "task_id": task["task_id"],
            "base_sha": task["base_sha"],
            "worktree": str(worktree),
        }
        safe_env = command_environment(policy)
        executor_result = run_command(
            render_command(executor, command_context),
            cwd=worktree,
            timeout_seconds=policy.command_timeout_seconds,
            env=safe_env,
        )
        ref_changes = changed_refs(repo_root, protected_ref_state)
        if ref_changes:
            raise RunnerError(
                "protected ref changed during executor: " + "; ".join(ref_changes)
            )
        if not executor_result.passed:
            raise RunnerError(f"executor failed with exit {executor_result.returncode}")

        changes = changed_paths(worktree, task["base_sha"])
        scope_errors = validate_changed_paths(task, changes)
        if scope_errors:
            raise RunnerError("; ".join(scope_errors))
        if git(worktree, "status", "--porcelain", "--untracked-files=all"):
            raise RunnerError("executor left uncommitted changes; exact candidate SHA cannot be proven")
        candidate_sha = require_candidate_progress(worktree, task["base_sha"], changes)

        validation: list[dict[str, Any]] = []
        for validation_id in task["validation"]:
            command = render_command(policy.validation_commands[validation_id], command_context)
            result = run_command(
                command,
                cwd=worktree,
                timeout_seconds=policy.command_timeout_seconds,
                env=safe_env,
            )
            ref_changes = changed_refs(repo_root, protected_ref_state)
            if ref_changes:
                raise RunnerError(
                    f"protected ref changed during validation {validation_id}: "
                    + "; ".join(ref_changes)
                )
            validation.append(
                {
                    "id": validation_id,
                    "status": "pass" if result.passed else "fail",
                    "returncode": result.returncode,
                    "summary": f"exit={result.returncode}",
                }
            )
            if not result.passed:
                raise RunnerError(f"validation failed: {validation_id}")

        outcome = {
            "task_id": task["task_id"],
            "base_sha": task["base_sha"],
            "candidate_sha": candidate_sha,
            "claim_ref": claim_ref,
            "branch": _branch_for(task["task_id"]),
            "worktree": str(worktree),
            "changed_paths": changes,
            "protected_state": "unchanged",
            "validation": validation,
        }
        outcome_path = policy.state_root / "outcomes" / f"{task['task_id']}.json"
        atomic_write_text(outcome_path, json.dumps(outcome, indent=2, sort_keys=True) + "\n")
        try:
            outcome_path.chmod(0o600)
        except OSError:
            pass
        return outcome


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--policy", required=True)
    parser.add_argument("--trusted-ref-sha", required=True)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    try:
        task = load_json_object(Path(args.task))
        policy_data = load_json_object(Path(args.policy))
        policy = RunnerPolicy.from_dict(policy_data, base_dir=Path(args.policy).resolve().parent)
        outcome = execute_task(repo, task, policy, trusted_ref_sha=args.trusted_ref_sha)
    except (RunnerError, TaskValidationError, OSError, ValueError) as exc:
        if args.as_json:
            print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True))
        else:
            print(f"LOCAL RUNNER: FAIL: {exc}", file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps({"status": "PASS", "outcome": outcome}, sort_keys=True))
    else:
        print(
            "LOCAL RUNNER: PASS "
            f"task={outcome['task_id']} candidate={outcome['candidate_sha']} "
            f"changed_paths={len(outcome['changed_paths'])}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
