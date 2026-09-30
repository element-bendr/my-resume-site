# Rendering Technology Contract

## Purpose

This document freezes the rendering/runtime technology policy for Portfolio World v1.

The objective is to preserve production reliability today while keeping the architecture ready for WebGPU and selective WebAssembly use without coupling application logic to either technology.

## V1 production rendering

Primary production renderer:
- WebGL 2 through stable Three.js / React Three Fiber.

Application framework:
- React;
- TypeScript;
- Vite;
- stable React Three Fiber;
- Three.js;
- Drei where useful.

WebGPU is not a mandatory v1 runtime dependency.

## Renderer boundary

Application and world logic must not depend directly on a single GPU backend.

```text
React Application
      │
      ├─ Content
      ├─ PlayerController
      ├─ NavigationController
      ├─ InteractionController
      ├─ World / Scene
      │
      ▼
Renderer Boundary
      │
      ├─ WebGL 2      ← v1 production
      └─ WebGPU       ← optional experimental path
```

Movement, content, navigation, interaction state, project data, and HTML UI must remain renderer-independent.

A renderer change must not require rewriting character movement or portfolio content logic.

## WebGPU policy

WebGPU is an architecture-ready capability, not a v1 requirement.

Allowed uses after the Command Center vertical slice is stable:
- experimental renderer comparison;
- advanced hologram effects;
- GPU-driven particles;
- signal-flow visualizations;
- modern shader/compute experiments;
- visual effects that have a measurable benefit over the WebGL implementation.

WebGPU adoption into production requires evidence from the same scene and assets.

Required comparison:
- frame time;
- frame rate;
- GPU/CPU cost where measurable;
- memory;
- bundle/runtime cost;
- browser/device compatibility;
- visual capability gained;
- fallback behavior.

WebGPU must not become production-critical merely because it benchmarks faster on a high-end development machine.

## WebGPU production rule

If WebGPU is introduced later:
1. the same essential portfolio content must remain available through WebGL 2 or the HTML fallback;
2. feature detection must be used;
3. unsupported devices must not see a broken world;
4. renderer-specific effects must degrade gracefully;
5. WebGPU-specific code must remain behind the renderer/effect boundary;
6. adoption requires a recorded decision and certification evidence.

## WebAssembly policy

WebAssembly is permitted as a selective implementation detail when a mature library provides a measured benefit.

Acceptable examples:
- geometry decoding;
- texture transcoding;
- compression/decompression;
- mature navigation/pathfinding implementation;
- computationally expensive asset/runtime helpers.

WebAssembly is not the default language/runtime for:
- player input;
- ordinary character movement;
- React UI;
- portfolio content;
- ordinary application state;
- simple interaction logic.

Do not rewrite TypeScript application logic in Rust/C/C++/Wasm without a measured performance or capability need.

## Wasm boundary

```text
Application Logic
   │
   ├─ TypeScript / React
   │
   ▼
Specialized helper
   │
   ├─ JS implementation
   └─ mature Wasm-backed library
```

The application consumes the helper contract. It does not become coupled to the binary implementation.

## Asset-codec rule

Wasm-backed decoders/transcoders are encouraged where they reduce shipped asset size or improve decode performance without violating the asset budget.

Examples include compressed geometry and GPU texture formats.

Their own binary payloads count toward performance budgets and must be measured.

## Cloudflare boundary

The browser performs 3D rendering.

Cloudflare Workers:
- serve static application/world assets;
- run dynamic APIs where required;
- do not perform browser rendering.

Server-side Wasm inside Workers is permitted only for a separately justified backend computation requirement.

## Progressive enhancement

Rendering capability tiers:

```text
Tier A
WebGPU-enhanced effects, when explicitly enabled and supported

Tier B
WebGL 2 production world

Tier C
low-power / reduced-effects WebGL experience

Tier D
conventional HTML portfolio/resume
```

Tier D is always valid and complete for essential portfolio use.

## Command Center experiment gate

The Command Center vertical slice is built first with the production WebGL 2 path.

Only after that slice passes its functional, asset, performance, mobile, and accessibility gates may a WebGPU comparison branch/experiment be created.

The experiment must use:
- the same Command Center;
- the same avatar;
- the same assets;
- the same interactions;
- the same content.

This prevents visual or asset changes from contaminating renderer comparisons.

## Non-negotiable invariants

1. WebGL 2 is the v1 production renderer.
2. WebGPU is optional and must never block essential portfolio access.
3. Wasm is selective infrastructure, not the application architecture.
4. Player/navigation/content logic remains renderer-independent.
5. WebGPU or Wasm adoption requires measured benefit.
6. Unsupported GPU capability falls back rather than fails closed to a blank portfolio.
7. Renderer experiments occur after, not before, the Command Center vertical slice.
8. Technology experiments must remain within the repository asset/performance budgets.
