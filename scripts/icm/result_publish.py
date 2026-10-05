from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from task_validate import load_json_object, validate_schema

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
API_ROOT = "https://api.github.com"


class PublishError(RuntimeError):
    pass


class ClaimConflict(PublishError):
    pass


class Transport(Protocol):
    def request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
    ) -> tuple[int, dict[str, Any] | list[Any] | None]: ...


@dataclass
class UrllibTransport:
    token: str
    api_root: str = API_ROOT
    timeout_seconds: int = 30

    def request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
    ) -> tuple[int, dict[str, Any] | list[Any] | None]:
        url = self.api_root.rstrip("/") + path
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "icm-local-execution-bridge/1",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                body = response.read().decode("utf-8")
                value = json.loads(body) if body else None
                return response.status, value
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            try:
                value = json.loads(body) if body else None
            except json.JSONDecodeError:
                value = {"message": body[:1000]}
            return exc.code, value
        except OSError as exc:
            raise PublishError(f"GitHub request failed: {type(exc).__name__}") from exc


class GitHubControlPlane:
    def __init__(self, repository: str, transport: Transport):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
            raise PublishError(f"invalid repository: {repository!r}")
        self.repository = repository
        self.transport = transport
        owner, repo = repository.split("/", 1)
        self.owner = urllib.parse.quote(owner, safe="")
        self.repo = urllib.parse.quote(repo, safe="")
        self.prefix = f"/repos/{self.owner}/{self.repo}"

    @staticmethod
    def _message(body: dict[str, Any] | list[Any] | None) -> str:
        if isinstance(body, dict) and isinstance(body.get("message"), str):
            return body["message"][:500]
        return "GitHub API request failed"

    @staticmethod
    def _branch_name(ref: str) -> str:
        prefix = "refs/heads/"
        if not ref.startswith(prefix) or len(ref) <= len(prefix):
            raise PublishError(f"expected branch ref, got {ref!r}")
        return ref[len(prefix):]

    def read_ref(self, ref: str) -> str | None:
        encoded = urllib.parse.quote(ref.removeprefix("refs/"), safe="/")
        status, body = self.transport.request("GET", f"{self.prefix}/git/ref/{encoded}")
        if status == 404:
            return None
        if status != 200 or not isinstance(body, dict):
            raise PublishError(self._message(body))
        obj = body.get("object")
        sha = obj.get("sha") if isinstance(obj, dict) else None
        if not isinstance(sha, str) or not SHA_RE.fullmatch(sha):
            raise PublishError("GitHub ref response did not contain a valid SHA")
        return sha

    def create_claim(self, task_id: str, base_sha: str) -> str:
        if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{2,127}", task_id):
            raise PublishError(f"invalid task id: {task_id!r}")
        if not SHA_RE.fullmatch(base_sha):
            raise PublishError("claim base SHA must be 40 lowercase hex characters")
        ref = f"refs/heads/icm/claims/{task_id}"
        status, body = self.transport.request(
            "POST",
            f"{self.prefix}/git/refs",
            payload={"ref": ref, "sha": base_sha},
        )
        if status in {409, 422}:
            current = self.read_ref(ref)
            raise ClaimConflict(f"task already claimed: {task_id}; current={current or 'unknown'}")
        if status != 201 or not isinstance(body, dict):
            raise PublishError(self._message(body))
        created = body.get("ref")
        obj = body.get("object")
        resolved = obj.get("sha") if isinstance(obj, dict) else None
        if created != ref or resolved != base_sha:
            raise PublishError("created claim ref did not match requested task/base SHA")
        return ref

    def fetch_json_file(self, path: str, ref: str) -> tuple[dict[str, Any], str]:
        if path.startswith("/") or ".." in Path(path).parts:
            raise PublishError(f"unsafe repository path: {path!r}")
        encoded_path = urllib.parse.quote(path, safe="/")
        refish = ref if SHA_RE.fullmatch(ref) else self._branch_name(ref)
        query = urllib.parse.urlencode({"ref": refish})
        status, body = self.transport.request("GET", f"{self.prefix}/contents/{encoded_path}?{query}")
        if status != 200 or not isinstance(body, dict):
            raise PublishError(self._message(body))
        content = body.get("content")
        blob_sha = body.get("sha")
        encoding = body.get("encoding")
        if (
            not isinstance(content, str)
            or encoding != "base64"
            or not isinstance(blob_sha, str)
            or not SHA_RE.fullmatch(blob_sha)
        ):
            raise PublishError("GitHub content response is incomplete")
        try:
            decoded = base64.b64decode(content, validate=False).decode("utf-8")
            value = json.loads(decoded)
        except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PublishError(f"invalid JSON content at {path}") from exc
        if not isinstance(value, dict):
            raise PublishError(f"expected JSON object at {path}")
        return value, blob_sha

    def create_text_file(self, path: str, content: str, *, branch_ref: str, message: str) -> str:
        if path.startswith("/") or ".." in Path(path).parts:
            raise PublishError(f"unsafe repository path: {path!r}")
        encoded_path = urllib.parse.quote(path, safe="/")
        status, body = self.transport.request(
            "PUT",
            f"{self.prefix}/contents/{encoded_path}",
            payload={
                "message": message,
                "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
                "branch": self._branch_name(branch_ref),
            },
        )
        if status == 422:
            raise PublishError(f"refusing to overwrite existing control-plane record: {path}")
        if status not in {200, 201} or not isinstance(body, dict):
            raise PublishError(self._message(body))
        commit = body.get("commit")
        sha = commit.get("sha") if isinstance(commit, dict) else None
        if not isinstance(sha, str) or not SHA_RE.fullmatch(sha):
            raise PublishError("GitHub content write did not return a valid commit SHA")
        return sha

    def post_pr_comment(self, pr_number: int, body_text: str) -> int:
        if pr_number <= 0:
            raise PublishError("PR number must be positive")
        status, body = self.transport.request(
            "POST", f"{self.prefix}/issues/{pr_number}/comments", payload={"body": body_text}
        )
        if status != 201 or not isinstance(body, dict) or not isinstance(body.get("id"), int):
            raise PublishError(self._message(body))
        return body["id"]


class GitHubClaimStore:
    """Duck-typed claim store accepted by local_runner.execute_task."""

    def __init__(self, control_plane: GitHubControlPlane):
        self.control_plane = control_plane

    def create(self, task_id: str, base_sha: str) -> str:
        return self.control_plane.create_claim(task_id, base_sha)


def _task_schema(repo_root: Path) -> dict[str, Any]:
    return load_json_object(Path(repo_root) / "schemas/icm-task.schema.json")


def _result_schema(repo_root: Path) -> dict[str, Any]:
    return load_json_object(Path(repo_root) / "schemas/icm-result.schema.json")


def build_result(
    repo_root: Path,
    task: dict[str, Any],
    outcome: dict[str, Any],
    *,
    executor_identity: str,
) -> dict[str, Any]:
    task_errors = validate_schema(task, _task_schema(repo_root))
    if task_errors:
        raise PublishError("invalid task record: " + "; ".join(task_errors))
    if not isinstance(executor_identity, str) or not executor_identity.strip():
        raise PublishError("executor identity must be non-empty")
    if task.get("task_id") != outcome.get("task_id"):
        raise PublishError("task/outcome task_id mismatch")
    if task.get("base_sha") != outcome.get("base_sha"):
        raise PublishError("task/outcome base_sha mismatch")
    candidate = outcome.get("candidate_sha")
    if not isinstance(candidate, str) or not SHA_RE.fullmatch(candidate):
        raise PublishError("runner outcome candidate_sha is invalid")
    if outcome.get("protected_state") != "unchanged":
        raise PublishError("passing result requires unchanged protected state")
    validations = outcome.get("validation")
    if not isinstance(validations, list) or not validations:
        raise PublishError("runner outcome has no validation evidence")

    normalized_validation: list[dict[str, Any]] = []
    for item in validations:
        if not isinstance(item, dict):
            raise PublishError("runner validation entry must be an object")
        vid = item.get("id")
        status = item.get("status")
        summary = item.get("summary")
        if not isinstance(vid, str) or status not in {"pass", "fail", "skipped"}:
            raise PublishError("runner validation entry is malformed")
        if not isinstance(summary, str) or not summary:
            summary = f"status={status}"
        normalized_validation.append({"id": vid, "status": status, "summary": summary})
    if any(item["status"] == "fail" for item in normalized_validation):
        raise PublishError("passing result cannot contain failed validation")

    worktree = outcome.get("worktree")
    branch = outcome.get("branch")
    if not isinstance(worktree, str) or not worktree or not isinstance(branch, str) or not branch:
        raise PublishError("runner outcome execution identity is incomplete")

    claim_ref = outcome.get("claim_ref")
    expected_claim_ref = f"refs/heads/icm/claims/{task['task_id']}"
    if claim_ref != expected_claim_ref:
        raise PublishError(f"runner outcome claim_ref mismatch: {claim_ref!r}")

    candidate_ref = outcome.get("candidate_ref")
    expected_candidate_ref = f"refs/heads/icm/candidates/{task['task_id']}"
    if candidate_ref != expected_candidate_ref:
        raise PublishError(f"runner outcome candidate_ref mismatch: {candidate_ref!r}")

    result = {
        "schema_version": 1,
        "record_type": "result",
        "task_id": task["task_id"],
        "repository": task["repository"],
        "workflow_id": task["workflow_id"],
        "stage_id": task["stage_id"],
        "base_sha": task["base_sha"],
        "candidate_sha": candidate,
        "candidate_ref": candidate_ref,
        "claim_ref": claim_ref,
        "executor_identity": executor_identity,
        "execution": {"branch": branch, "worktree_id": Path(worktree).name},
        "status": "pass",
        "changed_paths": sorted(set(outcome.get("changed_paths", []))),
        "validation": normalized_validation,
        "protected_state": "unchanged",
        "blockers": [],
        "next_action": "await_review",
    }
    errors = validate_schema(result, _result_schema(repo_root))
    if errors:
        raise PublishError("invalid result record: " + "; ".join(errors))
    return result


def result_path(task_id: str) -> str:
    if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{2,127}", task_id):
        raise PublishError(f"invalid task id: {task_id!r}")
    return f"workflow/local-execution/results/{task_id}.json"


def render_pr_comment(result: dict[str, Any]) -> str:
    validations = ", ".join(
        f"{item['id']}={item['status'].upper()}" for item in result.get("validation", [])
    ) or "none"
    return (
        "ICM RESULT\n\n"
        f"task: `{result['task_id']}`\n"
        f"status: **{result['status'].upper()}**\n"
        f"candidate: `{result['candidate_sha']}`\n"
        f"candidate ref: `{result['candidate_ref']}`\n"
        f"protected state: **{result['protected_state'].upper()}**\n"
        f"validation: {validations}\n"
        f"next action: `{result['next_action']}`\n\n"
        "Machine-readable repository result record is authoritative."
    )


def publish_result(
    repo_root: Path,
    control_plane: GitHubControlPlane,
    task: dict[str, Any],
    outcome: dict[str, Any],
    *,
    executor_identity: str,
    branch_ref: str,
    pr_number: int | None = None,
) -> dict[str, Any]:
    if control_plane.repository != task.get("repository"):
        raise PublishError(
            f"control-plane repository mismatch: {control_plane.repository!r} != {task.get('repository')!r}"
        )
    if branch_ref != task.get("origin", {}).get("ref"):
        raise PublishError("result branch must equal the task origin control ref")
    result = build_result(repo_root, task, outcome, executor_identity=executor_identity)
    path = result_path(result["task_id"])
    content = json.dumps(result, indent=2, sort_keys=True) + "\n"
    commit_sha = control_plane.create_text_file(
        path,
        content,
        branch_ref=branch_ref,
        message=f"Record ICM result {result['task_id']}",
    )
    comment_id = None
    comment_error = None
    if pr_number is not None:
        try:
            comment_id = control_plane.post_pr_comment(pr_number, render_pr_comment(result))
        except PublishError as exc:
            # The repository result is authoritative and already durable. A human-facing
            # comment failure must not downgrade or duplicate that immutable record.
            comment_error = str(exc)
    return {
        "path": path,
        "commit_sha": commit_sha,
        "comment_id": comment_id,
        "comment_error": comment_error,
        "result": result,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--executor-identity", required=True)
    parser.add_argument("--branch-ref", required=True)
    parser.add_argument("--pr-number", type=int)
    parser.add_argument("--token-env", default="GITHUB_TOKEN")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    token = os.environ.get(args.token_env, "")
    if not token:
        print(f"RESULT PUBLISH: FAIL: missing token env {args.token_env}", file=sys.stderr)
        return 2
    try:
        task = load_json_object(Path(args.task))
        outcome = load_json_object(Path(args.outcome))
        plane = GitHubControlPlane(args.repository, UrllibTransport(token))
        published = publish_result(
            Path(args.repo_root),
            plane,
            task,
            outcome,
            executor_identity=args.executor_identity,
            branch_ref=args.branch_ref,
            pr_number=args.pr_number,
        )
    except (PublishError, OSError, ValueError) as exc:
        if args.as_json:
            print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True))
        else:
            print(f"RESULT PUBLISH: FAIL: {exc}", file=sys.stderr)
        return 1
    if args.as_json:
        print(json.dumps({"status": "PASS", "published": published}, sort_keys=True))
    else:
        print(
            f"RESULT PUBLISH: PASS task={published['result']['task_id']} "
            f"commit={published['commit_sha']} path={published['path']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
