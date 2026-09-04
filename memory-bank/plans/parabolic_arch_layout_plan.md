# Parabolic Arch Candle Arrangement Plan

## Objective

1. **Replace the `downward_arc_layout` single semicircular arc with a single concave-down *parabolic arch*** on the 9-inch face, keeping all design constraints satisfied.
2. **Eliminate candle-holder intersections inside the assembled menorah** — specifically the bottom (foot) holders on adjacent faces, which currently overlap — and keep the bottom holders' screw holes clear of the equatorial-connector screw holes.
3. **Reconcile the memory-bank documentation** so it unambiguously reflects the 9-inch face and the new parabolic arch: remove the remaining 7-inch references, and fix the stale arc geometry that no longer matches the code.

This plan is intended to be turned into a story via the `add-new-story.pdd.script.md` script; the Story-Writer Guidance section at the end supplies the parameters and task decomposition that script's executor needs.

## Background

- Story003 (already merged) enlarged the face plates to **9-inch** equilateral triangles and rewrote `downward_arc_layout` from the 7-inch two-arc design to a **single concave-down circular arc**. The merged code is a **semicircle**: center `(0, 12.7)`, radius `59.7` mm, peak `(0, 72.4)`, ends at `(±59.7, 12.7)` on a 0.5-in bottom-edge inset, with holders rotated tangent to the arc.
- A design review found the semicircle's crown (`y = 72.4`, 36.6 % of the 197.97 mm face height) leaves an unnecessarily large **≈ 89 mm** gap to the shamash at `(0, 161.17)`. On the 9-inch face this is *not* forced: the shamash 2.5-in (63.5 mm) exclusion circle bottoms out at `y = 97.67`, so the crown can rise to ≈ 95–97 mm. A **parabolic arch** reclaims that space while staying "flowing" and non-linear.
- **New defect found during planning (holder–holder collision):** the bottom (foot) holders on *adjacent* faces intersect inside the die. Measured in the merged assembly: each foot holder overlaps the adjacent face's foot holder by **≈ 3375 mm³** (≈ 49 % of the 19.05 mm³ holder) in the current semicircle design — 8 such pairs total. Story003's assembled-die check verified holder↔connector only, not holder↔holder, so this went undetected. The same collision exists for a parabolic arch with the semicircle's feet `(±59.7, 12.7)` (≈ 3224 mm³ per pair).
- **Fix found:** the foot holders must sit further from the bottom *edge* (the edge shared by the two colliding faces). Empirically, the adjacent-face collision clears when the feet move up to `y ≈ 27–28` mm, and the equatorial-connector clearance still allows the feet to widen slightly (connector zero-clearance at `y = 28` is `x ≈ 65`, so `x = 63` leaves ~2–3 mm margin). This raises the feet from `(±59.7, 12.7)` to **`(±63, 28)`**, which in turn requires the crown at **`y = 95`** to keep the 8-candle spacing comfortable.
- **Screw-hole concern (verified safe):** the foot holder's four M2 screw holes stay **≈ 22.5 mm** from the nearest equatorial-connector M2 screw hole (countersink head Ø 4.5 mm), so there is no interference; this is still recorded as a verification gate.
- **Documentation debt to fix in the same plan**: several live docs still describe the superseded arc geometry — `candle-arrangement-arc.md` and `design.md` still cite the pre-merge circle (center `(0, 8.287)`, radius `59.713`, peak `(0, 68.0)`, spacing `26.23` mm, shamash `~95.5` mm) which does **not** match the merged semicircle code; `requirements.md` repeats the stale `26.23` mm figures; `concepts.md` and `resources/chanukah-halacha/candle_arrangement.md` still describe the face as "7-inch". These must be reconciled to the parabolic design.

## Design: the parabolic arch (9-inch face, collision-free)

### Face geometry (unchanged by this plan)

- Face: equilateral triangle, side **9 in (228.6 mm)**, height **197.97 mm**, half-base **114.3 mm**.
- Coordinates: base at `y = 0`, triangle point at `(0, 197.97)`; face symmetric about `x = 0`.
- Shamash (starter candle) center: `(0, 161.17)` mm (≈ height − 36.8; the 35 mm-from-tip rule plus the plate's bevel offset — unchanged).
- Holder block: 0.75 in / 19.05 mm cube (half-width `hw = 9.525` mm).

### The parabola

- **Feet (arc endpoints)**: `(±63.0, 28.0)` mm.
  - `y = 28` clears the adjacent-face foot-holder collision (threshold ≈ 27–28 mm, verified 0 overlap).
  - `x = 63` clears the equatorial connector with ~2–3 mm margin (empirical zero-clearance ≈ `x = 65` at `y = 28`), and keeps the holder fully inside the triangle with ≥ 12.7 mm edge inset.
- **Crown (peak)**: `(0, 95)` mm (top of the requested 90–95 range; 66.2 mm below the shamash).
- **Curve** (concave down, symmetric about `x = 0`):

  ```
  y(x) = 28 + 67 · (1 − (x / 63)²)          A = crown − 28 = 67 mm
  ```

- **Equivalent quadratic Bézier** (exact — a quadratic Bézier *is* a parabola), used for the embossed groove:

  ```
  P0 = ( 63.0, 28.0)     # bottom right (start)
  P1 = (  0.0, 162.0)    # control point = tangent intersection = 2·crown − 28
  P2 = (−63.0, 28.0)     # bottom left (end)
  ```

  Note: `P1` lies just above the shamash (`161.17`). That is correct — a quadratic Bézier's middle point is a *control point* (tangent intersection), not a point on the curve; the groove still peaks at `(0, 95)`.

### Candle positions (8 candles, equal arc length, hole 1 = bottom right)

Eight candles are placed **evenly by arc length** along the parabola, ordered from the bottom right up the right side, over the crown, and down the left side to the bottom left:

| Hole # | Position (mm) | Location |
|--------|---------------|----------|
| 1 | ( 63.000, 28.000) | bottom right (start) |
| 2 | ( 50.261, 52.356) | right side, up |
| 3 | ( 34.534, 74.867) | right side, up |
| 4 | ( 13.312, 92.008) | top right (just right of crown) |
| 5 | (−13.312, 92.008) | top left (just left of crown) |
| 6 | (−34.534, 74.867) | left side, down |
| 7 | (−50.261, 52.356) | left side, down |
| 8 | (−63.000, 28.000) | bottom left (end) |

Coordinates are rounded to 3 decimals; tests assert within `0.1` mm (existing convention). Face `n` uses `candle_positions(n) == list(DOWNWARD_ARC_PARABOLIC_9IN)[:n]` (continuous over-the-top traversal, same count rule as the current single-arc design).

### Holder rotation

Each holder keeps the "2 screw holes inboard / 2 outboard of the arc" property, but the arc is now a parabola so the tangent direction changes:

- `holder_rotation_angle(cx, cy)` returns the angle of the parabola's tangent vector in traversal direction (bottom-right → crown → bottom-left), aligning the holder's local +X with the tangent and its local +Y with the inboard normal (toward the base).

  ```
  angle(cx) = degrees( atan2( 2·A·cx / XFOOT , −XFOOT ) )      A = 67, XFOOT = 63
  ```

- End values: hole 1 ≈ **115.18°**, hole 8 ≈ **244.82°** (mirror sum 360°); holes 4/5 ≈ ±155.8°; the crown tangent (unoccupied) is 180°. The exact sign convention is pinned in TDD by the invariants — mirror symmetry (`angle(x) + angle(−x) = 360°`) and 2-inboard/2-outboard (reformulated against the parabola's inboard normal instead of a circle's radial vector).

### Embossed groove

- One continuous groove following the **same parabola** as the candles, drawn on every face regardless of candle count; shamash excluded; decorative (spacing rules do not apply).
- Path = the single quadratic Bézier `(P0, P1, P2)` above. The existing per-arc sweep in `src/main.py` is reused, but the curve primitive changes from `ThreePointArc` (circular) to `Bezier` (quadratic) — see Step 2. A single smooth Bézier has no C1 joints, so the multi-arc "shear at the joints" pitfall does not apply.

### Constraint verification (feet ±63/28, crown 95)

| Constraint | Requirement | This design |
|------------|-------------|-------------|
| Regular-candle spacing (min adjacent chord) | ≥ 25.4 mm | **26.62 mm** (arc-top pair, holes 4–5; side gaps ≈ 27.3–27.5 mm) |
| Shamash-to-nearest candle | ≥ 44.45 mm (1.75 in, relaxed; also ≥ 63.5 mm / 2.5 in) | **70.43 mm** (holes 4/5 at `(±13.312, 92.008)`) |
| Shamash visibility (arc-top pair) | ≥ 12.7 mm between innermost tops | **26.62 mm** |
| Equatorial-connector clearance | start holder clear of connector | **0 overlap**; feet `(±63, 28)`, ≈ 2–3 mm margin (empirical) |
| **Adjacent-face holder non-intersection** | **0 overlap between holders on faces sharing a bottom edge** | **0 overlap across all 36 mounted holders** (empirical, all pairs) |
| **Screw-hole clearance (holder vs connector)** | bottom holder M2 holes clear of equatorial-connector M2 holes | **≈ 22.5 mm** min center-to-center (countersink Ø 4.5 mm) |
| Holder fit | all 4 corners inside the 9-in triangle | pass |
| Edge inset | candle centers ≥ 0.5 in (12.7 mm) from every edge | pass (feet at 28 mm bottom inset) |

## Impacted files

| File | Change |
|------|--------|
| `src/face_plate_layouts.py` | Replace `DOWNWARD_ARC_9IN` with the ordered parabolic `DOWNWARD_ARC_PARABOLIC_9IN` tuple (feet ±63/28, crown 95); replace `DOWNWARD_ARC_CENTER` usage in `holder_rotation_angle` with the parabola-tangent formula (A=67, XFOOT=63); change `groove_arcs` to return the single quadratic-Bézier control-point triple `(P0, P1, P2)`; update docstrings/comments. `CircularLayout` untouched. |
| `tests/test_downward_arc_layout.py` | Rewrite (TDD): parabolic positions, count rule, min spacing ≥ 25.35, shamash ≥ 44.4, edge inset, groove Bézier triple, holder rotation (tangent alignment, mirror symmetry, 2/2 split vs the parabola normal). |
| `src/main.py` | Groove sweep only: `ThreePointArc(...)` → `Bezier(...)` for the groove path (the holder-rotation call is already generic). No other change. |
| `manufacture/*.step`, `manufacture/face_plate_baseline.md` | Regenerate both layouts + assembly; record the parabolic-arc baseline (keep the 9-in circular record for the circular layout). |
| `memory-bank/design/candle-arrangement-arc.md` | Rewrite to the parabolic spec (coordinates, Bézier groove, count rule, constraint table incl. holder non-intersection, 9-in geometry); keep the 7-in two-arc note only as superseded history. |
| `memory-bank/design/design.md` | Update the Candle Arrangement table row and the Face Plate paragraph (parabola, not circle; fix 26.23 → 26.62 and 95.5 → 70.4). |
| `memory-bank/requirements.md` | FR #4 wording ("parabolic arch"); Constraint #3 spacing figure (26.62 mm) and Constraint #4 arc-top figure (26.62 mm); add a note that the foot holders must not intersect across adjacent faces. |
| `memory-bank/concepts.md` | "Candle Spacing vs. Face Capacity" — change "fixed 7-inch" to 9-inch and update the 8-candle pattern to the single parabolic arch. |
| `resources/chanukah-halacha/candle_arrangement.md` | "Feasibility note (fixed 7-inch faces)" → 9-inch faces. |
| `memory-bank/context.md` | Record this task at start and clear on completion (standard task discipline). |
| `memory-bank/arrangement_approach.md` | Optional: add a "parabolic arch (9-in, collision-free)" worked example; leave the existing 7-in examples as method history. |

## Constraints

- **Minimal/additive**: the die architecture (octahedron, connectors fixed at 1.5-in/2.0-in, holders 0.75-in, taper) is unchanged. Only the `downward_arc_layout` geometry changes. `CircularLayout` is untouched. Do not touch `src/manora_parameters.py`.
- **Feet and connector clearance**: start points at `(±63, 28)`; the assembled-die holder↔connector collision check **must be re-run** (feet widened from ±59.7 to ±63 and raised to y=28).
- **Adjacent-face holder non-intersection (new)**: the bottom (foot) holders must not intersect holders on the adjacent face sharing the bottom edge. Verified by an all-pairs holder↔holder intersection check over the 36 mounted holders (0 overlap).
- **Screw-hole clearance (new)**: each bottom holder's four M2 screw holes must stay ≥ 4.5 mm center-to-center from every equatorial-connector M2 screw hole (countersink head Ø 4.5 mm); design gives ≈ 22.5 mm.
- **Spacing**: adjacent regular-candle centers ≥ 25.4 mm for every candle count (assert ≥ 25.35 with the 0.05 tolerance convention).
- **Shamash**: minimum 44.45 mm center-to-center from the shamash (design gives ≈ 70.4 mm, also ≥ 63.5 mm).
- **Module purity**: `src/face_plate_layouts.py` stays `math` + `manora_parameters` only (no `build123d`).
- **Groove geometry**: single continuous 1/8 in (3.175 mm) × 1 mm groove on the outside face following the parabola; on every face; shamash never crossed.
- **No new dependency**: stdlib `unittest` only.
- **Documentation rule**: do **not** rewrite frozen historical records (`memory-bank/plans/downward_arc_layout_plan.md`, `memory-bank/plans/adjust_size_and_arc_plan.md`, `memory-bank/stories/Story00*`, and the "Recently Completed" history in `context.md`). Only live, current-state docs are updated.

## Steps

### Step 1: Rewrite `downward_arc_layout` to the parabolic arch (TDD)

**Goal**: the layout returns the parabolic 8-candle positions, the parabola-tangent holder rotation, and the Bézier groove path; unit tests pin the geometry.

**Completion criteria**: the rewritten `tests/test_downward_arc_layout.py` is red first, then green after the implementation.

- (a) **Structural definition / red tests first** — rewrite `tests/test_downward_arc_layout.py` (using `9.0 * INCH_MM` face height, stdlib `unittest`) to assert:
  - `candle_positions(8)` equals the eight parabolic coordinates above (delta 0.1).
  - Count rule: `candle_positions(n) == list(DOWNWARD_ARC_PARABOLIC_9IN)[:n]`; `candle_positions(1) == [(63.000, 28.000)]`; `candle_positions(4)[-1] == (13.312, 92.008)`; `candle_positions(5)[-1] == (−13.312, 92.008)`.
  - Min pairwise spacing ≥ 25.35 for `n` 2–8.
  - Shamash distance ≥ 44.4 for `n = 8` (shamash center `(0, 161.17)`).
  - Edge inset: every center ≥ 0.5 in from every edge (keep the existing `test_edge_inset_half_inch`).
  - `groove_arcs(n)` returns `[(P0, P1, P2)]` — the single quadratic-Bézier control-point triple `((63.0, 28.0), (0.0, 162.0), (−63.0, 28.0))` — for every `n`; `CircularLayout.groove_arcs(8) == []`.
  - Holder rotation: tangent alignment at the ends (hole 1 ≈ 115.18°, hole 8 ≈ 244.82°), mirror symmetry (`angle[i] + angle[7−i] == 360°`), and the 2-inboard/2-outboard split **reformulated against the parabola's inboard normal** at each candle (no circle center).
  - Run `source venv/bin/activate && python -m unittest discover -s tests -v` — red (the layout still returns the semicircle).
- (b) **Implement** — in `src/face_plate_layouts.py`:
  - Replace `DOWNWARD_ARC_9IN` with the ordered `DOWNWARD_ARC_PARABOLIC_9IN` tuple (hole 1 = bottom right).
  - Update `holder_rotation_angle` to the parabola-tangent formula with `A = 67`, `XFOOT = 63` (drop the `DOWNWARD_ARC_CENTER` radial approach).
  - Update `groove_arcs` to return `[((63.0, 28.0), (0.0, 162.0), (−63.0, 28.0))]`.
  - Update module docstrings/comments to the parabola (feet ±63/28, crown 95, Bézier control point `(0, 162)`).
- (c) Run the suite — green.

### Step 2: Draw the groove as a Bézier in `src/main.py`

**Goal**: the embossed groove follows the parabola, not a circle.

**Completion criteria**: `src/main.py` generates the `downward_arc_layout` plates with a single smooth parabolic groove (programmatic gates below), and `circular` output is unchanged (no grooves).

- In `create_face_plate`, change the groove curve primitive from `ThreePointArc(...)` to `Bezier(...)` for the three groove points, and update the surrounding comment (a single quadratic Bézier is the exact parabola; no C1 joints, so the per-arc `is_frenet=True` sweep still produces one clean uniform groove). The holder-rotation call (`layout.holder_rotation_angle`) is already generic — no change.
- Programmatic gate: every `downward_arc_layout` plate is valid, and each plate is strictly lighter than the same-number `circular` plate (groove removes material); the groove prism z-range remains `[plate_thickness − 1.0, plate_thickness]`.
- Run `source venv/bin/activate && python src/main.py --layout downward_arc_layout -o /tmp/parab_arc` and `python src/main.py --layout circular -o /tmp/parab_circular` — both complete; `circular` bbox/volume unchanged from the Story003 9-in baseline.

### Step 3: Regenerate and verify geometry (run-only)

**Goal**: regenerate the manufacture artifacts and confirm the parabolic arch satisfies all constraints in the assembled die — including the two new ones (holder↔holder non-intersection and screw-hole clearance).

**Completion criteria**: STEP files regenerated; holder↔holder, holder↔connector, and screw-hole checks pass; unit suite green; human visual sign-off surfaced to the user.

- Regenerate `manufacture/` for both layouts (`--layout circular`, `--layout downward_arc_layout`) and the assembly.
- **Holder↔holder collision check (critical, new):** build all 36 holders (faces carry 1–8 candles: 1+2+…+8 = 36) in assembly positions and pairwise-intersect them; require **0 overlap** across every pair (not just adjacent-face feet). This is the gate that catches the pre-existing defect this plan fixes.
- **Holder↔connector collision check (critical):** confirm no candle-holder solid intersects any connector solid, for both layouts (feet widened to ±63 and raised to y=28; reuse the Story003 empirical method).
- **Screw-hole clearance check (new):** for each bottom holder, confirm its four M2 screw-hole centers are ≥ 4.5 mm from every equatorial-connector M2 screw-hole center (design gives ≈ 22.5 mm).
- Update `manufacture/face_plate_baseline.md`: keep the existing 9-in circular record; add a "9-in parabolic-arc" record for the `downward_arc_layout` plates (bbox/volume).
- `python src/main.py --layout bogus` still names both layouts; full unit suite green.
- **Human visual sign-off gate**: inspect `face_plate_8` and `face_plate_2` (arc layout) and the assembly — a single continuous concave-down parabolic groove from bottom right over the crown (y ≈ 95) to bottom left, shamash clear, no holder/holder or holder/connector overlap. This is where the crown height (90/95) and foot position are finalized with the user.

### Step 4: Reconcile memory-bank documentation

**Goal**: the live docs unambiguously describe the 9-inch face, the parabolic arch, and the holder non-intersection constraint, with no 7-inch or stale-arc confusion.

**Completion criteria**: the files below are updated; a `grep` for stale markers (`7-inch`, `7-in`, `8.287`, `59.713`, `26.23`, `95.5`, `peak (0, 68.0)`) returns no hits in live docs (historical plans/stories/context-history are expected and left intact).

- `memory-bank/design/candle-arrangement-arc.md` — rewrite to the parabolic spec (coordinates table, Bézier groove, count rule, constraint table incl. holder non-intersection, 9-in face geometry); retain the 7-in two-arc note only as a superseded-history note.
- `memory-bank/design/design.md` — update the Candle Arrangement pointer table row and the Face Plate paragraph ("parabolic arch", crown `(0, 95)`, spacing 26.62 mm, shamash ≈ 70.4 mm).
- `memory-bank/requirements.md` — FR #4 ("single concave-down parabolic arch"); Constraint #3 (26.62 mm) and Constraint #4 (26.62 mm arc-top pair); note the adjacent-face holder non-intersection requirement.
- `memory-bank/concepts.md` — "Candle Spacing vs. Face Capacity": 9-inch face, single parabolic arch holds 8.
- `resources/chanukah-halacha/candle_arrangement.md` — feasibility note → 9-inch faces.
- `memory-bank/context.md` — record start/end of this work.
- Optional: add a "parabolic arch (9-in, collision-free)" worked example to `memory-bank/arrangement_approach.md` (leave 7-in examples as history).

## Verification Checklist

- [ ] `tests/test_downward_arc_layout.py` rewritten; `python -m unittest discover -s tests -v` passes.
- [ ] `src/face_plate_layouts.py` contains the ordered `DOWNWARD_ARC_PARABOLIC_9IN` tuple (hole 1 = bottom right, feet ±63/28), the parabola-tangent `holder_rotation_angle` (A=67, XFOOT=63), and `groove_arcs(n)` returning `[((63.0, 28.0), (0.0, 162.0), (−63.0, 28.0))]`; module still imports no `build123d`.
- [ ] `src/main.py` draws the groove with `Bezier` (not `ThreePointArc`); `circular` output unchanged.
- [ ] Every `downward_arc_layout` plate valid and strictly lighter than its `circular` counterpart; groove prism z-range `[0.27, 1.27]`.
- [ ] Regenerated `manufacture/*.step` + assembly.
- [ ] **Holder↔holder intersection check: 0 overlap across all 36 mounted holders.**
- [ ] **Holder↔connector intersection check: 0 overlap for both layouts.**
- [ ] **Screw-hole clearance check: every bottom holder's M2 holes ≥ 4.5 mm from every equatorial-connector M2 hole.**
- [ ] `manufacture/face_plate_baseline.md` has the 9-in parabolic-arc record.
- [ ] `python src/main.py --layout bogus` names both layouts.
- [ ] Live docs (`candle-arrangement-arc.md`, `design.md`, `requirements.md`, `concepts.md`, `resources/chanukah-halacha/candle_arrangement.md`) describe the 9-in parabolic arch; no stale `7-inch`/`8.287`/`59.713`/`26.23`/`95.5` markers remain in live docs.
- [ ] Human visual sign-off recorded (crown height and foot position finalized).

## Story-Writer Guidance (for `add-new-story.pdd.script.md`)

- **story_name** (recommended): `parabolic-arch-layout` (must match `^[a-zA-Z0-9_-]+$`).
- **description** (recommended, ≤ 200 chars): `Replace the downward_arc_layout semicircular arc with a collision-free concave-down parabolic arch (feet ±63/28, crown y=95) on the 9-in face and reconcile the 7-in/stale-arc docs.` (~184 chars)
- **Dependencies**: Story003 (9-in face + single-arc `downward_arc_layout`, holder rotation, groove sweep).
- **References** (relative to `memory-bank/`): this plan (`plans/parabolic_arch_layout_plan.md`), `design/candle-arrangement-arc.md`, `design/design.md`, `requirements.md`, `concepts.md`, `arrangement_approach.md`.

### Recommended task decomposition

- **Task 1** (medium, code-for-story-implementor): **Rewrite `downward_arc_layout` to the parabolic arch (TDD).** Files: `src/face_plate_layouts.py` + `tests/test_downward_arc_layout.py`. Follows the Logical TDD Lifecycle (red → implement → green) as one cohesive unit.
- **Task 2** (small): **Draw the groove with `Bezier` in `src/main.py`.** Single-file, additive-curve change. Sequential after Task 1 (Task 1 changes the groove tuple semantics). Run-verified (no unit-test target for build123d sweep).
- **Task 3** (medium, run-only): **Regenerate + verify geometry.** Files: `manufacture/*.step`, `manufacture/face_plate_baseline.md`. Regenerate; holder↔holder (all-pairs), holder↔connector, and screw-hole clearance checks; yield check; unit suite; human visual sign-off (final crown/foot decision by the user). Depends on Tasks 1–2.
- **Task 4** (tech-writer): **Reconcile documentation.** Files: `memory-bank/design/candle-arrangement-arc.md`, `design.md`, `requirements.md`, `concepts.md`, `resources/chanukah-halacha/candle_arrangement.md`, `context.md` (optional `arrangement_approach.md`). **Parallel group A with Task 3** (disjoint: `manufacture/` vs `memory-bank/` + `resources/`). Must not embed Task 3's measured bbox/volume figures (coordination guard).
- **Parallel group A: Tasks 3 and 4** — merge order any; integration tests after merge: full unit suite + both-layout generation + the three assembly checks (holder↔holder, holder↔connector, screw-hole); watch for `manufacture/*.step` nondeterministic diffs (discard spurious) and `memory-bank/context.md`.

## Open Questions

None — the design is settled:
- **Feet**: pinned at `(±63.0, 28.0)` mm (clears adjacent-face holders and the equatorial connector, ~2–3 mm connector margin).
- **Crown**: pinned at `y = 95` mm (90 and 92 also feasible; finalized by the user at the Step 3 / Task 3 visual sign-off).
- **Groove curve**: single quadratic Bézier `(P0, P1, P2)` drawn with `Bezier` in `main.py`.
- **Holder rotation**: parabola tangent; invariants (mirror symmetry, 2-inboard/2-outboard) preserved.
- **New constraints**: adjacent-face holder non-intersection (0 overlap) and bottom-holder screw-hole clearance (≥ 4.5 mm) are explicit design and verification requirements.
- **Doc cleanup scope**: live docs only; historical plans/stories/context-history left intact.
