# Stage 06 validation — cumulative evidence

Status: **BLOCKED**

Stage 06 remains active. This file records completed bounded lanes and does not certify Stage 06 as a whole.

## Final acceptance audit — blocked

PR: #10 — `stage06/final-acceptance-audit`

Audited pickup head: `79ccc4f3210e2bdb71b3867484578ae7928da437`

Passed evidence before the mandatory stop:

- Node `22.22.0` and npm `11.20.0`
- clean `npm ci`
- ICM bootstrap/workflow/strict status: PASS
- offline verification and typecheck: PASS
- full suite: 66/66 PASS
- production build: PASS
- critical conventional JS: 89.2 KiB gzip
- total client JS: 334.8 KiB gzip
- `WorldEntry`: 956.62 kB raw / 254.81 KiB gzip
- conventional and world asset budgets: PASS
- Ask disclosure and world Ask boundary guards: PASS
- 360/390/768/1024/1440 route matrix: no horizontal overflow
- conventional routes do not load `WorldEntry`
- initial `/play` load retains five lazy district chunks
- Ask Terminal overlay focus, Escape close, and movement resume: PASS
- destination routes render after each tested SPA exit

Mandatory runtime failure:

- leaving `/play` through header Ask, Projects, or Resume; world HUD Contact; or Ask Terminal Open Ask emits `NotFoundError: Failed to execute 'removeChild' on 'Node'`
- instrumentation isolated the operation to React removing a world-zone label wrapper from a disconnected Drei `Html` container during full Canvas teardown
- the failure is not Ask-specific and is distinct from the previously repaired fast-travel portal lifecycle
- no failed network request accompanied the error, and each destination route still rendered

Independent review:

- Terra reproduced the failure at 1440px through header Ask and at 390px through world HUD Ask
- Terra verdict: **FAIL**
- Stage 06 certification: NOT RUN

Required repair lane:

- coordinate R3F/Drei `Html` portal cleanup during `/play` route unmount
- preserve world labels, topology, navigation, movement, Ask behavior, and the existing fast-travel repair
- prove header, world HUD, and Ask Terminal exits have zero page errors
- rerun fast-travel regression, focused/full tests, build, budgets, and independent review

Protected state remained intact: no application repair was attempted in the audit lane; no content, Ask, dependency, topology, controller, `main`, production, or Stage 07 change occurred.

## Lane 1 — narrow homepage overflow

PR: #6 — `fix(stage06): eliminate narrow homepage overflow`

Validated head: `61900faf6e7510b8cd99db0e5d39a77d850c3b8e`

Evidence:

- root cause isolated to the narrow-screen homepage hero heading using `15vw`
- fix changed the narrow-screen fluid size to `12vw`
- 360px: `scrollWidth=360`, `innerWidth=360`
- 390px: `scrollWidth=390`, `innerWidth=390`
- 768/1024/1440: no horizontal overflow or typography regression
- header/navigation and focus visibility preserved
- typecheck: PASS
- full tests: 66/66 PASS
- build/offline/assets/world budgets: PASS
- Terra: PASS
- `main` and deployment untouched

## Lane 2 — world/map touch targets

PR: #7 — `fix(stage06): harden world map touch targets`

Implementation/evidence head validated locally: `86c9fe441ceddba0f90d0bb19e1450b581a7fd0a`

Implementation:

- coarse-pointer HUD links and Map button: minimum 44px height
- coarse-pointer Close control: minimum 44×44px
- coarse-pointer map destination rows: minimum 44px height
- fine-pointer desktop sizing unchanged

Repository gates:

- ICM bootstrap/workflow/strict status: PASS
- focused world/topology/movement tests: 17/17 PASS
- full suite: 66/66 PASS
- typecheck: PASS
- offline verification: PASS
- production build: PASS
- asset budget: PASS, 89.2 KiB critical gzip
- world budget: PASS, 334.8 KiB JS gzip
- Ask disclosure guard: PASS
- world Ask boundary guard: PASS

Browser matrix with coarse pointer at 360, 390, 768, 1024, and 1440px:

- HUD links and Map button: 44px high
- Close: 44×44px
- map destination rows: 44px high
- no horizontal overflow or clipping
- zero application console errors or failed requests

Fine-pointer desktop measurements remained unchanged:

- Map: 48.7×32.59px
- Close: 32×32px
- destinations: 41.78px high

Keyboard/focus evidence:

- native semantics retained
- visible focus outlines retained
- Enter opens Map
- Escape closes Map
- focus returns to Map trigger

Independent review:

- Terra verdict: **PASS**
- no required fixes

Protected state:

- no dependency change
- no Ask/content/topology/controller change
- integration branch untouched
- `main` untouched
- no deployment
- Stage 07 not started

## Remaining Stage 06 work

- map overlay semantics and focus entry/return consistency
- remaining Stage 06 accessibility/reduced-motion/runtime/fallback review required by the active contract
- complete Stage 06 regression
- final Terra audit
- Stage 06 completion report and certification

Stage 07 remains blocked until Stage 06 is fully completed and certified.


## Lane 3 — map semantics and focus lifecycle

PR: #8 — `fix(stage06): align map semantics and focus lifecycle`

Validated implementation head: `95202d4155c5ac5b829cc4d0f3591def3d6de4d2`

Implementation:

- map panel exposes non-modal `role="dialog"` semantics with explicit accessible label
- opening Map focuses the native Close control
- Escape, explicit Close, and fast travel restore focus to the Map trigger
- initial closed render does not steal focus
- current-zone visible heading remains unchanged
- no focus trap and no `aria-modal`

Validation:

- targeted topology tests: 7/7 PASS
- full suite: 66/66 PASS
- ICM bootstrap/workflow/strict status: PASS
- typecheck: PASS
- offline verification: PASS
- production build: PASS
- asset and world budgets: PASS
- Ask disclosure and world Ask boundary guards: PASS
- browser focus lifecycle: PASS at 390px and desktop
- PR #7 touch-target sizing preserved
- no horizontal overflow

Independent review:

- Terra verdict: **PASS**
- no required fixes

Inherited follow-up discovered during browser validation:

- headless fast travel emits a React DOM `removeChild` exception
- reproduced unchanged on untouched Stage 06 root base `16ae381aa1bbf7f04da1873993dbf8378bc0be7d`
- PR #8 does not alter fast-travel, Canvas, controller, or topology code
- defect is therefore isolated to a separate bounded Stage 06 lane before final certification

Protected state remains intact: no CSS/touch-target, content, Ask, dependency, controller, topology, `main`, deployment, or Stage 07 changes.


## Lane 4 — headless fast-travel portal lifecycle

PR: #9 — `fix(stage06): isolate headless fast-travel removeChild exception`

Validated implementation head: `82476d6d8afef3e256e9fa4db05465811a27bf06`

Reproduced root cause:

- changing zones conditionally unmounted a Drei `Html` zone-label portal during the first lazy district load
- React DOM then attempted to remove a wrapper already detached by the portal lifecycle
- failure had previously been reproduced on untouched Stage 06 root before the PR #8 runtime change

Repair:

- non-Command-Center zone-label portals remain mounted across fast travel
- only the current-zone label is hidden using CSS `visibility`
- the existing world-zone guard now enforces the portal-lifecycle invariant
- fast-travel behavior, topology data, controller/movement semantics, map focus lifecycle, and lazy district loading remain unchanged

Validation:

- ICM bootstrap/workflow/strict status: PASS
- world-zone guard: PASS
- focused topology tests: 7/7 PASS
- full suite: 66/66 PASS
- typecheck: PASS
- production build: PASS
- critical asset budget: PASS, 89.2 KiB gzip
- world JS budget: PASS, 334.8 KiB gzip
- Ask disclosure/world boundary guards: PASS
- production-browser fast travel through Client Street, Build Lab, and Automation Lab: PASS
- browser runtime exceptions: zero
- failed browser requests: zero
- map focus restored to Map after each travel
- coarse-pointer controls remain 44px
- 390px viewport retains no horizontal overflow

Independent review:

- Terra verdict: **PASS**
- no required fixes

Protected state:

- PR #7 touch-target implementation unchanged
- PR #8 map dialog/focus implementation unchanged
- no controller or topology-data change
- no Ask/content/dependency change
- `main` and production untouched
- Stage 07 not started


## Lane 5 — Canvas route teardown investigation — blocked

PR: #11 — `fix(stage06): repair Canvas route teardown lifecycle`

Pickup head: `ecce3e529eee7c3d1fdb7b0e8e699cdbe9ac9163`

Reproduction:

- the Stage 06 `/play` SPA-exit `removeChild` failure reproduced on the exact pickup
- header Ask, Projects, Resume, world HUD Contact, and the previously evidenced Ask Terminal path remain affected
- destination routes still render and requests succeed
- failure remains isolated to Drei `Html` cleanup during full world Canvas teardown

Bounded attempts:

1. `WorldEntry` layout cleanup using public R3F `unmountComponentAtNode(canvas)`
2. the same cleanup wrapped with R3F `flushSync`

Result:

- both attempts retained the teardown failure
- both attempts were reverted
- no runtime candidate exists on this lane
- branch returned clean to the pickup implementation state
- Terra confirmed the two-attempt stop rule and returned BLOCKED / no promotable candidate

Next materially different approach:

- move Drei `Html` zone-label output to a dedicated persistent DOM host owned by `SiteShell`, outside the routed `Outlet`
- pass that persistent host to Drei through its public `Html portal` ref API
- preserve label projection/stacking, the PR #9 fast-travel portal-lifecycle invariant, SPA navigation, lazy districts, topology/controller behavior, map focus, and route isolation
- prove portal-host behavior before rerunning the five SPA-exit regression paths

Protected state:

- no failed repair retained
- no dependency change
- no `main` or production change
- Stage 06 remains active
- Stage 07 remains pending
