# Parabolic-Arch Candle Arrangement

The candle arrangement designed for the densest face of the die (8 regular
candles plus the shamash). It places all 8 regular candles on a **single
concave-down parabolic arch** (an arch, ∩) running from the lower-right of the
face, over the crown, to the lower-left, and it is engineered to satisfy the
project's spacing, shamash, connector-clearance, holder-fit, and
holder-collision constraints on the 9-in face.

This is the current arrangement; it supersedes the earlier 7-in two-arc design
(start holders at (±56.862, 9.525)), which collided with the equatorial
connectors in the assembled die and could not carry 8 candles on a single arc
at the 7-in size, and the 9-in single circular arc of Story003 (a semicircle:
center (0, 12.7), radius 59.7 mm, peak (0, 72.4), ends (±59.7, 12.7)), whose
low crown wasted the space between the arc and the shamash and whose bottom
(foot) holders intersected the adjacent faces' foot holders in the assembled
die. The parabolic arch fixes both: the crown rises to (0, 95) and the feet
move up to (±63, 28), so the adjacent-face holders no longer collide.

## Scope

This document describes the 8-candle (densest) face and how faces with 1–7
candles are derived from it (see [Candle Counts](#candle-counts-faces-with-17-candles)).
The arrangement is implemented as the `downward_arc_layout` face-plate layout
(see the [parabolic arch layout plan](../plans/parabolic_arch_layout_plan.md)).

## Design Constraints

1. **Regular candle spacing:** the centers of adjacent regular candle holders
   must be at least **1.0 inch (25.4 mm)** apart. The parabolic arch meets this
   at **26.62 mm** (arc-top pair, holes 4–5) for every prefix count; the side
   gaps run ≈ 27.3–27.5 mm.
2. **Shamash location:** the shamash holder stays fixed by the apex connector:
   the starter-hole rule puts it **35 mm from the triangle's point** (plus the
   plate's bevel offset), i.e. at `(0, 161.17)` mm from the base on the 9-in
   face.
3. **Shamash clearance:** the shamash candle hole center must be at least
   **1.75 inches (44.45 mm)** (the relaxed minimum) from the nearest regular
   candle holder center. The design gives **≈ 70.4 mm** (also ≥ 2.5 in /
   63.5 mm).
4. **Equatorial-connector clearance:** the start holder block nearest each
   bottom (equatorial) connector must clear the connector solid in the
   assembled die. Clearance is verified empirically against the real connector
   geometry (not a simplified footprint): at `y = 28` the zero-clearance start
   limit is ≈ `x = 65`; the design starts at **(±63.0, 28.0)**, leaving
   ~2–3 mm margin.
5. **Adjacent-face holder non-intersection:** the bottom (foot) holders must
   not intersect holders on the adjacent face sharing the bottom edge. The feet
   at `y = 28` clear this (threshold ≈ 27–28 mm): **0 overlap across all 36
   mounted holders** (empirical, all pairs).
6. **Screw-hole clearance:** each bottom holder's four M2 screw holes must stay
   ≥ **4.5 mm** center-to-center from every equatorial-connector M2 screw hole
   (countersink head Ø 4.5 mm); the design gives ≈ **22.5 mm**.
7. **Smooth single arch:** all eight candles lie on **one** smooth
   concave-down parabola rising from the connector-cleared feet near the base,
   over the crown, and down to the mirrored feet near the base.
8. All candle-holder blocks (0.75 in / 19.05 mm square) must lie fully inside
   the triangular face plate; the four corners of every holder are inside the
   9-in triangle.

## Face Geometry and Coordinates

- Face: equilateral triangle, side 9 in (**228.6 mm**), height **197.97 mm**
  (= 9-in side × √3/2), half-base **114.3 mm**.
- Coordinates: base at `y = 0`, triangle point at `(0, 197.97)`; the face is
  symmetric about `x = 0`.
- Shamash (starter candle) center: `(0, 161.17)` mm (≈ height − 36.8, the
  35 mm-from-tip rule plus the plate's bevel offset; pinned as the
  design/test constant).
- Holder block half-width: `hw = 9.525 mm`.

## The Single Concave-Down Parabolic Arch

All eight regular-candle positions lie on one parabola, concave down and
symmetric about `x = 0`:

- **Feet (arch endpoints)**: `(±63.0, 28.0)` mm.
  - `y = 28` clears the adjacent-face foot-holder collision (threshold
    ≈ 27–28 mm).
  - `x = 63` clears the equatorial connector with ~2–3 mm margin (empirical
    zero-clearance ≈ `x = 65` at `y = 28`) and keeps the holder fully inside
    the triangle with ≥ 12.7 mm edge inset.
- **Crown (peak)**: `(0, 95)` mm (66.2 mm below the shamash).
- **Curve**:

  ```
  y(x) = 28 + 67 · (1 − (x / 63)²)          A = crown − 28 = 67 mm
  ```

- **Equivalent quadratic Bézier** (exact — a quadratic Bézier *is* a
  parabola), used for the embossed groove:

  ```
  P0 = ( 63.0, 28.0)     # bottom right (start)
  P1 = (  0.0, 162.0)    # control point = tangent intersection = 2·crown − 28
  P2 = (−63.0, 28.0)     # bottom left (end)
  ```

  Note: `P1` lies just above the shamash (`161.17`). That is correct — a
  quadratic Bézier's middle point is a *control point* (the tangent
  intersection), not a point on the curve; the groove still peaks at `(0, 95)`.

The eight candles are placed **evenly by arc length** along this sweep, so
adjacent chords are nearly equal.

## Solved Layout (8-Candle Face)

The positions are the ground truth of the design, hard-coded as the ordered
`DOWNWARD_ARC_PARABOLIC_9IN` tuple. Hole 1 is the bottom-right start; the order
runs up the right side, over the crown, and down the left side to the
bottom-left end:

| Hole # | Position (mm) | Parabola location |
|--------|---------------|-------------------|
| 1 | (63.000, 28.000) | bottom right (start) |
| 2 | (50.261, 52.356) | right side, up |
| 3 | (34.534, 74.867) | right side, up |
| 4 | (13.312, 92.008) | top right (just right of crown) |
| 5 | (−13.312, 92.008) | top left (just left of crown) |
| 6 | (−34.534, 74.867) | left side, down |
| 7 | (−50.261, 52.356) | left side, down |
| 8 | (−63.000, 28.000) | bottom left (end) |

### Constraint Verification

| Constraint | Requirement | This design |
|------------|-------------|-------------|
| Regular-candle spacing | ≥ 25.4 mm adjacent | **26.62 mm** (arc-top pair, holes 4–5; side gaps ≈ 27.3–27.5 mm) |
| Shamash-to-nearest candle | ≥ 44.45 mm (1.75 in, relaxed; also ≥ 63.5 mm / 2.5 in) | **≈ 70.4 mm** (holes 4/5 at `(±13.312, 92.008)`) |
| Shamash visibility (arc-top pair) | ≥ 12.7 mm between innermost tops | **26.62 mm** |
| Equatorial-connector clearance | start holder clear of connector | **0 overlap**; feet `(±63, 28)`, ≈ 2–3 mm margin (empirical) |
| **Adjacent-face holder non-intersection** | **0 overlap between holders on faces sharing a bottom edge** | **0 overlap across all 36 mounted holders** (empirical, all pairs) |
| **Screw-hole clearance (holder vs connector)** | bottom holder M2 holes clear of equatorial-connector M2 holes (≥ 4.5 mm center-to-center) | **≈ 22.5 mm** min center-to-center (countersink Ø 4.5 mm) |
| Holder fit | all 4 corners inside the 9-in triangle | pass |
| Edge inset | candle centers ≥ 0.5 in (12.7 mm) from every edge | pass (feet at 28 mm bottom inset) |

## Candle Counts (Faces with 1–7 Candles)

A face with `n` candles uses the **first `n` positions of the ordered 8-candle
sequence**, so each candle occupies exactly the same position as the
corresponding candle on the 8-candle face:

```
candle_positions(n) == DOWNWARD_ARC_PARABOLIC_9IN[:n]      (n = 1–8)
```

This is a **continuous over-the-top traversal**: position 1 is the bottom
right, position 4 the top right, position 5 the top left, and position 8 the
bottom left. It differs from the superseded two-arc rule ("right arc
bottom-to-top, then left arc bottom-to-top"), which placed the 5th candle at
the bottom left. Notable checkpoints: `candle_positions(1) ==
[(63.000, 28.000)]` and `candle_positions(5)[-1] == (−13.312, 92.008)`. Every
count keeps the adjacent regular-candle spacing at **26.62 mm** (≥ 1.0 in /
25.4 mm).

## Embossed Parabolic Groove

Each face carries an engraved line that forms **one continuous arch** across the
face: it starts at the bottom right, rises over the crown, and descends to the
bottom left, following exactly the same parabola as the candles.

- **Cross-section**: 1/8 in (3.175 mm) wide across the line, 1 mm deep into the
  face, milled into the **outside** face of the plate.
- **Path**: the single quadratic-Bézier control-point triple
  `((63.0, 28.0), (0.0, 162.0), (−63.0, 28.0))` — start, control point, end —
  swept with `Bezier` in `src/manora/generate_manora.py`. A quadratic Bézier *is* the exact
  parabola, so the sweep produces one clean uniform groove with no C1 joints
  (the "shear at the joints" pitfall of the old multi-arc approach does not
  apply). The control point `(0, 162)` is the tangent intersection — **not** a
  point on the curve; the groove peaks at `(0, 95)`. `P1 = (0, 162)` lies just
  above the shamash at `161.17`, which is correct: the curve itself never
  reaches `y = 162`.
- **Every face**: the full continuous line is drawn on **every** face regardless
  of candle count. The candle through-holes visually interrupt it where they
  exist (the line appears to pass through the holes), and the line remains
  continuous where holes are missing.
- **Not subject to candle spacing**: the embossed line is decorative — the
  1.0 in candle-separation rules do not apply to it.
- **Shamash excluded**: the shamash hole does not participate — the line never
  runs to the shamash.
- **Geometry**: the parabola `y = 28 + 67·(1 − (x/63)²)` — the same curve as
  the candles.

## Shamash Visibility and Distinctness

Because the shamash sits ≈ 70.4 mm from the nearest regular candle (the two
arc-top candles at `(±13.312, 92.008)`), it is clearly separate from the
cluster of eight, satisfying the halachic requirement that the shamash be
unmistakably not one of the regular candles. When the fully populated face is
viewed from its base edge at eye level with the top of the die (a "forest"
view), the arc-top pair (26.62 mm apart) and the arch's low, open center leave
a clear sightline to the shamash on the centerline above the arch crown.

## Ritual Ordering

Which positions a face uses is fixed by [Candle Counts](#candle-counts-faces-with-17-candles)
(the first `n` of the ordered 8-candle sequence). The halachic ritual still
needs an unambiguous left-to-right order for lighting (night-one candle on the
right, add new candles leftward, light left-to-right); this is a lighting
convention applied by the user on top of the fixed positions and is not part
of the geometric layout.

## Implementation Notes

- Implemented as the `downward_arc_layout` face-plate layout in
  `src/manora/face_plate_layouts.py` (see the
  [parabolic arch layout plan](../plans/parabolic_arch_layout_plan.md)):
  - `DOWNWARD_ARC_PARABOLIC_9IN` is the ordered 8-position tuple from the table
    above, with a comment noting the feet `(±63, 28)` clear the adjacent-face
    holder collision (threshold ≈ 27–28 mm) and sit ~2–3 mm inside the
    equatorial-connector zero-clearance limit at `y = 28` (`x ≈ 65`), and that
    the eight points lie on `y = 28 + 67·(1 − (x/63)²)`.
  - `candle_positions(num_candles)` returns
    `list(DOWNWARD_ARC_PARABOLIC_9IN)[:num_candles]`.
  - `groove_arcs(num_candles)` returns the single quadratic-Bézier control-point
    triple `((63.0, 28.0), (0.0, 162.0), (−63.0, 28.0))` for every face,
    regardless of candle count.
  - `holder_rotation_angle(cx, cy)` returns the parabola-tangent angle
    `degrees(atan2(2·A·cx / XFOOT, −XFOOT))` with `A = 67` and `XFOOT = 63`,
    aligning the holder's local +X with the tangent in traversal direction
    (bottom-right → crown → bottom-left) and its local +Y with the inboard
    normal (toward the base). End values: hole 1 ≈ 115.18°, hole 8 ≈ 244.82°
    (mirror sum 360°); the crown tangent (unoccupied) is 180°.
  - `__init__` stores but does not use `triangle_height`: the parabolic-arch
    geometry is fixed for the 9-in face (connector clearance and holder
    margins are constant, not proportional to face height).
  - The layout registry name `"downward_arc_layout"` is unchanged, so
    CLI/export/`--show` keys stay stable.
- The groove sweep is drawn by the shared plate builder in `src/manora/generate_manora.py` (one
  `BuildLine` + one sweep per face for the single Bézier path).
- The geometry above assumes the standard face: side 9 in, height 197.97 mm,
  holder width 0.75 in, and the shamash at 35 mm from the tip (center
  `(0, 161.17)`).
- **History**: the previous 7-in two-arc design (arc starts ±56.862 mm, 3 mm
  simplified-footprint clearance) and the 9-in single circular arc of Story003
  (a semicircle: center (0, 12.7), radius 59.7 mm, peak (0, 72.4)) are
  superseded; they are recorded for traceability in
  `memory-bank/plans/downward_arc_layout_plan.md` and
  `memory-bank/plans/adjust_size_and_arc_plan.md`.
