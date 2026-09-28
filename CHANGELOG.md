# Changelog

All notable changes to the canonical ICM repository template are recorded here.

## [2.1.0] - 2026-09-27

### Added
- graph-native, Git-backed ICM compiler with versioned node/edge schemas and deterministic JSONL storage;
- `icm audit`, `icm init`, `icm validate`, `icm status`, and `icm handoff` command surfaces;
- graph-derived human projections while preserving the existing repository folder structure;
- protected-resource diff enforcement with deny and approval-required policies;
- execution-DAG lifecycle checks, evidence-linked acceptance, bounded status/handoff views, and reusable CI validation;
- read-only certification fixtures derived from KPDC, Authority Engine, and PCAS project shapes;
- red-team coverage for stale proposals, partial/corrupt stores, path escapes, cycles, missing evidence, projection drift, and protected-state failures.

### Changed
- generated Markdown is explicitly a projection of canonical graph/state rather than competing machine authority;
- repository audit discovers ADRs from both `decisions/` and `docs/decisions/`;
- audit proposals carry a versioned input fingerprint and cannot be promoted after relevant repository inputs change;
- graph handoff includes responsible actors and unresolved state.

### Fixed
- partial graph stores are rejected instead of being interpreted as empty/default state;
- repository-audit paths are confined to the repository boundary;
- stale/legacy audit proposals fail closed during initialization.

## [2.0.0] - 2026-09-25

### Added
- hardened bootstrap validation and enum enforcement;
- production-first execution ownership and audit-mode controls;
- deterministic certification/completion lifecycle tooling;
- durable decision/ADR contract;
- canonical template self-testing and updated optional child CI;
- versioning and migration policy.

### Changed
- workflow state and validation are fail-closed around provenance, stale dependencies, completion, and identity;
- generic executor routing replaces model-name-specific canonical policy;
- promotion records use domain-neutral source terminology.

### Fixed
- malformed Python string literals in workflow tooling/tests;
- historical workflow validation semantics;
- certified-stage re-pinning bypass.
