# Requirements

This document defines the requirements for the Hanukkah Menorah project.

## Functional Requirements

1. **Shape:** The menorah must be in the shape of an eight-sided die (an octahedron).
2. **Faces:** The die will have 8 triangular faces.
3. **Candle Holders per Face:** Each face will have a specific number of candle holders, ranging from 1 to 8.
4. **Candle Arrangement:** The arrangement of the candle holders for each face must be selectable, with a `circular` layout as the default. The available layouts are `circular` (the default; holders conceptually arranged in a circle centered in the bottom, wider half of the triangle) and `downward_arc_layout` (the 8-candle face on the 9-in face: a single concave-down parabolic arch — feet (±63, 28), crown (0, 95) — carrying all 8 regular candles from the bottom right, over the crown, to the bottom left). Halachic practices that govern candle arrangement (distinct shamash, unambiguous left-to-right ordering, candle separation; equal level of the lit face's candles follows automatically from the die resting flat on a face) are captured in `resources/chanukah-halacha/candle_arrangement.md` and must be satisfied by the default face layout.
5. **Starter Candle (Shamash):** Each face must have a single candle holder near the point of the triangle to serve as the starter candle.
6. **Assembly:** The faces must be held together securely. The starter candle holder may serve as the structural connector to hold the sides together at the points.
7. **Candle Fit:** The candle holders must accommodate candles with a nominal 8.5 mm diameter base.

## Non-Functional Requirements

1. **Material:** The menorah must be milled out of aluminum to withstand the heat of the candles.
2. **Stock Material:**
   - Faces: 0.05 inch (1.27 mm) thick aluminum plate, cut into 12×12 inch (304.8 mm) squares, then halved diagonally — one right-isosceles-triangular half per face (the diagonal cut is a separate pre-mill operation; the full square is not generated).
   - Candle Holders: 0.75 inch (19.05 mm) square aluminum bar stock.
   - Apex Connectors: 2 inch (50.8 mm) square aluminum bar stock.
   - Equator Connectors: 1.5 inch (38.1 mm) square aluminum bar stock.
   - All bars: 12 inches (304.8 mm) long.
   - The plastic stock is 3D-printed at 100% infill for CAM verification.
3. **Candle Holder Dimensions:**
   - Length: 0.75 inches.
   - Central Hole Depth: 0.6 inches.
4. **Fasteners:** All components (candle holders and connectors) will be attached to the plates using M2 flat head screws, 6 mm long.

## Constraints

1. **Manufacturing:** The design must be suitable for CNC milling.
2. **Material Yield:** Each 9-in face is milled from one diagonal half of a 12×12-in square of 0.05-in plate. One 12×12-in square yields two diagonal halves, i.e. two faces.
3. **Candle Spacing:** The centers of adjacent regular candle holders on a face must be at least 1.0 inch (25.4 mm) apart. They may be spaced further apart where a larger spacing yields a more symmetrical arrangement. The parabolic-arch arrangement keeps adjacent centers at **26.62 mm** (≥ 25.4 mm) for every candle count.
4. **Shamash Visibility:** When the face is viewed from its base edge toward the point (through the "forest" of fully populated candle holders), the shamash must not be occluded by the regular candles. For the parabolic-arch arrangement the innermost candle tops (the pair of candles straddling the arch crown) must therefore be separated by at least 0.5 inches (12.7 mm); the parabolic-arch design gives 26.62 mm between the arc-top pair (holes 4–5).

Note: the foot (bottom) holders of faces sharing a bottom edge must not intersect one another in the assembled die; the parabolic-arch design clears this with **0 overlap across all 36 mounted holders** (feet at (±63, 28) sit above the ≈ 27–28 mm collision threshold), and each bottom holder's M2 screw holes stay ≥ 4.5 mm center-to-center from every equatorial-connector M2 hole (design ≈ 22.5 mm).
