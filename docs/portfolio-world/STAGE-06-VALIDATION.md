# Stage 06 validation — cumulative evidence

Status: **IN PROGRESS**

Stage 06 remains active. This file records completed bounded lanes and does not certify Stage 06 as a whole.

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
