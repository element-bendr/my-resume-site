# Command Center Draco/CSP correction contract

Status: active after browser certification STOP on `command-center-browser-cert-001`.

## Root cause

The certified production GLB is valid and downloads successfully, but it requires `KHR_draco_mesh_compression` for all 253 mesh primitives.

The current Drei `useGLTF` path enables Draco by default and uses the Google-hosted decoder path. Production CSP permits only self-hosted script/connect sources and does not permit WebAssembly compilation, so the model fetch succeeds but decoding/rendering fails.

The failed browser evidence is preserved at candidate:

`bee352c0c2cf81f7564fb6b61864dc693cdb6720`

Terra verdict: STOP.

## Decision

Preserve the certified GLB and preserve CSP.

Correct the runtime by:

1. vendoring the JavaScript Draco decoder from the exact installed `three@0.186.0` package into:
   `public/draco/draco_decoder.js`;
2. configuring a dedicated `DRACOLoader` for Command Center with:
   - decoder path `/draco/`;
   - decoder config `{ type: "js" }`;
3. passing that loader to `GLTFLoader` through the `useGLTF` extension hook;
4. disabling Drei's default Draco loader for this call by passing `false` as the second `useGLTF` argument.

Do not add `wasm-unsafe-eval`.
Do not add `unsafe-eval`.
Do not add external Draco CDN origins to CSP.
Do not change the production GLB.

## Decoder provenance

The executor must copy the decoder from the installed package corresponding to the repository's locked `three@0.186.0`, preferably:

`node_modules/three/examples/jsm/libs/draco/gltf/draco_decoder.js`

If that exact path is absent, STOP rather than downloading an arbitrary decoder from the network.

Record the source path/version and SHA-256 in the correction evidence.

## Validation

Required validations:

- `command-center-draco-local`
- `blender-assets`
- `runtime-integration`
- `icm-stage`

The dedicated validator proves:

- the certified GLB hash/size are unchanged;
- the GLB still requires Draco;
- the local JS decoder exists;
- Command Center disables Drei's default Draco loader;
- the dedicated loader points at `/draco/` and forces JS decoding;
- CSP contains no eval/WebAssembly relaxation and no external Google decoder origin.

## Browser follow-up

This correction task does not itself certify visual success.

After independent PASS, rerun browser certification as a new task against the exact correction candidate.

The next browser run must prove:

- no gstatic Draco request;
- no WebAssembly/CSP error;
- local `/draco/draco_decoder.js` request succeeds;
- Command Center GLB renders;
- application errors return to zero;
- the full visual/runtime acceptance matrix can resume.
