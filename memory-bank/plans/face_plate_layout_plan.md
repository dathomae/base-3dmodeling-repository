# Face Plate Layout Refactor Plan

## Objective

Refactor the menorah face-plate builder so the placement of regular candle
holes is driven by a pluggable "layout" strategy instead of being hard-coded
inside `create_face_plate()`. The existing arrangement is preserved under the
name **`circular`**, and `main.py` gains a `--layout` command-line parameter.

The refactor keeps constant for every layout:

- face size, position, and taper (triangle geometry),
- the samash (starter) candle hole,
- the apex/equatorial connector screw holes at the three vertices.

What varies between layouts is only:

- where the regular candle holes are centered (returned by the layout),
- the candle hole diameter (`candle_hole_diameter`, always circular),
- whether M2 screw holes are cut around each candle holder (`screw_holes`).

## Design

### New module: `src/face_plate_layouts.py`

Introduces a small Strategy hierarchy with a registry (no factory class), per
the agreed design:

```python
from abc import ABC, abstractmethod
from manora_parameters import CANDLE_HOLE_DIAMETER_MM

class FaceLayout(ABC):
    name: str = ""
    candle_hole_diameter: float = CANDLE_HOLE_DIAMETER_MM  # 8.75 mm
    screw_holes: bool = True

    @abstractmethod
    def candle_positions(self, num_candles: int) -> list[tuple[float, float]]:
        """Return (x, y) candle centers in face-plate coordinates."""
```

- `candle_positions()` is the **only** abstract method — the layout's sole job
  is to answer "where".
- `candle_hole_diameter` and `screw_holes` are data attributes with defaults on
  the base class, so the current behavior is unchanged and future layouts
  (e.g. a half-inch wooden variant with no screws) override only these.
- The M2 screw-hole offset is **not** part of the layout. It is derived in the
  shared builder from `candle_holder_width` (0.75"), since the screw pattern is
  a property of the holder footprint, independent of the layout.

`CircularLayout` reproduces the exact current placement logic (including the
special cases for 1, 2, 3, and 4 candles) verbatim:

```python
class CircularLayout(FaceLayout):
    name = "circular"
    circle_radius = 28.0      # moved from main.py
    circle_center_y = 40.5    # moved from main.py

    def __init__(self, triangle_height: float):
        self.triangle_height = triangle_height

    def candle_positions(self, num_candles):
        # exact copy of the current loop in create_face_plate()/main():
        #   num_candles == 1 -> centroid (0, triangle_height / 3)
        #   num_candles == 2 -> horizontal pair at +-circle_radius
        #   num_candles == 3 -> circle + 0.05 * triangle_height
        #   num_candles == 4 -> circle rotated 45deg + 0.10 * triangle_height
        #   else             -> plain circle
```

`triangle_height` is passed to the constructor because it is face geometry
shared with the plate builder, not a layout-specific constant.

Registry and lookup (used to build the `--layout` CLI choices):

```python
LAYOUTS = {"circular": CircularLayout}

def create_layout(name: str, **params) -> FaceLayout:
    try:
        cls = LAYOUTS[name]
    except KeyError:
        raise ValueError(
            f"Unknown layout {name!r}. Available: {sorted(LAYOUTS)}"
        )
    return cls(**params)
```

### `create_face_plate(num_candles, layout)` — `src/main.py`

Becomes a generic builder that reads the layout's attributes:

1. Build the triangle body (sketch + tapered extrude) — **unchanged**.
2. Cut connector M2 holes at the three vertices — **unchanged**.
3. Cut the starter candle hole — **unchanged**.
4. For each `(cx, cy)` in `layout.candle_positions(num_candles)`:
   - cut a circular candle hole of radius `layout.candle_hole_diameter / 2`
     (through the plate),
   - if `layout.screw_holes` is truthy, cut the 4 M2 clearance holes and
     countersinks at `(cx ± offset, cy ± offset)`, where
     `offset = candle_holder_width / 2 - 3.0`.

The per-candle hole and M2-hole loops currently at lines 150–207 are replaced
by the step-4 logic; the connector-hole and starter-hole code is untouched.

### `main()` — `src/main.py`

1. Add the CLI argument:
   `--layout`, default `"circular"`, `choices=sorted(LAYOUTS)`.
2. Instantiate the layout once:
   `layout = create_layout(args.layout, triangle_height=triangle_height)`.
3. Pass it to `create_face_plate(i, layout)`.
4. Replace the duplicated candle-position computation in the assembly loop
   (lines 334–351) with `layout.candle_positions(num_candles)` so the placed
   candle holders always match the plate holes.
5. Remove the now-moved module constants `circle_radius` and `circle_center_y`
   from `main.py`.

Face-plate output filenames include the layout name so faces from different
layouts can be kept apart: `face_plate_{layout}_{i}.step` (e.g.
`face_plate_circular_1.step`). The component keys used by `--show` remain
`face_plate_1` … `face_plate_8`.

## Implementation Steps

### Step 1: Capture a pre-refactor baseline

Run the current `python src/main.py` and keep the generated
`manufacture/face_plate_*.step` files (or their bounding-box/volume figures)
as the reference for the `circular` layout. These are the "before" artifacts
used to prove geometric equivalence in Step 5.

### Step 2: Create `src/face_plate_layouts.py`

Add the module with:

1. `FaceLayout` ABC (as designed above).
2. `CircularLayout` with `candle_positions()` implementing the exact current
   placement logic, including the 1/2/3/4 special cases, with a brief comment
   documenting each special case.
3. `LAYOUTS` registry and `create_layout()` factory function.

### Step 3: Refactor `create_face_plate()` in `src/main.py`

1. Change the signature to `create_face_plate(num_candles, layout)`.
2. Keep the triangle body, connector holes, and starter hole unchanged.
3. Replace the per-candle hole and M2-hole loops with the generic
   layout-driven logic (candle hole radius from `layout.candle_hole_diameter`,
   M2 holes guarded by `layout.screw_holes`).

### Step 4: Refactor `main()` in `src/main.py`

1. Add the `--layout` argument (`choices=sorted(LAYOUTS)`, default
   `"circular"`).
2. Instantiate the layout once and thread it into `create_face_plate()`.
3. Replace the assembly-loop candle-position code with
   `layout.candle_positions(num_candles)`.
4. Remove the moved constants `circle_radius` and `circle_center_y`.
5. Import `create_layout` and `LAYOUTS` from `face_plate_layouts`.
6. Build the face-plate export filename as
   `face_plate_{layout.name}_{i}.step` (e.g. `face_plate_circular_1.step`).

### Step 5: Verify

1. Run `python src/main.py --layout circular` and confirm the output
   `face_plate_circular_*.step` files are geometrically identical to the
   Step 1 baseline (no change to the `circular` output — only the filenames
   differ).
2. Run with an invalid layout name and confirm a clear error listing valid
   choices.
3. Confirm `--show face_plate_N` still works for the circular layout.

### Step 6: Update memory-bank documentation

The refactor introduces a new concept (selectable face-plate layouts) and
changes how the code is organized, so the following docs are updated to match:

1. **`memory-bank/design/design.md`**
   - Reframe the "Candle Arrangement" section (currently lines 54–61) as the
     default **`circular`** layout, keeping the existing placement values
     (circle center 40.5 mm from base, radius 28.0 mm, plus the 1/2/3/4
     special cases).
   - Add a note to the Face Plate part (part #1) that the regular-candle hole
     pattern is now selected by a `--layout` option, with `circular` as the
     current layout; mention the two per-layout knobs (`candle_hole_diameter`,
     `screw_holes`) that future layouts (e.g. a half-inch wooden variant)
     override.

2. **`memory-bank/requirements.md`**
   - Generalize Functional Requirement #4 ("Candle Arrangement") to state the
     arrangement is selectable per layout, with `circular` as the default
     (the circle arrangement remains the current requirement).

3. **`memory-bank/context.md`**
   - Add this refactor as an active task at the start of execution and mark it
     completed (or remove it) when done, per the standard task discipline.

Not changed: `brief.md` (high-level physical overview — still accurate) and
`terms.md`/`concepts.md` (currently hold unrelated/stale bee-house content and
are out of scope for this refactor).

## Verification Checklist

- [ ] `create_face_plate()` no longer contains any candle-position math; it
      delegates to `layout.candle_positions()`.
- [ ] The assembly loop uses `layout.candle_positions()`, not inline math.
- [ ] `circle_radius` and `circle_center_y` no longer exist as module-level
      constants in `main.py`.
- [ ] `python src/main.py --layout circular` produces output identical to the
      pre-refactor baseline.
- [ ] An invalid `--layout` value fails with a clear error naming valid choices.
- [ ] All STEP files still export, with face plates named
      `face_plate_{layout}_{i}.step` (connectors, holders, assembly unchanged).
- [ ] `memory-bank/design/design.md` reflects the selectable-layout mechanism and
      renames the candle arrangement to the `circular` layout.
- [ ] `memory-bank/requirements.md` generalizes the candle-arrangement
      requirement to allow selectable layouts.
- [ ] `memory-bank/context.md` records the task at start and clears it on
      completion.
