# Hardened Operating Profile

This file is the compact acceptance checklist for repositories created from the canonical ICM template.

A repository may tailor implementation details to its domain, but the controls below define the default hardened operating model for substantial work.

## Authority and context

- GitHub repository state is the durable source of truth.
- Root context is loaded progressively: AGENTS -> CONTEXT -> HANDOFF -> active stage -> explicit references.
- Conversation history does not override repository canon.
- Fresh conversations resume from bounded repository state rather than transcript replay.

## Planning and execution

- Material scope/architecture decisions are recorded before implementation.
- One managed stage has one primary objective.
- Main remains the canonical integrated baseline.
- Substantial, risky, or parallel work uses isolated branches/worktrees.
- Parallel lanes have explicit ownership and non-overlapping write boundaries.
- Execution mode, branch/worktree, owner, and write scope are machine-readable.
- Read-only audit mode cannot declare write paths.

## Production discipline

- Components that feed, trigger, update, influence, or are consumed by another production system must be production-ready before becoming dependencies.
- Missing evidence, stale required inputs, ambiguous authority, or protected-state uncertainty fail closed.
- Certified dependencies cannot be silently re-pinned.
- Secrets, production defaults, frozen assets, and unrelated certified state remain protected.

## Validation and certification

- Validation matches the change class and blast radius.
- Validation occurs at meaningful build checkpoints, not only at the end.
- Certified unchanged state is not repeatedly re-proven without new evidence.
- Dependency changes stale only affected downstream stages.
- Local structural proof is never presented as proof of remote existence or production correctness.
- Managed stages require deterministic certification evidence before completion.
- Completed workflows are historical evidence snapshots.

## Delegation

- Delegated workers receive bounded context and explicit ownership.
- Workers do not inherit full transcripts by default.
- Completion reports return state changed, evidence, validation, blockers, protected-state status, uncertainty, and next action.
- Coordinator context consumes summarized evidence rather than raw logs when practical.

## Handoff continuity

`HANDOFF.md` preserves:

- goal and phase;
- execution mode;
- repository/branch/worktree/stage;
- last completed action and current state;
- material changes;
- canonical and closed decisions;
- validation evidence and validated commit;
- protected-state status;
- stale/uncertain assumptions;
- blockers;
- exact next atomic action;
- minimum resume context.

Update it at meaningful stage boundaries, before delegation, before leaving unfinished work, and after certification/merge.

## Efficiency controls

- No new evidence means no new scan.
- Status requests do not trigger tools merely for reassurance.
- Repeated corrections modify the upstream source rule where possible.
- Two materially similar failed/rejected attempts trigger a contract/assumption review.
- Tool output is bounded to the evidence needed to decide or validate.

## Bootstrap gate

A child repository is not considered initialized until:

1. `CONTEXT.md` identifies repository class, risk tier, runtime/dependency role, CI policy, boundaries, and protected state.
2. `HANDOFF.md` contains no unresolved template placeholders.
3. template source/version is recorded.
4. `python3 scripts/bootstrap_check.py` passes.
5. `python3 scripts/workflow_check.py` passes.
6. substantial initial work has a complete managed stage contract.
7. `workflow_activate.py` has validated and activated that contract before implementation.
8. execution mode, ownership, branch/worktree, and write scope are machine-readable.

## CI

CI is risk-based, not ceremonial.

Low-risk repositories may remain without continuous CI. Production/code/security-sensitive repositories should install `templates/icm/.github/workflows/context-integrity.yml` when automated enforcement materially reduces risk.

The canonical template repository itself uses `.github/workflows/template-self-test.yml`; child repositories do not inherit canonical-template semantics.

## Optional graph-backed machine state

Template 2.1 can add canonical graph/state under `.icm/` without replacing the repository's ordinary folder structure.

When enabled:

- Git remains durable authority.
- Authored project files, decisions, evidence, and managed workflow folders remain first-class artifacts.
- Versioned nodes/typed edges represent machine relationships.
- Generated Markdown under `.icm/generated/` is derived output, not independently editable machine truth.
- Unknown or contradictory project facts remain explicit unresolved state.
- Protected resources are evaluated against actual changed paths when a diff is available.
- Execution DAG completion cannot bypass prerequisite or required-evidence checks.
- Audit proposals become stale when relevant repository control inputs change.

A repository may remain on the folder-only 2.0 model when graph-backed enforcement adds no material value.
