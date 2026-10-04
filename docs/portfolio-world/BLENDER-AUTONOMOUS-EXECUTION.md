# Blender autonomous execution under ICM

Status: migration contract
Parent workflow: `portfolio-world-blender-art`
Active stage: `02-command-center-integration`

## Purpose

Move Command Center authoring from repeated coordinator-driven prompt/render/check cycles to a bounded local execution loop using the current graph-backed ICM runtime.

## Control flow

```text
canonical graph + exact Git/source fingerprints
                  |
                  v
         icm context --compact
                  |
                  v
          bounded task record
                  |
                  v
         trusted local runner
                  |
                  v
                Luna
          Blender scene builder
                  |
          canonical render suite
                  |
                  v
         bounded visual critique
                  |
            fix / converge
                  |
                  v
        committed candidate SHA
                  |
                  v
   create-only remote candidate ref
                  |
                  v
        Terra detached review
                  |
          PASS / FIX / STOP
                  |
                  v
         formal ICM certification
```

## Runtime context policy

Bootstrap only what is required to start safely: the active Stage 02 contract, accepted camera/composition decision, Command Center specification, direct protected-state constraints, source-validation requirements, modified artifacts and blockers. Keep unrelated website/runtime source on-demand until a named uncertainty requires it.

## Visual iteration policy

One bounded authoring task may perform multiple local scene/render corrections while its objective, allowed write paths and protected assumptions remain unchanged. Each iteration must leave compact evidence sufficient to explain the next change.

A materially repeated failure twice triggers STOP and an upstream correction to the scene rule, reference interpretation or task/stage contract. It does not authorize a third cosmetic variation.

## Roles

- **Sol:** coordinator, architecture, ambiguity and escalation.
- **Luna:** Blender implementation, source edits, material/lighting work within scope, canonical renders, source validation and candidate preparation.
- **Terra:** visual criticism and detached independent review.
- **ICM:** graph/source freshness, claims, candidate refs, protected state, lifecycle, evidence linkage, certification and promotion boundaries.

## Durable and local state

Git-side records:

```text
workflow/local-execution/
  queue/<task-id>.json
  results/<task-id>.json
  reviews/<task-id>.json
```

Refs:

```text
refs/heads/icm/control
refs/heads/icm/claims/<task-id>
refs/heads/icm/candidates/<task-id>
```

Machine-local policies, credentials, locks and recovery receipts stay outside Git under `.icm-local/` or another protected local path.

## Adoption sequence

1. install the pinned compiler, schemas and local-execution bridge;
2. initialize canonical graph state from the exact migrated head;
3. validate graph/source freshness and Stage 02 subject resolution;
4. create/protect `icm/control`;
5. configure local Luna executor and Terra reviewer profiles;
6. run one no-production-change fixture task;
7. create the first bounded Command Center detailed-authoring task;
8. retain immutable candidate/result/review evidence;
9. continue the existing detailed visual, source, export and runtime gates.

## Protected state

This migration does not authorize changes to `main`, production, the accepted Massing V2 spatial composition, approved preview camera, runtime camera semantics, world topology or bridge bounds, player spawn, Ask content/interaction, fallback/accessibility behavior, user-owned `AGENTS.md`, or production `command-center.glb` before detailed visual/source approval.
