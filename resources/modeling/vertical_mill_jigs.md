# Vertical Mill Jig Mounting

This document is the reference for creating jigs that mount to the vertical mill bed. It ties together the standardized mounting screw, the hole feature cut for it, and the bed's mounting-hole pattern. Consult this file whenever a vertical mill jig is being created.

## Standardized mounting screw

All jigs mount with a single standardized screw, documented in full in [screws.md](screws.md) (section 8):

| Property | Value |
|----------|-------|
| Thread | M5 (coarse, 0.80 mm pitch) |
| Length | 30 mm |
| Thread coverage | Full thread |
| Head style | Flat head (countersunk / conical), hex socket |
| Head diameter | 10 mm |
| Countersink angle | 90° (included, ISO metric standard) |
| Head height (cone depth) | ~2.5 mm |

## Mounting hole feature

Each mounting location gets a countersunk through-hole sized for the screw. The through-hole clears the M5 shank and threads, and the countersink buries the conical head below the working face. In build123d this is a single `CounterSinkHole` operation (see [screws.md](screws.md) section 9):

- Clearance (through-hole) radius: 5.8 / 2 = **2.9 mm**
- Countersink (head) radius: 10 / 2 = **5.0 mm**
- Countersink angle: **90°**

```python
from build123d import *

clearance_radius = 5.8 / 2  # 2.9 mm
head_radius = 10 / 2        # 5.0 mm

with BuildPart() as base:
    Box(50, 50, 4)  # jig base
    with Locations((0, 0, 2)):  # top face
        CounterSinkHole(
            radius=clearance_radius,
            counter_sink_radius=head_radius,
            counter_sink_angle=90,
        )
```

## Jig base thickness

The base must be at least **4 mm** thick. The 90° head cone is ~2.5 mm tall (a 10 mm head over a 5 mm thread), so 4 mm buries the head below the working face with ~1.5 mm of material to spare.

## Bed mounting-hole pattern

The bed's M5 mounting holes form a grid measured from the bed origin at the **lower-left** corner.

| Parameter | Value |
|-----------|-------|
| Columns (x direction) | 7 |
| Rows (y direction) | 5 |
| Left column offset from left edge | 26 mm |
| Bottom row offset from bottom edge | 16 mm |
| Horizontal spacing between column centers | 41 mm |
| Vertical spacing between row centers | 46 mm |

**Exception:** the lower-left hole sits at **38 mm** from the bottom edge (instead of 16 mm); it is 24 mm below the first hole of the second row (y = 62 mm).

The hole centers are:

| y \ x | 26 | 67 | 108 | 149 | 190 | 231 | 272 |
|-------|----|----|-----|-----|-----|-----|-----|
| **200** | (26, 200) | (67, 200) | (108, 200) | (149, 200) | (190, 200) | (231, 200) | (272, 200) |
| **154** | (26, 154) | (67, 154) | (108, 154) | (149, 154) | (190, 154) | (231, 154) | (272, 154) |
| **108** | (26, 108) | (67, 108) | (108, 108) | (149, 108) | (190, 108) | (231, 108) | (272, 108) |
| **62** | (26, 62) | (67, 62) | (108, 62) | (149, 62) | (190, 62) | (231, 62) | (272, 62) |
| **16** | (26, 38) *exception* | (67, 16) | (108, 16) | (149, 16) | (190, 16) | (231, 16) | (272, 16) |

That is 35 holes total: the regular 7 × 5 grid with the lower-left hole relocated from (26, 16) to (26, 38).

## Using the pattern in a jig

To mount a jig, cut a countersunk M5 hole at each bed location the jig covers. The pattern is regular with a single exception, so generate the locations from the parameters above rather than hard-coding 35 coordinates:

```python
def mounting_hole_locations():
    columns = [26 + 41 * i for i in range(7)]
    rows = [16 + 46 * j for j in range(5)]
    locations = [(x, y) for y in rows for x in columns]
    locations[locations.index((26, 16))] = (26, 38)  # lower-left exception
    return locations
```

This helper is the canonical source of the grid. The reusable, importable version of it lives in the package as `scaffold.mill_bed`:

```python
from scaffold.mill_bed import mounting_hole_locations

for x, y in mounting_hole_locations():
    ...
```

Jig programs should import `mounting_hole_locations` from there rather than re-deriving the pattern.
