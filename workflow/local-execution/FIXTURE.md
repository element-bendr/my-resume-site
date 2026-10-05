# Local execution fixture

The first bridge exercise is intentionally deterministic. It proves ICM transport and isolation before any model is allowed to edit Blender.

## What it proves

- trusted `icm/control` task transport;
- exact code-base SHA binding;
- create-only claim ref;
- isolated `icm/run/<task-id>` worktree;
- bounded executor writes;
- allowlisted validation;
- committed clean candidate;
- create-only remote candidate ref;
- immutable result publication;
- detached reviewer worktree;
- executor/reviewer identity separation;
- immutable review publication.

The fixture may write only:

`workflow/local-execution/fixtures/<task-id>.txt`

It must not modify Blender, GLB, React, graph authority, workflow contracts, `AGENTS.md`, `main`, the active Blender branch, or `icm/control`.

## Machine-local setup

Copy the two example policies into `.icm-local/` and keep them uncommitted:

```bash
mkdir -p .icm-local
cp workflow/local-execution/policy.fixture.example.json .icm-local/runner-policy.json
cp workflow/local-execution/reviewer-policy.fixture.example.json .icm-local/reviewer-policy.json
```

The fixture uses only Python and Git. No model credentials are required.
