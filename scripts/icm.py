from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Callable, Sequence

from icm_audit import audit_repository, write_audit_proposal
from icm_init import InitConflict, initialize_repository
from icm_protected import ProtectedStateError, git_changed_paths
from icm_graph_render import GENERATED_ROOT, render_handoff, render_status
from icm_validate import validate_repository
from icm_refresh import RefreshConflict, refresh_repository
from icm_io import atomic_write_text, safe_repo_path
from icm_context import build_context_manifest, compact_context_manifest

ICM_COMPILER_VERSION = "1.0.0"
CORE_COMMANDS = ("audit", "init", "refresh", "validate", "status", "handoff", "context")


class CLIError(ValueError):
    pass


def _looks_like_repo(path: Path) -> bool:
    return (
        (path / ".git").exists()
        or (
            (path / "AGENTS.md").is_file()
            and (path / "workflow").is_dir()
        )
    )


def find_repo_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).expanduser().resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if _looks_like_repo(candidate):
            return candidate
    raise CLIError(f"no ICM/Git repository found from {current}")


def resolve_repo(explicit: str | None, cwd: Path | None = None) -> Path:
    if explicit is None:
        return find_repo_root(cwd)
    candidate = Path(explicit).expanduser().resolve()
    if not candidate.exists():
        raise CLIError(f"repository path does not exist: {candidate}")
    if not candidate.is_dir():
        raise CLIError(f"repository path is not a directory: {candidate}")
    if not _looks_like_repo(candidate):
        raise CLIError(f"path is not an ICM/Git repository: {candidate}")
    return candidate


def _emit_error(message: str, *, json_mode: bool) -> None:
    if json_mode:
        print(json.dumps({"status": "ERROR", "error": message}, sort_keys=True), file=sys.stderr)
    else:
        print(f"ICM: ERROR: {message}", file=sys.stderr)


def _audit(args: argparse.Namespace) -> int:
    report = audit_repository(args.repo_root)
    proposal_path = None
    if args.write:
        proposal_path = write_audit_proposal(args.repo_root, report)
    if args.json:
        payload = dict(report)
        payload["proposal_path"] = str(proposal_path.relative_to(args.repo_root)) if proposal_path else None
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        graph = report["graph"]
        print(f"ICM AUDIT: {report['status']}")
        print(f"nodes={len(graph['nodes'])}")
        print(f"edges={len(graph['edges'])}")
        print(f"unresolved={len(report['unresolved'])}")
        if proposal_path is not None:
            print(f"proposal={proposal_path.relative_to(args.repo_root)}")
        for item in report["diagnostics"]:
            print(f"{item['severity']}: {item['code']}: {item['subject']}: {item['message']}")
    return 1 if report["status"] == "FAIL" else 0


def _init(args: argparse.Namespace) -> int:
    result = initialize_repository(args.repo_root, write=args.write)
    payload = {
        "status": result["status"],
        "source": result["source"],
        "changes": result["changes"],
        "written": result["written"],
        "already_initialized": result["already_initialized"],
        "mode": "write" if args.write else "dry-run",
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"ICM INIT: {payload['status']} ({payload['mode']})")
        print(f"source={payload['source']}")
        print(f"changes={len(payload['changes'])}")
        print(f"written={len(payload['written'])}")
        print(f"already_initialized={str(payload['already_initialized']).lower()}")
        for path in payload["changes"]:
            print(f"- {path}")
    return 0


def _refresh(args: argparse.Namespace) -> int:
    result = refresh_repository(args.repo_root, write=args.write)
    payload = {
        "status": result["status"],
        "changes": result["changes"],
        "written": result["written"],
        "graph_changed": result["graph_changed"],
        "recovery_mode": result["recovery_mode"],
        "already_fresh": result["already_fresh"],
        "mode": "write" if args.write else "dry-run",
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"ICM REFRESH: {payload['status']} ({payload['mode']})")
        print(f"changes={len(payload['changes'])}")
        print(f"written={len(payload['written'])}")
        print(f"graph_changed={str(payload['graph_changed']).lower()}")
        print(f"recovery_mode={str(payload['recovery_mode']).lower()}")
        print(f"already_fresh={str(payload['already_fresh']).lower()}")
        for path in payload["changes"]:
            print(f"- {path}")
    return 0


def _validate(args: argparse.Namespace) -> int:
    if bool(args.base) != bool(args.head):
        raise CLIError("--base and --head must be supplied together")
    changed_paths = None
    if args.changed_path:
        changed_paths = list(args.changed_path)
    if args.base and args.head:
        diff_paths = git_changed_paths(args.repo_root, args.base, args.head)
        changed_paths = sorted(set((changed_paths or []) + diff_paths))
    report = validate_repository(
        args.repo_root,
        changed_paths=changed_paths,
        approvals=set(args.approve_protected or []),
    )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"ICM VALIDATE: {report['status']}")
        for item in report["diagnostics"]:
            print(f"{item['severity']}: {item['code']}: {item['subject']}: {item['message']}")
    return 1 if report["status"] == "FAIL" else 0


def _status(args: argparse.Namespace) -> int:
    content = render_status(args.repo_root)
    if args.json:
        print(json.dumps({"status": "PASS", "content": content}, sort_keys=True))
    else:
        print(content, end="")
    return 0


def _handoff(args: argparse.Namespace) -> int:
    content = render_handoff(args.repo_root)
    if args.write:
        path = safe_repo_path(args.repo_root, GENERATED_ROOT / "HANDOFF.md")
        path.parent.mkdir(parents=True, exist_ok=True)
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != content:
            atomic_write_text(path, content)
        if args.json:
            print(json.dumps({"status": "PASS", "path": str(path.relative_to(args.repo_root))}, sort_keys=True))
        else:
            print(f"ICM HANDOFF: PASS path={path.relative_to(args.repo_root)}")
    else:
        if args.json:
            print(json.dumps({"status": "PASS", "content": content}, sort_keys=True))
        else:
            print(content, end="")
    return 0


def _context(args: argparse.Namespace) -> int:
    manifest = build_context_manifest(args.repo_root, subject=args.subject)
    if args.compact:
        manifest = compact_context_manifest(manifest)
    if args.json:
        print(json.dumps(manifest, indent=2, sort_keys=True))
    else:
        budget = manifest["budget"]
        print(f"ICM CONTEXT: {manifest['status']}")
        print(f"subject={manifest['subject']}")
        print(f"repository={manifest['repository']}")
        print(f"base_sha={manifest['base_sha']}")
        print(f"nodes={len(manifest['items'])}")
        print(f"sources={len(manifest['sources'])}")
        print(
            "estimated_tokens_if_all_text_sources_loaded="
            f"{budget['estimated_tokens_if_all_text_sources_loaded']}"
        )
        for item in manifest["items"]:
            reason = item["reasons"][0] if item["reasons"] else "selected"
            print(
                f"- {item['node_id']} [{item['type']}] "
                f"{item['priority']}: {reason}"
            )
        if manifest["blocking_unresolved"]:
            print("blocking_unresolved=" + ",".join(manifest["blocking_unresolved"]))
    return 0


def _not_implemented(args: argparse.Namespace) -> int:
    _emit_error(
        f"{args.command} is registered but not implemented in this foundation PR",
        json_mode=args.json,
    )
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="icm", description="Graph-native, Git-backed ICM compiler")
    parser.add_argument("--version", action="store_true", help="print compiler version and exit")
    parser.add_argument("--repo", help="explicit repository root; otherwise discover from current directory")
    parser.add_argument("--json", action="store_true", help="emit machine-readable command output where supported")

    subparsers = parser.add_subparsers(dest="command")
    for name in CORE_COMMANDS:
        sub = subparsers.add_parser(name, help=f"{name} ICM graph/compiler state")
        handlers = {"audit": _audit, "init": _init, "refresh": _refresh, "validate": _validate, "status": _status, "handoff": _handoff, "context": _context}
        sub.set_defaults(handler=handlers.get(name, _not_implemented))
        if name in {"audit", "init", "refresh", "handoff"}:
            sub.add_argument("--write", action="store_true", help="allow repository writes for this command")
        if name == "validate":
            sub.add_argument("--changed-path", action="append", help="repository-relative changed path; repeatable")
            sub.add_argument("--base", help="Git base ref for protected-state diff")
            sub.add_argument("--head", help="Git head ref for protected-state diff")
            sub.add_argument("--approve-protected", action="append", help="explicit protected_resource node approval; repeatable")
        if name == "context":
            sub.add_argument("--subject", help="explicit workflow/stage/task node ID; otherwise resolve one active subject")
            sub.add_argument("--compact", action="store_true", help="emit the bounded runtime projection rather than the full audit manifest")
    return parser


def main(argv: Sequence[str] | None = None, *, cwd: Path | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    if args.version:
        print(f"icm graph-compiler {ICM_COMPILER_VERSION}")
        return 0
    if args.command is None:
        parser.print_help()
        return 0
    try:
        args.repo_root = resolve_repo(args.repo, cwd)
        handler: Callable[[argparse.Namespace], int] = args.handler
        return int(handler(args))
    except (CLIError, InitConflict, RefreshConflict, ProtectedStateError, ValueError, OSError, json.JSONDecodeError) as exc:
        _emit_error(str(exc), json_mode=args.json)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
