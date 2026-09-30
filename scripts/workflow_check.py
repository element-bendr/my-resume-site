from __future__ import annotations
import sys
from workflow_lib import repo_root,state_files,validate_state
from workflow_selection import validate_index
REQUIRED_ROOT_FILES=[".gitignore","AGENTS.md","BOOTSTRAP.md","CHANGELOG.md","CONTEXT.md","HANDOFF.md","VERSION","decisions/README.md","workflow/README.md","docs/icm-git-workflow.md","docs/hardened-operating-profile.md","docs/repository-governance.md","docs/versioning-and-migrations.md"]
def main():
    root=repo_root(); errors=[]
    for rel in REQUIRED_ROOT_FILES:
        if not (root/rel).is_file():errors.append(f"missing required file: {rel}")
    try:
        active=state_files(root,include_completed=False); all_states=state_files(root,include_completed=True)
    except Exception as exc:
        active=[]; all_states=[]; errors.append(f"workflow discovery failed: {exc}")
    for path in all_states: errors.extend(validate_state(root,path,historical="workflow/completed/" in path.as_posix()))
    errors.extend(validate_index(root))
    if errors:
        print("WORKFLOW CHECK: FAIL")
        for e in errors:print(f"- {e}")
        return 1
    print("WORKFLOW CHECK: PASS"); print(f"active_workflows={len(active)}"); print(f"state_records={len(all_states)}"); return 0
if __name__=="__main__":sys.exit(main())
