# Operational Benchmark Protocol

The reference implementation tracks four operational benchmarks independently of reference qualification.

## Status values

- PASS — exercised with retained evidence satisfying the benchmark.
- STRUCTURAL — required mechanism exists, but no retained real execution proves it yet.
- PENDING — mechanism or execution has not yet been completed.
- FAIL — exercised and acceptance criteria were not met.

Do not upgrade a benchmark because a template exists.

## Cold start

Evidence must show a fresh context, without the originating transcript, can recover:

- repository authority;
- current phase/stage;
- closed decisions;
- required context;
- validation state;
- next atomic action.

## Delegation

Evidence must show a bounded worker received only the declared context bundle, executed the bounded task, and returned the required compact completion report.

## Staleness

Evidence must show a changed declared input invalidates affected downstream work while unrelated work remains current.

Synthetic unit tests are valid evidence for deterministic staleness mechanics.

## Promotion

Evidence must show:

1. project-specific authority moved to a destination repository;
2. authoritative material exists at the destination, verified with an appropriate connector/tool;
3. the source repository retains a promotion pointer or equivalent historical trace when appropriate;
4. the source copy is no longer treated as competing project canon.

Local promotion validation alone is STRUCTURAL evidence, not PASS.

## Retention

Use templates/icm/BENCHMARK-EVIDENCE.md and retain evidence in the relevant completed workflow or project repository.
