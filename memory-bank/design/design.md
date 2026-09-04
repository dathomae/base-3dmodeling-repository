# System Design

This document captures the design and list of parts for the 3D modeled Hanukkah Menorah project. The models will be created using the `build123d` package.

The candle-holder arrangements for the face plates are documented separately and are referenced from the Face Plate part below:

- [Circular candle arrangement](candle-arrangement-circular.md) — the current default layout (slated for later removal).
- [Arc-based candle arrangement](candle-arrangement-arc.md) — the layout for the densest face (8 regular candles) on the 9-in face: a single concave-down parabolic arch (feet (±63, 28), crown (0, 95)) carrying all 8 candles from the bottom right, over the crown, to the bottom left, satisfying the spacing, shamash, connector-clearance, and holder-fit constraints and keeping adjacent-face holders non-intersecting; implemented as the `downward_arc_layout` selectable layout, with a single continuous embossed parabolic groove on every face.

## Architecture Overview

The menorah is an eight-sided die (regular octahedron) resting on one of its faces. It is constructed from 8 aluminum plates (the faces) held together by 6 internal connector blocks at the vertices. The regular candle holders are attached to the inside of the plates, with holes in the plates for the candles to pass through. The starter candle holders are integrated into the top and bottom apex connector blocks.

When the die rests on a face, the opposite face is perfectly horizontal and facing up. The candles on this top face will be vertical and ready to be lit. The user rotates the die each day to bring the appropriate face to the top.

## List of Parts to Model

1. **Face Plate (8 variations):**
   - Equilateral triangle, side length 9 inches (228.6 mm) on the outside face.
   - Thickness: 0.05 inches (1.27 mm).
   - Features:
     - Beveled edges (tapered inward by 35.264°) so the plates meet perfectly flush on the inside.
     - Countersunk holes for M2 screws to attach to the vertex connectors.
     - Countersunk holes for M2 screws to attach the regular candle holders.
     - 8.5 mm through-holes for the regular candles to pass through into the holders.
     - One 8.5 mm through-hole near the "top" vertex for the starter candle.
   - Variations: 8 different plates, having 1 to 8 sets of mounting holes for the regular candle holders.

   The regular-candle hole pattern is produced by a pluggable layout strategy: `src/manora/generate_manora.py` accepts a `--layout` option (default `"circular"`), and each layout in `src/manora/face_plate_layouts.py` returns the hole centers via `candle_positions(num_candles)`. Beyond providing the centers, a layout overrides only two class-level values: `candle_hole_diameter` (always circular, defaulting to `CANDLE_HOLE_DIAMETER_MM`) and `screw_holes` (whether the M2 screw holes around each candle holder are cut, default true). A half-inch wooden variant, for example, might use a larger diameter and set `screw_holes = False`. The two designed arrangements are documented in [candle-arrangement-circular.md](candle-arrangement-circular.md) and [candle-arrangement-arc.md](candle-arrangement-arc.md); the arc arrangement is implemented as the `downward_arc_layout` layout (selectable with `--layout downward_arc_layout`, alongside the default `circular`): on the 9-in face it is a single concave-down parabolic arch — feet (±63, 28), crown (0, 95) — carrying all 8 regular candles from the bottom right, over the crown, to the bottom left, with regular centers 26.62 mm apart and the shamash ≈ 70.4 mm from the nearest regular candle, and it draws its single continuous embossed parabolic groove on every face.

2. **Regular Candle Holder (36 pieces):**
   - Material: 0.75 inch (19.05 mm) square aluminum bar stock.
   - Length: 0.75 inches (19.05 mm).
   - Features:
     - Central cylindrical hole: 8.5 mm diameter, 0.6 inches (15.24 mm) deep.
     - 4 tapped holes for M2 screws at the corners of the base, 3 mm from the edges. Tapped depth is 10 mm to accommodate 6 mm long screws.

3. **Apex Connector (2 pieces):**
   - Material: 2 inch (50.8 mm) square aluminum bar stock.
   - Shape: Square pyramid (or frustum) with faces at 54.73° to the base.
   - Features:
     - 4 planar faces to mate with the inside of the aluminum plates.
     - Tapped holes for M2 screws on each face to attach to the plates. Tapped depth is 10 mm to accommodate 6 mm long screws.
     - 4 cylindrical holes (8.5 mm diameter, 15.24 mm deep) drilled perpendicular to the faces to serve as the starter candle holders.

4. **Equator Connector (4 pieces):**
   - Material: 1.5 inch (38.1 mm) square aluminum bar stock.
   - Shape: Same as the Apex Connector.
   - Features:
     - 4 planar faces to mate with the inside of the aluminum plates.
     - Tapped holes for M2 screws on each face to attach to the plates. Tapped depth is 10 mm to accommodate 6 mm long screws.
     - *No starter candle holes.*

## Component Details & Measurements

- **Octahedron Geometry:**
  - Dihedral angle (between adjacent faces): 109.47°
  - Angle between opposite faces meeting at a vertex: 70.53°
  - The connectors are designed to fit exactly into the 109.47° internal corners of the vertices.

- **Starter Candle Placement:**
  - The starter candle hole is located near the "top" vertex of each face.
  - The hole is positioned such that it aligns perfectly with the starter candle hole in the Apex Connector.
  - Distance from the vertex tip to the center of the starter candle hole: **35 mm**. This distance ensures that the 15.24 mm deep holes in the Apex Connector do not intersect with each other internally.
  - On the 9-in face plate this places the shamash holder center at **(0, 161.17) mm** from the base (the triangle point is at `y = 197.97`; the center is ≈ 36.8 mm from the point, i.e. the 35 mm rule plus the plate's bevel offset), which is the fixed shamash location used by the candle-arrangement documents.

## Candle Arrangement

How the regular candle holders are placed on each face is a design decision independent of the die geometry above. Two arrangements have been designed:

| Document | Description |
|----------|-------------|
| [Circular candle arrangement](candle-arrangement-circular.md) | The current default: holders on a circle of radius 28.0 mm centered 40.5 mm from the base, with special cases for 1–4 candles. Positions are absolute constants and were unchanged by the 9-in face growth; the layout is slated for later removal. |
| [Arc-based candle arrangement](candle-arrangement-arc.md) | On the 9-in face (side 228.6 mm): one concave-down parabolic arch — `y = 28 + 67·(1 − (x/63)²)`, feet (±63.0, 28.0), crown (0, 95) — carrying all 8 candles from the bottom right, over the crown, to the bottom left; regular centers 26.62 mm apart (≥ 1.0 in), shamash ≈ 70.4 mm from the nearest regular candle (≥ 1.75 in, also ≥ 63.5 mm), start holders (feet) ~2–3 mm clear of the equatorial connectors (empirical; zero-clearance ≈ x = 65 at y = 28), adjacent-face holders non-intersecting (0 overlap across all 36 mounted holders), and bottom-holder screw holes ≈ 22.5 mm clear of the equatorial-connector M2 holes (≥ 4.5 mm center-to-center). Implemented as the `downward_arc_layout` selectable layout (alongside the default `circular`), with a single continuous embossed parabolic groove (1/8 in × 1 mm groove on the outside face) drawn on every face. |
