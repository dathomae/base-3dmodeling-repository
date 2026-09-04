# Story001 Walkthrough: Face Plate Layout Refactor

This walkthrough records how [Story001: Face Plate Layout Refactor](../../finished-stories/Story001_face-plate-layout-refactor.md) was executed. The story's goal was to replace the hard-coded candle-hole placement math inside `create_face_plate()` in `src/main.py` with a pluggable **layout** strategy. The original arrangement is preserved as the **`circular`** layout, and `main.py` now accepts a `--layout` command-line option with `circular` as the default, so future face-plate variants can be added without touching the shared builder.

The story was driven by the approved plan `memory-bank/plans/face_plate_layout_plan.md`. Each task ran in its own isolated git worktree, was merged back into the feature branch `story/001`, and was verified by integration tests after merging.

## Task 1: Capture the pre-refactor `circular` baseline

Task 1 established a trustworthy pre-refactor reference so the refactor could later be proven to preserve the `circular` output.

- The tracked Aug 11 STEP build of `manufacture/face_plate_1.step` … `manufacture/face_plate_8.step` was confirmed current and preserved byte-identical; the files were not regenerated.
- A small build123d inspection snippet computed the bounding box and volume of each of the 8 plates and recorded them in `manufacture/face_plate_baseline.md`.
- No source files were modified.

## Task 2: Create the layout strategy module (test-first)

Task 2 extracted the candle-placement decision into a pure, pluggable, and unit-tested layout strategy module, following the project's test-first discipline (red → green).

- **Red step:** `tests/test_face_plate_layouts.py` was written first using Python's stdlib `unittest` (no new dependency in `requirements.txt`). The file inserts `src/` into `sys.path` because `face_plate_layouts` imports `manora_parameters`. The tests assert that:
  - `CircularLayout(triangle_height=…)` `candle_positions(num_candles)` returns the exact positions produced by the original `main.py` logic, using `assertAlmostEqual` with a small tolerance: 1 candle at the centroid `(0, triangle_height / 3)`; 2 candles as a horizontal pair at `(-28.0, 40.5)` and `(28.0, 40.5)`; 3 candles on a circle of radius 28.0 centered at y = 40.5 with a `+0.05 · triangle_height` offset; 4 candles on the same circle rotated 45° with a `+0.10 · triangle_height` offset; 5 candles on the plain circle. The test `triangle_height` is `7.0 * 25.4 * math.sqrt(3) / 2`.
  - The default attribute values on `CircularLayout`: `name == "circular"`, `candle_hole_diameter == CANDLE_HOLE_DIAMETER_MM` (8.75), and `screw_holes is True`.
  - `create_layout("circular", triangle_height=…)` returns a `CircularLayout` instance, and `create_layout("<unknown>")` raises a `ValueError` whose message lists the valid choices.
  - Running `python -m unittest discover -s tests -v` at this point fails because the module does not yet exist — the intended TDD red step.
- **Green step:** `src/face_plate_layouts.py` was implemented per the plan design:
  - `FaceLayout` ABC with class attributes `name = ""`, `candle_hole_diameter = CANDLE_HOLE_DIAMETER_MM`, `screw_holes = True`, and the sole abstract method `candle_positions(self, num_candles) -> list[tuple[float, float]]`.
  - `CircularLayout` with `name = "circular"`, module constants `circle_radius = 28.0` and `circle_center_y = 40.5` (moved from `src/main.py`), a constructor taking `triangle_height`, and a `candle_positions()` method that is an exact copy of the original placement loop, including the 1/2/3/4 special cases each documented with a brief comment.
  - A `LAYOUTS = {"circular": CircularLayout}` registry and a `create_layout(name, **params)` factory that raises a `ValueError` naming the valid choices for an unknown name.
  - The module imports no `build123d`; it depends only on `manora_parameters`.
- The test suite was run again and all 8 tests passed — the TDD green step.

## Task 3: Refactor `src/main.py` to consume the layout

Task 3 made the shared plate builder and the `main()` wiring consume the layout, removing all hard-coded placement math from `src/main.py`.

- The signature changed to `create_face_plate(num_candles, layout)`. The triangle-body sketch/extrude, the connector M2 holes, and the starter candle hole were kept exactly unchanged.
- The per-candle position and M2-position computation (originally lines 150–179) was removed, and the M2-hole loop and candle-hole loop (originally lines 195–207) were replaced with generic layout-driven logic: for each `(cx, cy)` in `layout.candle_positions(num_candles)`, a circular candle hole of radius `layout.candle_hole_diameter / 2` is cut through the plate; if `layout.screw_holes` is truthy, the 4 M2 clearance holes and countersinks are also cut at `(cx ± offset, cy ± offset)` where `offset = candle_holder_width / 2 - 3.0`.
- In `main()`:
  - Added the argparse argument `--layout` with `choices=sorted(LAYOUTS)` and `default="circular"`.
  - Imported `create_layout` and `LAYOUTS` from `face_plate_layouts` and removed the moved module constants `circle_radius` and `circle_center_y`.
  - Instantiated the layout once with `layout = create_layout(args.layout, triangle_height=triangle_height)` and passed it to every `create_face_plate(i, layout)` call.
  - Replaced the duplicated candle-position computation in the assembly loop with `layout.candle_positions(num_candles)` so the placed candle holders always match the plate holes.
  - Renamed the face-plate exports to `face_plate_{layout.name}_{i}.step` (for example, `face_plate_circular_1.step`), while keeping the component keys used by `--show` as `face_plate_1` … `face_plate_8`.
  - Updated the progress print for each face plate to include the layout name, for example `print(f"Generating Face Plate {i} (layout: {layout.name})...")`.
- Verification used structural greps plus full runs: `create_face_plate` contains no candle-position math (only a call to `layout.candle_positions()`), `circle_radius` and `circle_center_y` no longer exist in `src/main.py`, and the assembly loop uses `layout.candle_positions()`.

## Task 4: Verify geometric equivalence

Task 4 proved that the refactored `circular` layout is geometrically identical to the baseline and that the new `--layout` option behaves correctly.

- `python src/main.py --layout circular` was run, and the exported `manufacture/face_plate_circular_1.step` … `manufacture/face_plate_circular_8.step` were confirmed geometrically identical (same bounding box and volume) to the Task 1 baseline for all 8 plates — only the filenames differ from the pre-refactor output.
- `python src/main.py --layout bogus` was run and confirmed to fail with a clear error naming the valid choices (`circular`).
- `python src/main.py --show face_plate_1` was run and confirmed the component key still resolves — the `--show` path is unaffected by the renamed exports.

## Task 5: Update memory-bank documentation

Task 5 kept the project's design, requirements, and context documentation consistent with the selectable-layout mechanism.

- `memory-bank/design/design.md`: the "Candle Arrangement" section was reframed as the default **`circular`** layout, keeping the existing placement values (circle center 40.5 mm from the base, radius 28.0 mm, plus the 1/2/3/4 special cases). A note was added to the Face Plate part that the regular-candle hole pattern is now selected by the `--layout` option, with the two per-layout knobs (`candle_hole_diameter`, `screw_holes`) that future layouts override.
- `memory-bank/requirements.md`: Functional Requirement #4 ("Candle Arrangement") was generalized to state that the arrangement is selectable per layout, with `circular` as the default.
- `memory-bank/context.md`: the refactor was recorded as an active task at the start of execution and moved to "Recently Completed" when done.
- One minor review-fix iteration was applied after the initial doc commit (commit `101a37c`, "apply minor doc revision feedback").

## Execution notes

- Each task ran in an isolated git worktree at `worktrees/story-001-task-N/`, created off the feature branch.
- **Group A (Tasks 1 and 2)** ran in parallel; both were merged before Task 3 started.
- **Group B (Tasks 4 and 5)** ran in parallel after Task 3 was merged.
- All work was merged into the feature branch `story/001`.
- Integration tests passed after each group: the unittest suite passed 8/8, all `circular` face plates matched the Task 1 baseline bounding box and volume, the invalid-layout path was rejected with a clear error, and the default-layout run was unaffected by the refactor.

## Post-Mortem

The post-mortem for Story001 identified three operational lessons, recorded here and in `memory-bank/lessons-learned.md`.

| Lesson | Description |
|--------|-------------|
| Verify Worktree Branch Before Committing | When a sub-agent works in an isolated git worktree, it MUST verify it is in the correct worktree before committing: check `pwd` (should be the worktree path) and `git rev-parse --abbrev-ref HEAD` (should be the task branch, e.g. `story-001-task-2`) before running `git commit`. During Story001, a sub-agent committed its work to the feature branch (`story/001`) instead of its worktree branch, contaminating the feature branch; recovery required `git reset --hard` plus `git cherry-pick` onto the correct branch. |
| Use the Parent Repo's venv in Git Worktrees | The project's Python virtual environment (`venv/`) is gitignored and therefore absent from git worktrees. Sub-agents working in a worktree must use the parent repo's venv python via its absolute path (e.g. `/home/doug/projects/github/3dmodel/hanukkah-candle/venv/bin/python`) or `source` its `activate` script, rather than creating a new venv in the worktree. |
| Use the worktrees Symlink for Sub-Agent Paths | Sub-agent `workdir` and file paths must use the `worktrees/` symlink (e.g. `worktrees/story-001-task-3`), not the real `.kilo/worktrees/...` path. Paths starting with a dot (`.kilo`) trigger a bug in the tool permissions checker, causing sub-agent tool calls to be rejected. |
