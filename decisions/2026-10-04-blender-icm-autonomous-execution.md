# Decision: adopt graph-backed ICM execution for Blender authoring

Date: 2026-10-04
Status: accepted
Upstream ICM source: `element-bendr/icm-repo-template@5fa96deb6c3b54f6d9c17def2ea51e69e6a1fb5e`

## Context

Stage 02 is already governed, Blender-authored and fail-closed, but the visual authoring loop still pays unnecessary coordination cost through broad context reloads and repeated prompt/render/review handoffs. PR #22 proved graph-backed compact context against this repository in a disposable benchmark, but deliberately did not install it.

The accepted Massing V2 composition, preview camera, Blender source, runtime topology, spawn, Ask interaction, bridge entrances, React ownership boundaries and user-owned `AGENTS.md` remain protected.

## Decision

- inherit the certified graph-backed ICM compiler, schemas and local-execution bridge from the pinned upstream commit;
- use `icm context --compact` as the default context surface for substantial Blender tasks;
- keep Git and canonical graph/state authoritative; generated Markdown remains a projection;
- Sol owns coordination, architecture and escalation rather than routine render corrections;
- Luna is the bounded Blender executor;
- Terra provides visual critique and detached independent review;
- ICM owns freshness, lifecycle, protected state, evidence, claims, candidate durability, certification and promotion;
- bounded scene -> render -> critique -> correction iterations may occur inside one declared authoring task while scope and protected assumptions remain unchanged;
- two materially similar failed repairs trigger an upstream rule/reference/contract correction instead of a third near-identical patch;
- claims and candidates use create-only `refs/heads/icm/claims/<task-id>` and `refs/heads/icm/candidates/<task-id>`;
- production GLB export, React integration, merge and deployment remain blocked by the existing Stage 02 gates;
- this migration itself makes no visual scene change and must not modify `AGENTS.md`.

## Consequences

Turnaround should improve through smaller initial context, on-demand dependency bodies, reusable evidence, incremental staleness and fewer coordinator round-trips. The target is less orchestration latency, not weaker review.
