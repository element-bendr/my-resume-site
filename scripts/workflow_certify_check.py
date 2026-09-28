from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from workflow_lib import SHA_RE, current_commit, load_json, safe_repo_path, stage_staleness, validate_state
from workflow_selection import active_workflows, select_workflow

REQUIRED_REPORT_FIELDS = {
    "status": "complete",
    "validation_result": "PASS",
    "protected_state": "PASS",
    "handoff_updated": "YES",
}
REQUIRED_REPORT_SECTIONS = (
    "## Workflow / Stage",
    "## Working location",
    "## Provenance",
    "## State changed",
    "## Files / outputs",
    "## Evidence",
    "## Validation",
    "## Protected state",
    "## Stale / uncertain state",
    "## Blockers",
    "## Closed decisions",
    "## Handoff update",
    "## Next action",
)
PLACEHOLDER_RE = re.compile(r"<[^>\n]+>")


def parse_report_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw in text.splitlines()[1:]:
        line = raw.strip()
        if not line:
            if fields:
                break
            continue
        if line.startswith("## "):
            break
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


def validate_completion_report(root: Path, relative: str) -> list[str]:
    errors: list[str] = []
    try:
        path = safe_repo_path(root, relative)
    except ValueError as exc:
        return [str(exc)]
    if not path.is_file():
        return [f"missing completion report {relative}"]
    text = path.read_text(encoding="utf-8")
    fields = parse_report_fields(text)
    for key, expected in REQUIRED_REPORT_FIELDS.items():
        if fields.get(key) != expected:
            errors.append(f"{relative}: {key} must be {expected}")
    for section in REQUIRED_REPORT_SECTIONS:
        if section not in text:
            errors.append(f"{relative}: missing section {section}")
    for placeholder in sorted(set(PLACEHOLDER_RE.findall(text))):
        errors.append(f"{relative}: unresolved placeholder: {placeholder}")
    if "FAIL" in text and "validation_result: PASS" in text:
        for line in text.splitlines():
            if line.lstrip().startswith("-") and ": FAIL" in line:
                errors.append(f"{relative}: validation evidence still contains FAIL")
                break
    return errors


def _git_clean(root: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain", "--untracked-files=all"],
        check=True,
        capture_output=True,
        text=True,
    )
    return not result.stdout.strip()


def certification_report(
    root: Path,
    workflow_id: str | None = None,
    stage_id: str | None = None,
    *,
    require_clean: bool = True,
) -> dict[str, Any]:
    errors: list[str] = []
    try:
        selected = select_workflow(root, workflow_id)
        state_path = active_workflows(root)[selected]
        state = load_json(state_path)
    except Exception as exc:
        return {"workflow_id": workflow_id, "stage": stage_id, "candidate_commit": None, "errors": [str(exc)]}

    errors.extend(validate_state(root, state_path))
    if state.get("status") != "active":
        errors.append("workflow must be active before stage certification")
    selected_stage_id = stage_id or state.get("active_stage")
    stage = next((item for item in state.get("stages", []) if item.get("id") == selected_stage_id), None)
    if not stage:
        errors.append(f"stage not found: {selected_stage_id!r}")
    elif stage.get("status") != "active":
        errors.append(f"stage {selected_stage_id} must be active before certification")

    candidate = current_commit(root)
    if not candidate or not SHA_RE.fullmatch(candidate):
        errors.append("candidate commit is unavailable or invalid")
    provenance = state.get("provenance") if isinstance(state.get("provenance"), dict) else {}
    started = provenance.get("started_from_commit")
    if not isinstance(started, str) or not SHA_RE.fullmatch(started):
        errors.append("started_from_commit must be recorded before certification")

    if stage:
        stale = stage_staleness(root, state).get(str(selected_stage_id), {})
        if stale.get("stale"):
            errors.append(f"stage {selected_stage_id} is stale")
        if stale.get("unpinned"):
            errors.append(f"stage {selected_stage_id} has unpinned dependencies: {', '.join(stale['unpinned'])}")
        for output in stage.get("outputs", []):
            try:
                if not safe_repo_path(root, output).exists():
                    errors.append(f"missing declared output: {output}")
            except ValueError as exc:
                errors.append(str(exc))
        report_path = stage.get("completion_report")
        if not isinstance(report_path, str) or not report_path:
            errors.append("stage completion_report path is required")
        else:
            errors.extend(validate_completion_report(root, report_path))

    if require_clean:
        try:
            if not _git_clean(root):
                errors.append("working tree must be clean for certification")
        except Exception as exc:
            errors.append(f"unable to verify clean working tree: {exc}")

    return {"workflow_id": selected, "stage": selected_stage_id, "candidate_commit": candidate, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow")
    parser.add_argument("--stage")
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    report = certification_report(Path(__file__).resolve().parents[1], args.workflow, args.stage, require_clean=not args.allow_dirty)
    if args.as_json:
        print(json.dumps(report, indent=2))
    else:
        if report["errors"]:
            print("CERTIFY CHECK: FAIL")
            for error in report["errors"]:
                print(f"- {error}")
        else:
            print(f"CERTIFY CHECK: PASS workflow={report['workflow_id']} stage={report['stage']} candidate={report['candidate_commit']}")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
