# Versioning and Migration Policy

The canonical template follows semantic versioning.

- **MAJOR**: breaking workflow/state/bootstrap contract changes requiring child-repository migration.
- **MINOR**: backwards-compatible capabilities, templates, checks, or optional policy additions.
- **PATCH**: backwards-compatible fixes, documentation corrections, and test improvements.

Child repositories record the template version or source commit in `HANDOFF.md`/repository context. They do not automatically track `main`.

## Migration rule

A child repository upgrades deliberately:

1. identify current template version/commit;
2. read intervening changelog entries and migration notes;
3. apply changes on an isolated branch/worktree;
4. preserve project-specific policy intentionally;
5. run bootstrap/workflow/tests appropriate to the repository risk;
6. record the adopted version and migration evidence.

## 2.0.0 migration notes

Repositories created before 2.0.0 should review:

- workflow execution metadata (mode, branch/worktree, owner, write scope);
- provenance enforcement;
- active-stage contract completeness;
- completed-workflow terminal-state rules;
- optional child CI trigger/check updates;
- decision-record location and template.

Do not mass-migrate stable repositories merely to chase the template version. Upgrade when the repository is actively worked on or when a fixed control materially affects its risk.

## 2.1.0 migration notes

2.1.0 is backward-compatible with the 2.0 folder/workflow contract. Existing repositories may continue using the hardened folder model without initializing a graph.

Repositories adopting the graph compiler should:

1. upgrade template scripts/schemas on an isolated branch;
2. run `python3 scripts/icm.py audit` without writes and review unresolved state;
3. optionally persist the proposal with `icm audit --write`;
4. review the proposed graph and protected-resource policy;
5. run `icm init` as a dry run;
6. materialize only with `icm init --write`;
7. run `icm validate` plus the repository's existing tests/workflow checks;
8. add the optional child context-integrity workflow only when repository risk justifies continuous enforcement;
9. record the adopted template version/commit and migration evidence.

Do not copy the KPDC, Authority Engine, or PCAS certification fixtures into child project canon. They are template-level regression evidence only.
