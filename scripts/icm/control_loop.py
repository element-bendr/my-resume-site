from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

from candidate_publish import CandidatePublishError, publish_candidate
from local_runner import RunnerError, RunnerPolicy, execute_task
from result_publish import GitHubClaimStore, GitHubControlPlane, PublishError, UrllibTransport, publish_result
from reviewer_dispatch import ReviewError, ReviewerPolicy, coordinator_action, publish_review, run_reviewer
from task_validate import TaskValidationError, load_json_object

TASK_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,127}$")


class ControlLoopError(RuntimeError):
    pass


def queue_path(task_id: str) -> str:
    if not TASK_ID_RE.fullmatch(task_id):
        raise ControlLoopError(f"invalid task id: {task_id!r}")
    return f"workflow/local-execution/queue/{task_id}.json"


def fetch_queued_task(
    control_plane: GitHubControlPlane,
    task_id: str,
    control_ref: str,
) -> tuple[dict[str, Any], dict[str, str]]:
    if not control_ref.startswith("refs/heads/"):
        raise ControlLoopError("control ref must be a branch ref")
    source_head = control_plane.read_ref(control_ref)
    if source_head is None:
        raise ControlLoopError(f"control ref not found: {control_ref}")
    path = queue_path(task_id)
    task, blob_sha = control_plane.fetch_json_file(path, source_head)
    current_head = control_plane.read_ref(control_ref)
    if current_head != source_head:
        raise ControlLoopError("control ref moved during task fetch; retry from fresh state")
    if task.get("task_id") != task_id:
        raise ControlLoopError("queued task id does not match requested task")
    if task.get("repository") != control_plane.repository:
        raise ControlLoopError("queued task repository does not match control plane")
    if task.get("origin", {}).get("ref") != control_ref:
        raise ControlLoopError("queued task origin ref does not match trusted control ref")
    return task, {
        "task_path": path,
        "source_ref": control_ref,
        "source_head_sha": source_head,
        "source_blob_sha": blob_sha,
    }


def run_once(
    repo_root: Path,
    control_plane: GitHubControlPlane,
    task_id: str,
    control_ref: str,
    runner_policy: RunnerPolicy,
    reviewer_policy: ReviewerPolicy,
    *,
    executor_identity: str,
    reviewer_profile: str,
    reviewer_identity: str,
    pr_number: int | None = None,
) -> dict[str, Any]:
    task, source = fetch_queued_task(control_plane, task_id, control_ref)
    trusted_ref_sha = control_plane.read_ref(task["trusted_ref"])
    if trusted_ref_sha is None:
        raise ControlLoopError(f"trusted ref not found: {task['trusted_ref']}")
    try:
        outcome = execute_task(
            repo_root,
            task,
            runner_policy,
            trusted_ref_sha=trusted_ref_sha,
            claim_store=GitHubClaimStore(control_plane),
        )
        remote_candidate_ref = publish_candidate(
            repo_root,
            control_plane,
            repository=task["repository"],
            task_id=task["task_id"],
            base_sha=task["base_sha"],
            candidate_sha=outcome["candidate_sha"],
            remote=runner_policy.candidate_remote,
        )
        outcome = dict(outcome)
        outcome["candidate_ref"] = remote_candidate_ref
        published_result = publish_result(
            repo_root,
            control_plane,
            task,
            outcome,
            executor_identity=executor_identity,
            branch_ref=control_ref,
            pr_number=pr_number,
        )
        if control_plane.read_ref(remote_candidate_ref) != outcome["candidate_sha"]:
            raise ControlLoopError("remote candidate ref changed before independent review")
        review = run_reviewer(
            repo_root,
            task,
            published_result["result"],
            reviewer_policy,
            reviewer_profile=reviewer_profile,
            reviewer_identity=reviewer_identity,
        )
        if control_plane.read_ref(remote_candidate_ref) != outcome["candidate_sha"]:
            raise ControlLoopError("remote candidate ref changed during independent review")
        published_review = publish_review(
            control_plane,
            task,
            review,
            branch_ref=control_ref,
            pr_number=pr_number,
        )
    except (
        CandidatePublishError,
        RunnerError,
        TaskValidationError,
        PublishError,
        ReviewError,
        OSError,
        ValueError,
    ) as exc:
        raise ControlLoopError(str(exc)) from exc
    return {
        "task_id": task_id,
        "source": source,
        "outcome": outcome,
        "candidate_ref": remote_candidate_ref,
        "result": published_result["result"],
        "review": review,
        "coordinator_action": coordinator_action(review),
        "result_path": published_result["path"],
        "review_path": published_review["path"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--control-ref", required=True)
    parser.add_argument("--runner-policy", required=True)
    parser.add_argument("--reviewer-policy", required=True)
    parser.add_argument("--executor-identity", required=True)
    parser.add_argument("--reviewer-profile", required=True)
    parser.add_argument("--reviewer-identity", required=True)
    parser.add_argument("--pr-number", type=int)
    parser.add_argument("--token-env", default="GITHUB_TOKEN")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    token = os.environ.get(args.token_env, "")
    if not token:
        print(f"CONTROL LOOP: FAIL: missing token env {args.token_env}", file=sys.stderr)
        return 2
    try:
        runner_data = load_json_object(Path(args.runner_policy))
        reviewer_data = load_json_object(Path(args.reviewer_policy))
        runner_policy = RunnerPolicy.from_dict(
            runner_data, base_dir=Path(args.runner_policy).resolve().parent
        )
        reviewer_policy = ReviewerPolicy.from_dict(
            reviewer_data, base_dir=Path(args.reviewer_policy).resolve().parent
        )
        plane = GitHubControlPlane(args.repository, UrllibTransport(token))
        result = run_once(
            Path(args.repo_root),
            plane,
            args.task_id,
            args.control_ref,
            runner_policy,
            reviewer_policy,
            executor_identity=args.executor_identity,
            reviewer_profile=args.reviewer_profile,
            reviewer_identity=args.reviewer_identity,
            pr_number=args.pr_number,
        )
    except (
        CandidatePublishError,
        ControlLoopError,
        RunnerError,
        ReviewError,
        PublishError,
        TaskValidationError,
        OSError,
        ValueError,
    ) as exc:
        if args.as_json:
            print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True))
        else:
            print(f"CONTROL LOOP: FAIL: {exc}", file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps({"status": "PASS", "run": result}, sort_keys=True))
    else:
        print(
            f"CONTROL LOOP: PASS task={result['task_id']} "
            f"action={result['coordinator_action']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
