# Circular Candle Arrangement

The default face-plate candle arrangement. It preserves the original hard-coded
placement from the first version of the plate builder, captured as a pluggable
layout strategy (`CircularLayout` in `src/manora/face_plate_layouts.py`) so other
arrangements can be added without touching the plate builder.

## Mechanism

- Selected with `--layout circular` (the default) in `src/manora/generate_manora.py`.
- `candle_positions(num_candles)` returns the candle hole centers in face-plate
  coordinates (base at y = 0, triangle point at y = triangle height).
- Layout knobs: `candle_hole_diameter` (8.75 mm) and `screw_holes` (True).
- The surrounding M2 screw holes for each candle holder are derived by the
  shared builder from the holder footprint (`candle_holder_width`), not by the
  layout.
- Face-plate exports are named `face_plate_circular_<n>.step`.

## Placement Rules

The holders are arranged on a circle, with special cases for small counts:

| Candles | Placement |
|---------|-----------|
| 1 | Centroid of the face: `(0, triangle_height / 3)` |
| 2 | Horizontal pair at `(±28.0, 40.5)` mm |
| 3 | Evenly spaced on a circle of radius 28.0 mm centered 40.5 mm from the base, plus a vertical offset of `+0.05 × triangle_height` |
| 4 | Circle radius 28.0 mm rotated 45°, centered 40.5 mm from the base, plus a vertical offset of `+0.10 × triangle_height` |
| 5–8 | Evenly spaced on the circle of radius 28.0 mm centered 40.5 mm from the base |

Constants: `circle_radius = 28.0 mm`, `circle_center_y = 40.5 mm`.

## Starter Candle

The shamash is not part of the layout; it is fixed near the triangle's point by
the apex connector geometry (see the Starter Candle Placement section of
[design.md](design.md)) at 35 mm from the tip, i.e. `(0, ~161.2)` mm on the
9-in face.

## Spacing Characteristics

Adjacent spacing along the circle depends on the candle count (radius 28.0 mm):

| Candles | Adjacent spacing |
|---------|------------------|
| 2 | 56.0 mm = 2.20 in |
| 3 | 48.5 mm = 1.91 in |
| 4 | 39.6 mm = 1.56 in |
| 5 | 32.9 mm = 1.30 in |
| 6 | 28.0 mm = 1.10 in |
| 7 | 24.3 mm = 0.96 in |
| 8 | 21.4 mm = 0.84 in |

**Note:** at the current radius the 7- and 8-candle faces fall below the
project's 1.0 inch minimum regular-candle spacing (0.96 in and 0.84 in). The
circular arrangement predates that constraint; the
[arc-based arrangement](candle-arrangement-arc.md) is the design that satisfies
it for the densest face.

## Status on the 9-in Face

The candle positions of this layout are **absolute constants** (circle radius
28.0 mm, center y 40.5 mm) and were **not** adjusted when the face plates were
enlarged to 9-in equilateral triangles in Story003. The 9-in face growth
applies to the shared plate geometry only; the circular candles keep their
current positions, clustered low in the bigger face. This layout is slated for
**later removal** (it does not satisfy the menorah candle-spacing rules for
its 7- and 8-candle faces), and no further changes to it are planned.
