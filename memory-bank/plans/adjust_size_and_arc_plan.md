# Adjust Face Size to 9 Inches and Revise Downward Arc Layout Plan

## Objective

1. **Increase the face-plate triangle side from 7 in (177.8 mm) to 9 in (228.6 mm)** for **all** layouts (the shared plate builder, connectors, assembly, shamash, and connector-hole positions already derive from `triangle_side`, so this is one constant change; the `circular` layout's candle coordinates are **unchanged** — it is slated for later removal — and only `downward_arc_layout` gets new coordinates).
2. **Revise `downward_arc_layout`** to the single **concave-down circular arc** design agreed in the 9-in feasibility discussion: all 8 regular candles sit on one smooth arch from the lower-right to the lower-left of the face, and the embossed groove follows the same curve.

This plan is intended to be turned into a story via the `add-new-story.pdd.script.md` script; the Story-Writer Guidance section at the end supplies the parameters and task decomposition that script's executor needs.

## Background

- The current `downward_arc_layout` (Story002) uses **two** symmetric circular arcs (R1–R4 right, L1–L4 left) joined by a tangent bridge, carrying 8 candles on the 7-in face.
- A design review found two problems with the current state:
  1. **Aesthetic**: the user wants a *single* smooth concave-down arc from the lower-right to the lower-left, not two arcs + a bridge.
  2. **Defect**: on the current 7-in face, the start candle holders at (±56.862, 9.525) **collide with the equatorial connectors** in the assembled die (measured ~3532 mm³ intersection each; the documented "3 mm clearance" constraint `33x + 19.05y ≤ 2057.9` was derived against a connector footprint smaller than the real 1.5-in pyramid).
- Feasibility analysis (empirical, using the real connector geometry):
  - On the **7-in** face, a single concave-down arc cannot hold 8 candles at 25.4 mm spacing (the connector clearance caps a single arc at ~146 mm length ≈ 6 candles).
  - On the **9-in** face, a single concave-down arc **is feasible**: the connector footprint is fixed-size and sits at the (further-out) vertex, so the arc can bulge to a higher peak (≈66–68 mm) while the intermediate holders stay clear. Relaxing the shamash distance is unnecessary — the nearest candle is ~95 mm from the shamash on the 9-in face.
- The 9-in empirical connector-collision-free limit for a start holder at y = 9.525 is **x = ±60.7 mm** (zero clearance). A start at **±59.7 mm** leaves ~1 mm clearance margin and is the recommended design point.

## Design: the revised `downward_arc_layout` (single arc, 9-in face)

### Face geometry (9 in)

- side `S = 9.0 * INCH_MM = 228.6 mm`; height `H = S * √3/2 = 197.97 mm`; half-base `= 114.3 mm`.
- Shamash (starter candle) at `(0, H − 36.8) = (0, ~161.18)` — unchanged 35 mm-from-tip rule, auto-derived from `triangle_height` in `main.py`.

### The arc

- **Single circular arc, concave down (∩)**: circle center `(0, 8.287)`, radius `59.713 mm`, peak `(0, 68.0)`.
- **8 candle positions, ordered per the user's count rule** (hole 1 = bottom right; up the right side to the top; then down the left side to the bottom left):

| Hole # | Position (mm) | Arc location |
|--------|---------------|--------------|
| 1 | (59.700, 9.525) | bottom right (start) |
| 2 | (53.410, 34.989) | right side, up |
| 3 | (36.814, 55.301) | right side, up |
| 4 | (13.115, 66.542) | top right (just right of peak) |
| 5 | (−13.115, 66.542) | top left (just left of peak) |
| 6 | (−36.814, 55.301) | left side, down |
| 7 | (−53.410, 34.989) | left side, down |
| 8 | (−59.700, 9.525) | bottom left (end) |

- **Count rule**: `candle_positions(n) == DOWNWARD_ARC_9IN[:n]` for n = 1–8, where `DOWNWARD_ARC_9IN` is the ordered list above. This is *different* from the old two-arc rule ("right arc bottom→top then left arc bottom→top", which put the 5th candle at the bottom left); the new rule is a continuous over-the-top traversal.
- **Groove**: `groove_arcs(n)` returns **one** three-point arc definition — `((59.700, 9.525), (0.0, 68.0), (−59.700, 9.525))` — which lies on the same circle as the candles (any three of the eight points define it). The existing per-arc groove sweep in `main.py` handles a single-arc list unchanged (one `BuildLine` + one sweep). Drawn on every face regardless of count; shamash excluded.

### Constraint satisfaction (verified numerically)

| Constraint | Requirement | This design |
|------------|-------------|-------------|
| Regular-candle spacing | ≥ 25.4 mm adjacent | **26.23 mm** (equal arc-length; chord) for every prefix n |
| Shamash-to-nearest candle | ≥ 44.45 mm (1.75 in, relaxed) | **~95.5 mm** (also ≥ 63.5 mm / 2.5 in) |
| Shamash visibility (arc-top pair) | ≥ 12.7 mm between innermost tops | **26.23 mm** |
| Equatorial-connector clearance | start holder clear of connector | ~1 mm margin at x = ±59.7 (empirical zero-clearance limit 60.7) |
| Holder fit | all 4 corners inside the 9-in triangle | pass |

## Design: the `circular` layout on the 9-in face

**Unchanged (user decision).** The circular layout's candle positions are absolute constants (radius 28.0 mm, center y 40.5 mm) and are **not** adjusted in this story. The layout is already known not to satisfy the menorah candle-spacing rules (its 7- and 8-candle faces fall below the 1.0-in minimum even on the 7-in face), and the user intends to remove it in a later story. The 9-in face growth applies to the shared plate geometry only; the circular candles keep their current positions (clustered low in the bigger face) until the layout is removed. No circular code or test changes are made.

## Impacted files

| File | Change |
|------|--------|
| `src/main.py` | `triangle_side = 7.0 * INCH_MM` → `9.0 * INCH_MM` (line ~25). Everything else (height, shamash, connector holes, assembly, exports) derives from it. |
| `src/face_plate_layouts.py` | `DownwardArcLayout` rewritten to the single arc (replace `DOWNWARD_ARC_RIGHT` with the ordered `DOWNWARD_ARC_9IN` list; new count rule; `groove_arcs` returns one arc). `CircularLayout` untouched (slated for later removal). |
| `tests/test_face_plate_layouts.py` | No change expected (circular layout unchanged; its tests construct the layout with a passed-in `triangle_height`). |
| `tests/test_downward_arc_layout.py` | Full rewrite (TDD): new positions, new count rule, single-arc groove; use the 9-in face-height constant. |
| `manufacture/face_plate_baseline.md` | Regenerate/update the circular bbox/volume baseline for the 9-in geometry. |
| `manufacture/*.step` | Regenerate all plates (both layouts), connectors, holders, assembly. |
| `memory-bank/design/candle-arrangement-arc.md` | Rewrite to the single-arc spec (coordinates, count rule, groove). |
| `memory-bank/design/candle-arrangement-circular.md` | No change (layout unchanged); optionally note its 9-in status / removal intent. |
| `memory-bank/design/design.md` | Update the Candle Arrangement pointer table (arc = single concave-down arc on 9-in faces). |
| `memory-bank/requirements.md` | FR #4 wording (layouts), "standard face" 7 in → 9 in, Constraint #3/#4 notes, material-yield check. |
| `memory-bank/context.md` | Task record start/end. |
| `memory-bank/arrangement_approach.md` | Optional: add the 9-in single-arc worked example. |

## Constraints (updated for the 9-in face)

- **Additive/minimal**: the die architecture (octahedron, connectors fixed at 1.5-in/2.0-in, holders 0.75-in, taper) is unchanged; only `triangle_side` and the `downward_arc_layout` coordinates change. The `circular` layout is untouched. Do not touch `src/manora_parameters.py`.
- **Spacing**: adjacent regular-candle centers ≥ 25.4 mm (assert ≥ 25.35 with the 0.05 tolerance convention) for every candle count.
- **Shamash**: minimum 44.45 mm center-to-center from the shamash; the new design gives ~95.5 mm.
- **Connector clearance**: start holders must clear the equatorial connectors (empirical check, not the old simplified footprint constraint). The new start at ±59.7 mm satisfies this with ~1 mm margin; **the verification task MUST re-run the assembled-die collision check** (holder ↔ connector intersections) for both layouts.
- **Holder fit**: all four 19.05-mm-square holder corners inside the 9-in triangle.
- **Material yield**: the 8 faces (9-in equilateral, 7.79-in tall) must fit the 12 in × 48 in sheet — 8 triangles nest in a zigzag strip of ≈ 36–40.5 in × 7.8 in, which fits; verify in Task 3.
- **No new dependency**: stdlib `unittest` only.
- **Module purity**: `src/face_plate_layouts.py` stays `math` + `manora_parameters` only (no `build123d`).
- **Embossed groove**: single continuous 1/8 in × 1 mm groove on the outside face following the candle arc; on every face; shamash never crossed.

## Steps

### Step 1: Change the face size to 9 in

- `src/main.py`: `triangle_side = 9.0 * INCH_MM`.
- Confirm the module still generates for both layouts: `python src/main.py --layout circular -o /tmp/plan_9in_circular` and `python src/main.py --layout downward_arc_layout -o /tmp/plan_9in_arc` — plates export with the 9-in bounding box (x −114.3…114.3, y 0…197.97, z 0…1.27), and the assembly completes. The `circular` candle positions are unchanged (absolute constants); `downward_arc_layout` keeps its current 7-in coordinates only until Step 2 rewrites them.

### Step 2: Revise `downward_arc_layout` to the single arc (TDD)

- `tests/test_downward_arc_layout.py` rewrite first (red step): assert the ordered 8 positions (delta 0.1), the first-n count rule (`candle_positions(n) == full[:n]`, with `candle_positions(1) == [(59.700, 9.525)]` and `candle_positions(5)[-1] == (−13.115, 66.542)`), minimum pairwise spacing ≥ 25.35 for n ≥ 2, shamash distance ≥ 44.4 for n = 8, `groove_arcs(n)` equals the single `((59.700, 9.525), (0.0, 68.0), (−59.700, 9.525))` arc for every n, and `CircularLayout.groove_arcs(8) == []`.
- `src/face_plate_layouts.py`: replace `DOWNWARD_ARC_RIGHT` with the ordered `DOWNWARD_ARC_9IN` tuple; `candle_positions(n)` returns `list(DOWNWARD_ARC_9IN)[:n]`; `groove_arcs(n)` returns `[((59.700, 9.525), (0.0, 68.0), (−59.700, 9.525))]`; keep the `__init__` storing `triangle_height` unused (docstring: single-arc geometry is fixed for the 9-in face, connector clearance is not proportional to height). Update the `"downward_arc_layout"` registry (name unchanged).
- Run the full suite — green. Run `python src/main.py --layout downward_arc_layout -o /tmp/plan_9in_arc` and confirm the plates export and groove progress prints appear (per-face groove sweep with the single arc).

### Step 3: Verify generated geometry (run-only)

- Regenerate `manufacture/` for both layouts (`--layout circular`, `--layout downward_arc_layout`) and the assembly.
- Update `manufacture/face_plate_baseline.md` with the 9-in circular bbox/volume table (name the record "9-in post-resize baseline"; keep the old 7-in record as a historical section).
- **Assembled-die collision check** (critical): for each layout, verify no candle-holder solid intersects any connector solid (reuse the empirical method from this plan's analysis — build the connectors in assembly positions, place the holders via the plate locations, intersect). Both layouts must pass (circular is expected clear; the arc start at ±59.7 must be clear).
- Verify the 8 × 9-in faces fit the 12 × 48 in sheet (yield check).
- `python src/main.py --layout bogus` still names both layouts.
- Full unit suite green.
- **Human visual sign-off gate** (story-implementor surfaces to the user): inspect `face_plate_8`/`face_plate_2` and the assembly — single continuous concave-down groove from bottom right over the top to bottom left, on the outside face, shamash clear. The user will perform the final qualification on the visible result.

### Step 4: Update memory-bank documentation

- `memory-bank/design/candle-arrangement-arc.md`: rewrite to the single-arc spec (coordinates table, count rule, single groove arc, 9-in face geometry).
- `memory-bank/design/candle-arrangement-circular.md`: no change; optionally note its 9-in status / removal intent.
- `memory-bank/design/design.md`: Candle Arrangement pointer table — arc is a single concave-down circular arc on 9-in faces.
- `memory-bank/requirements.md`: FR #4 layout list; "standard face" → 9 in; adjust Constraint #3/#4 wording (single-arc visibility note); note the 9-in material-yield result.
- `memory-bank/context.md`: record start/end.
- Optional: add the 9-in single-arc worked example to `memory-bank/arrangement_approach.md`.

## Story-Writer Guidance (for `add-new-story.pdd.script.md`)

- **story_name** (recommended): `nine-inch-face-single-arc` (must match `^[a-zA-Z0-9_-]+$`).
- **description** (recommended, ≤ 200 chars): `Enlarge the face plates to 9-inch equilateral triangles for all layouts and revise the downward_arc_layout to a single concave-down circular arc carrying all 8 candles.` (~165 chars)
- **Dependencies**: Story002 (implemented the pluggable layout infra + current two-arc `downward_arc_layout` and the groove sweep that this story revises).
- **References** (relative to `memory-bank/`): this plan (`plans/adjust_size_and_arc_plan.md`), `design/candle-arrangement-arc.md`, `design/candle-arrangement-circular.md`, `design/design.md`, `requirements.md`, `arrangement_approach.md` (feasibility method + worked example).

### Recommended task decomposition

- **Task 1** `[Small]`: **9-in face size.** Files: `src/main.py` (`triangle_side = 9.0 * INCH_MM`) only; smoke-verify both layouts still generate on the 9-in plate (no layout or test changes — the circular layout is untouched, and the arc layout coordinates are rewritten in Task 2).
- **Task 2** (medium): **Revise `downward_arc_layout` to the single arc (TDD).** Files: `src/face_plate_layouts.py` + `tests/test_downward_arc_layout.py`. Sequential after Task 1 (both edit `face_plate_layouts.py`; do NOT parallelize).
- **Task 3** (medium, run-only): **Verify generated geometry.** Files: `manufacture/*.step`, `manufacture/face_plate_baseline.md`. Regenerate, baseline, assembled-die collision check, yield check, unit suite, human visual gate (final qualification by the user). Depends on Tasks 1–2.
- **Task 4** (tech-writer): **Update memory-bank docs.** Files: `memory-bank/design/candle-arrangement-arc.md`, `design.md`, `requirements.md`, `context.md` (optional `arrangement_approach.md`; `candle-arrangement-circular.md` unchanged). **Parallel group A with Task 3** (disjoint: `manufacture/` vs `memory-bank/`). Must not embed Task 3's measured bbox/volume figures.
- **Parallel group A: Tasks 3 and 4** — merge order any (default 3 then 4); integration tests after merge: full unit suite + both-layout generation + assembly collision spot-check; watch for `manufacture/*.step` nondeterministic diffs (discard spurious) and `memory-bank/context.md`.
- **Sizing notes**: Task 1 is `[Small]` (single-file constant change); Tasks 2–3 are medium (2-file TDD / run-only with human gate); Task 4 is a writing task (not `[Small]`). The single-arc coordinates are pinned by the plan (no ambiguity), so Task 2's rewrite is a bounded 2-file TDD task.

### Resolved decisions (confirmed by the user)

1. **Circular layout**: unchanged — no adjustment; it is slated for later removal. The 9-in face growth still applies to the shared plate geometry.
2. **Arc start**: ±59.7 mm (≈1 mm connector clearance) — the recommended design point.
3. **Final qualification**: the user will do a final visual qualification pass on the visible result; the story's Task 3 human visual sign-off gate must be surfaced to the user.

### Other suggestions

- Keep the layout registry names (`circular`, `downward_arc_layout`) unchanged so CLI/exports/`--show` keys stay stable.
- Update the `face_plate_baseline.md` title/label to reflect it is now the 9-in baseline (the old 7-in record can stay as a historical section).
- Record the connector-collision discovery (7-in design) in the story notes so the fix's rationale is traceable.
