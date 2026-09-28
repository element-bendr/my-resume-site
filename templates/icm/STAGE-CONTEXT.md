# <Stage Name>

## Authority / ownership

- repository: <owner/repository>
- branch/worktree: <owned branch/worktree>
- owner: <agent/person/lane>
- execution mode: <read-only-audit | implementation | certification | research>
- parallel-write boundaries: <paths/lane boundaries or none>

## Inputs

- <required input>

## Objective

<one primary deliverable>

## In Scope

- <included work>

## Out of Scope

- <excluded work>

## Dependencies

- <stable reference or previous-stage output, or none>

## Process

1. Inspect current repository state and relevant diff.
2. Load only context needed for this stage.
3. Confirm execution mode, protected state, and ownership.
4. Execute only work allowed by the contract.
5. Validate at meaningful checkpoints.
6. Inspect final diff/status.
7. Update handoff/completion evidence.

## Outputs

- <durable output>

## Acceptance

- <observable pass condition>

## Verify

- <specific command/check>

## Protected State

- <state that must not change>

## Known closed decisions

- <closed decision, or none>

## Stop Conditions

- <condition requiring stop/escalation>
