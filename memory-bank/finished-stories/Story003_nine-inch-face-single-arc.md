# Story003: Nine-Inch Face, Single Arc

## Goal

Enlarge the face plates from 7-inch to 9-inch equilateral triangles for **all** layouts and revise the `downward_arc_layout` from the current two-arc design to a **single concave-down circular arc** carrying all 8 regular candles.

The 9-in face growth is a one-constant change: `src/main.py` sets `triangle_side = 9.0 * INCH_MM`, and everything else (triangle height, shamash position, connector holes, assembly scale, exports) already derives from `triangle_side`. The `circular` layout's candle positions are absolute constants and are **unchanged** — the 9-in growth applies to the shared plate geometry only, and the `circular` layout is slated for later removal. Only the `downward_arc_layout` candle coordinates change: the eight regular candles move onto **one smooth concave-down circular arc** (center `(0, 8.287)`, radius `59.713` mm, peak `(0, 68.0)`), with the embossed groove following the same single curve.

This revision fixes a defect found on the 7-in face: the start candle holders at `(±56.862, 9.525)` collided with the equatorial connectors in the assembled die (measured ~3532 mm³ intersection each), because the documented "3 mm clearance" constraint `33x + 19.05y ≤ 2057.9` was derived against a connector footprint smaller than the real 1.5-in pyramid. On the 9-in face a single concave-down arc is feasible with the start holders at **±59.7 mm**, leaving ~1 mm empirical clearance margin (zero-clearance limit measured at ±60.7).

This story is driven by the approved plan `memory-bank/plans/adjust_size_and_arc_plan.md`.

## References

Links are relative to the `memory-bank` directory:

- [Adjust Face Size to 9 Inches and Revise Downward Arc Layout Plan](../plans/adjust_size_and_arc_plan.md)
- [Arc-Based Candle Arrangement Design](../design/candle-arrangement-arc.md)
- [Circular Candle Arrangement Design](../design/candle-arrangement-circular.md)
- [Design](../design/design.md)
- [Requirements](../requirements.md)
- [Arrangement Approach (feasibility method)](../arrangement_approach.md)

## Dependencies

- [Story002_downward-arc-layout.md](Story002_downward-arc-layout.md) — implemented the pluggable layout infrastructure this story revises: the `DownwardArcLayout` strategy (currently the two-arc design), the `groove_arcs()` capability on `FaceLayout`, the per-arc groove sweep in `src/main.py`, and the `tests/test_downward_arc_layout.py` test file. That work is implemented (see the [walkthrough](walkthrough/Story002_downward-arc-layout.md) if present); this story changes the 7-in geometry and rewrites the arc layout to the single-arc design.

## Dependent Stories

None.

## Tasks

### Task Sizing

The architect-for-story-planning reviewed the decomposition, sizing, and parallelism of every task:

- **Task 1** is annotated `[Small]`: one file (`src/main.py`), one constant change (`triangle_side = 7.0 * INCH_MM` → `9.0 * INCH_MM`), additive, zero test-file changes, one concern. The within-task generation runs are run-only to `/tmp` outdirs with exactly bounded bbox expectations (x ±114.3, y 0–197.97, z 0–1.27).
- **Task 2** is **not** `[Small]`: it is a full rewrite of the layout internals in `src/face_plate_layouts.py` (new ordered `DOWNWARD_ARC_9IN` tuple, reworked `candle_positions`/`groove_arcs` semantics) plus a full rewrite of `tests/test_downward_arc_layout.py`. Not additive — replaces existing behavior, requires reasoning about arc geometry, connector clearance at ±59.7, and the groove path. Routes to `code-for-story-implementor`.
- **Task 3a** is **not** `[Small]`: it regenerates 20 committed `.step` artifacts (8 `face_plate_circular_*`, 8 `face_plate_downward_arc_layout_*`, plus `regular_candle_holder`, `apex_connector`, `equator_connector`, `assembly`) and updates `manufacture/face_plate_baseline.md`, and includes a hard-gate boolean-intersection collision check with STOP-on-failure control flow. Routes to `code-for-story-implementor`.
- **Task 3b** is **not** `[Small]` (borderline — writes zero committed files): it spans four distinct checks (sheet-yield math, CLI error behavior, full unit suite, and a human visual sign-off gate requiring CAD judgment). Conservative default applied; routes to `code-for-story-implementor`.
- **Task 4** is **not** `[Small]` and is a tech-writer task: a multi-file markdown rewrite (4–6 files) with a cross-task hidden-dependency guard. Routes to the `technical-writer-for-story-implementor` agent, not a code agent.

### Task 1: Change the face size to 9 in — Completed [Small]

Architect note (decomposition): at its natural granularity — one file, one constant; cannot be smaller. The architect confirmed `[Small]` sizing (single additive constant, run-only verification, exactly bounded bbox expectations).

1. Change the face size to 9 in - Not Started
   a. In `src/main.py`, change `triangle_side = 7.0 * INCH_MM` (line ~25) to `triangle_side = 9.0 * INCH_MM`. Everything else (triangle height, shamash position, connector holes, assembly, exports) derives from this constant. Do **not** change any other line in this task.
   b. Smoke-verify both layouts still generate on the 9-in plate. Do **not** modify any layout or test file in this task (the `circular` candle positions are unchanged absolute constants; the `downward_arc_layout` keeps its current 7-in coordinates until Task 2 rewrites them):
      - `source venv/bin/activate && python src/main.py --layout circular -o /tmp/plan_9in_circular` — completes and exports plates with the 9-in bounding box (x −114.3…114.3, y 0…197.97, z 0…1.27) and the assembly completes.
      - `source venv/bin/activate && python src/main.py --layout downward_arc_layout -o /tmp/plan_9in_arc` — completes and exports plates and the assembly.
      - Both runs use temp `/tmp` outdirs so the committed `manufacture/*.step` files are not churned by this task (they are regenerated in Task 3a).

### Task 2: Revise `downward_arc_layout` to the single concave-down arc (TDD) — Completed

Architect note (decomposition): at its natural granularity — the red test step is a deliberately failing state, not an independently mergeable deliverable, and splitting the test rewrite from the implementation would split the same two files with no isolation benefit. The task is a full rewrite (not additive); it is **not** `[Small]`. Depends on Task 1 (the new arc coordinates are 9-in design constants and must be exercised against the 9-in face).

1. Revise the downward arc layout to the single concave-down arc (test-first) - Not Started
   a. Rewrite `tests/test_downward_arc_layout.py` (full rewrite of the existing file) using Python's stdlib `unittest`, following the conventions of the current file and `tests/test_face_plate_layouts.py` (a `sys.path` insertion at the top so `src/` is importable; `REPO_ROOT` derived from `__file__`). Use the **9-in** face-height constant `TRIANGLE_HEIGHT = 9.0 * INCH_MM * math.sqrt(3) / 2` and the 9-in shamash center `(0.0, 161.18)` (= `9-in height − 36.8`). Do **not** add pytest or any package to `requirements.txt`. The tests assert:
      - **Ordered 8-candle positions match the design**: `candle_positions(8)` equals the ordered list `DOWNWARD_ARC_9IN` (bottom right → up the right side → over the top → down the left side → bottom left), compared with `assertAlmostEqual(..., delta=0.1)` (design values are quoted to 3 decimals):
        1. (59.700, 9.525) — bottom right (start)
        2. (53.410, 34.989) — right side, up
        3. (36.814, 55.301) — right side, up
        4. (13.115, 66.542) — top right (just right of peak)
        5. (−13.115, 66.542) — top left (just left of peak)
        6. (−36.814, 55.301) — left side, down
        7. (−53.410, 34.989) — left side, down
        8. (−59.700, 9.525) — bottom left (end)
      - **Count rule (first n of the ordered sequence)**: `candle_positions(n)` equals `list(DOWNWARD_ARC_9IN)[:n]` for every n 1–8; specifically `candle_positions(1) == [(59.700, 9.525)]`, `candle_positions(4)[-1] == (13.115, 66.542)`, and `candle_positions(5)[-1] == (−13.115, 66.542)`. This is the **continuous over-the-top traversal** (different from the old two-arc "right arc bottom→top then left arc bottom→top" rule, which put the 5th candle at the bottom left).
      - **Spacing minimum**: for every `num_candles` 1–8 **with at least two positions** (`n == 1` has no pairs — guard the test so `min()` is never computed over an empty sequence), the minimum pairwise distance between positions is ≥ 25.35 mm (the 1.0 in / 25.4 mm requirement with 0.05 mm tolerance). The single-arc design gives 26.23 mm for every prefix.
      - **Shamash distance**: for `n = 8`, the minimum distance from the shamash center `(0.0, 161.18)` to any candle position is ≥ 44.4 mm (the relaxed 1.75 in / 44.45 mm requirement). The design gives ~95.5 mm (also ≥ 63.5 mm / 2.5 in).
      - **Default attributes**: `name == "downward_arc_layout"`, `candle_hole_diameter == CANDLE_HOLE_DIAMETER_MM`, and `screw_holes is True`.
      - **Groove arcs**: `groove_arcs(n)` returns **one** three-point arc definition — `((59.700, 9.525), (0.0, 68.0), (−59.700, 9.525))` — for **every** n 1–8 (the single concave-down curve through the candle arc; any three of the eight points define the same circle). `CircularLayout.groove_arcs(8)` returns `[]`.
      - **Retain the `create_layout` registry tests** from the current file (the registry entry is unchanged, so they remain valid): `create_layout("downward_arc_layout", triangle_height=…)` returns a `DownwardArcLayout` instance, and `create_layout("<unknown>")` raises `ValueError` whose message lists **both** `circular` and `downward_arc_layout`.
      - Run `source venv/bin/activate && python -m unittest discover -s tests -v` — the new tests fail because the layout still returns the old 7-in two-arc geometry (intended TDD red step; this is not an independent task).
   b. Implement in `src/face_plate_layouts.py` (rewrite of `DownwardArcLayout`; the `circular` layout is untouched):
      - Replace the module constant `DOWNWARD_ARC_RIGHT` with an ordered tuple `DOWNWARD_ARC_9IN` containing the eight coordinates above (hole 1 = bottom right start, up the right side, over the top, down the left side to the bottom left), with a comment noting the arc start at ±59.7 mm is the 9-in design point (~1 mm empirical connector clearance; zero-clearance limit measured at ±60.7) and that the eight points lie on one concave-down circular arc (center (0, 8.287), radius 59.713 mm).
      - `candle_positions(self, num_candles)` returns `list(DOWNWARD_ARC_9IN)[:num_candles]`.
      - `groove_arcs(self, num_candles)` returns `[((59.700, 9.525), (0.0, 68.0), (−59.700, 9.525))]` — one three-point arc on the same circle, for every n (the existing single-arc groove sweep in `main.py` handles a single-arc list unchanged: one `BuildLine` + one sweep).
      - Keep `__init__(self, triangle_height: float)` storing `triangle_height` but intentionally not using it, with the docstring updated: the single-arc geometry is fixed for the 9-in face (connector clearance and holder margins are constant, not proportional to face height).
      - Keep the `"downward_arc_layout"` registry entry (name unchanged) so CLI/export/`--show` keys stay stable.
      - The module must still import only `manora_parameters` and `math` (no `build123d`).
   c. Run `source venv/bin/activate && python -m unittest discover -s tests -v` again — all tests pass (the TDD green step).
   d. Run `source venv/bin/activate && python src/main.py --layout downward_arc_layout -o /tmp/plan_9in_arc` and confirm the plates export (with the 9-in bbox) and the groove progress prints appear (a per-face "Grooving face plate n..." print for each face 1–8, with the single-arc sweep). Use the temp outdir so the committed `manufacture/*.step` files are not churned.

### Task 3a: Regenerate `manufacture/`, run the assembled-die collision gate, record the 9-in baseline — Completed

Run/record over `manufacture/*.step` and `manufacture/face_plate_baseline.md`; no source edits. Depends on Tasks 1–2.

Architect note (decomposition): Task 3 was split into Task 3a and Task 3b. 3a is the artifact-production + geometry-integrity-gate + baseline-record concern (everything that ships in and documents `manufacture/`); the collision gate is ordered **before** the baseline write so the recorded table reflects verified geometry. 3b (separate task below) is the independent regression/robustness battery.

1. Regenerate manufacture, run the collision gate, record the 9-in baseline - Not Started
   a. Regenerate the committed `manufacture/` artifacts for **both** layouts and the assembly:
      - `source venv/bin/activate && python src/main.py --layout circular` (default outdir = `manufacture/`) — regenerates `face_plate_circular_1.step` … `face_plate_circular_8.step` plus the shared parts (`regular_candle_holder.step`, `apex_connector.step`, `equator_connector.step`) and `assembly.step`.
      - `source venv/bin/activate && python src/main.py --layout downward_arc_layout` — regenerates `face_plate_downward_arc_layout_1.step` … `face_plate_downward_arc_layout_8.step` plus the shared parts and assembly.
   b. **Assembled-die collision check (critical, hard gate)**: for **each** layout, verify no candle-holder solid intersects any connector solid. Reuse the empirical method from the plan's analysis (build the connectors in their assembly positions, place the candle-holder solids via the plate locations, boolean-intersect the holder solids against the connector solids). Both layouts must pass: the `circular` layout is expected clear; the arc-layout start holders at ±59.7 must be clear (zero-clearance limit measured at ±60.7). If **any** holder ↔ connector intersection is found, record the failing layout and coordinates, and **STOP before recording the baseline** — do not write the baseline for geometry that fails the collision gate.
   c. Only after the collision gate passes, update `manufacture/face_plate_baseline.md`: add a **"9-in post-resize baseline"** record with the circular-layout bbox/volume table for the 9-in geometry (x ±114.3, y 0–197.97, z 0–1.27), measured from the regenerated `face_plate_circular_*.step` files. Keep the old 7-in record as a historical section (retitle it, e.g., "7-in pre-resize baseline (historical)").

### Task 3b: Run the verification battery (yield, CLI, suite, human sign-off) — Completed

Run-only; writes **no** committed files. Depends on Tasks 1–2.

**Guardrail (from the architect's parallelism analysis):** every `python src/main.py` invocation in this task — **including the `--show` commands** — MUST pass `-o /tmp/...`. In `src/main.py` the `--show` flag does NOT short-circuit generation: exports run unconditionally before the show block and default to the committed `manufacture/` outdir. Without `-o /tmp/...`, the show commands would churn the committed files that Task 3a is regenerating (collision with the parallel worktree).

1. Run the verification battery - Not Started
   a. **Material-yield check**: verify the 8 faces (9-in equilateral, 7.79-in tall) fit the 12 in × 48 in sheet — 8 triangles nest in a zigzag strip of ≈ 36–40.5 in × 7.8 in, which fits. Compute/record the nesting dimensions.
   b. `source venv/bin/activate && python src/main.py --layout bogus -o /tmp/plan_9in_bogus` — confirm the error names **both** `circular` and `downward_arc_layout`.
   c. `source venv/bin/activate && python -m unittest discover -s tests -v` — the full unit suite is green.
   d. **Human visual sign-off gate** (the story's final gate regardless of task numbering — the story-implementor surfaces this to the user): run `python src/main.py --show face_plate_8 -o /tmp/plan_9in_show` and `python src/main.py --show face_plate_2 -o /tmp/plan_9in_show` in `ocp_vscode` and confirm (a human-visible check): every face shows a **single continuous concave-down groove** from bottom right, over the top, to bottom left, on the outside face (1/8 in × 1 mm), continuous where candle holes are missing and passing visually through existing holes; the shamash hole is not crossed. The user performs the final qualification on the visible result.

### Task 4: Update memory-bank documentation — Completed

Tech-writer task; routes to the `technical-writer-for-story-implementor` agent, not a code agent. Depends on Task 2 conceptually (documents the implemented feature) and is file-disjoint from Tasks 3a/3b.

**Coordination guard**: this task must **not** embed any measured bounding-box/volume figures from Task 3a (embedding them would create a hidden dependency and break the parallel group). All content is derivable from the plan and design docs.

1. Update memory-bank documentation - Not Started
   a. `memory-bank/design/candle-arrangement-arc.md` — rewrite to the **single-arc** spec: the 9-in face geometry (side 228.6 mm, height 197.97 mm, half-base 114.3 mm), the single concave-down circular arc (center (0, 8.287), radius 59.713 mm, peak (0, 68.0)), the ordered 8-position coordinates table, the continuous over-the-top count rule (`candle_positions(n) == DOWNWARD_ARC_9IN[:n]`), and the single groove arc `((59.700, 9.525), (0.0, 68.0), (−59.700, 9.525))` drawn on every face.
   b. `memory-bank/design/candle-arrangement-circular.md` — no change to the layout; optionally note its 9-in status and removal intent (the layout is slated for later removal; the 9-in growth applies to the shared plate geometry only).
   c. `memory-bank/design/design.md` — update the Candle Arrangement pointer table: the arc arrangement is a **single concave-down circular arc on the 9-in face**, implemented as the `downward_arc_layout` selectable layout, with the single continuous embossed arc line.
   d. `memory-bank/requirements.md` — update Functional Requirement #4's layout wording; update the "standard face" from 7 in to 9 in; adjust Constraint #3/#4 wording for the single-arc arrangement (single-arc visibility note) and note the 9-in material-yield result.
   e. `memory-bank/context.md` — record the task at start and clear it on completion, per the standard task discipline.
   f. Optional: add the 9-in single-arc worked example to `memory-bank/arrangement_approach.md`.

### Parallel Execution

- **Group A: Tasks 3a, 3b, and 4** — File-disjoint and independent. Task 3a writes `manufacture/*.step` and `manufacture/face_plate_baseline.md`; Task 3b writes **nothing** (run-only, all its `python src/main.py` invocations pass `-o /tmp/...` — **required guardrail**, including the `--show` commands, because `--show` does not short-circuit exports in `src/main.py`); Task 4 writes `memory-bank/*.md`. Task 4's content (single-arc spec, layout name, count rule) comes from the plan and design doc, **not** from Task 3a's measurements — Task 4 must not embed Task 3a's measured figures (hidden dependency guard). Contingency: if Task 3a's collision gate fails, the story needs rework and the baseline/artifacts must not be recorded.

All other task pairs are sequential: Task 2 depends on Task 1 (the new arc coordinates are 9-in design constants and are verified against the 9-in face); Group A depends on Tasks 1–2.

### Execution Order

```
        ┌─────────────┐
        │  Task 1     │  (9-in face size — [Small], small-code agent)
        └──────┬──────┘
               ▼
        ┌──────┴──────┐
        │  Task 2     │  (single-arc layout rewrite, TDD — depends on Task 1)
        └──────┬──────┘
               ▼
     ┌─────────┴──────────┐
     │                    │
┌────┴──────┐   ┌─────────┴────┐   ┌──────────────┐
│ Task 3a   │   │  Task 3b    │   │   Task 4     │
│(manufact.)│   │ (battery)   │   │ (memory-bank)│
└───────────┘   └─────────────┘   └──────────────┘
   ───────────────── Group A (parallel): Tasks 3a, 3b, 4 ─────────────────
```

Task 1 must be merged before Task 2 starts (Task 2's constants and generation check assume the 9-in face). Task 2 must be merged before Group A starts (Task 3a verifies Task 2's output; Task 3b's battery depends only on Tasks 1–2; Task 4 documents the implemented feature). Task 3b's human visual sign-off gate (subtask d) is the story's **final gate regardless of task numbering** — the user performs the final qualification on the visible result.

### Reintegration

Reintegration instructions refer to the "story branch" generically (the branch the story-implementor selects at runtime via the user configuration).

**Sequential chain (Task 1 → Task 2):**
- Merge order: Task 1 branch first, then Task 2 branch. Task 2's generation check and every downstream gate (3a collision at ±59.7, 3b visual sign-off) assume the 9-in face from Task 1 is in the base.
- Integration test: `source venv/bin/activate && python -m unittest discover -s tests -v` — confirms Task 2's rewritten layout tests pass against the post-Task-1 tree (the combined state both downstream tasks build on).
- Watch for conflicts in: `src/main.py` (touched only by Task 1 within this story, but concurrent parent-repo stories may modify it).

**Group A (Tasks 3a, 3b, 4):**
- Merge order: Task 3a first, then 3b, then 4 (task-number order). 3a-before-4 is a soft preference: with 3a's baseline figures already in the tree, a diff review of Task 4's docs immediately confirms the hidden-dependency guard held (no measured bbox/volume figures embedded). Task 3b produces no commits — expect a no-op/empty merge (its worktree exists for isolation and verification only).
- Integration tests (run from the repo root on the merged story branch):
  - `source venv/bin/activate && python -m unittest discover -s tests -v` — the full unit suite stays green after the group merges.
  - `source venv/bin/activate && python src/main.py --layout circular -o /tmp/integration_circular && source venv/bin/activate && python src/main.py --layout downward_arc_layout -o /tmp/integration_arc` — end-to-end generation for both layouts on the merged branch; the circular plate bbox must be the 9-in values (x ±114.3, y 0–197.97).
  - `git status --short manufacture/` (or diff against committed `.step` artifacts after regeneration) — confirms the committed `manufacture/` artifacts match the merged code; spurious STEP entity-ordering diffs should be discarded, not committed.
  - Task 3b subtask d (human visual sign-off gate) — the story's final gate regardless of task numbering.
- Watch for conflicts in: `manufacture/*.step` (STEP export entity ordering is nondeterministic between runs/worktrees — spurious diffs to discard, not real conflicts); `memory-bank/context.md` (touched by Task 4 within this story, but it is the project's task-record file — genuine conflict risk at story-branch merge time if the parent repo edits it concurrently); `manufacture/face_plate_baseline.md` (only Task 3a here, but other stories may append baseline records); `memory-bank/design/candle-arrangement-arc.md` (only Task 4 here; low risk, shared design doc). `venv/` is gitignored and absent from worktrees, so each worktree needs the parent repo's Python environment with build123d installed (see the Story001/Story002 walkthrough lessons: use the parent repo's `venv/bin/python` via its absolute path).

## Test-First Development

This project follows the Logical TDD Lifecycle. The coding task with a natural unit-test target (Task 2) integrates the test-and-implement cycle inside the task: the rewritten failing test file is written first (subtask a, the red step), then the layout is rewritten (subtask b), then the tests are run to green (subtask c). Task 2 uses Python's stdlib `unittest` with no new dependency, following the convention established in Story001 (`tests/` directory, `sys.path` insertion, namespace-package discovery). Task 1 is a one-constant change verified by run-only generation smoke tests (no unit-test target). Tasks 3a/3b are run-based verification with programmatic gates: the assembled-die collision check (3a subtask b) is a hard STOP-on-failure gate that must pass before the baseline is recorded, the yield check and CLI/suite checks (3b) run with `-o /tmp/...` guardrails, and the human visual sign-off gate (3b subtask d) is surfaced to the user. Task 4 is a documentation task with no test target.

## Constraints

- **Additive/minimal**: the die architecture (octahedron, connectors fixed at 1.5-in/2.0-in, holders 0.75-in, taper) is unchanged; only `triangle_side` and the `downward_arc_layout` coordinates change. The `circular` layout is **untouched** (slated for later removal). Do **not** touch `src/manora_parameters.py`.
- **No new dependency**: use Python's stdlib `unittest`; do not add pytest or any package to `requirements.txt`.
- **Module purity**: `src/face_plate_layouts.py` must not import `build123d`; only `manora_parameters` and `math`.
- **Design conformance**: positions must match `memory-bank/design/candle-arrangement-arc.md` (as rewritten in Task 4) within 0.1 mm; the layout must keep regular spacing ≥ 1.0 in (25.4 mm) for every candle count.
- **Spacing**: adjacent regular-candle centers ≥ 25.4 mm (assert ≥ 25.35 with the 0.05 tolerance convention) for every candle count.
- **Shamash**: minimum 44.45 mm center-to-center from the shamash (the new design gives ~95.5 mm, also ≥ 63.5 mm / 2.5 in).
- **Connector clearance**: start holders must clear the equatorial connectors (empirical check, not the old simplified footprint constraint). The new start at ±59.7 mm satisfies this with ~1 mm margin; **the verification task MUST re-run the assembled-die collision check** (holder ↔ connector intersections) for both layouts.
- **Holder fit**: all four 19.05-mm-square holder corners inside the 9-in triangle.
- **Material yield**: the 8 faces (9-in equilateral, 7.79-in tall) must fit the 12 in × 48 in sheet — 8 triangles nest in a zigzag strip of ≈ 36–40.5 in × 7.8 in, which fits; verify in Task 3b.
- **Embossed groove**: single continuous 1/8 in × 1 mm groove on the **outside** face following the candle arc; on every face; shamash never crossed.
- **Unchanged code**: in `create_face_plate()`, the triangle body, the taper, the connector M2 holes, the starter candle hole, and the groove sweep are untouched in Task 1 (only the `triangle_side` constant changes). Component keys for `--show` remain `face_plate_1` … `face_plate_8`; exports remain `face_plate_circular_<n>.step` and `face_plate_downward_arc_layout_<n>.step`.
- **Environment**: the Python virtual environment lives at `venv/`; activate it with `source venv/bin/activate` before running `python` commands. In git worktrees, use the parent repo's `venv` via its absolute path (see the Story001/Story002 walkthrough lessons). Use temp `-o /tmp/...` outdirs for any generation that must not churn the committed `manufacture/*.step` files.
- **Convention followed**: Story001 introduced the `tests/` directory and `unittest`-based tests; this story follows that convention (no new convention changes).

## Intent

The purpose of each task, stated so the goal remains clear even if implementation details change:

- **Task 1** — Enlarge the shared face-plate geometry to 9-in equilateral triangles via the single `triangle_side` constant, leaving layouts, tests, and all other geometry derivation untouched.
- **Task 2** — Rewrite `downward_arc_layout` to the single concave-down circular arc carrying all 8 candles (ordered over-the-top traversal, single groove arc), pinned by unit tests written first.
- **Task 3a** — Regenerate the committed models for both layouts and record the 9-in baseline, gated on the assembled-die collision check (start holders must clear the equatorial connectors).
- **Task 3b** — Verify the 9-in material yield, CLI robustness, the full unit suite, and obtain the human visual sign-off for the single continuous concave-down groove.
- **Task 4** — Keep the project's design, requirements, and context documentation consistent with the 9-in face and the single-arc layout.

## Acceptance Criteria

- [ ] `src/main.py` contains `triangle_side = 9.0 * INCH_MM`; both `--layout circular` and `--layout downward_arc_layout` generate plates with the 9-in bounding box (x −114.3…114.3, y 0…197.97, z 0–1.27) and the assembly completes.
- [ ] `tests/test_downward_arc_layout.py` is rewritten (9-in constants) and `source venv/bin/activate && python -m unittest discover -s tests -v` passes; the tests pin the 8 ordered positions, the first-n-of-8 count rule, spacing ≥ 25.35 mm, shamash distance ≥ 44.4 mm for n = 8, and the single groove arc for every n.
- [ ] `src/face_plate_layouts.py` contains the ordered `DOWNWARD_ARC_9IN` tuple, `candle_positions(n) == list(DOWNWARD_ARC_9IN)[:n]`, `groove_arcs(n)` returning the single `((59.700, 9.525), (0.0, 68.0), (−59.700, 9.525))` arc, the `__init__` storing-but-unusing `triangle_height`, and the unchanged `"downward_arc_layout"` registry entry; the module imports no `build123d`.
- [ ] The assembled-die collision check passes for **both** layouts (circular clear; arc start at ±59.7 clear); if it fails, no 9-in baseline was recorded.
- [ ] `manufacture/face_plate_circular_*.step` and `manufacture/face_plate_downward_arc_layout_*.step` plus the shared parts and assembly are regenerated at the 9-in size; `manufacture/face_plate_baseline.md` has a "9-in post-resize baseline" record (old 7-in record retained as historical).
- [ ] The material-yield check passes (8 × 9-in faces fit the 12 in × 48 in sheet).
- [ ] `python src/main.py --layout bogus` fails with an error naming both `circular` and `downward_arc_layout`.
- [ ] `memory-bank/design/candle-arrangement-arc.md`, `memory-bank/design/design.md`, `memory-bank/requirements.md`, and `memory-bank/context.md` reflect the 9-in face and the single-arc layout; Task 4 embedded no measured bbox/volume figures from Task 3a.
- [ ] Human visual sign-off obtained: a single continuous concave-down groove from bottom right, over the top, to bottom left on the outside face, shamash clear (final qualification by the user).

## Requesting Clarification

If at any point during story construction there is confusion or ambiguity about the goal or how to accomplish it, stop and ask the user for clarification.

## Notes

- The exact single-arc coordinates, count rule, groove arc, and 9-in face geometry are settled in `memory-bank/plans/adjust_size_and_arc_plan.md` and the design docs; the story's Task 2 rewrite is pinned by the plan (no ambiguity) — a bounded 2-file TDD task.
- **Resolved decisions (confirmed by the user)**: (1) the `circular` layout is unchanged — no adjustment; it is slated for later removal, and the 9-in face growth still applies to the shared plate geometry; (2) the arc start is **±59.7 mm** (~1 mm connector clearance), the recommended design point; (3) the user will do the final visual qualification pass on the visible result — the story's Task 3b human visual sign-off gate must be surfaced to the user.
- **Traceability**: the connector-collision discovery on the 7-in design (start holders at (±56.862, 9.525) intersecting the equatorial connectors, ~3532 mm³ each) is recorded in the plan and should be captured in the story notes/docs so the fix's rationale is traceable.
- The layout registry names (`circular`, `downward_arc_layout`) are kept unchanged so CLI/export/`--show` keys stay stable.
- `manufacture/face_plate_baseline.md` should be relabeled to reflect it is now the 9-in baseline (the old 7-in record stays as a historical section).
- Story001/Story002 walkthrough lessons apply to this story's worktrees: verify the worktree branch before committing, use the parent repo's `venv` (it is gitignored and absent from worktrees), and use the `worktrees/` symlink for sub-agent paths.
