# Story002: Downward Arc Layout

## Goal

Add the `downward_arc_layout` face-plate candle arrangement (two symmetric circular arcs, 4 per side) with its continuous embossed arc line, per the arc design doc, with unit tests and verification.

The arc arrangement places the regular candles of the densest (8-candle) face on two symmetric, smooth circular arcs — four on the right (R1–R4, bottom to top) and four mirrored on the left (L1–L4) — satisfying the project's spacing (adjacent centers ≥ 1.0 in / 25.4 mm), shamash clearance (≥ 2.5 in / 63.5 mm from the fixed shamash at (0, 117.2)), and equatorial-connector clearance (3 mm) constraints. A face with `n` candles uses the first `n` positions of the 8-candle sequence (right arc bottom-to-top, then left arc bottom-to-top), so every face's candles sit at the same positions as the corresponding candles on the 8-candle face. Every face also carries one **continuous embossed arc line** (a milled groove, 1/8 in = 3.175 mm wide × 1 mm deep, on the outside face) running from the bottom right, up the right candle arc, across the center (tangent bridge), and down the left candle arc to the bottom left. The line is decorative (candle-spacing rules do not apply) and the shamash does not participate.

The new layout is added **alongside** the existing `circular` layout, which remains the default and must be unchanged. `src/main.py` gains only the groove-drawing sweep in `create_face_plate()`; layout selection, the plate builder, and the assembly already consume layouts generically (`--layout choices=sorted(LAYOUTS)`, `create_layout(...)`, `layout.candle_positions(num_candles)`), so registering the layout makes `--layout downward_arc_layout` work for the candle holes with no further wiring.

This story is driven by the approved plan `memory-bank/plans/downward_arc_layout_plan.md`.

## References

Links are relative to the `memory-bank` directory:

- [Downward Arc Layout Plan](../plans/downward_arc_layout_plan.md)
- [Arc-Based Candle Arrangement Design](../design/candle-arrangement-arc.md)
- [Design](../design/design.md)
- [Requirements](../requirements.md)

## Dependencies

- [Story001_face-plate-layout-refactor.md](Story001_face-plate-layout-refactor.md) — introduced the layout strategy infrastructure this story extends: the `FaceLayout` ABC, the `CircularLayout`, the `LAYOUTS` registry, the `create_layout()` factory, and the `--layout` CLI option in `src/main.py` (default `"circular"`). That work is implemented (see the [walkthrough](walkthrough/Story001_face-plate-layout-refactor.md)); this story builds directly on its infrastructure.

## Dependent Stories

None.

## Tasks

### Task Sizing

The architect-for-story-planning reviewed the decomposition and sizing of every task:

- **Task 1** is annotated `[Small]`: 2 files (one new test file + one additively-modified source file), additive to an existing interface, and the plan pins the exact implementation code while the design doc pins the coordinates — no ambiguity for a limited-context agent. The TDD red→green cycle is a single integrated test-then-implement unit.
- **Task 2** is medium: single file, but the build123d sweep geometry (per-segment 3.175 mm × 1.0 mm profile sweeps — one per groove arc, width axis in the face plane and depth toward −z, `Mode.SUBTRACT`; sweeping a joined multi-arc wire shears non-circular profiles at curvature-discontinuous joints, so each arc must be swept separately) is non-trivial and the plan gives prose, not code. Routes to `code-for-story-implementor` (escalation to `big-code-for-story-implementor` if the sweep/boolean geometry proves unstable).
- **Task 3** is medium (run-only): no source edits, but it regenerates full models, compares STEP bounding boxes/volumes against the Story001 baseline, and includes a human sign-off gate for the visual inspection. Routes to `code-for-story-implementor`.
- **Task 4** is a tech-writer task (3 doc files); it is **not** annotated `[Small]` so it is not misrouted to a code agent.

### Task 1: Implement `DownwardArcLayout` with tests (test-first) — Completed [Small]

Architect note (decomposition): kept as one task because the TDD red step (failing tests) is not an independently mergeable deliverable, and splitting the `groove_arcs()` base-class capability from the new class would split the same two files (tests exercise both `CircularLayout`'s inherited default and `DownwardArcLayout`) with overlapping file sets and no isolation benefit. The task is at its natural granularity.

1. Implement DownwardArcLayout with tests (test-first) - Not Started
   a. Write `tests/test_downward_arc_layout.py` (new file) using Python's stdlib `unittest`, following the conventions of `tests/test_face_plate_layouts.py` (a `sys.path` insertion at the top so `src/` is importable; `REPO_ROOT` derived from `__file__`). Do **not** add pytest or any package to `requirements.txt`. The tests assert:
      - **8-candle positions match the design doc**: `candle_positions(8)` equals the eight coordinates of the design doc (right arc R1–R4 then left arc L1–L4; left = mirrors of right), compared with `assertAlmostEqual(..., delta=0.1)` (design values are quoted to 3 decimals):
        - R1 (56.862, 9.525), R2 (31.467, 10.025), R3 (13.426, 27.905), R4 (12.700, 53.295)
        - L1 (−56.862, 9.525), L2 (−31.467, 10.025), L3 (−13.426, 27.905), L4 (−12.700, 53.295)
      - **Count rule (first n of the sequence)**: `candle_positions(n)` equals `candle_positions(8)[:n]` for every n 1–7; specifically `candle_positions(1) == [(56.862, 9.525)]`, `candle_positions(4)` returns R1–R4, and `candle_positions(5)` returns R1–R4 then L1.
      - **Spacing minimum**: for every `num_candles` 1–8 **with at least two positions** (`n == 1` has no pairs — guard the test so `min()` is never computed over an empty sequence), the minimum pairwise distance between positions is ≥ 25.35 mm (the 1.0 in / 25.4 mm requirement with 0.05 mm tolerance for coordinate rounding).
      - **Default attributes**: `name == "downward_arc_layout"`, `candle_hole_diameter == CANDLE_HOLE_DIAMETER_MM`, and `screw_holes is True`.
      - **Registry**: `create_layout("downward_arc_layout", triangle_height=…)` returns a `DownwardArcLayout` instance, and `create_layout("<unknown>")` raises `ValueError` whose message lists **both** `circular` and `downward_arc_layout`.
      - **Groove arcs**: `groove_arcs(n)` returns the same continuous path for every n 1–8: three arc definitions — `(R1, R3, R4)`, `(R4, (0.0, 44.44), L4)`, `(L4, L3, L1)` — where Lk = (−Rk.x, Rk.y). Additionally assert the **continuity** of the path: consecutive arcs join end-to-start (`arc[k][-1] == arc[k+1][0]` for k = 0, 1) and the bridge midpoint is exactly `(0.0, 44.44)`. `CircularLayout.groove_arcs(8)` returns `[]`.
      - Run `source venv/bin/activate && python -m unittest discover -s tests -v` — the new tests fail because the class does not exist yet (intended TDD red step; this is not an independent task).
   b. Implement in `src/face_plate_layouts.py` (additive, per the plan's Design section):
      - Add the module constant `DOWNWARD_ARC_RIGHT = ((56.862, 9.525), (31.467, 10.025), (13.426, 27.905), (12.700, 53.295))` with a comment noting the arc start is 3 mm clear of the equatorial connector and R4 is the arc top.
      - Add an optional `groove_arcs(self, num_candles: int) -> list[tuple[tuple[float, float], tuple[float, float], tuple[float, float]]]` capability on the `FaceLayout` base class that returns `[]` by default (decorative/embossed arc paths, three points per arc, in the face plane; default: no grooves). The return-type annotation follows the codebase's annotated-signature convention (matching `candle_positions(self, num_candles) -> list[tuple[float, float]]`).
      - Add the `DownwardArcLayout(FaceLayout)` class mirroring the `CircularLayout` style (pure Python, `math` only, no `build123d` import):
        - `name = "downward_arc_layout"`.
        - `__init__(self, triangle_height: float)` that stores `triangle_height` but intentionally does not use it (documented: the arc geometry is fixed for the standard 7-in face — connector clearance and holder margins are constant, not proportional to face height).
        - `candle_positions(self, num_candles)` returning `(list(DOWNWARD_ARC_RIGHT) + [(-x, y) for x, y in DOWNWARD_ARC_RIGHT])[:num_candles]` (right arc bottom-to-top R1–R4, then left arc bottom-to-top L1–L4).
        - `groove_arcs(self, num_candles)` returning one continuous embossed arc line on every face: `[(r1, r3, r4), (r4, (0.0, 44.44), l4), (l4, l3, l1)]` where `l1..l4` are the mirrors of `r1..r4` — each element is three (x, y) points defining a circular arc; consecutive arcs join end-to-start.
      - Register the layout: add `"downward_arc_layout": DownwardArcLayout` to the `LAYOUTS` dict.
      - The module must still import only `manora_parameters` and `math` (no `build123d`).
   c. Run `source venv/bin/activate && python -m unittest discover -s tests -v` again — all tests pass (the TDD green step).

### Task 2: Implement the embossed groove sweep in `src/main.py` — Completed

Depends on Task 1 (consumes `layout.groove_arcs(...)`).

1. Implement the embossed groove sweep in `src/main.py` - Not Started
   a. In `create_face_plate(num_candles, layout)`, after the candle-hole loop (the existing per-candle candle-hole and M2-hole cuts), add a loop over `layout.groove_arcs(num_candles)` that mills the embossed lines:
      - **Sweep per arc segment — do NOT join the arcs into one wire swept once.** For each three-point circular arc definition, build the circular arc at `z = plate_thickness` (the outside face) as its own `BuildLine` (an `Arc3`/`ThreePointArc` through the three points) and sweep the profile along it, `mode=Mode.SUBTRACT`. Sweeping a non-circular profile along a single wire that joins arcs of *different radii* (34.19 → 13.5 → 34.19 mm) makes the pipe-shell section shear at the curvature-discontinuous C1 joints: the swept solid silently loses ~35% of its volume and its top face undulates coplanar with the outside face, which then corrupts the plate boolean (plates collapse to empty geometry for n = 1–3). This is the failure class documented in `resources/modeling/general_knowledge.md` §3. Per-segment sweeps produce clean flat-topped prisms that meet flush at the tangent-continuous joints, so subtracting them in sequence yields one visually continuous groove.
      - **Profile**: a rectangle **3.175 mm (1/8 in) wide** (in the face plane, perpendicular to the path) × **1.0 mm deep** (into the plate, toward −z), positioned so its top is flush with `z = plate_thickness` (the prism spans `z = plate_thickness − 1.0` to `plate_thickness`). The rectangle's depth axis is the face normal; its width axis lies in the face plane perpendicular to the path. Center the profile on the arc's start point (shifted down 0.5 mm in z) so the groove top is flush with the outside face.
      - The groove is one continuous cut per face (no breaks at candle-hole positions); the candle through-holes are cut as before and will visually interrupt the groove at the holes, which is the intended "passes through" look. The groove is drawn on every face regardless of candle count.
      - Do **not** change any existing triangle-body sketch/extrude, taper, connector M2 holes, starter candle hole, or the assembly loop. No change to `--layout` defaults.
      - **Progress and error reporting** (consistent with the project's `print()`-based style in `main.py`): emit a one-line per-face progress print for the groove (e.g. `print(f"Grooving face plate {num_candles}...")` before the sweep loop in `create_face_plate`), and wrap the groove loop so a sweep-geometry failure is reported with the face number (e.g. `print(f"Error grooving face plate {num_candles}: {e}", file=sys.stderr)` and re-raise) rather than surfacing an unannotated build123d exception.
   b. **Programmatic groove-geometry gate (the build123d sweep geometry IS verifiable — do not skip this)**: build the three per-arc sweeps for the `downward_arc_layout` groove path (as standalone solids, no plate) and assert:
      - each prism is a valid solid with z-range ∈ [0.27, 1.27] (flat top flush with the outside face at `z = plate_thickness = 1.27`, flat bottom at `z = 0.27`);
      - the three prism volumes sum to ≈ 600 mm³ (right arc ≈ 247.9 + bridge ≈ 104.7 + left arc ≈ 247.9; tolerance ± 3 mm³) — a sheared single-wire sweep instead measures ~391 mm³ and fails this gate.
      Then generate the plates and assert for every `num_candles` 1–8: the `downward_arc_layout` plate is a valid solid (`is_valid`), is non-empty, and its volume is strictly less than the corresponding `circular` plate's volume (the groove removes material). Optionally cross-section at the bridge midpoint (0, 44.44) on the `z = plate_thickness` face: the groove is ~3.175 mm wide × 1.0 mm deep. Use temp `-o` outdirs (`/tmp/downward_arc_task2_*`) so the committed `manufacture/*.step` files are not churned.
   c. Verify the module still runs: `source venv/bin/activate && python src/main.py --layout circular -o /tmp/downward_arc_task2_circular` — the regenerated `face_plate_circular_*.step` must have bounding boxes and volumes identical to the values recorded in `manufacture/face_plate_baseline.md` (the Story001 baseline), i.e. **geometry unchanged** — no grooves, because the `circular` layout returns no arcs. Use the temp `-o` outdir so the committed `manufacture/*.step` files are not churned by this smoke test; the "unchanged" check is a bbox/volume comparison against the baseline, not a byte comparison of files that land in the temp dir. Use a temp outdir name distinct from Task 3's (`/tmp/downward_arc_verify_circular` is reused by Task 3 — a distinct name here avoids stale-file confusion across worktrees).

### Task 3: Verify generated geometry — In Progress

Run-only over `manufacture/*.step` (and temp outdirs); no source edits. Depends on Task 2.

1. Verify generated geometry - Not Started
   a. Run `source venv/bin/activate && python src/main.py --layout downward_arc_layout` — confirm it completes and exports `manufacture/face_plate_downward_arc_layout_1.step` … `manufacture/face_plate_downward_arc_layout_8.step` plus the unchanged shared parts (`regular_candle_holder.step`, `apex_connector.step`, `equator_connector.step`) and `assembly.step`.
   b. **Programmatic groove-presence check**: for each plate `n` 1–8, the arc-layout plate's volume must be strictly less than the corresponding `circular` plate's volume (the groove subtract removes material). The "corresponding `circular` plate's volume" is taken from the committed `manufacture/face_plate_circular_*.step` files (same `n`), or from the temp outdir regenerated in subtask c — state the source used in the recorded output. Print the measured per-plate volumes and the arc-vs-circular delta for the human record (consistent with the project's `print()`-based style). Where practical, spot-check the groove depth/width via a boolean-intersect cross-section at the plate's `z = plate_thickness` face (the groove should be ~3.175 mm wide, 1.0 mm deep, on the outside face). **Visual sign-off gate**: run `python src/main.py --show face_plate_8` and `python src/main.py --show face_plate_2` in `ocp_vscode` and confirm (this is a human-visible check the story-implementor surfaces to the user): every face (including low-count faces) shows the full continuous line from bottom right, up the right arc, across the center, down the left arc to bottom left; the line passes through existing candle holes and is continuous where holes are missing; the shamash hole is not crossed; the line is on the outside face, 1 mm deep, 3.175 mm wide.
   c. **`circular` unchanged**: run `python src/main.py --layout circular -o /tmp/downward_arc_verify_circular` and verify the bounding boxes and volumes of `face_plate_circular_1.step` … `face_plate_circular_8.step` are identical to the values recorded in `manufacture/face_plate_baseline.md` (the Story001 baseline; the comparison is name-agnostic — the baseline rows are the pre-refactor `face_plate_{i}.step` figures for the same geometry). Additive change must not alter them, and the `circular` layout draws no grooves.
   d. `python src/main.py --layout bogus` — confirm the error names **both** `circular` and `downward_arc_layout`.
   e. `python -m unittest discover -s tests -v` — all tests green.

### Task 4: Update memory-bank documentation — In Progress

Tech-writer task; routes to the `technical-writer-for-story-implementor` agent, not a code agent. Depends on Task 2 (documents the implemented feature).

**Coordination guard**: this task must **not** embed any measured bounding-box/volume figures from Task 3 (embedding them would create a hidden dependency and break the parallel group). All content is derivable from the plan and design docs.

1. Update memory-bank documentation - Not Started
   a. `memory-bank/design/candle-arrangement-arc.md` — already captures the count rule and the embossed arc line; verify it matches the implementation and adjust only if the implementation reveals a discrepancy.
   b. `memory-bank/design/design.md` — update the Candle Arrangement pointer table to state the arc arrangement is implemented as `downward_arc_layout` and that it includes the embossed arc line.
   c. `memory-bank/requirements.md` — update Functional Requirement #4 to list the available layouts (`circular`, the default; `downward_arc_layout` for the 8-candle face).
   d. `memory-bank/context.md` — record the task at start and clear it on completion, per the standard task discipline.

### Parallel Execution

- **Group A: Tasks 3 and 4** — File-disjoint and independent. Task 3 is run-only over `manufacture/*.step` (and temp outdirs); Task 4 edits `memory-bank/design/design.md`, `memory-bank/requirements.md`, and `memory-bank/context.md`. Task 4's content (layout name, embossed-line presence) comes from the plan and design doc, **not** from Task 3's measurements — Task 4 must not embed Task 3's measured figures (hidden dependency guard). Contingency: if Task 3's equivalence check fails, the story needs rework and Task 4's docs may need revision.

All other task pairs are sequential: Task 2 depends on Task 1 (it consumes `groove_arcs`); Group A depends on Task 2.

### Execution Order

```
        ┌─────────────┐
        │  Task 1     │  (layout + tests — [Small], small-code agent)
        └──────┬──────┘
               ▼
        ┌──────┴──────┐
        │  Task 2     │  (groove sweep in src/main.py — depends on Task 1)
        └──────┬──────┘
               ▼
     ┌─────────┴─────────┐
     │                   │
┌────┴─────┐       ┌─────┴─────┐
│  Task 3  │       │  Task 4   │  (Group A — parallel)
│ (verify) │       │  (docs)   │
└──────────┘       └───────────┘
```

Task 1 must be merged before Task 2 starts (Task 2 consumes `groove_arcs` from Task 1). Task 2 must be merged before Group A starts (Task 3 verifies Task 2's output; Task 4 documents the implemented feature).

### Reintegration

**Group A (Tasks 3 and 4):**
- Merge order: any order (fully disjoint files, no shared infrastructure); default Task 3 then Task 4 (task-number order). Task 3 adds new `manufacture/face_plate_downward_arc_layout_*.step` files; Task 4 edits `memory-bank/*.md`.
- Integration tests (run from the repo root on the merged story branch):
  - `source venv/bin/activate && python -m unittest discover -s tests -v` — the full unit suite stays green after both worktrees merge.
  - `source venv/bin/activate && python src/main.py --layout downward_arc_layout` — full model generation completes and exports `face_plate_downward_arc_layout_1.step` … `_8.step` plus the shared parts and assembly.
  - `source venv/bin/activate && python src/main.py --layout circular -o /tmp/downward_arc_integration` and compare the bounding boxes/volumes of the regenerated `face_plate_circular_*.step` against `manufacture/face_plate_baseline.md` (additive-only guarantee).
- Watch for conflicts in: `manufacture/face_plate_circular_*.step` (tracked generated outputs that Task 2's smoke test and Task 3's comparison both regenerate — both use temp `-o` outdirs so the committed STEPs never churn in any worktree; if STEP export is nondeterministic, discard spurious diffs rather than merging them); `manufacture/face_plate_downward_arc_layout_*.step` (new tracked files created by Task 3 only — no conflict, but they must be present in the merged tree for the integration test); the **shared tracked STEPs** `regular_candle_holder.step`, `apex_connector.step`, `equator_connector.step`, and `assembly.step` (regenerated into tracked `manufacture/` by Task 3 subtask a's full `--layout downward_arc_layout` run — discard spurious nondeterministic diffs rather than merging them); `memory-bank/context.md` (edited by Task 4; within this story only Task 4 touches it). `venv/` is gitignored and absent from worktrees, so each worktree needs the parent repo's Python environment with build123d installed (see the Story001 walkthrough lesson: use the parent repo's `venv/bin/python` via its absolute path).

## Test-First Development

This project follows the Logical TDD Lifecycle. The one coding task with a natural unit-test target (Task 1) integrates the test-and-implement cycle inside the task: the failing test file is written first (subtask a, the red step), then the module is implemented (subtask b), then the tests are run to green (subtask c). Task 1 uses Python's stdlib `unittest` with no new dependency, following the convention established in Story001 (`tests/` directory, `sys.path` insertion, namespace-package discovery). Task 2's groove sweep exercises `build123d` geometry; its verification is run-based but includes programmatic geometry gates inside the task (per-prism volumes summing to ≈ 600 mm³ and z-range [0.27, 1.27], all plates valid and strictly lighter than the `circular` baseline) that catch a sheared multi-arc sweep immediately, plus an unchanged-`circular` smoke test inside the task and the run-based verification in Task 3 (STEP bounding-box/volume comparison against the Story001 baseline, plus the visual sign-off gate).

## Constraints

- **Additive only**: the `circular` layout and all other output (connectors, holders, assembly) must be unchanged. Do not touch `src/manora_parameters.py`.
- **No new dependency**: use Python's stdlib `unittest`; do not add pytest or any package to `requirements.txt`.
- **Module purity**: `src/face_plate_layouts.py` must not import `build123d`; only `manora_parameters` and `math`.
- **Design conformance**: positions must match `memory-bank/design/candle-arrangement-arc.md` within 0.1 mm; the layout must keep regular spacing ≥ 1.0 in for every candle count and keep the start holders 3 mm clear of the equatorial connectors.
- **Groove geometry**: the embossed line is a groove 1/8 in (3.175 mm) wide and 1 mm deep, on the **outside** face, drawn as **one continuous** path on every face (right candle arc → tangent bridge across the center → left candle arc). It is decorative: the candle-spacing rules do not apply to it. The shamash hole is never crossed by the line.
- **Standard face**: the coordinates assume the standard face (side 7 in, height 153.98 mm, holder width 0.75 in, shamash 35 mm from the tip).
- **Unchanged code**: in `create_face_plate()`, the triangle body, the taper, the connector M2 holes, and the starter candle hole are untouched. Component keys for `--show` remain `face_plate_1` … `face_plate_8`; exports become `face_plate_downward_arc_layout_<n>.step`.
- **Environment**: the Python virtual environment lives at `venv/`; activate it with `source venv/bin/activate` before running `python` commands. In git worktrees, use the parent repo's `venv` via its absolute path (see the Story001 walkthrough lesson).
- **Convention followed**: Story001 introduced the `tests/` directory and `unittest`-based tests; this story follows that convention (no new convention changes).

## Intent

The purpose of each task, stated so the goal remains clear even if implementation details change:

- **Task 1** — Add the pure-Python `DownwardArcLayout` strategy (arc coordinates, count rule, groove-arc paths) to the layout module, pinned by unit tests written first, and register it so `--layout downward_arc_layout` becomes selectable.
- **Task 2** — Draw the embossed arc line: extend the shared plate builder with a continuous three-arc groove sweep that is additive to all existing geometry.
- **Task 3** — Prove the new layout generates correct geometry (groove present, circular output unchanged, invalid layout rejected) and obtain the human visual sign-off for the continuous line.
- **Task 4** — Keep the project's design, requirements, and context documentation consistent with the new selectable layout and the embossed arc line.

## Acceptance Criteria

- [ ] `tests/test_downward_arc_layout.py` exists; `source venv/bin/activate && python -m unittest discover -s tests -v` passes.
- [ ] `src/face_plate_layouts.py` contains `DOWNWARD_ARC_RIGHT`, `DownwardArcLayout`, the `"downward_arc_layout"` registry entry, and the `groove_arcs()` capability on `FaceLayout`; the module still imports no `build123d`.
- [ ] `DownwardArcLayout.candle_positions(8)` returns the eight documented coordinates (within 0.1 mm); `candle_positions(n) == candle_positions(8)[:n]` for n 1–7.
- [ ] For every `num_candles` 1–8, the minimum pairwise distance of `candle_positions(num_candles)` is ≥ 25.35 mm (the 1.0 in requirement).
- [ ] `DownwardArcLayout.groove_arcs(n)` returns the same continuous path (right arc + center bridge + left arc) for every n 1–8; `CircularLayout.groove_arcs(n) == []`.
- [ ] `python src/main.py --layout downward_arc_layout` generates `manufacture/face_plate_downward_arc_layout_1.step` … `_8.step` and the assembly without errors; every face shows the full continuous line (bottom-right → center → bottom-left) on visual inspection (continuous, 3.175 mm × 1 mm, outside face, shamash clear).
- [ ] `face_plate_circular_*.step` bounding boxes/volumes are unchanged from the Story001 baseline (additive change only; no grooves on circular).
- [ ] `python src/main.py --layout bogus` fails with an error naming both layouts.
- [ ] `memory-bank/design/design.md`, `memory-bank/requirements.md`, and `memory-bank/context.md` reflect the new layout.

## Requesting Clarification

If at any point during story construction there is confusion or ambiguity about the goal or how to accomplish it, stop and ask the user for clarification.

## Notes

- The exact arc coordinates, count rule, groove-arc path, and groove geometry are settled in `memory-bank/design/candle-arrangement-arc.md` and the plan; no open questions remain.
- The visual inspection (Task 3 subtask b) requires a human sign-off gate: a sub-agent cannot see the `ocp_vscode` viewer, so the story-implementor surfaces that check to the user. The programmatic volume/cross-section checks in the same subtask run without human eyes.
- Story001's walkthrough lessons apply to this story's worktrees: verify the worktree branch before committing, use the parent repo's `venv` (it is gitignored and absent from worktrees), and use the `worktrees/` symlink for sub-agent paths.
