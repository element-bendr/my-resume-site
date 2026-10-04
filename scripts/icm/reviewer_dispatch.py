from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from result_publish import GitHubControlPlane, PublishError, UrllibTransport
from task_validate import changed_refs, load_json_object, snapshot_refs, validate_schema


class ReviewError(RuntimeError):
    pass


@dataclass(frozen=True)
class ReviewerPolicy:
    reviewer_commands: dict[str, tuple[str, ...]]
    review_root: Path
    state_root: Path
    environment_allowlist: frozenset[str]
    command_timeout_seconds: int = 900

    @classmethod
    def from_dict(cls, data: dict[str, Any], *, base_dir: Path) -> "ReviewerPolicy":
        required = {"reviewer_commands", "review_root", "state_root"}
        optional = {"environment_allowlist", "command_timeout_seconds"}
        missing = required - set(data)
        extra = set(data) - required - optional
        if missing:
            raise ReviewError(f"review policy missing fields: {', '.join(sorted(missing))}")
        if extra:
            raise ReviewError(f"review policy has unsupported fields: {', '.join(sorted(extra))}")

        raw_commands = data["reviewer_commands"]
        if not isinstance(raw_commands, dict) or not raw_commands:
            raise ReviewError("reviewer_commands must be a non-empty object")
        commands: dict[str, tuple[str, ...]] = {}
        for profile, argv in raw_commands.items():
            if not isinstance(profile, str) or not profile:
                raise ReviewError("reviewer profile keys must be non-empty strings")
            if not isinstance(argv, list) or not argv or not all(isinstance(part, str) and part for part in argv):
                raise ReviewError(f"reviewer command {profile!r} must be a non-empty argv list")
            commands[profile] = tuple(argv)

        raw_allowlist = data.get("environment_allowlist", [])
        if not isinstance(raw_allowlist, list) or not all(isinstance(item, str) and item for item in raw_allowlist):
            raise ReviewError("environment_allowlist must be a string list")

        timeout = data.get("command_timeout_seconds", 900)
        if not isinstance(timeout, int) or timeout <= 0 or timeout > 7200:
            raise ReviewError("command_timeout_seconds must be 1..7200")

        def local_path(value: Any, field: str) -> Path:
            if not isinstance(value, str) or not value:
                raise ReviewError(f"{field} must be a non-empty path string")
            path = Path(value)
            return path if path.is_absolute() else (base_dir / path).resolve()

        return cls(
            reviewer_commands=commands,
            review_root=local_path(data["review_root"], "review_root"),
            state_root=local_path(data["state_root"], "state_root"),
            environment_allowlist=frozenset(raw_allowlist),
            command_timeout_seconds=timeout,
        )


def git(root: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout or "git command failed").strip()
        raise ReviewError(detail)
    return result.stdout.strip()


def prepare_review_worktree(repo_root: Path, review_root: Path, task_id: str, candidate_sha: str) -> Path:
    repo_root = Path(repo_root).resolve()
    review_root = Path(review_root).resolve()
    review_root.mkdir(parents=True, exist_ok=True)
    target = review_root / task_id

    try:
        git(repo_root, "cat-file", "-e", f"{candidate_sha}^{{commit}}")
    except ReviewError as exc:
        raise ReviewError(f"candidate SHA does not exist locally: {candidate_sha}") from exc

    if target.exists():
        if not (target / ".git").exists():
            raise ReviewError(f"existing review path is not a Git worktree: {target}")
        if git(target, "status", "--porcelain", "--untracked-files=all"):
            raise ReviewError(f"existing review worktree is dirty: {target}")
        if git(target, "rev-parse", "HEAD") != candidate_sha:
            raise ReviewError(f"existing review worktree is not at candidate SHA: {target}")
        if git(target, "branch", "--show-current"):
            raise ReviewError(f"review worktree must remain detached: {target}")
        return target

    git(repo_root, "worktree", "add", "--detach", str(target), candidate_sha)
    if git(target, "rev-parse", "HEAD") != candidate_sha:
        raise ReviewError("review worktree did not resolve to exact candidate SHA")
    if git(target, "branch", "--show-current"):
        raise ReviewError("review worktree unexpectedly attached to a branch")
    return target


def _schema(repo_root: Path, name: str) -> dict[str, Any]:
    return load_json_object(Path(repo_root) / "schemas" / name)


def validate_review_inputs(repo_root: Path, task: dict[str, Any], result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    errors.extend(f"task: {item}" for item in validate_schema(task, _schema(repo_root, "icm-task.schema.json")))
    errors.extend(f"result: {item}" for item in validate_schema(result, _schema(repo_root, "icm-result.schema.json")))
    if errors:
        return sorted(set(errors))

    for field in ("task_id", "repository", "workflow_id", "stage_id", "base_sha"):
        if task[field] != result[field]:
            errors.append(f"task/result identity mismatch: {field}")
    if result["status"] != "pass":
        errors.append("independent review requires a passing execution result")
    if result["protected_state"] != "unchanged":
        errors.append("independent review requires unchanged protected state")
    if result["next_action"] != "await_review":
        errors.append("execution result is not awaiting review")
    if not isinstance(result.get("candidate_sha"), str):
        errors.append("independent review requires an exact candidate SHA")
    if any(item.get("status") == "fail" for item in result.get("validation", [])):
        errors.append("execution result contains failed validation")
    return sorted(set(errors))


def _safe_finding_path(path: str) -> bool:
    if not path or path.startswith("/"):
        return False
    return ".." not in Path(path.replace("\\", "/")).parts


def build_review(
    repo_root: Path,
    task: dict[str, Any],
    result: dict[str, Any],
    decision: dict[str, Any],
    *,
    reviewer_profile: str,
    reviewer_identity: str,
) -> dict[str, Any]:
    input_errors = validate_review_inputs(repo_root, task, result)
    if input_errors:
        raise ReviewError("; ".join(input_errors))
    if not reviewer_identity.strip():
        raise ReviewError("reviewer identity must be non-empty")
    if reviewer_identity == result["executor_identity"]:
        raise ReviewError("reviewer identity must differ from executor identity")

    allowed = {"verdict", "findings", "required_fixes", "validation_summary"}
    if not isinstance(decision, dict):
        raise ReviewError("reviewer decision must be a JSON object")
    extra = set(decision) - allowed
    missing = allowed - set(decision)
    if missing:
        raise ReviewError(f"reviewer decision missing fields: {', '.join(sorted(missing))}")
    if extra:
        raise ReviewError(f"reviewer decision has unsupported fields: {', '.join(sorted(extra))}")

    review = {
        "schema_version": 1,
        "record_type": "review",
        "task_id": task["task_id"],
        "repository": task["repository"],
        "workflow_id": task["workflow_id"],
        "stage_id": task["stage_id"],
        "base_sha": task["base_sha"],
        "candidate_sha": result["candidate_sha"],
        "executor_identity": result["executor_identity"],
        "reviewer_profile": reviewer_profile,
        "reviewer_identity": reviewer_identity,
        "independent": True,
        "verdict": decision["verdict"],
        "findings": decision["findings"],
        "required_fixes": decision["required_fixes"],
        "validation_summary": decision["validation_summary"],
    }
    schema_errors = validate_schema(review, _schema(repo_root, "icm-review.schema.json"))
    if schema_errors:
        raise ReviewError("invalid review record: " + "; ".join(schema_errors))

    for finding in review["findings"]:
        for path in finding.get("paths", []):
            if not _safe_finding_path(path):
                raise ReviewError(f"unsafe finding path: {path!r}")

    verdict = review["verdict"]
    severities = {item["severity"] for item in review["findings"]}
    if verdict == "pass":
        if review["required_fixes"]:
            raise ReviewError("PASS review cannot contain required fixes")
        if severities & {"error", "blocker"}:
            raise ReviewError("PASS review cannot contain error/blocker findings")
    elif verdict == "fix_required":
        if not review["required_fixes"]:
            raise ReviewError("FIX_REQUIRED review must contain required fixes")
    elif verdict == "stop":
        if "blocker" not in severities:
            raise ReviewError("STOP review must contain a blocker finding")
    return review


def write_review_context(
    policy: ReviewerPolicy,
    task: dict[str, Any],
    result: dict[str, Any],
    review_worktree: Path,
) -> tuple[Path, Path]:
    context_path = policy.state_root / "review-context" / f"{task['task_id']}.json"
    output_path = policy.state_root / "review-decisions" / f"{task['task_id']}.json"
    context_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.unlink(missing_ok=True)
    payload = {
        "schema_version": 1,
        "task": task,
        "result": result,
        "review": {
            "candidate_worktree": str(review_worktree),
            "decision_output": str(output_path),
            "allowed_decision_fields": ["verdict", "findings", "required_fixes", "validation_summary"],
        },
    }
    context_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    try:
        context_path.chmod(0o600)
    except OSError:
        pass
    return context_path, output_path


def render_command(argv: tuple[str, ...], values: dict[str, str]) -> tuple[str, ...]:
    tokens = {f"{{{key}}}": value for key, value in values.items()}
    return tuple(tokens.get(part, part) for part in argv)


def reviewer_environment(policy: ReviewerPolicy) -> dict[str, str]:
    safe_defaults = {"PATH", "HOME", "TMPDIR", "LANG", "LC_ALL"}
    allowed = safe_defaults | set(policy.environment_allowlist)
    return {key: value for key, value in os.environ.items() if key in allowed}


def run_reviewer(
    repo_root: Path,
    task: dict[str, Any],
    result: dict[str, Any],
    policy: ReviewerPolicy,
    *,
    reviewer_profile: str,
    reviewer_identity: str,
) -> dict[str, Any]:
    input_errors = validate_review_inputs(repo_root, task, result)
    if input_errors:
        raise ReviewError("; ".join(input_errors))
    if reviewer_identity == result["executor_identity"]:
        raise ReviewError("reviewer identity must differ from executor identity")
    command = policy.reviewer_commands.get(reviewer_profile)
    if command is None:
        raise ReviewError(f"reviewer profile is not configured: {reviewer_profile}")

    worktree = prepare_review_worktree(
        repo_root,
        policy.review_root,
        task["task_id"],
        result["candidate_sha"],
    )
    protected_ref_state = snapshot_refs(repo_root, task["protected_refs"])
    context_path, output_path = write_review_context(policy, task, result, worktree)
    values = {
        "review_context": str(context_path),
        "review_output": str(output_path),
        "task_id": task["task_id"],
        "candidate_sha": result["candidate_sha"],
        "review_worktree": str(worktree),
    }
    try:
        completed = subprocess.run(
            list(render_command(command, values)),
            cwd=str(worktree),
            capture_output=True,
            text=True,
            timeout=policy.command_timeout_seconds,
            shell=False,
            env=reviewer_environment(policy),
        )
    except subprocess.TimeoutExpired as exc:
        raise ReviewError(f"reviewer timed out after {policy.command_timeout_seconds}s") from exc
    ref_changes = changed_refs(repo_root, protected_ref_state)
    if ref_changes:
        raise ReviewError(
            "protected ref changed during reviewer: " + "; ".join(ref_changes)
        )
    if completed.returncode != 0:
        raise ReviewError(f"reviewer failed with exit {completed.returncode}")
    if git(worktree, "rev-parse", "HEAD") != result["candidate_sha"]:
        raise ReviewError("reviewer changed candidate HEAD")
    if git(worktree, "status", "--porcelain", "--untracked-files=all"):
        raise ReviewError("reviewer modified the candidate worktree")
    if not output_path.is_file():
        raise ReviewError("reviewer did not produce a decision record")
    decision = load_json_object(output_path)
    return build_review(
        repo_root,
        task,
        result,
        decision,
        reviewer_profile=reviewer_profile,
        reviewer_identity=reviewer_identity,
    )


def review_path(task_id: str) -> str:
    return f"workflow/local-execution/reviews/{task_id}.json"


def render_pr_comment(review: dict[str, Any]) -> str:
    return (
        "ICM REVIEW\n\n"
        f"task: `{review['task_id']}`\n"
        f"candidate: `{review['candidate_sha']}`\n"
        f"verdict: **{review['verdict'].upper()}**\n"
        f"findings: {len(review['findings'])}\n"
        f"required fixes: {len(review['required_fixes'])}\n\n"
        "Machine-readable repository review record is authoritative."
    )


def publish_review(
    control_plane: GitHubControlPlane,
    task: dict[str, Any],
    review: dict[str, Any],
    *,
    branch_ref: str,
    pr_number: int | None = None,
) -> dict[str, Any]:
    if control_plane.repository != task.get("repository"):
        raise ReviewError("control-plane repository mismatch")
    if branch_ref != task.get("origin", {}).get("ref"):
        raise ReviewError("review branch must equal the task origin control ref")
    path = review_path(review["task_id"])
    content = json.dumps(review, indent=2, sort_keys=True) + "\n"
    try:
        commit_sha = control_plane.create_text_file(
            path,
            content,
            branch_ref=branch_ref,
            message=f"Record ICM review {review['task_id']}",
        )
    except PublishError as exc:
        raise ReviewError(str(exc)) from exc

    comment_id = None
    comment_error = None
    if pr_number is not None:
        try:
            comment_id = control_plane.post_pr_comment(pr_number, render_pr_comment(review))
        except PublishError as exc:
            comment_error = str(exc)
    return {
        "path": path,
        "commit_sha": commit_sha,
        "comment_id": comment_id,
        "comment_error": comment_error,
        "review": review,
    }


def coordinator_action(review: dict[str, Any]) -> str:
    return {
        "pass": "complete_task",
        "fix_required": "create_fix_task",
        "stop": "escalate",
    }[review["verdict"]]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--policy", required=True)
    parser.add_argument("--reviewer-profile", required=True)
    parser.add_argument("--reviewer-identity", required=True)
    parser.add_argument("--branch-ref", required=True)
    parser.add_argument("--pr-number", type=int)
    parser.add_argument("--token-env", default="GITHUB_TOKEN")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    token = os.environ.get(args.token_env, "")
    if not token:
        print(f"REVIEW DISPATCH: FAIL: missing token env {args.token_env}", file=sys.stderr)
        return 2
    try:
        task = load_json_object(Path(args.task))
        result = load_json_object(Path(args.result))
        policy_data = load_json_object(Path(args.policy))
        policy = ReviewerPolicy.from_dict(policy_data, base_dir=Path(args.policy).resolve().parent)
        review = run_reviewer(
            Path(args.repo_root),
            task,
            result,
            policy,
            reviewer_profile=args.reviewer_profile,
            reviewer_identity=args.reviewer_identity,
        )
        plane = GitHubControlPlane(args.repository, UrllibTransport(token))
        published = publish_review(
            plane,
            task,
            review,
            branch_ref=args.branch_ref,
            pr_number=args.pr_number,
        )
        payload = {**published, "coordinator_action": coordinator_action(review)}
    except (ReviewError, PublishError, OSError, ValueError) as exc:
        if args.as_json:
            print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True))
        else:
            print(f"REVIEW DISPATCH: FAIL: {exc}", file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps({"status": "PASS", "published": payload}, sort_keys=True))
    else:
        print(
            f"REVIEW DISPATCH: PASS task={review['task_id']} verdict={review['verdict']} "
            f"action={payload['coordinator_action']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
