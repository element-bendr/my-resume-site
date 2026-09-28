# Managed Workflow

Use this directory for substantial staged work with dependencies, acceptance criteria, delegation, production risk, or certification needs.

## Lifecycle

```text
capture
  -> contract
  -> activate
  -> execute
  -> verify
  -> certify
  -> complete/archive
```

Active workflows live under `workflow/active/<workflow-id>/`.
Completed historical records live under `workflow/completed/<workflow-id>/`.

## Required active files

Each active workflow requires:

- `CONTEXT.md`
- `state.json`
- `output/` when durable stage evidence or outputs are needed

Use `templates/icm/` as the starting point.

## Active workflow selection

`workflow/index.json` provides deterministic primary selection when more than one workflow is active.

Rules:

1. explicit `--workflow` wins if it names an active workflow;
2. one active workflow may be inferred;
3. multiple active workflows require a valid `primary`;
4. directory order is never priority;
5. stale or invalid primary selection fails closed;
6. duplicate workflow IDs and folder/state identity mismatches fail closed.

See `docs/workflow-selection.md`.

## State and dependency graph

State schema version is currently 1.

Workflow state records:

- workflow identity and status;
- active stage;
- provenance;
- execution mode, branch/worktree, owner, and write scope;
- stage relationships;
- file dependencies and pinned Git blob IDs;
- declared outputs;
- completion-report paths.

Stage dependency graphs must be acyclic.

Certified stages must pin declared dependencies. If a certified dependency changes, `workflow_pin.py --write` refuses to rewrite the evidence. Reopen the stage explicitly with `workflow_reopen.py`, which invalidates affected downstream state before re-pinning.

## Deterministic helper commands

```bash
python3 scripts/workflow_check.py
python3 scripts/workflow_status.py
python3 scripts/workflow_stale.py
python3 scripts/workflow_new.py <workflow-id>
python3 scripts/workflow_activate.py
python3 scripts/workflow_pin.py
python3 scripts/workflow_reopen.py <stage-id> --reason "..."
python3 scripts/workflow_context.py
python3 scripts/workflow_certify_check.py
python3 scripts/workflow_certify.py
python3 scripts/workflow_complete.py
python3 scripts/workflow_promote_check.py
```

## Contract and activation

`workflow_new.py` creates a conservative **BLOCKED** workflow with an incomplete stage contract. Work is not execution-ready until placeholders are resolved and `workflow_activate.py` passes.

Read-only audit mode is machine-readable and cannot declare write paths.

## Certification

`workflow_certify_check.py` validates:

- workflow/state integrity;
- complete stage contract;
- provenance;
- pinned/current dependencies;
- staleness;
- declared outputs;
- completion evidence;
- protected-state and handoff markers;
- candidate commit and, by default, clean working tree.

`workflow_certify.py --write` records the validated candidate commit and transitions stage/workflow state without pretending the certification-record commit is the implementation commit.

## Completion

`workflow_complete.py` accepts only a fully certified workflow. It:

- runs fail-closed preflight;
- requires completion reports;
- archives active → completed state;
- rewrites archived stage paths;
- updates `workflow/index.json` deterministically;
- uses rollback logic if the multi-file transition fails.

Completed workflows are historical evidence snapshots and are not required to remain valid against future edits to current source or global policy files.

## Context bundle

`workflow_context.py` emits only the ordered required context paths by default:

1. `AGENTS.md`
2. `CONTEXT.md`
3. `HANDOFF.md`
4. active stage `CONTEXT.md`
5. declared file dependencies

It does not dump file contents by default.

## Promotion

Promotion records use `templates/icm/PROMOTION-RECORD.md`.

Local validation proves local record structure, source existence, and explicit authority-transfer semantics only. Remote destination existence requires separate connector/tool evidence.

## Operational benchmarks

See `docs/benchmark-protocol.md` and `templates/icm/BENCHMARK-EVIDENCE.md`.

PASS requires retained evidence. STRUCTURAL means the mechanism exists but clean operational evidence is not yet retained.
