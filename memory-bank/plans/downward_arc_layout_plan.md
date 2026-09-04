# Downward Arc Layout Plan

## Objective

Implement the arc-based candle arrangement for the face plates as a new
selectable layout named **`downward_arc_layout`** in `src/face_plate_layouts.py`,
exactly as designed in `memory-bank/design/candle-arrangement-arc.md`, together
with the **embossed arc line** (a milled groove following each arc).

Design decisions already settled (recorded in the design doc):

- A face with `n` candles uses the **first `n` positions of the 8-candle
  sequence** (right arc bottom-to-top R1–R4, then left arc bottom-to-top
  L1–L4), so each candle sits at the same position on the same arc as the
  corresponding candle on the 8-candle face.
- Every face carries one **continuous** engraved line, **1/8 in (3.175 mm)
  wide and 1 mm deep**, on the **outside** face, running from the bottom of the
  right side up the right candle arc, across the middle of the face, and down
  the left candle arc to the bottom of the left side. It is decorative (the
  candle-spacing rules do not apply to it) and the shamash does not
  participate.
- `circular` remains the default; `downward_arc_layout` is added as selectable.

The new layout is added **alongside** the existing `circular` layout, which
remains the default. `src/main.py` gains only the groove-drawing sweep; layout
selection, the plate builder, and the assembly already consume layouts
generically (`--layout choices=sorted(LAYOUTS)`, `create_layout(...)`,
`layout.candle_positions(num_candles)`), so registering the layout makes
`--layout downward_arc_layout` work for the candle holes with no further
wiring.

## Design

### Background and constraints (from `memory-bank/design/candle-arrangement-arc.md`)

The 8-candle (densest) face places the regular candles on two symmetric,
smooth circular arcs — four on the right, four mirrored on the left. The
arrangement satisfies:

- Adjacent regular-candle centers ≥ **1.0 in (25.4 mm)** apart.
- The shamash holder stays at its current location, `(0, 117.2)` mm from the
  base (35 mm from the triangle's point), fixed by the apex connector; the
  shamash hole center is ≥ **2.5 in (63.5 mm)** from the nearest regular candle
  center (achieved: 65.14 mm).
- The start holder on each side keeps **3 mm** clearance from the bottom
  (equatorial) connector footprint — the right-side constraint is
  `33·x + 19.05·y ≤ 2057.9`, giving the start point `(56.862, 9.525)`.
- All holder blocks (0.75 in / 19.05 mm square) lie fully inside the face.

The right arc's four points (from the base upward) are the **ground truth** for
the implementation. They are the result of the constraint optimization
documented in the design doc — there is no simple closed-form derivation of the
arc-top point, so the plan hard-codes the optimized coordinates rather than
reconstructing them:

| Point | Right arc (mm) | Left arc (mm) |
|-------|----------------|---------------|
| 1 (start) | (56.862, 9.525) | (−56.862, 9.525) |
| 2 | (31.467, 10.025) | (−31.467, 10.025) |
| 3 | (13.426, 27.905) | (−13.426, 27.905) |
| 4 (top) | (12.700, 53.295) | (−12.700, 53.295) |

These points lie on a circular arc of radius 34.19 mm. Adjacent spacing is
25.40 mm along each arc and between the two arc tops.

The embossed line follows the right candle arc (circle center (44.79, 41.51) mm,
radius 34.19 mm) up from R1 to R4, bridges across the center to L4 on a circle
tangent to both candle arcs (center (0, 57.96) mm, radius 13.5 mm, passing
through (0, 44.44)), and descends the left candle arc (mirror circle) to L1 —
one continuous path.

### New code in `src/face_plate_layouts.py`

Add module-level constants, an optional `groove_arcs()` capability on the base
class, and the new layout class (mirroring the `CircularLayout` style — pure
Python, `math` only, no `build123d` import):

```python
DOWNWARD_ARC_RIGHT = (
    (56.862, 9.525),    # arc start — 3 mm clear of the equatorial connector
    (31.467, 10.025),
    (13.426, 27.905),
    (12.700, 53.295),   # arc top
)


class FaceLayout(ABC):
    # ... existing attributes and candle_positions() ...

    def groove_arcs(self, num_candles: int) -> list[tuple[tuple[float, float],
                                                          tuple[float, float],
                                                          tuple[float, float]]]:
        """Return decorative/embossed arc paths (three points per arc, in the
        face plane) to mill into the outside face. Default: no grooves."""
        return []


class DownwardArcLayout(FaceLayout):
    """Two symmetric circular arcs (4 candles per side) for the densest face.

    Designed for the standard 7-inch face; the coordinates are the optimum
    documented in memory-bank/design/candle-arrangement-arc.md. The shamash
    holder is not part of this layout (it is cut by the shared builder).
    """

    name = "downward_arc_layout"

    def __init__(self, triangle_height: float):
        # triangle_height is accepted for interface compatibility with
        # create_layout(); the arc geometry is fixed for the standard 7-in face
        # (connector clearance and holder margins are constant, not
        # proportional to face height), so it is intentionally not used.
        self.triangle_height = triangle_height

    def candle_positions(self, num_candles: int) -> list[tuple[float, float]]:
        # Face n uses the first n positions of the 8-candle sequence:
        # right arc bottom-to-top (R1..R4), then left arc bottom-to-top (L1..L4).
        full = list(DOWNWARD_ARC_RIGHT) + [
            (-x, y) for x, y in DOWNWARD_ARC_RIGHT
        ]
        return full[:num_candles]

    def groove_arcs(self, num_candles: int) -> list:
        # One continuous embossed arc line on every face: right candle arc
        # (R1->R4), bridge across the center, left candle arc (L4->L1). Each
        # element is three (x, y) points defining a circular arc; consecutive
        # arcs join end-to-start to form one smooth continuous path.
        r1, r2, r3, r4 = DOWNWARD_ARC_RIGHT
        l1, l2, l3, l4 = ((-r1[0], r1[1]), (-r2[0], r2[1]),
                          (-r3[0], r3[1]), (-r4[0], r4[1]))
        bridge_mid = (0.0, 44.44)
        return [
            (r1, r3, r4),              # right candle arc, up
            (r4, bridge_mid, l4),      # bridge across the center (tangent)
            (l4, l3, l1),              # left candle arc, down
        ]
```

Register the layout so `--layout downward_arc_layout` is available:

```python
LAYOUTS = {
    "circular": CircularLayout,
    "downward_arc_layout": DownwardArcLayout,
}
```

### `src/main.py` — groove sweep in the plate builder

`create_face_plate(num_candles, layout)` already cuts the candle holes from
`layout.candle_positions(num_candles)`. Add, after the candle-hole loop, a
loop over `layout.groove_arcs(num_candles)` that mills the embossed lines:

- **Sweep per arc segment** (do NOT join the arcs into one wire swept once).
  For each three-point circular arc definition, build the circular arc at
  `z = plate_thickness` (the outside face) as its own `BuildLine`
  (an `Arc3`/`ThreePointArc` through the three points) and sweep the profile
  along it with `mode=Mode.SUBTRACT`. Sweeping a non-circular profile along a
  single wire that joins arcs of *different radii* (34.19 → 13.5 → 34.19 mm)
  shears the pipe-shell section at the curvature-discontinuous C1 joints: the
  swept solid silently loses ~35% of its volume and its top face undulates
  coplanar with the outside face, which then corrupts the plate boolean
  (plates collapse to empty geometry for n = 1–3). This is the failure class
  documented in `resources/modeling/general_knowledge.md` §3. Per-segment
  sweeps produce clean flat-topped prisms that meet flush at the
  tangent-continuous joints, so subtracting them in sequence yields one
  visually continuous groove.
- Sweep a rectangle profile **3.175 mm (1/8 in) wide** (in the face plane,
  perpendicular to the path) × **1.0 mm deep** (into the plate, toward −z)
  with `mode=Mode.SUBTRACT`, positioned so its top is flush with
  `z = plate_thickness` (the prism spans `z = plate_thickness − 1.0` to
  `plate_thickness`). The rectangle's depth axis is the face normal; its
  width axis lies in the face plane perpendicular to the path. Center the
  profile on the arc's start point (shifted down 0.5 mm in z).
- The groove is one continuous cut per face (no breaks at candle-hole
  positions); the candle through-holes are cut as before and will visually
  interrupt the groove at the holes, which is the intended "passes through"
  look. The groove is drawn on every face regardless of candle count.
- No change to `--layout` defaults, connector holes, starter hole, or the
  assembly loop. Face-plate exports become `face_plate_downward_arc_layout_<n>.step`
  (existing `face_plate_{layout.name}_{i}.step` rule); the `--show` component
  keys stay `face_plate_1` … `face_plate_8`.

## Implementation Steps

### Step 1: Write layout tests first (TDD red)

Create `tests/test_downward_arc_layout.py` using Python's stdlib `unittest`
(same conventions as `tests/test_face_plate_layouts.py`: a `sys.path`
insertion at the top so `src/` is importable, `REPO_ROOT` derived from
`__file__`). Assert:

- **8-candle positions match the design doc**: `candle_positions(8)` equals the
  eight coordinates above (right arc R1–R4 then left arc L1–L4, left =
  mirrors), compared with `assertAlmostEqual(…, delta=0.1)` (the design values
  are quoted to 3 decimals).
- **Count rule (first n of the sequence)**: `candle_positions(n)` equals
  `candle_positions(8)[:n]` for every `n` 1–7, and specifically
  `candle_positions(1) == [(56.862, 9.525)]`,
  `candle_positions(4)` returns R1–R4,
  `candle_positions(5)` returns R1–R4 then L1.
- **Spacing minimum**: for every `num_candles` 1–8, the minimum pairwise
  distance between positions is ≥ 25.4 mm, allowing 0.05 mm tolerance for
  coordinate rounding (assert `>= 25.35`). This pins the 1.0 in requirement.
- **Default attributes**: `name == "downward_arc_layout"`,
  `candle_hole_diameter == CANDLE_HOLE_DIAMETER_MM`, `screw_holes is True`.
- **Registry**: `create_layout("downward_arc_layout", triangle_height=…)`
  returns a `DownwardArcLayout` instance, and `create_layout("<unknown>")`
  raises `ValueError` whose message lists **both** `circular` and
  `downward_arc_layout`.
- **Groove arcs**: `groove_arcs(n)` returns the same continuous path for every
  `n` 1–8: three arc definitions — (R1, R3, R4), (R4, (0, 44.44), L4),
  (L4, L3, L1) — where Lk = (−Rk.x, Rk.y). `CircularLayout.groove_arcs(8)`
  returns `[]`.

Run `source venv/bin/activate && python -m unittest discover -s tests -v` — the
new tests fail because the class does not exist yet (intended red step).

### Step 2: Implement `DownwardArcLayout` (TDD green)

Add `DOWNWARD_ARC_RIGHT`, the `groove_arcs()` default on `FaceLayout`, the
`DownwardArcLayout` class, and the registry entry to `src/face_plate_layouts.py`
exactly as specified in the Design section. Keep the module free of
`build123d` imports (it may import only `manora_parameters`). Run the tests
again — all pass (green step).

### Step 3: Implement the embossed groove sweep in `src/main.py`

Add the groove sweep to `create_face_plate(num_candles, layout)` as described in
the Design section: loop over `layout.groove_arcs(num_candles)` and sweep a
3.175 mm × 1.0 mm rectangle along **each** three-point circular arc separately
(per-segment sweeps; do not join the arcs into one wire — see the Design
section for why that shears the section), subtract, with per-face progress and
error reporting. Do not change any existing hole, taper, connector,
starter-hole, or assembly code.

Run the programmatic groove-geometry gate (per-prism z-range [0.27, 1.27] and
total volume ≈ 600 mm³, all plates valid and strictly lighter than `circular`)
and verify the module still runs:
`source venv/bin/activate && python src/main.py --layout circular` produces
unchanged `face_plate_circular_*.step` (no grooves — the circular layout
returns no arcs).

### Step 4: Verify generated geometry

1. `source venv/bin/activate && python src/main.py --layout downward_arc_layout`
   — confirm it completes and exports
   `manufacture/face_plate_downward_arc_layout_1.step` …
   `face_plate_downward_arc_layout_8.step` plus the unchanged shared parts and
   assembly.
2. Visually inspect (e.g. `python src/main.py --show face_plate_8` and
   `python src/main.py --show face_plate_2` in `ocp_vscode`) that:
   - every face (including low-count faces) shows the full continuous line from
     the bottom right, up through the center, down to the bottom left;
   - the line passes through the existing candle holes and is continuous where
     holes are missing;
   - the shamash hole is not crossed by the line;
   - the line is on the outside face, 1 mm deep, 3.175 mm wide.
3. Confirm the `circular` output is **unchanged**: run
   `python src/main.py --layout circular` and verify
   `face_plate_circular_1.step` … `face_plate_circular_8.step` bounding boxes
   and volumes are identical to their values before this change (additive
   change must not alter them, and the circular layout draws no grooves).
4. `python src/main.py --layout bogus` — confirm the error names both
   `circular` and `downward_arc_layout`.
5. `python -m unittest discover -s tests -v` — all tests green.

### Step 5: Update memory-bank documentation

1. `memory-bank/design/candle-arrangement-arc.md` — already captures the
   count rule and the embossed arc line; verify it matches the implementation
   and adjust only if the implementation reveals a discrepancy.
2. `memory-bank/design/design.md` — update the Candle Arrangement pointer table
   to state the arc arrangement is implemented as `downward_arc_layout` and
   that it includes the embossed arc line.
3. `memory-bank/requirements.md` — update Functional Requirement #4 to list the
   available layouts (`circular`, the default; `downward_arc_layout` for the
   8-candle face).
4. `memory-bank/context.md` — record the task at start and clear it on
   completion, per the standard task discipline.

## Verification Checklist

- [ ] `tests/test_downward_arc_layout.py` exists; `python -m unittest discover
      -s tests -v` passes.
- [ ] `src/face_plate_layouts.py` contains `DOWNWARD_ARC_RIGHT`,
      `DownwardArcLayout`, the `"downward_arc_layout"` registry entry, and the
      `groove_arcs()` capability; the module still imports no `build123d`.
- [ ] `DownwardArcLayout.candle_positions(8)` returns the eight documented
      coordinates (within 0.1 mm); `candle_positions(n) == candle_positions(8)[:n]`
      for `n` 1–7.
- [ ] For every `num_candles` 1–8, the minimum pairwise distance of
      `candle_positions(num_candles)` is ≥ 25.35 mm (the 1.0 in requirement).
- [ ] `DownwardArcLayout.groove_arcs(n)` returns the same continuous path
      (right arc + center bridge + left arc) for every `n` 1–8;
      `CircularLayout.groove_arcs(n) == []`.
- [ ] `python src/main.py --layout downward_arc_layout` generates
      `manufacture/face_plate_downward_arc_layout_1.step` … `_8.step` and the
      assembly without errors; every face shows the full continuous line
      (bottom-right → center → bottom-left) on visual inspection (continuous,
      3.175 mm × 1 mm, outside face, shamash clear).
- [ ] `face_plate_circular_*.step` bounding boxes/volumes are unchanged from
      before this story (additive change only; no grooves on circular).
- [ ] `python src/main.py --layout bogus` fails with an error naming both
      layouts.
- [ ] `memory-bank/design/design.md`, `memory-bank/requirements.md`, and
      `memory-bank/context.md` reflect the new layout.

## Constraints

- **Additive only**: the `circular` layout and all other output (connectors,
  holders, assembly) must be unchanged. Do not touch `src/manora_parameters.py`.
- **No new dependency**: use Python's stdlib `unittest`; do not add pytest or
  any package to `requirements.txt`.
- **Module purity**: `src/face_plate_layouts.py` must not import `build123d`;
  only `manora_parameters` and `math`.
- **Design conformance**: positions must match
  `memory-bank/design/candle-arrangement-arc.md` within 0.1 mm; the layout must
  keep regular spacing ≥ 1.0 in for every candle count and keep the start
  holders 3 mm clear of the equatorial connectors.
- **Groove geometry**: the embossed line is a groove 1/8 in (3.175 mm) wide and
  1 mm deep, on the **outside** face, drawn as **one continuous** path on every
  face (right candle arc → tangent bridge across the center → left candle arc).
  It is decorative: the candle-spacing rules do not apply to it. The shamash
  hole is never crossed by the line.
- **Standard face**: the coordinates assume the standard face (side 7 in,
  height 153.98 mm, holder width 0.75 in, shamash 35 mm from the tip).
- **Environment**: activate `source venv/bin/activate` before running `python`.

## Story Writer Guidance

The plan is intended to be turned into a story with the `add-new-story` PDD
script. Suggested inputs:

- **story_name**: `downward-arc-layout`
- **description** (≤ 200 chars): "Add the `downward_arc_layout` face-plate
  candle arrangement (two symmetric circular arcs, 4 per side) with its
  continuous embossed arc line, per the arc design doc, with unit tests and
  verification."

Suggested task decomposition (for the technical-writer and the
architect-for-story-planning review):

1. **Implement `DownwardArcLayout` with tests (test-first)** — touches
   `tests/test_downward_arc_layout.py` (new) and `src/face_plate_layouts.py`
   (additive: constant, base-class `groove_arcs()` default, class, registry
   entry). TDD cycle integrated in this one task. Candidate for
   `small-code-for-story-implementor` if the reviewer judges it straightforward
   (it follows the existing `CircularLayout` pattern).
2. **Implement the embossed groove sweep in `src/main.py`** — a single-file,
   additive change to `create_face_plate` (loop over `layout.groove_arcs`,
   build the three-arc continuous path, sweep a 3.175 mm × 1.0 mm rectangle
   along it, subtract). Depends on Task 1 (it consumes `groove_arcs`). Small,
   single-file — but build123d sweep geometry is non-trivial; route to
   `code-for-story-implementor`.
3. **Verify generated geometry** — run-only over `manufacture/*.step` plus
   visual inspection (Step 4 of this plan); no source edits.
4. **Update memory-bank documentation** — edits `memory-bank/design/design.md`,
   `memory-bank/requirements.md`, `memory-bank/context.md`; routes to the
   tech-writer, not a code agent.

Execution order: Task 1 → Task 2 → {Tasks 3 and 4 in parallel}. Tasks 3 and 4
are file-disjoint (manufacture vs. memory-bank); Task 3's measured figures must
not be embedded in Task 4's docs (hidden dependency). Reintegration: merge
Tasks 3 and 4 in any order after Task 2; integration test after merge is
`python -m unittest discover -s tests -v` plus a final
`python src/main.py --layout downward_arc_layout` run.

## Open Questions

None — all previously open points are settled:

- **Candle counts**: face `n` uses the first `n` positions of the 8-candle
  sequence (resolved).
- **Embossed line**: one continuous arc on every face, bridging across the
  center; decorative (spacing rules do not apply); shamash excluded (resolved).
- **Default layout**: `circular` remains the default (resolved).
- **Return order**: right arc then left arc — order does not affect the model,
  so the simplest form is used (resolved).
