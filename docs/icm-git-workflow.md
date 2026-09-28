# ICM + Git Workflow

Status: ACTIVE REFERENCE
Repository: element-bendr/icm-repo-template

## Purpose

This workflow combines staged context management with GitHub-backed durable state. The goal is to minimize unnecessary context, repeated scans, transcript replay, and indiscriminate validation while keeping risky work auditable.

The methodology is inspired by Interpretable Context Methodology (ICM):
https://arxiv.org/html/2603.16021v2

This repository adds project governance, validation discipline, executor routing, certification, stale-state handling, and promotion between repositories.

## Four layers

### 1. Durable state: GitHub

Git commits, repository files, decisions, and retained outputs preserve authoritative history.

### 2. Context architecture: progressive routing

- L0: repository identity and global policy
- L1: root context router
- L2: active stage contract
- L3: stable references
- L4: current working artifacts

### 3. Execution policy: AGENTS.md

`AGENTS.md` defines how work is scoped, delegated, validated, stopped, handed off, and certified.

### 4. Enforcement: deterministic checks and risk-based CI

Local or agent-run scripts validate workflow structure, ownership, provenance, dependency state, certification, and completion.

CI is not universal. Low-risk documentation/research repositories may remain without continuous CI. Production/code repositories may install `templates/icm/.github/workflows/context-integrity.yml`. The canonical template itself uses `.github/workflows/template-self-test.yml`.

## Two operating modes

### Lightweight repository mode

Use for simple bounded work that does not benefit from staged dependency tracking, such as small documentation changes, isolated configuration edits, straightforward research notes, or low-risk content updates.

### Managed workflow mode

Use when work has multiple stages, dependencies, acceptance criteria, meaningful delegation, production risk, or certification needs.

Create:

```text
workflow/active/<workflow-id>/
  CONTEXT.md
  state.json
  output/
```

The stage contract is the task contract.

## Managed lifecycle

```text
capture
  -> contract
  -> activate
  -> execute
  -> verify
  -> certify
  -> complete/archive
```

### Initialization and activation

`workflow_new.py` creates a blocked scaffold and records starting provenance plus execution metadata.

`workflow_activate.py` refuses activation until the stage contract is complete and execution state is valid.

### Dependency pinning and reopening

`workflow_pin.py` computes Git blob IDs for declared dependencies. It is dry-run by default.

Certified dependencies cannot be silently repinned. If a certified dependency changes, `workflow_reopen.py` explicitly reopens the stage, clears workflow certification, records the reason, and marks affected downstream work stale before re-pinning.

### Staleness

Changed declared inputs invalidate affected downstream stages only. Unrelated stages remain current.

### Certification

`workflow_certify_check.py` validates:

- workflow/state integrity;
- stage contract completeness;
- provenance;
- dependency pin/current state;
- staleness;
- declared outputs;
- completion evidence;
- protected-state and handoff markers;
- candidate commit;
- clean working tree by default.

`workflow_certify.py` records the validated candidate commit and transitions stage/workflow state.

Certification is permission to stop re-proving unchanged facts, not permission to ignore changed dependencies.

### Completion

`workflow_complete.py` accepts only a fully certified workflow, archives it atomically as far as ordinary filesystem semantics allow, updates primary selection deterministically, and rolls back ambiguous partial moves when possible.

Completed workflows are historical evidence snapshots. They are validated for record integrity, not against future live dependency/output paths.

## Conversation policy

Conversation boundaries follow workflow state, not arbitrary length.

Prefer a fresh bounded context when architecture becomes implementation, implementation becomes certification, canonical decisions materially change, several rejected approaches remain active, exact state becomes uncertain after compaction, or a bounded worker is delegated.

Fresh context should normally consist of repository entry files plus the active stage contract, not transcript replay.

## Edit-source principle

If the same correction is repeatedly applied to outputs, fix the rule, reference, template, or stage contract that causes the error.

## Decisions

Durable architecture/scope/governance decisions live under `decisions/` using `templates/icm/DECISION.md`. Supersede old decisions explicitly rather than silently rewriting history.

## Promotion

Promotion records transfer authority explicitly from a source repository to a destination repository. Local promotion validation never claims that a remote destination exists without connector/tool evidence.

## Reference acceptance tests

1. **Cold start** — fresh context recovers authority, state, closed decisions, and next action.
2. **Delegation** — a bounded worker executes from compact context and returns required evidence.
3. **Staleness** — changed declared inputs invalidate only affected work.
4. **Promotion** — authority moves without creating competing sources of truth.

Benchmark states remain PASS, STRUCTURAL, PENDING, or FAIL. Structural capability alone does not count as operational PASS.

## Provenance

Certification records the commit whose implementation was actually validated.

The certification record itself is committed after that candidate and therefore does not attempt to contain its own future Git SHA.

## Bounded execution

Prefer targeted reads, bounded command output, summarized JSON, and batched related QA over full logs or recursive discovery.

Status requests do not trigger rescans merely for reassurance.

## Adoption rule

Do not mass-migrate stable repositories merely to chase the template version. Adopt or upgrade when the repository is next actively worked on or when a fixed control materially affects its risk.

ICM + Git organizes work around production systems. It does not replace runtime orchestration, databases, queues, APIs, or event state.
