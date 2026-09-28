# Agent Operating Policy

GitHub repository state is authoritative for durable project context. Conversation history and model memory may help locate context, but they do not override repository canon.

## 1. Context loading

Load context progressively.

For substantial work, start with:

1. `AGENTS.md`
2. `CONTEXT.md`
3. `HANDOFF.md`
4. the active workflow stage `CONTEXT.md`, when one exists
5. only references explicitly required by that stage

Do not recursively scan the repository by default. Broaden context only to resolve a named uncertainty.

On continuation work, inspect current state and diff before broad discovery.

### Canonical-template repository exception

In `element-bendr/icm-repo-template` itself, root `CONTEXT.md` and `HANDOFF.md` are intentionally the bootstrap payload inherited by child repositories and therefore contain placeholders.

For maintenance of the canonical template repository, after `AGENTS.md` read:

1. `PROVENANCE.md`;
2. `workflow/index.json`;
3. the active workflow `CONTEXT.md`, when one exists;
4. only references required by that workflow.

Do not rewrite root `CONTEXT.md` or `HANDOFF.md` with template-maintainer runtime state, because that state would leak into every child repository. Child repositories use the normal context-loading order above after bootstrap.

## 2. Plan and record before implementation

For complex, risky, multi-stage, parallel, or production-affecting work, record the contract in Git before implementation begins.

The stage contract must define inputs, objective, in-scope and out-of-scope work, dependencies, process, outputs, acceptance criteria, verification, protected state, and stop conditions.

One stage should have one primary job.

If implementation direction materially changes, update the durable contract first rather than allowing chat instructions to silently outrun repository canon.

## 3. Main, branches, and worktrees

Treat `main` as the canonical integrated baseline.

Use an isolated branch/worktree for substantial implementation, parallel work, risky changes, or work that could collide with production state.

Parallel lanes must have explicit ownership boundaries. Avoid overlapping writes unless the integration plan explicitly coordinates them.

Lifecycle:

```text
plan/contract
  -> branch/worktree
  -> implement
  -> targeted validation
  -> integration
  -> certification
  -> merge
  -> archive evidence
  -> delete temporary branch/worktree
```

Do not keep merged feature or hardening branches as pseudo-documentation. Git history and completed workflow evidence preserve provenance.

## 4. Production-first dependency rule

Any component that can feed, influence, trigger, update, or be consumed by another system must be production-ready before it becomes a dependency.

Demo-grade components may be explored, but they must not become part of the production dependency graph.

For production systems, fail closed: missing evidence, unresolved validation, ambiguous authority, stale required inputs, or protected-state uncertainty block certification, promotion, or merge.

## 5. Validation by change class

Run the smallest validation capable of proving the relevant acceptance criteria.

- documentation: diff plus reference/link sanity
- static content: targeted content/render check
- visual-only layout: visual inspection
- localized code: targeted unit/component tests
- schema/API contract: contract plus affected integration tests
- shared runtime/library: affected package and dependent tests
- dependency/configuration: build plus affected integration tests
- security/production workflow: targeted tests plus relevant certification
- frozen asset: integrity/hash validation unless the asset itself changed

Validate incrementally at meaningful build checkpoints. Do not defer all proof until the end of a long implementation pass.

Before finishing, inspect diff/status and run the smallest relevant final proof.

## 6. Certification, promotion, and stale state

A certified result remains trusted for the commit and dependencies against which it was certified.

Do not recertify unchanged components merely for reassurance.

When a declared dependency changes, mark only affected downstream work stale. Prefer incremental proof over repeated full-system proof.

Historical completed workflows are evidence snapshots. Do not reinterpret them as current state.

Promotion requires explicit authority transfer. Local structural validation must never be represented as proof that a remote destination exists or is correct.

## 7. No new evidence, no new scan

Do not repeat repository scans, searches, audits, builds, or tests unless relevant state changed, freshness materially matters, the previous result was incomplete, or new evidence creates a specific unresolved question.

A status request alone is not justification for rerunning tools.

Research stops when the defined questions are answered and no material contradiction remains. Additional research requires a named unresolved question.

## 8. Conversation boundaries

Continue in the same conversation while the active problem and stage remain coherent.

Prefer a fresh bounded context when architecture becomes implementation, implementation becomes certification, research becomes a final deliverable, a prototype becomes frozen design, canonical inputs change materially, multiple rejected approaches remain in active context, compaction makes exact operational state uncertain, or work is delegated to another model/worker.

A fresh conversation receives repository state plus a concise handoff, not the full transcript.

## 9. Delegation and routing

Route work by ambiguity, coupling, and blast radius rather than task length.

Use lower-cost or deterministic workers for bounded extraction, scanning, classification, repetitive tests, and verification.

Use stronger implementation/reasoning workers for coupled code changes, debugging, architecture, risky decisions, integration, and final review.

Delegated work receives fresh bounded context and must return:

- state changed;
- evidence;
- validation;
- blockers;
- protected-state status;
- stale or uncertain assumptions;
- next action.

The coordinator should consume summarized evidence rather than raw command output whenever practical.

## 10. Prototype limits and edit-source principle

Do not continue materially similar implementation attempts indefinitely.

After two unsuccessful or rejected attempts:

1. stop implementation;
2. summarize the evidence;
3. revisit assumptions, contract, or source rule;
4. freeze the corrected direction;
5. resume only from the updated source.

If the same correction is repeatedly applied to outputs, fix the upstream rule, reference, template, or stage contract that causes the error.

## 11. Bounded tool output

Prefer bounded evidence over broad output.

Use targeted file reads, searches, line ranges, counts, and summarized JSON when they can answer the question. Avoid dumping full repository trees, logs, test output, or API payloads when a compact summary is sufficient.

Batch closely related reads and QA checks when doing so preserves clarity. Expand output only when the bounded result is incomplete or contradictory.

Tool use should reduce uncertainty, not manufacture transcript volume.

## 12. Feedback consolidation

When new non-blocking feedback arrives during an active execution pass, incorporate it into the current contract or next safe checkpoint before starting another pass.

Do not repeatedly restart scans, builds, or implementation for each minor steering comment.

Restart or invalidate current evidence only when feedback materially changes scope, authoritative sources, acceptance criteria, safety or protected state, architecture, or assumptions on which the current evidence depends.

## 13. Handoff discipline

A handoff is a state transfer, not a diary.

It must preserve enough durable information for a fresh agent or conversation to resume without replaying the transcript:

- current goal and phase;
- canonical repository/branch/worktree;
- active workflow/stage;
- last completed action;
- current state;
- material changes;
- canonical decisions;
- closed decisions that should not be reopened without new evidence;
- validation evidence and validated commit;
- protected-state status;
- stale or uncertain assumptions;
- blockers;
- exact next atomic action;
- minimum resume context.

Update `HANDOFF.md` at meaningful stage boundaries, before delegation, before ending a work session with unfinished state, and after certification/merge.

## 14. Status requests

A status request should normally be answered from known repository and execution state.

Use this compact shape:

- Phase
- Last completed action
- Current state
- Validation
- Blocker
- Next atomic action

Do not run tools merely because status was requested. Refresh only when known state is stale, incomplete, or materially uncertain.

## 15. Secrets and protected state

Protect production assets, defaults, secrets, credentials, frozen canon, and certified outputs during exploration.

Never commit secrets, private keys, access tokens, or environment-specific credentials.

Do not modify unrelated production state merely to simplify local implementation.

## 16. Repository-template inheritance

Projects created from this template own their project-specific implementation and decisions.

Reusable ICM methodology and tooling are governed by `element-bendr/icm-repo-template`.

If a project deliberately diverges from the reusable standard, record the reason locally rather than silently mutating the inherited contract.
