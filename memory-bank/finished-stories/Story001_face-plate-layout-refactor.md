# Story001: Face Plate Layout Refactor

## Goal

Refactor the menorah face-plate builder so the placement of regular candle holes is driven by a pluggable **layout** strategy instead of being hard-coded inside `create_face_plate()` in `src/main.py`. The existing arrangement is preserved under the name **`circular`**, and `main.py` gains a `--layout` command-line parameter (`circular` as the default) so future face-plate variants (for example, a half-inch wooden layout with no screws) can be added without touching the shared builder.

The refactor keeps constant for every layout:

- face size, position, and taper (the triangle geometry),
- the samash (starter) candle hole,
- the apex/equatorial connector screw holes at the three vertices.

What varies between layouts is only:

- where the regular candle holes are centered (returned by the layout),
- the candle hole diameter (`candle_hole_diameter`, always circular),
- whether M2 screw holes are cut around each candle holder (`screw_holes`).

This story is driven by the approved plan `memory-bank/plans/face_plate_layout_plan.md`.

## References

Links are relative to the `memory-bank` directory:

- [Face Plate Layout Refactor Plan](../plans/face_plate_layout_plan.md)
- [Design](../design/design.md)
- [Requirements](../requirements.md)

## Dependencies

None — this is the first story for the face-plate layout refactor. The plan is already approved, and no other story must complete before work on this one can begin.

## Dependent Stories

None.

## Tasks

### Task Sizing

The architect-for-story-planning reviewed the decomposition and sizing of every task. No task qualifies for the `[Small]` annotation (the 2-file or narrow-scope thresholds are not met):

- **Task 1** and **Task 4** are run-only verification/setup tasks whose real complexity is in STEP bounding-box/volume comparison reasoning and baseline validity, not in a small code change.
- **Task 2** lays down new code infrastructure (a new module introducing an ABC, a concrete class, a registry, and a factory) plus a test file — a new abstraction another task consumes.
- **Task 3** is a single-file but multi-concern coordinated refactor of `src/main.py` (signature change, hole-loop replacement, CLI wiring, assembly-loop replacement, constant removal, filename changes).
- **Task 5** touches three files and is doc editing — it should be routed to the tech-writer, not a code agent.

All coding tasks therefore route to `code-for-story-implementor` (or the tech-writer for Task 5), never to `small-code-for-story-implementor`.

### Task 1: Capture the pre-refactor `circular` baseline — Completed

1. Capture the pre-refactor `circular` baseline - Not Started
   a. Run `source venv/bin/activate && python src/main.py` with the current, un-refactored code to regenerate `manufacture/face_plate_1.step` … `manufacture/face_plate_8.step`. (If the existing Aug 11 build of these files is confirmed current, they may be preserved instead of regenerated; the goal is an accurate pre-refactor reference.)
   b. Record the bounding box and volume of each `face_plate_N.step` (for `N` = 1..8) into a baseline reference file, for example `manufacture/face_plate_baseline.md`, using a small build123d inspection snippet. Task 4 uses these figures to prove geometric equivalence of the post-refactor `circular` layout. Do not modify any source files.

### Task 2: Create the layout strategy module (test-first) — Completed

1. Create the layout strategy module (test-first) - Not Started
   a. Write `tests/test_face_plate_layouts.py` using Python's stdlib `unittest` (do **not** add pytest or any new dependency to `requirements.txt`). The test must make `src/` importable (for example, a `sys.path` insertion at the top of the file, because `face_plate_layouts` imports `manora_parameters`). It asserts:
      - `CircularLayout(triangle_height=…)` `candle_positions(num_candles)` returns the exact positions produced by the current `main.py` logic (lines 150–179), including:
        - `num_candles == 1` → a single position at the centroid `(0, triangle_height / 3)`;
        - `num_candles == 2` → a horizontal pair at `(-28.0, 40.5)` and `(28.0, 40.5)`;
        - `num_candles == 3` → three positions on a circle of radius 28.0 centered at y = 40.5, each offset +0.05·`triangle_height` in y;
        - `num_candles == 4` → four positions on the same circle rotated 45°, each offset +0.10·`triangle_height` in y;
        - `num_candles == 5` → five positions on the plain circle (no offset).
        Use `assertAlmostEqual` with a small tolerance. `triangle_height` for the test is `7.0 * 25.4 * math.sqrt(3) / 2`, matching `src/main.py`.
      - The default attribute values on `CircularLayout`: `name == "circular"`, `candle_hole_diameter == CANDLE_HOLE_DIAMETER_MM` (8.75), and `screw_holes is True`.
      - `create_layout("circular", triangle_height=…)` returns a `CircularLayout` instance, and `create_layout("<unknown>")` raises `ValueError` whose message lists the valid choices.
      - Run `source venv/bin/activate && python -m unittest discover -s tests -v` — the tests fail at this point because the module does not yet exist (the TDD red step; this is intended and is not an independent task).
   b. Implement `src/face_plate_layouts.py` per the plan design:
      - `FaceLayout` ABC with class attributes `name = ""`, `candle_hole_diameter = CANDLE_HOLE_DIAMETER_MM`, `screw_holes = True`, and the sole abstract method `candle_positions(self, num_candles) -> list[tuple[float, float]]`.
      - `CircularLayout` with `name = "circular"`, module constants `circle_radius = 28.0` and `circle_center_y = 40.5` (moved from `src/main.py`), a constructor taking `triangle_height`, and a `candle_positions()` method that is an exact copy of the current placement loop in `src/main.py` (including the 1/2/3/4 special cases, each documented with a brief comment).
      - `LAYOUTS = {"circular": CircularLayout}` registry and `create_layout(name, **params)` that raises a `ValueError` naming the valid choices for an unknown name.
      - This module must not import `build123d`; it depends only on `manora_parameters`.
   c. Run `source venv/bin/activate && python -m unittest discover -s tests -v` again — all tests pass (the TDD green step).

### Task 3: Refactor `src/main.py` to consume the layout — Completed

1. Refactor `src/main.py` to consume the layout - Not Started
   a. Change the signature to `create_face_plate(num_candles, layout)`. Keep the triangle-body sketch/extrude, the connector M2 holes, and the starter candle hole exactly unchanged. Remove the per-candle position and M2-position computation (currently lines 150–179) and replace the M2-hole loop and candle-hole loop (currently lines 195–207) with generic layout-driven logic: for each `(cx, cy)` in `layout.candle_positions(num_candles)`, cut a circular candle hole of radius `layout.candle_hole_diameter / 2` through the plate; if `layout.screw_holes` is truthy, also cut the 4 M2 clearance holes and countersinks at `(cx ± offset, cy ± offset)` where `offset = candle_holder_width / 2 - 3.0`.
   b. In `main()`:
      - Add the argparse argument `--layout` with `choices=sorted(LAYOUTS)` and `default="circular"`.
      - Import `create_layout` and `LAYOUTS` from `face_plate_layouts`; remove the now-moved module constants `circle_radius` and `circle_center_y`.
      - Instantiate the layout once with `layout = create_layout(args.layout, triangle_height=triangle_height)` and pass it to every `create_face_plate(i, layout)` call.
      - Replace the duplicated candle-position computation in the assembly loop (currently lines 334–351) with `layout.candle_positions(num_candles)` so the placed candle holders always match the plate holes.
      - Export face plates with the layout name in the filename: `face_plate_{layout.name}_{i}.step` (for example, `face_plate_circular_1.step`). Keep the component keys used by `--show` as `face_plate_1` … `face_plate_8`.
      - Update the existing progress print for each face plate to include the layout name, for example `print(f"Generating Face Plate {i} (layout: {layout.name})...")`, so the active layout is visible in the output (consistent with the existing `print()`-based progress style).
   c. Structural verification: grep `src/main.py` and confirm (i) `create_face_plate` contains no candle-position math — only a call to `layout.candle_positions()`, (ii) `circle_radius` and `circle_center_y` no longer exist, and (iii) the assembly loop uses `layout.candle_positions()`.

### Task 4: Verify geometric equivalence — Completed

1. Verify geometric equivalence - Not Started
   a. Run `source venv/bin/activate && python src/main.py --layout circular` and confirm the exported `manufacture/face_plate_circular_1.step` … `face_plate_circular_8.step` are geometrically identical (same bounding box and volume) to the Task 1 baseline — only the filenames differ from the pre-refactor output.
   b. Run `python src/main.py --layout bogus` (any invalid name) and confirm it fails with a clear error naming the valid choices (`circular`).
   c. Run `python src/main.py --show face_plate_1` and confirm the component key still resolves (the `--show` path is unaffected by the renamed exports).

### Task 5: Update memory-bank documentation — Completed

1. Update memory-bank documentation - Not Started
   a. `memory-bank/design/design.md`: reframe the "Candle Arrangement" section (currently lines 54–61) as the default **`circular`** layout, keeping the existing placement values (circle center 40.5 mm from the base, radius 28.0 mm, plus the 1/2/3/4 special cases). Add a note to the Face Plate part (#1) that the regular-candle hole pattern is now selected by a `--layout` option with `circular` as the current layout, and mention the two per-layout knobs (`candle_hole_diameter`, `screw_holes`) that future layouts (for example, a half-inch wooden variant) override.
   b. `memory-bank/requirements.md`: generalize Functional Requirement #4 ("Candle Arrangement") to state the arrangement is selectable per layout, with `circular` as the default (the circle arrangement remains the current requirement).
   c. `memory-bank/context.md`: add this refactor as an active task at the start of execution and mark it completed (or remove it) when done, per the standard task discipline.

### Parallel Execution

- **Group A: Tasks 1 and 2** — File-disjoint and independent. Task 1 is run-only over `manufacture/face_plate_*.step`; Task 2 creates new files `src/face_plate_layouts.py` and `tests/test_face_plate_layouts.py`. Nothing in the un-refactored `main.py` imports the new module yet, and no existing code references it, so each verifies independently.
- **Group B: Tasks 4 and 5** — File-disjoint and independent. Task 4 is run-only and writes new `manufacture/face_plate_circular_*.step` files; Task 5 edits `memory-bank/design/design.md`, `memory-bank/requirements.md`, and `memory-bank/context.md`. Task 5 documents the settled design and does not consume Task 4's verification output — **Task 5 must not embed any measured bounding-box/volume figures from Task 4** (embedding them would create a hidden dependency and break the parallel group). Contingency: if Task 4's equivalence check fails, the story needs rework and Task 5's docs may need revision.

All other task pairs are sequential (Task 3 depends on both Group A tasks; Tasks 4 and 5 depend on Task 3).

### Execution Order

```
   ┌─────────────┐      ┌─────────────┐
   │  Task 1     │      │  Task 2     │  (Group A — parallel)
   │  (baseline) │      │  (module)   │
   └──────┬──────┘      └──────┬──────┘
          │                    │
          └─────────┬──────────┘
                    ▼
             ┌──────┴──────┐
             │  Task 3     │  (refactor src/main.py — depends on Task 1 AND Task 2)
             └──────┬──────┘
                    │
          ┌─────────┴─────────┐
          │                   │
   ┌──────┴──────┐    ┌───────┴──────┐
   │  Task 4     │    │  Task 5      │  (Group B — parallel)
   │  (verify)   │    │  (docs)      │
   └─────────────┘    └──────────────┘
```

Group A runs in parallel and both tasks must be merged before Task 3 starts (Task 1's baseline must be captured against pre-refactor code; Task 3 consumes Task 2's module). Task 3 must be merged before Group B starts.

### Reintegration

**Group A (Tasks 1 and 2):**
- Merge order: any order (default: Task 1 then Task 2). Task 1 touches only tracked `manufacture/*.step` (content-preserving, run-only); Task 2 adds new `src/` and `tests/` files. No shared files and no shared infrastructure file.
- Integration tests:
  - `source venv/bin/activate && python -m unittest discover -s tests -v` — Task 2's new module tests are green after the merge.
  - `source venv/bin/activate && python src/main.py` — the un-refactored run still succeeds after Task 2's additive files land (Task 2 changes nothing `main.py` imports yet), and Task 1's preserved `manufacture/face_plate_1..8.step` remain byte-identical (they are the baseline Task 4 will compare against).
- Watch for conflicts in: `manufacture/face_plate_1..8.step` (tracked generated outputs — if STEP export is nondeterministic, discard spurious diffs; a diff here is Task 1's preserve-intent, not a cross-task conflict). `venv/` is gitignored and absent from worktrees, so each worktree needs a Python environment with build123d installed before running anything (operational, not a merge conflict).

**Group B (Tasks 4 and 5):**
- Merge order: any order (default: Task 4 then Task 5). Task 4 adds new `manufacture/face_plate_circular_*.step` files; Task 5 edits `memory-bank/*.md`. Fully disjoint.
- Integration tests:
  - `source venv/bin/activate && python src/main.py --layout circular` — regenerates `manufacture/face_plate_circular_*.step`; verify the bounding boxes/volumes of `face_plate_circular_1..8.step` match the Task 1 baseline (the story's equivalence criterion).
  - `source venv/bin/activate && python src/main.py --layout bogus` — confirms the invalid-layout error path exits with a clear error.
  - `source venv/bin/activate && python src/main.py` — confirms the default layout path is unaffected by the refactor; `assembly.step`, `regular_candle_holder.step`, `apex_connector.step`, and the other shared STEPs should remain byte-identical to the Task 1 baseline (no new failures threshold).
- Watch for conflicts in: shared tracked STEPs that a full `main.py` run regenerates alongside the new circular plates (`regular_candle_holder.step`, `apex_connector.step`, `equator_connector.step`, `assembly.step` — discard spurious nondeterministic diffs rather than merging them); `memory-bank/context.md` (edited by Task 5; within this story only Task 5 touches it).

## Test-First Development

This project follows the Logical TDD Lifecycle. For the one coding task that has a natural unit-test target (Task 2), the test-and-implement cycle is integrated inside the task: the failing test is written first (subtask a), then the module is implemented (subtask b), then the tests are run to green (subtask c). The project has no test framework, so Task 2 uses Python's stdlib `unittest` with no new dependency, which introduces the project's first `tests/` directory — a convention change recorded in Constraints below. A `tests/__init__.py` is not required: `python -m unittest discover -s tests` uses namespace-package discovery on modern Python. The remaining verification in this story is run-based (STEP bounding-box/volume comparison) because it exercises `build123d` geometry that is not unit-testable without a heavier harness; that verification is woven into Tasks 1, 3 (structural grep), and 4.

## Constraints

- **Geometric equivalence**: The `circular` layout must reproduce the current arrangement exactly — no change to any hole position, hole diameter, screw pattern, or triangle geometry. Only the face-plate output filenames change.
- **No new dependency**: Use Python's stdlib `unittest` for the new test file. Do **not** add pytest or any other package to `requirements.txt`.
- **Module purity**: `src/face_plate_layouts.py` must not import `build123d`; it depends only on `manora_parameters` (`CANDLE_HOLE_DIAMETER_MM`).
- **Design conformance**: Follow the agreed "strategy with a registry, no factory class" design exactly as specified in the plan (`FaceLayout` ABC, `CircularLayout`, `LAYOUTS` dict, `create_layout()` factory function). The M2 screw-hole offset is derived in the shared builder from `candle_holder_width` (0.75"), not from the layout.
- **Unchanged code**: In `create_face_plate()`, the triangle body, the connector M2 holes, and the starter candle hole are untouched. Component keys for `--show` remain `face_plate_1` … `face_plate_8`.
- **Convention change (documented)**: This story introduces the project's first `tests/` directory and first test file (`tests/test_face_plate_layouts.py`) using stdlib `unittest`. This is the only convention change the story makes; all other code follows existing `src/` conventions.
- **Environment**: The Python virtual environment lives at `venv/`; activate it with `source venv/bin/activate` before running `python` commands.

## Intent

The purpose of each task, stated so the goal remains clear even if implementation details change:

- **Task 1** — Establish a trustworthy pre-refactor reference so the refactor can be proven to preserve the `circular` output.
- **Task 2** — Extract the candle-placement decision into a pure, pluggable, and unit-tested layout strategy module.
- **Task 3** — Make the shared plate builder and the `main()` wiring consume the layout, removing all hard-coded placement math from `src/main.py`.
- **Task 4** — Prove the refactored `circular` layout is geometrically identical to the baseline and that the new `--layout` option behaves correctly.
- **Task 5** — Keep the project's design, requirements, and context documentation consistent with the selectable-layout mechanism.

## Acceptance Criteria

- [ ] `create_face_plate()` in `src/main.py` no longer contains any candle-position math; it delegates to `layout.candle_positions()`.
- [ ] The assembly loop in `main()` uses `layout.candle_positions()`, not inline math.
- [ ] `circle_radius` and `circle_center_y` no longer exist as module-level constants in `src/main.py`.
- [ ] `src/face_plate_layouts.py` exists with `FaceLayout`, `CircularLayout`, `LAYOUTS`, and `create_layout()`, and `python -m unittest discover -s tests -v` passes.
- [ ] `python src/main.py --layout circular` produces `face_plate_circular_1.step` … `face_plate_circular_8.step` geometrically identical (bounding box/volume) to the pre-refactor baseline.
- [ ] An invalid `--layout` value fails with a clear error naming the valid choices.
- [ ] All STEP files still export, with face plates named `face_plate_{layout}_{i}.step` (connectors, holders, and assembly unchanged; `--show face_plate_N` still resolves).
- [ ] `memory-bank/design/design.md` reflects the selectable-layout mechanism and renames the candle arrangement to the `circular` layout.
- [ ] `memory-bank/requirements.md` generalizes the candle-arrangement requirement to allow selectable layouts.
- [ ] `memory-bank/context.md` records the task at start and clears it on completion.

## Requesting Clarification

If at any point during story construction there is confusion or ambiguity about the goal or how to accomplish it, stop and ask the user for clarification.

## Notes

- This story is the first story for this project; the `toc.md` entry was pre-seeded alongside it.
- `memory-bank/terms.md` and `memory-bank/concepts.md` currently hold unrelated/stale bee-house content and are out of scope for this refactor (they are not updated).
- The `--layout` option is validated via argparse `choices`, so an invalid name fails before any geometry is generated.
