# Tapping Jig Plan

## Objective

Design and generate a 3D-printed tapping jig to assist with hand-tapping M2
holes in the aluminum apex connectors and regular candle holders. The jig
uses a central collar to keep the tap vertical, with replaceable bottom
plates to position different parts/holes under the collar.

## Reference: M2 Tap Dimensions

| Parameter             | Value        |
| --------------------- | ------------ |
| Total length          | 43.5 mm      |
| Shank diameter        | 3.0 mm       |
| Shank length          | 13.0 mm      |
| Square head           | above shank  |
| Cutting portion       | 30.5 mm      |
| Tapped hole depth     | 10.0 mm      |

> The tap's cutting portion extends only 10 mm into the part; the remaining
> 20.5 mm of cutting length and the 13 mm shank sit above the part face.
> The collar must clear the cutting portion (33.5 mm above the part face).

## Design — Frame and Collar

### Frame (one piece, exported as `jig_frame.step`)

- **Footprint**: 80 × 80 mm.
- **Base plate**: z = 0 to z = 3 mm. A centered 60 × 60 mm × 3 mm deep
  pocket accepts replaceable plates. Plates sit flush — their top surfaces
  are at z = 3 mm.
- **Keying**: A 4 mm wide × 3 mm deep key slot in one side of the pocket
  wall (e.g., the +Y wall, centered at y = 30, x = 0). Each replaceable
  plate has a matching 4 mm tab.
- **Collar**: Centered at (0, 0).
  - ID: 3.2 mm (0.1 mm radial clearance on the 3 mm shank).
  - OD: 9.0 mm (3 mm wall).
  - Height: 12 mm.
  - Bottom of collar: z = 60 mm.
  - Top of collar: z = 72 mm.
  - The collar bore runs from z = 60 to z = 72 (shank enters from top).
- **4 struts**: From the 4 corners of the base at z = 3 mm (the base
  plate top surface) angling inward to merge with the collar cylinder.
  - Corner positions: (40, 40, 3), (40, −40, 3), (−40, 40, 3), (−40, −40, 3).
  - Strut path: line segment from corner to (0, 0, 60) — the collar center
    at collar bottom.
  - Strut profile: circle of radius 3.0 mm (6 mm diameter), swept along path.
  - Because the collar OD (4.5 mm radius) exceeds the strut radius (3.0 mm),
    sweeping to the collar center and unioning produces a clean merge.
  - Strut centerline angle from vertical: atan(40√2 / 57) = atan(56.57 / 57)
    = **44.8°**. Safely under the 45° limit for FDM without supports.
  - The strut body at z = 3 extends to radius 3 mm from each corner, staying
    well outside the 60 × 60 mm replaceable‑plate pocket (pocket edge at
    ±30 mm; nearest strut body at ±37 mm). No interference.
  - Fillet of radius 2 mm at each strut‑to‑base junction for strength.
  - **Fallback if needed**: If 44.8° proves marginal on a given printer,
    add a short vertical section (z = 3 to z = 8) before angling inward.
    The angled section then has horizontal span 56.57 mm, vertical rise
    52 mm, angle = atan(56.57/52) = 47.4° — worse for the angled span
    alone, but the vertical section prints perfectly and the total strut
    length is unchanged. The better mitigation is a slightly larger base
    (e.g., 85 × 85 with struts starting 5 mm inward from corners:
    horizontal span 52.33 mm, rise 57 mm, angle = 42.6°).

### Vertical Clearance Verification

**Candle holder** (block 19.05 × 19.05 × 19.05 mm):
- Block sits in a 1.5 mm deep recess in the replaceable plate.
- Plate top at z = 3 mm; recess floor at z = 1.5 mm.
- Block bottom at z = 1.5 mm; block top (face with holes) at z = 20.55 mm.
- Clearance to collar bottom: 60 − 20.55 = **39.45 mm**.
- Tap above face: 33.5 mm (13 mm shank + 20.5 mm excess cutting).
- Headroom: **5.95 mm**. ✓

**Apex connector** (square pyramid, base 50.8 × 50.8, height 35.92 mm):
- Sits in a tilted cradle. Face is horizontal at z = 3 + 20.735 = 23.735 mm
  (see Apex Cradle Geometry section below).
- Clearance to collar bottom: 60 − 23.735 = **36.265 mm**.
- Tap above face: 33.5 mm.
- Headroom: **2.765 mm**. ✓

## Design — Candle Holder Plate

### Plate 1: Candle Holder (1 plate, exported as `jig_candle_holder_plate.step`)

- 60 × 60 × 3 mm plate with 4 mm keying tab.
- A square recess in the plate top surface to locate the candle holder block:
  - Recess size: 19.3 × 19.3 mm (0.25 mm clearance on the 19.05 mm block).
  - Recess depth: 1.5 mm.
  - **Recess center offset from plate center: (−6.525, −6.525) mm.**
- **Usage**: The plate is keyed and does NOT rotate. The user places the
  candle holder block in the recess, rotating the **block itself** 90° in
  the recess to access different holes. Proof:

  | Holder rotation | Holder hole at plate (6.525, 6.525) | World XY |
  | --------------- | ----------------------------------- | -------- |
  | 0°              | hole (6.525, 6.525)                 | (0, 0) ✓ |
  | 90°             | hole (6.525, −6.525) → rotate → (6.525, 6.525) | (0, 0) ✓ |
  | 180°            | hole (−6.525, −6.525) → rotate → (6.525, 6.525) | (0, 0) ✓ |
  | 270°            | hole (−6.525, 6.525) → rotate → (6.525, 6.525) | (0, 0) ✓ |

  Rotation formula: rotate((hx, hy), α) where α = 0/90/180/270°.
  For α = 90°: (−hy, hx) = (6.525, 6.525) → hx = 6.525, hy = −6.525. ✓

- The block is lifted out, rotated, and dropped back in for each hole.
  (The recess is only 19.3 mm — the block's 26.94 mm diagonal would not
  clear during in-place rotation.)

## Design — Apex Connector Plates

### Apex Connector Geometry (reference)

From `src/main.py`:
- `connector_width` = 2.0 × 25.4 = **50.8 mm** (square base).
- Connector height `h` = (50.8 / 2) × √2 = **35.921 mm**.
- The connector is a regular square pyramid: 4 identical triangular faces.
- Face dihedral angle with base: acos(1/√3) ≈ **54.7356°**.
- Face slant height (apex to base edge midpoint): √(25.4² + 35.921²) =
  **43.988 mm**.
- Two M2 tapped holes on each face, at distances **15 mm** and **25 mm**
  from the apex along the face centerline (apex → base edge midpoint).
  (See `main.py` line 87: `Locations((0, 15), (0, 25))` on the face plane.)

### Apex Cradle Geometry (resolved)

The cradle holds the connector with one triangular face horizontal. This
requires tilting the connector by θ = acos(1/√3) = 54.7356°.

Define the tilt: rotate the connector around the X‑axis by +θ (right‑hand
rule). In the connector's natural frame (base center at origin, base on XY
plane, apex at z = h), the face on the +Y side (Face +Y) becomes horizontal.

**Exact values:**
```
θ  = acos(1/√3) = acos(√3/3)
sin θ = √(2/3) ≈ 0.81649658   (exact: (√6)/3)
cos θ = √(1/3) ≈ 0.57735027   (exact: (√3)/3)
h  = 25.4 × √2 ≈ 35.9214
```

After tilting (rotation around X by +θ), in world coordinates with base
center at origin:

| Point                    | x         | y                          | z               |
| ------------------------ | --------- | -------------------------- | --------------- |
| Base center              | 0         | 0                          | 0               |
| Apex                     | 0         | −h·sin θ = **−29.322**     | h·cos θ = **20.735** |
| Face +Y base edge mid    | 0         | 25.4·cos θ = **14.664**    | 25.4·sin θ = **20.735** |

Face +Y is horizontal at z = 20.735 mm. Its centerline runs along the
Y‑axis from apex (y = −29.322) to base edge midpoint (y = +14.664).

**Hole positions** (distance d from apex along face centerline):

| Hole  | x   | y = −29.322 + d   | z       |
| ----- | --- | ----------------- | ------- |
| 15 mm | 0   | **−14.322**       | 20.735  |
| 25 mm | 0   | **−4.322**        | 20.735  |

**Cradle position on the replaceable plate:**

The plate sits at z = 3 mm (frame base top). The connector base center
should be placed at z = 3 mm. The cradle pocket holds the base. To align
a hole under the collar at (0, 0, z_collar), the base center is offset
in Y:

| Plate            | Hole world target | Base center Y offset  | Hole world position        |
| ---------------- | ----------------- | --------------------- | -------------------------- |
| apex_plate_15    | (0, 0)            | +14.322 mm            | (0, −14.322 + 14.322) = (0, 0) ✓ |
| apex_plate_25    | (0, 0)            | +4.322 mm             | (0, −4.322 + 4.322) = (0, 0) ✓  |

**Cradle pocket design:**

The pocket is a square cutout tilted at 54.7356° around the X‑axis,
carved into the 3 mm thick replaceable plate. The pocket floor plane:
- Origin: (0, y_base, 3) in frame coords (where y_base = 14.322 or 4.322).
- x_dir = (1, 0, 0) — the tilt axis (horizontal).
- z_dir = (0, sin θ, cos θ) = (0, 0.8165, 0.5774) — normal to the tilted
  floor, pointing "upward" from the floor toward the apex direction.

The pocket is a 51.0 × 51.0 mm square (0.2 mm clearance on each side of
the 50.8 mm base) on this tilted plane, extruded downward into the plate.
Extrusion depth: 5 mm perpendicular to the tilted floor (ensuring the
connector base seats fully below the plate surface).

**Rotating to access other faces:**

After tapping a hole on one face, the user removes the connector, rotates
it 90° around the connector's central axis, and re-inserts it into the
cradle. Proof that the next face becomes horizontal:

The connector's central axis (base center → apex) is at angle θ from
vertical. Rotating the connector 90° around this axis in the cradle
(which is equivalent to rotating the connector 90° around Z in its natural
frame, then re‑applying the tilt) maps Face +Y to Face +X. Since the cradle
is symmetric under this rotation (the pocket is a square, and the tilt
axis remains X), Face +X ends up horizontal at the same z = 20.735 mm,
and its centerline points in the same Y‑direction. The 15 mm (or 25 mm)
hole on Face +X is at the same (0, y_hole, 20.735) world position as on
Face +Y. ✓

All 4 faces are accessible by removing, rotating 90°, and re‑inserting.
One plate covers all 4 faces for a given hole distance.

### Plate 2: Apex Connector — 15 mm hole (exported as `jig_apex_plate_15.step`)

- 60 × 60 × 3 mm plate with 4 mm keying tab.
- Tilted square pocket, 51.0 × 51.0 mm, 5 mm deep perpendicular to floor.
- Pocket center at plate (0, 14.322) in frame XY.

### Plate 3: Apex Connector — 25 mm hole (exported as `jig_apex_plate_25.step`)

- Same as Plate 2, but pocket center at plate (0, 4.322).

## Strut-to-Collar Junction

- **Strut profile**: circle, 3.0 mm radius (6 mm diameter).
- **Sweep path**: line segment from corner point to (0, 0, 60) — the collar
  center at the collar's bottom plane. The collar body (9 mm OD = 4.5 mm
  radius) fully contains the 3 mm radius strut at the junction, so a
  boolean union produces a smooth merge.
- **Build123d approach**: Create 4 line segments (`Edge.make_line`), sweep
  a `Circle(3.0)` along each, union with the collar cylinder and base plate.
- **No fillets needed** at the collar end (union handles it). A fillet of
  radius 2 mm at each base corner where the strut meets the base plate
  reduces stress concentration. Use `fillet()` on the edge loops at the
  strut–base intersections.

## Updated Implementation Steps

### Pre‑requisite: Geometry Constants

In `src/jig.py`, compute these values from existing `manora_parameters.py`
imports:

```python
CONNECTOR_WIDTH = 2.0 * INCH_MM           # 50.8
CONNECTOR_HEIGHT = CONNECTOR_WIDTH / 2 * sqrt(2)  # 35.921
CANDLE_HOLDER_SIZE = 0.75 * INCH_MM       # 19.05
M2_HOLE_OFFSET = CANDLE_HOLDER_SIZE / 2 - 3.0  # 6.525
TILT_ANGLE_RAD = acos(1 / sqrt(3))        # 54.7356° in radians
TILT_SIN = sqrt(2 / 3)
TILT_COS = sqrt(1 / 3)

# Apex geometry after tilt
APEX_Y = -CONNECTOR_HEIGHT * TILT_SIN     # -29.322
APEX_Z = CONNECTOR_HEIGHT * TILT_COS      # 20.735

# Cradle offsets for each plate
APEX_15_OFFSET_Y = -(APEX_Y + 15)         # +14.322
APEX_25_OFFSET_Y = -(APEX_Y + 25)         # +4.322
```

### Step 1: Add tap dimensions to `manora_parameters.py`

```python
M2_TAP_SHANK_DIAMETER_MM = 3.0
M2_TAP_SHANK_LENGTH_MM = 13.0
M2_TAP_TOTAL_LENGTH_MM = 43.5
```

### Step 2: Create `src/jig.py`

Build order within the file:
1. `create_frame()` — base plate (80 × 80 × 3) with 60 × 60 × 3 pocket and
   4 mm key slot; collar cylinder (9 mm OD, 3.2 mm ID, z = 60 to 72); 4
   swept struts (6 mm diameter circle, corner to collar center).
2. `create_candle_holder_plate()` — 60 × 60 × 3 plate with 4 mm key tab;
   19.3 × 19.3 × 1.5 mm recess centered at (−6.525, −6.525) from plate
   center. Pocket floor at z = 1.5 (plate‑local).
3. `create_apex_plate(y_offset)` — parameterized: 60 × 60 × 3 plate with
   4 mm key tab; tilted square pocket (51.0 × 51.0, 5 mm deep perpendicular
   to tilted floor) centered at (0, y_offset). Uses a workplane at angle
   θ = 54.7356° around X‑axis. Two instances: `create_apex_plate(14.322)`
   and `create_apex_plate(4.322)`.
4. `create_assembly()` — combines all components in their working positions.
5. `main()` — CLI with `-o`/`--outdir` (default `manufacture`) and `-s`/`--show`.

### Step 3: Output files

| File                          | Description                  |
| ----------------------------- | ---------------------------- |
| `manufacture/jig_frame.step`              | Frame + collar + struts      |
| `manufacture/jig_candle_holder_plate.step`| Plate for candle holder      |
| `manufacture/jig_apex_plate_15.step`      | Plate for apex 15 mm hole    |
| `manufacture/jig_apex_plate_25.step`      | Plate for apex 25 mm hole    |
| `manufacture/jig_assembly.step`           | All components in place      |

### Step 4: `--show` component names

| Name                   | Description                              |
| ---------------------- | ---------------------------------------- |
| `frame`                | Frame with collar and struts             |
| `candle_holder_plate`  | Plate for candle holder block            |
| `apex_plate_15`        | Plate for apex 15 mm hole                |
| `apex_plate_25`        | Plate for apex 25 mm hole                |
| `assembly`             | All components together                  |
