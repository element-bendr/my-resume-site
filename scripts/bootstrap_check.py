from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED = ("CONTEXT.md", "HANDOFF.md")
PLACEHOLDER_PATTERN = re.compile(r"<[^>\n]+>")
ALLOWED_REPOSITORY_CLASSES = {"production-system", "client-code", "research", "documentation/archive", "mixed"}
ALLOWED_RISK_TIERS = {"low", "medium", "high"}
ALLOWED_DEPENDENCY_ROLES = {"standalone", "feeds-other-systems", "consumed-by-other-systems", "both"}
ALLOWED_CI_POLICIES = {"required", "optional", "none"}
ALLOWED_EXECUTION_MODES = {"read-only-audit", "implementation", "certification", "research"}

REQUIRED_CONTEXT_LABELS = (
    "Repository class:",
    "Risk tier:",
    "Runtime/dependency role:",
    "CI policy:",
    "Protected state",
)
REQUIRED_HANDOFF_LABELS = (
    "## Execution mode",
    "## Authority / location",
    "## Validation evidence",
    "## Protected state",
    "## Stale / uncertain state",
    "## Next atomic action",
    "## Minimum resume context",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def find_placeholders(text: str) -> list[str]:
    return sorted(set(PLACEHOLDER_PATTERN.findall(text)))


def field_value(text: str, label: str) -> str | None:
    match = re.search(rf"^{re.escape(label)}\s*(.+?)\s*$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else None


def section_value(text: str, heading: str) -> str | None:
    match = re.search(rf"^{re.escape(heading)}\s*\n+\s*([^\n]+)", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else None


def validate_enum(name: str, value: str | None, allowed: set[str], errors: list[str]) -> None:
    if value is None:
        return
    if value not in allowed:
        errors.append(f"{name}: invalid value {value!r}; allowed: {', '.join(sorted(allowed))}")


def validate_texts(context: str, handoff: str, *, allow_placeholders: bool = False) -> list[str]:
    errors: list[str] = []
    if not allow_placeholders:
        for relative, text in (("CONTEXT.md", context), ("HANDOFF.md", handoff)):
            for placeholder in find_placeholders(text):
                errors.append(f"{relative}: unresolved placeholder: {placeholder}")

    for label in REQUIRED_CONTEXT_LABELS:
        if label not in context:
            errors.append(f"CONTEXT.md: missing required bootstrap field: {label}")
    for label in REQUIRED_HANDOFF_LABELS:
        if label not in handoff:
            errors.append(f"HANDOFF.md: missing required handoff section: {label}")

    if not allow_placeholders:
        validate_enum("Repository class", field_value(context, "Repository class:"), ALLOWED_REPOSITORY_CLASSES, errors)
        validate_enum("Risk tier", field_value(context, "Risk tier:"), ALLOWED_RISK_TIERS, errors)
        validate_enum("Runtime/dependency role", field_value(context, "Runtime/dependency role:"), ALLOWED_DEPENDENCY_ROLES, errors)
        validate_enum("CI policy", field_value(context, "CI policy:"), ALLOWED_CI_POLICIES, errors)
        validate_enum("Execution mode", section_value(handoff, "## Execution mode"), ALLOWED_EXECUTION_MODES, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", action="store_true", help="validate canonical template structure while allowing placeholders")
    args = parser.parse_args()
    root = repo_root()
    texts: dict[str, str] = {}
    errors: list[str] = []
    for relative in REQUIRED:
        path = root / relative
        if not path.is_file():
            errors.append(f"missing required file: {relative}")
            continue
        texts[relative] = path.read_text(encoding="utf-8")
    if not errors:
        errors.extend(validate_texts(texts["CONTEXT.md"], texts["HANDOFF.md"], allow_placeholders=args.template))
    if errors:
        print("BOOTSTRAP CHECK: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("BOOTSTRAP CHECK: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
