# Delegation Contract

## Task

<one bounded task>

## Provenance / working location

- source commit: <commit SHA>
- branch/worktree: <assigned branch/worktree>
- execution mode: <read-only audit | implementation | certification | research>
- owned paths: <paths>
- must not modify: <protected/unowned paths>

## Read

Load only:

1. AGENTS.md
2. CONTEXT.md
3. HANDOFF.md
4. <active stage CONTEXT.md>
5. <explicitly required references>

Do not inherit or request the full originating transcript unless a named ambiguity cannot be resolved from repository state.

## Scope

### In scope

- <bounded work>

### Out of scope

- architecture changes unless explicitly delegated
- unrelated cleanup
- writes outside owned paths
- writes of any kind when execution mode is read-only audit
- reopening closed decisions without new evidence
- production promotion/merge unless explicitly delegated

## Acceptance

- <observable pass condition>

## Validation

- <smallest relevant check>

## Protected state

- <must remain unchanged>

## Return

Return a compact completion report containing:

- state changed;
- files/paths changed;
- evidence;
- validation;
- blockers;
- protected-state status;
- stale or uncertain assumptions;
- exact next action.

Do not return raw logs when a bounded summary is sufficient.
