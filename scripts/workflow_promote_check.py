from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
REQUIRED_FIELDS = {
    "date",
    "status",
    "source_repository",
    "destination_repository",
    "source_record",
    "destination_record",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def safe_repo_path(root: Path, relative: str) -> Path:
    if not relative or Path(relative).is_absolute():
        raise ValueError(f"invalid repository-relative path: {relative!r}")
    root = root.resolve()
    candidate = (root / relative).resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError(f"path escapes repository root: {relative}")
    return candidate


def parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    started = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("# ") and not started:
            started = True
            continue
        if started and not line:
            if fields:
                break
            continue
        if started and ":" in line and not line.startswith("#"):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
        elif fields:
            break
    return fields


def placeholder(value: str) -> bool:
    return not value or "<" in value or ">" in value


def validate_promotion(root: Path, record_path: Path) -> list[str]:
    errors: list[str] = []
    text = record_path.read_text(encoding="utf-8")
    fields = parse_fields(text)

    missing = sorted(REQUIRED_FIELDS - fields.keys())
    for key in missing:
        errors.append(f"missing field: {key}")

    for key in REQUIRED_FIELDS & fields.keys():
        if placeholder(fields[key]):
            errors.append(f"unresolved placeholder: {key}")

    if fields.get("status") not in {None, "promoted"}:
        errors.append("status must be promoted")
    if fields.get("date") and not DATE_RE.fullmatch(fields["date"]):
        errors.append("date must be YYYY-MM-DD")
    for key in ("source_repository", "destination_repository"):
        value = fields.get(key)
        if value and not placeholder(value) and not REPO_RE.fullmatch(value):
            errors.append(f"{key} must be owner/repo")

    source = fields.get("source_record")
    if source and not placeholder(source):
        try:
            source_path = safe_repo_path(root, source)
            if not source_path.is_file():
                errors.append(f"source_record does not exist: {source}")
            if source_path.resolve() == record_path.resolve():
                errors.append("source_record cannot be the promotion record itself")
        except ValueError as exc:
            errors.append(str(exc))

    lowered = text.lower()
    if "destination repository is authoritative" not in lowered:
        errors.append("missing explicit destination-authority transfer statement")
    if "historical pointer" not in lowered:
        errors.append("missing historical-pointer statement")

    return errors


def discover_records(root: Path) -> list[Path]:
    promoted = root / "promoted"
    return sorted(promoted.rglob("*.md")) if promoted.exists() else []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("records", nargs="*")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    root = repo_root()
    records = [safe_repo_path(root, item) for item in args.records] if args.records else discover_records(root)
    report = []
    failed = False
    for path in records:
        errors = validate_promotion(root, path)
        failed = failed or bool(errors)
        report.append({"record": str(path.relative_to(root)), "errors": errors})

    if args.as_json:
        print(json.dumps({"records": report, "remote_verified": False}, indent=2))
    else:
        if not records:
            print("PROMOTION CHECK: PASS (no local promotion records)")
        for item in report:
            state = "FAIL" if item["errors"] else "PASS"
            print(f"{item['record']}: {state}")
            for error in item["errors"]:
                print(f"  - {error}")
        print("Remote destination existence is not verified by this local checker.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
