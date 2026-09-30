# Decision: WebGL 2 production renderer with WebGPU-ready architecture and selective Wasm

date: 2026-09-28
status: accepted
owners: coordinator
supersedes: none
superseded_by: none

## Context

Portfolio World needs dependable browser reach, a small asset/runtime footprint, and room for richer GPU-driven visuals later.

WebGPU can provide a modern rendering/compute path, but making it mandatory in v1 would increase compatibility and implementation risk before the basic world has been proven.

WebAssembly can improve selected CPU-heavy or codec workloads, but application-wide Wasm would add complexity without a demonstrated need for ordinary movement, interaction, content, or UI.

## Decision

For v1:
- use WebGL 2 through stable Three.js / React Three Fiber as the production renderer;
- keep a renderer boundary so WebGPU can be tested later without rewriting world/application logic;
- perform any WebGPU comparison only after the Command Center vertical slice is stable;
- permit Wasm only as a selective implementation detail of mature libraries or helpers with measurable benefit;
- keep movement, navigation, interaction, content, and HTML UI in the normal TypeScript/React architecture;
- preserve a complete conventional HTML fallback regardless of GPU capability.

WebGPU and Wasm are not rejected. They are deliberately prevented from becoming premature architectural dependencies.

## Consequences

- v1 prioritizes compatibility and maturity;
- WebGPU experiments can be isolated and benchmarked against the same scene;
- visual effects can later become progressively enhanced rather than mandatory;
- Wasm remains available for codecs, navigation, or heavy helpers without infecting ordinary application code;
- the project avoids maintaining two rendering/application architectures.

## Validation / evidence

Governed by:
- `docs/portfolio-world/RENDERING-TECHNOLOGY.md`;
- `docs/portfolio-world/ARCHITECTURE.md`;
- `docs/portfolio-world/ASSET-BUDGET.md`;
- the Command Center vertical-slice performance/capability evidence when implemented.

## Revisit when

- the Command Center vertical slice is certified and a controlled WebGPU comparison demonstrates material benefit;
- stable ecosystem support changes enough to lower production risk materially;
- a concrete workload demonstrates that TypeScript/JavaScript is the limiting factor and a Wasm helper can improve it;
- a required visual effect cannot be delivered acceptably through the production WebGL path.
