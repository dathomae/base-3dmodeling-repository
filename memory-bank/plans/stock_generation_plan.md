# Milling Stock Generation Plan

## Objective

1. **Create a stock-generation utility** in `src/stock/` that emits `.step` models of the four raw-stock pieces the menorah is milled from, so they can be 3D-printed at 100% infill and used to test the CAM milling programs.
2. **Extract the shared `INCH_MM` unit constant** into a common definitions module (currently duplicated in spirit across packages and defined inside `manora_parameters.py`), per the user's request to keep only package-specific definitions local.
3. **Reconcile the stale stock documentation** so the memory-bank spec matches the actual stock (0.05 in plate, 12×12-in diagonal halves, 1.5-in equator-connector bar, 12-in bar lengths).

This plan is intended to be turned into a story via the `add-new-story.pdd.script.md` script; the Story-Writer Guidance section at the end supplies the parameters and task decomposition that script's executor needs.

## Background

- `src/` is already organized into three packages — `src/manora/`, `src/jigs/`, and `src/stock/` — with package-qualified imports rooted at `src/` and a `sys.path` bootstrap in each entry-point script. `src/stock/` currently contains only an empty `__init__.py`.
- `INCH_MM = 25.4` is defined in `src/manora/manora_parameters.py` and imported from there by `src/manora/generate_manora.py`, `src/jigs/jig.py`, and `src/jigs/stabilization_block.py`. It is a unit-conversion constant, not menorah-specific, so it belongs in a shared module.
- The stock is 3D-printed (100% infill) as a stand-in for the aluminum stock: the CAM program is run against the plastic stock to verify toolpaths before cutting metal. The stock models must therefore be **exact nominal dimensions** — no FDM compensation, no clearance/tolerance (unlike the jigs).
- The user's FDM printer build volume is **325 × 325 × 350 mm**, which accommodates the largest stock piece (the 304.8 mm face-plate half-square and the 304.8 mm long bars).

## Stock specification (finalized with the user)

| Stock piece | Cross-section / shape | Length / thickness | mm equivalent | Model shape |
|---|---|---|---|---|
| Candle-holder bar | 3/4 in (0.75") square | 12 in | 19.05 × 19.05 × 304.8 | square bar (`Box`) |
| Apex-connector bar | 2 in square | 12 in | 50.8 × 50.8 × 304.8 | square bar (`Box`) |
| Equator-connector bar | 1.5 in square | 12 in | 38.1 × 38.1 × 304.8 | square bar (`Box`) |
| Face-plate stock | 12 × 12 in square **cut in half diagonally** (right isosceles triangle) | 0.05 in | legs 304.8 mm, thickness 1.27 mm | triangular prism (sketch + `extrude`) |

Notes:

- The diagonal cut of the 12×12 in square is a **separate operation before the mill**, so the mill stock is one half — a right-isosceles triangle with legs 12 in (304.8 mm) and a 0.05 in (1.27 mm) thickness. The full square is **not** generated.
- The equator connector is milled from **1.5 in** square bar (the code already uses `equatorial_connector_width = 1.5 * INCH_MM`); only the apex connector uses 2 in square bar. The design docs currently say "2 inch" for both — this plan fixes that.
- All dimensions are nominal; the `.step` files are natively in mm (build123d convention).

## Design decisions

### Common definitions module — `src/common.py`

- New module `src/common.py` holding the shared unit-conversion constant:

  ```python
  INCH_MM = 25.4
  ```

- `src/manora/manora_parameters.py` imports it (`from common import INCH_MM`) and keeps using it internally (e.g. `CANDLE_HOLE_DEPTH_MM = 0.6 * INCH_MM`), so the constant is no longer *defined* there. Re-exporting it keeps any legacy `from manora.manora_parameters import INCH_MM` import working (backward-compatible).
- The three entry-point scripts — `src/manora/generate_manora.py`, `src/jigs/jig.py`, `src/jigs/stabilization_block.py` — switch their `INCH_MM` import to `from common import INCH_MM` so the shared constant is imported from its source of truth. M2 hardware constants (`M2_TAP_SHANK_DIAMETER_MM`, etc.) stay in `manora_parameters.py` (they are menorah-specific).
- `src/common.py` is the natural future home for other cross-package constants; it starts with `INCH_MM` only.

### Stock parameters — `src/stock/stock_parameters.py`

Local to the stock package (per "keep specific definitions local"), holding only the stock dimensions, named with unit suffixes and converted from the inch nominal:

```python
from common import INCH_MM

CANDLE_HOLDER_BAR_SIDE_MM = 0.75 * INCH_MM      # 3/4 in square bar
APEX_CONNECTOR_BAR_SIDE_MM = 2.0 * INCH_MM      # 2 in square bar
EQUATOR_CONNECTOR_BAR_SIDE_MM = 1.5 * INCH_MM   # 1.5 in square bar
BAR_LENGTH_MM = 12.0 * INCH_MM                  # 12 in long bars
FACE_PLATE_SQUARE_SIDE_MM = 12.0 * INCH_MM      # 12 in square plate
FACE_PLATE_THICKNESS_MM = 0.05 * INCH_MM        # 0.05 in thick plate
```

### Stock generator — `src/stock/generate_stock.py`

Single CLI entry point (matching the `generate_manora.py` / `jig.py` convention: `-o`/`--outdir` default `manufacture`, `-s`/`--show`, `sys.path` bootstrap rooted at `src/`, `ocp_vscode` show guarded by try/except). Builders:

- `create_square_bar(side_mm, length_mm) -> Part` — a `Box(side_mm, side_mm, length_mm)` centered at the origin (length along Z).
- `create_candle_holder_stock()`, `create_apex_connector_stock()`, `create_equator_connector_stock()` — thin wrappers over `create_square_bar` with the package constants.
- `create_face_plate_stock() -> Part` — a right-isosceles triangle sketch in the XY plane with vertices `(0,0)`, `(FACE_PLATE_SQUARE_SIDE_MM, 0)`, `(0, FACE_PLATE_SQUARE_SIDE_MM)` (right angle at the origin, legs along +X/+Y), extruded +Z by `FACE_PLATE_THICKNESS_MM`.

Orientation is a plain, deterministic default (right-angle corner at the origin; bars centered); the user sets the WCS in the CAM profile, so no datum features are required.

### Output files and component names

| Component (for `-s`/`--show`) | File (in `manufacture/`) |
|---|---|
| `candle_holder` | `stock_candle_holder.step` |
| `apex_connector` | `stock_apex_connector.step` |
| `equator_connector` | `stock_equator_connector.step` |
| `face_plate` | `stock_face_plate.step` |

The `stock_` prefix distinguishes these raw-stock solids from the existing finished-part files (`regular_candle_holder.step`, `apex_connector.step`, `equator_connector.step`, `face_plate_*.step`) already in `manufacture/`.

## Impacted files

| File | Change |
|------|--------|
| `src/common.py` | **New** — shared `INCH_MM = 25.4`. |
| `src/manora/manora_parameters.py` | Replace the local `INCH_MM = 25.4` with `from common import INCH_MM`. |
| `src/manora/generate_manora.py` | Change the `INCH_MM` import to `from common import INCH_MM`. |
| `src/jigs/jig.py` | Change the `INCH_MM` import to `from common import INCH_MM` (keep the `M2_TAP_SHANK_DIAMETER_MM` import from `manora_parameters`). |
| `src/jigs/stabilization_block.py` | Change the `INCH_MM` import to `from common import INCH_MM`. |
| `src/stock/stock_parameters.py` | **New** — stock dimension constants (above). |
| `src/stock/generate_stock.py` | **New** — stock builders + CLI. |
| `tests/test_common.py` | **New** — pins `common.INCH_MM` and the manora re-export/derived constant. |
| `tests/test_stock_parameters.py` | **New** — pins the stock dimension constants (TDD). |
| `manufacture/stock_*.step` | **New** — the four generated stock solids. |
| `memory-bank/requirements.md` | Update Non-Functional Requirement #2 "Stock Material" (0.05 in plate, 12×12 diagonal halves, 2 in apex + 1.5 in equator bar, 12 in lengths). |
| `memory-bank/design/design.md` | Fix the face-plate thickness (0.1 → 0.05 in) and the equator-connector material (2 → 1.5 in square bar). |
| `memory-bank/brief.md` | Fix the stale overview stock figures (0.5 in holder bar → 0.75 in; 0.1 in plate → 0.05 in; 12×48 sheet → 12×12 diagonal halves). |
| `memory-bank/context.md` | Record this task at start; clear on completion (standard discipline). |

## Constraints

- **Exact nominal dimensions**: the stock models have no FDM hole compensation and no clearance/tolerance. They are geometric stand-ins for the aluminum stock.
- **No new dependency**: stdlib `unittest` only; build123d is already a project dependency.
- **Module purity**: `src/stock/stock_parameters.py` imports only `common` (no `build123d`, no `manora`); `src/common.py` has no imports. This mirrors the "pure Python, unit-testable" convention used by `face_plate_layouts.py`.
- **Refactor is behavior-preserving**: moving `INCH_MM` must not change any generated geometry; the existing 26-test suite is the regression gate.
- **CLI convention**: `-o`/`--outdir` (default `manufacture`), `-s`/`--show` with graceful "unknown component" error listing available names.
- **Documentation rule**: do not rewrite frozen historical records (`memory-bank/plans/*`, `memory-bank/stories/*`, and the "Recently Completed" history in `context.md`). Only live, current-state docs are updated.

## Steps

### Step 1: Extract `INCH_MM` into `src/common.py`

**Goal**: the shared unit constant lives in one place and every consumer imports it from there.

**Completion criteria**: `src/common.py` defines `INCH_MM`; `manora_parameters.py` no longer defines it; the entry-point scripts import it from `common`; the existing unit suite stays green.

- (a) Create `src/common.py` with `INCH_MM = 25.4` (with a short docstring noting it is the inch→mm conversion shared by all packages).
- (b) In `src/manora/manora_parameters.py`, replace `INCH_MM = 25.4` with `from common import INCH_MM` (keeps `manora_parameters.INCH_MM` resolvable for backward compatibility, and keeps `CANDLE_HOLE_DEPTH_MM = 0.6 * INCH_MM` working).
- (c) In `src/manora/generate_manora.py`, `src/jigs/jig.py`, and `src/jigs/stabilization_block.py`, change the `INCH_MM` import to `from common import INCH_MM`.
- (d) Add `tests/test_common.py` (stdlib `unittest`, `sys.path` bootstrap) asserting `common.INCH_MM == 25.4`, `manora.manora_parameters.INCH_MM == 25.4`, and `manora.manora_parameters.CANDLE_HOLE_DEPTH_MM == 0.6 * INCH_MM` (regression that the refactor did not disturb the manora constants).
- (e) Run `source venv/bin/activate && python -m unittest discover -s tests -v` — all green (existing 26 tests plus the new `test_common.py`).

### Step 2: Add `src/stock/stock_parameters.py` (TDD)

**Goal**: the stock dimension constants are pinned by unit tests.

**Completion criteria**: `tests/test_stock_parameters.py` is red first (module missing), then green after `stock_parameters.py` is implemented.

- (a) **Red** — write `tests/test_stock_parameters.py` asserting each constant equals its inch nominal × `INCH_MM`:
  - `CANDLE_HOLDER_BAR_SIDE_MM == 0.75 * INCH_MM`
  - `APEX_CONNECTOR_BAR_SIDE_MM == 2.0 * INCH_MM`
  - `EQUATOR_CONNECTOR_BAR_SIDE_MM == 1.5 * INCH_MM`
  - `BAR_LENGTH_MM == 12.0 * INCH_MM`
  - `FACE_PLATE_SQUARE_SIDE_MM == 12.0 * INCH_MM`
  - `FACE_PLATE_THICKNESS_MM == 0.05 * INCH_MM`
  - Run the suite — red (module does not exist yet).
- (b) **Green** — create `src/stock/stock_parameters.py` with the constants above (importing `INCH_MM` from `common`).
- (c) Run the suite — green.

### Step 3: Add `src/stock/generate_stock.py`

**Goal**: the CLI entry point builds and exports the four stock solids.

**Completion criteria**: `python src/stock/generate_stock.py -o <tmpdir>` produces four `.step` files; a bounding-box/volume check confirms each matches its nominal dimensions; `-s` names the components and errors gracefully on an unknown name.

- (a) Implement `create_square_bar(side_mm, length_mm)`, the three bar wrappers, and `create_face_plate_stock()` per the Design decisions (builders above).
- (b) Implement `main()` with `argparse` (`-o`/`--outdir` default `manufacture`, `-s`/`--show`), the `sys.path` bootstrap, the try/except `ocp_vscode` import, the component dict, and `export_step` for each of the four files.
- (c) Run-based gate: generate to a temp dir and load each `.step`; verify bounding-box sizes match `19.05 × 19.05 × 304.8`, `50.8 × 50.8 × 304.8`, `38.1 × 38.1 × 304.8`, and the face-plate triangle (legs 304.8 mm, thickness 1.27 mm), and that volumes equal the nominal products (`side² × length`, and `(304.8² / 2) × 1.27` for the triangle). Bars are centered at the origin; the triangle's right-angle corner is at the origin.
- (d) Verify `-s face_plate` and `-s bogus` behave like the existing scripts (show when `ocp_vscode` is available; graceful unknown-name error otherwise).

### Step 4: Regenerate the manufacture artifacts and verify

**Goal**: the persistent `manufacture/` stock solids exist and are correct.

**Completion criteria**: `manufacture/stock_*.step` are generated; bbox/volume checks pass; human visual sign-off recorded.

- (a) Run `source venv/bin/activate && python src/stock/generate_stock.py` (default `manufacture/`).
- (b) Confirm the four files exist and pass the bbox/volume gates from Step 3.
- (c) Human visual sign-off: inspect the four stock solids (a thin 304.8 mm right-triangle plate and three 304.8 mm bars) for correct shape and orientation.

### Step 5: Reconcile stock documentation

**Goal**: the memory-bank spec matches the actual stock.

**Completion criteria**: the three files below are updated; a grep for the stale markers (`0.1 inch`, `0.5 inch square`, `12 inch by 48 inch`, `2 inch square` on the equator connector) returns no hits in live docs.

- `memory-bank/requirements.md` — Non-Functional Requirement #2 "Stock Material": faces from **0.05 in** plate cut into **12×12 in squares, then halved diagonally** (one half per face); candle holders from **0.75 in square bar**; apex connectors from **2 in square bar**; equator connectors from **1.5 in square bar**; all bars **12 in long**. Optionally note the plastic stock is 3D-printed at 100% infill for CAM verification.
- `memory-bank/design/design.md` — face-plate "Thickness: 0.1 inches" → **0.05 inches**; equator-connector "Material: 2 inch square aluminum bar stock" → **1.5 inch**.
- `memory-bank/brief.md` — "Key Design Considerations" Material bullet: 0.5 in holder bar → **0.75 in**, 0.1 in plate → **0.05 in**, and the 12×48 sheet → **12×12 in squares halved diagonally**.
- `memory-bank/context.md` — record start/end of this work (standard discipline).

## Verification Checklist

- [ ] `src/common.py` exists with `INCH_MM = 25.4`; `manora_parameters.py` imports (not defines) it; the three entry-point scripts import it from `common`.
- [ ] `python -m unittest discover -s tests -v` passes — existing 26 tests plus `test_common.py` and `test_stock_parameters.py` green.
- [ ] `src/stock/stock_parameters.py` constants equal their inch nominals × `INCH_MM`.
- [ ] `python src/stock/generate_stock.py -o /tmp/stock` emits `stock_candle_holder.step`, `stock_apex_connector.step`, `stock_equator_connector.step`, `stock_face_plate.step`.
- [ ] Bounding-box/volume gates: bars 19.05/50.8/38.1 mm square × 304.8 mm long; face plate legs 304.8 mm, thickness 1.27 mm.
- [ ] `manufacture/stock_*.step` regenerated and match the same gates.
- [ ] `-s` shows a component (if `ocp_vscode` available) and `-s bogus` errors gracefully listing component names.
- [ ] Live docs (`requirements.md` NFR #2, `design.md`, `brief.md`) reflect 0.05 in plate / 12×12 diagonal halves / 1.5 in equator bar / 12 in bar lengths; no stale markers remain in live docs.
- [ ] Human visual sign-off recorded.

## Story-Writer Guidance (for `add-new-story.pdd.script.md`)

- **story_name** (recommended): `stock-generation-utility` (must match `^[a-zA-Z0-9_-]+$`).
- **description** (recommended, ≤ 200 chars): `Generate .step models of the milling stock (0.75in/1.5in/2in square bar and 12in half-square face plate) for 3D-print CAM testing, and extract INCH_MM into a shared common module.` (≈ 191 chars)
- **Dependencies**: None — the stock utility is independent of the candle-layout work (Story004); it only requires the already-merged `src/` package structure and build123d.
- **References** (relative to `memory-bank/`): this plan (`plans/stock_generation_plan.md`), `requirements.md`, `design/design.md`, `brief.md`.

### Recommended task decomposition

- **Task 1** (medium, code-for-story-implementor): **Extract `INCH_MM` into `src/common.py` and update imports.** Files: `src/common.py` (new), `src/manora/manora_parameters.py`, `src/manora/generate_manora.py`, `src/jigs/jig.py`, `src/jigs/stabilization_block.py`, `tests/test_common.py` (new). Behavior-preserving refactor; regression gate is the existing 26-test suite plus the new `test_common.py`. Not decomposed further — the five touched files are one coordinated mechanical rename/import change with no isolation benefit to splitting.
- **Task 2** (small, small-code-for-story-implementor): **Add `src/stock/stock_parameters.py` (TDD).** Files: `src/stock/stock_parameters.py` + `tests/test_stock_parameters.py`. Follows the Logical TDD Lifecycle (red → implement → green) as one unit. Depends on Task 1 (needs `common.INCH_MM`).
- **Task 3** (small, small-code-for-story-implementor): **Add `src/stock/generate_stock.py`.** Single new file with the builders + CLI. Depends on Task 2. Run-verified (bbox/volume gates; no unit-test target for the build123d geometry).
- **Task 4** (medium, run-only, code-for-story-implementor): **Regenerate `manufacture/stock_*.step` and verify.** Files: `manufacture/stock_*.step` (new artifacts). Regenerate to `manufacture/`, bbox/volume gates, human visual sign-off. Depends on Task 3.
- **Task 5** (tech-writer): **Reconcile stock documentation.** Files: `memory-bank/requirements.md`, `memory-bank/design/design.md`, `memory-bank/brief.md`, `memory-bank/context.md`. **Parallel group A with Task 4** (disjoint: `memory-bank/` vs `manufacture/`). Must not embed Task 4's measured bbox/volume figures (coordination guard — the stock spec is settled in this plan, not derived from the run).
- **Parallel group A: Tasks 4 and 5** — merge order any (fully disjoint file sets); integration tests after merge: full unit suite + `python src/stock/generate_stock.py -o /tmp/stock` bbox/volume gates; watch for conflicts in none expected (documentation vs generated artifacts).

## Open Questions

None — the spec is settled with the user:

- **Bar stock**: 12 in long for all three cross-sections (0.75 in, 1.5 in, 2 in).
- **Equator connector**: milled from 1.5 in square bar (2 in square is apex-only); the code already agrees, the docs are fixed here.
- **Face plate**: 0.05 in thick; stock piece is one diagonal half of a 12×12 in square (right-isosceles triangle, legs 304.8 mm, thickness 1.27 mm). The full square is not generated (cut off-mill).
- **Datum/orientation**: no special features; the user sets WCS in the CAM profile.
- **Common module**: `src/common.py` starts with `INCH_MM` only; package-specific constants stay local.
- **Exact dimensions**: no FDM compensation or clearance on the stock models.
