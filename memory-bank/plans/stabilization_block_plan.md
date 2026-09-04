# Stabilization Block Plan

## Objective

Design a 3D-printed stabilization block that holds apex and equatorial connectors
with one slanted face horizontal and flat, providing a stable platform for
hand-tapping M2 holes. The block is a standalone tool — not part of the collar jig.

A single block serves all four faces of a connector by rotating it 90° between
tappings. A screwdriver pop-out hole in the bottom of the block ejects the
connector after use.

## Design Approach — Bounding Box Subtract (Variant B)

The solid connector body (no holes) is tilted around the X-axis by
θ = acos(1/√3) ≈ 54.74° so that Face +Y becomes horizontal (normal pointing
straight up). An axis-aligned box is constructed around the tilted connector
with small margins on all sides. The oversized connector is subtracted from the
box, leaving a connector-shaped cavity. The cavity opening at the top of the
block is the triangular Face +Y profile, flush with the block's flat top surface.

When a real connector is placed in the cavity, Face +Y sits flush with the block
top, held horizontal and stable. The block's flat bottom sits securely on a
workbench.

## Reference — Connector Geometry (from `src/main.py`)

| Parameter                 | Value                          |
| ------------------------- | ------------------------------ |
| Base width                | 2.0 × 25.4 = **50.8 mm**       |
| Pyramid height            | (50.8 / 2) × √2 = **35.921 mm** |
| Base thickness            | 0.25 × 25.4 = **6.35 mm**      |
| Face dihedral angle       | acos(1/√3) ≈ **54.7356°**      |
| Slant height              | √(25.4² + 35.921²) ≈ **44.0 mm** |
| M2 hole positions (per face) | 15 mm and 25 mm from apex (along face centerline) |
| Starter candle hole (apex only) | 35 mm from apex (along face centerline) |

The solid form (without holes) is identical for apex and equatorial connectors.
Both use the same stabilization block.

## Reference — Tilted Connector Extents

After tilting the connector around X by θ with its base center at origin:

```
sin θ = √(2/3) ≈ 0.8165
cos θ = √(1/3) ≈ 0.5774
```

| Point                | X range | Y range                | Z range              |
| -------------------- | ------- | ---------------------- | -------------------- |
| Base corners (±25.4) | ±25.4   | ±25.4                  | −6.35 to 0           |
| Apex                 | 0       | −h·sin θ = **−29.32**  | h·cos θ = **+20.74** |
| Face +Y base edge    | 0       | 25.4·cos θ = **+14.66** | h·cos θ = **+20.74** |

Axis-aligned extents of the tilted connector body:

| Axis | Min      | Max       | Span    |
| ---- | -------- | --------- | ------- |
| X    | −25.4    | +25.4     | 50.8    |
| Y    | −35.67   | +25.4     | 61.07   |
| Z    | −6.35    | +20.74    | 27.09   |

(Face +Y is horizontal at Z = +20.74.)

## Design — Block Dimensions

### Tolerance

The cutter is oversized by adding tolerance to the connector dimensions:

| Dimension       | Nominal     | With tolerance (0.2 mm) |
| --------------- | ----------- | ----------------------- |
| Base width      | 50.8 mm     | 51.2 mm                 |
| Pyramid height  | 35.92 mm    | 36.12 mm                |
| Base thickness  | 6.35 mm     | 6.55 mm                 |
| Apex "point"    | 0.001 mm²   | 0.40 × 0.40 mm²         |

A small apex square (rather than a 0.001 mm point) prevents a razor-sharp cavity
tip that would be fragile when 3D printed and hard to clean.

An apex height increase of 0.2 mm is added: the apex square is placed at Z = h + 0.2 mm.

### Bounding Box

The box is constructed around the tilted, oversized connector with **3 mm margins**
on each side (6 mm total extra per dimension):

- X: 51.2 + 6.0 = **57.2 mm** (≈ 58 mm after rounding up for clean dims)
- Y: 61.5 + 6.0 = **67.5 mm** (≈ 68 mm)
- Z: 27.5 + 3.0 (bottom) + 3.0 (top margin above cavity) = **33.5 mm** (≈ 34 mm)

Final block: approximately **58 × 68 × 34 mm**.

The box is positioned so that the cavity opening is flush with the block top at
Z_box_top = +20.74 + 0.2 (apex tolerance) + margin ≈ +23.94 mm.

### Block Top Surface

After subtracting the oversized connector, the block top is a flat rectangle
with a triangular cutout — the opening to the cavity. When a connector is seated,
Face +Y is flush with this top surface and perfectly horizontal.

### Screwdriver Pop-out Hole

A cylindrical hole, **8 mm diameter**, drilled vertically from the bottom of the
block (Z = Z_box_bottom) through to intersect the bottom of the cavity (the cavity
floor is at approximately Z = −6.55, the bottom of the connector base).

The hole is positioned at the block's XY center (0, 0) — this lands near the
center of the cavity floor, directly under where the connector base sits.

A flathead screwdriver inserted through this hole pushes the connector up and
out of the cavity. The hole is large enough for a standard flathead screwdriver
(typical blade width 6–8 mm).

## Design — Usage

1. Place the stabilization block on a workbench (flat bottom).
2. Drop an apex or equatorial connector into the cavity. Face +Y of the
   connector is now horizontal and flush with the block top. The M2 holes at
   15 mm and 25 mm from the apex are visible and accessible.
3. Hand-tap the M2 holes using a tap with T-handle.
4. Rotate the connector 90° in the cavity to access the next face. Tap again.
5. Repeat for all four faces.
6. Insert a screwdriver through the bottom pop-out hole to eject the connector.

## Implementation Steps

### Pre-requisite: Shared Solid Connector Function

`create_solid_connector()` currently exists in `src/jig.py` (lines 216–241).
It produces a solid connector body without holes. This function will be
extracted to a shared location — either left in `jig.py` and imported by the
new program, or moved to a dedicated module (e.g., `src/connector_geometry.py`).

The function signature will be extended to accept a `tolerance` parameter:

```python
def create_solid_connector(tolerance: float = 0.0) -> Part:
```

When `tolerance > 0`:
- Base square: `CONNECTOR_WIDTH + 2 * tolerance`
- Apex square: `2 * tolerance` × `2 * tolerance` at Z = `CONNECTOR_HEIGHT + tolerance`
- Base extrude amount: `-(base_thickness + tolerance)`

### Step 1: Create `src/stabilization_block.py`

New standalone program with the following components:

1. **Imports**: build123d, math, argparse, os, sys. Import parameters from
   `manora_parameters.py`. Import `create_solid_connector` from `jig.py`.

2. **`create_stabilization_block(tolerance: float = 0.2) -> Part`**:
   - Create the oversized solid connector via `create_solid_connector(tolerance)`.
   - Apply tilt rotation around X-axis: `Location((0,0,0), (TILT_ANGLE_DEG, 0, 0))`.
   - Compute the axis-aligned bounding box of the tilted solid.
   - Build a box with 3 mm margins on each side enclosing the tilted solid.
   - Subtract the tilted oversized connector from the box.
   - Add the screwdriver pop-out hole: a vertical cylinder (8 mm diameter) from
     the block bottom up through the cavity floor. Height spans from the block's
     bottom Z to approximately Z = −3 mm (mid-cavity below the connector base),
     ensuring it clears the cavity floor.
   - Label the part and return it.

3. **`main()`**: CLI with `-o`/`--outdir` (default `manufacture`) and
   `-t`/`--tolerance` (default `0.2`) and `-s`/`--show`.

### Step 2: Output Files

| File                                     | Description                          |
| ---------------------------------------- | ------------------------------------ |
| `manufacture/stabilization_block.step`   | Stabilization block for all connectors |

A single STEP file is generated — the same block works for both apex and
equatorial connectors since their solid forms are identical.

### Step 3: `--show` Component Names

| Name   | Description            |
| ------ | ---------------------- |
| `block`| Stabilization block    |

## Verification Checklist

- [ ] Top face of cavity is flush with block top surface (Face +Y horizontal).
- [ ] Connector seats fully in cavity with clearance from tolerance.
- [ ] Cavity walls have 0.2 mm clearance on all four slanted faces.
- [ ] Connector can be removed by pushing through the screwdriver hole.
- [ ] Block has a flat bottom that sits stably on a surface.
- [ ] Rotating the connector 90° presents a different face at the top.
- [ ] The same block accepts both apex and equatorial connectors.
- [ ] STEP file exports successfully.
