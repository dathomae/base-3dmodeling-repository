# Story004: Parabolic Arch Layout

## Goal

Replace the `downward_arc_layout` single semicircular arc with a single concave-down **parabolic arch** on the 9-inch face, eliminating the candle-holder intersections found inside the assembled die and reconciling the stale 7-inch / old-arc documentation.

The current merged code (Story003) draws a **semicircle**: center `(0, 12.7)`, radius `59.7` mm, peak `(0, 72.4)`, ends at `(±59.7, 12.7)` on a 0.5-in bottom-edge inset. A design review found two problems with it:

1. **Wasted crown space** — the semicircle's crown (`y = 72.4`, 36.6 % of the 197.97 mm face height) leaves an unnecessarily large ≈ 89 mm gap to the shamash at `(0, 161.17)`. On the 9-in face this is *not* forced: the shamash 2.5-in (63.5 mm) exclusion circle bottoms out at `y = 97.67`, so the crown can rise to ≈ 95–97 mm.
2. **Holder–holder collision (new defect)** — the bottom (foot) holders on *adjacent* faces intersect inside the die (≈ 3375 mm³ per pair in the current semicircle design; 8 such pairs). Story003's assembled-die check verified holder↔connector only, not holder↔holder.

The fix, pinned by the approved plan `memory-bank/plans/parabolic_arch_layout_plan.md`:

- **Feet** at `(±63.0, 28.0)` mm — `y = 28` clears the adjacent-face collision (threshold ≈ 27–28 mm); `x = 63` clears the equatorial connector with ~2–3 mm margin (zero-clearance ≈ `x = 65` at `y = 28`).
- **Crown** at `(0, 95)` mm — 66.2 mm below the shamash, reclaiming the dead space while staying "flowing" and non-linear.
- **Curve** (concave down, symmetric about `x = 0`): `y(x) = 28 + 67·(1 − (x/63)²)`.
- **Groove**: the same parabola drawn as a single quadratic Bézier `((63.0, 28.0), (0.0, 162.0), (−63.0, 28.0))` (a quadratic Bézier *is* a parabola; the control point `(0, 162)` is the tangent intersection, not a point on the curve — the groove still peaks at `(0, 95)`).
- **Holder rotation**: the parabola's tangent vector (A = 67, XFOOT = 63), preserving the "2 screw holes inboard / 2 outboard" property vs the parabola's inboard normal.
- **Two new verification constraints**: adjacent-face holder non-intersection (0 overlap across all 36 mounted holders) and bottom-holder screw-hole clearance (≥ 4.5 mm center-to-center from every equatorial-connector M2 hole; design gives ≈ 22.5 mm).
- **Doc reconciliation**: remove the remaining 7-inch references and stale arc geometry (center `(0, 8.287)`, radius `59.713`, peak `(0, 68.0)`, spacing `26.23` mm, shamash `~95.5` mm) from all live docs.

`CircularLayout` is untouched (slated for later removal).

## References

Links are relative to the `memory-bank` directory:

- [Parabolic Arch Layout Plan](../plans/parabolic_arch_layout_plan.md)
- [Arc-Based Candle Arrangement Design](../design/candle-arrangement-arc.md)
- [Design](../design/design.md)
- [Requirements](../requirements.md)
- [Concepts](../concepts.md)
- [Arrangement Approach (feasibility method)](../arrangement_approach.md)

## Dependencies

- [Story003_nine-inch-face-single-arc.md](../finished-stories/Story003_nine-inch-face-single-arc.md) — implemented the 9-inch face plates and the current single semicircular `downward_arc_layout` (center `(0, 12.7)`, radius `59.7`, peak `(0, 72.4)`, holders rotated tangent to the arc, single-arc groove sweep via `ThreePointArc`, and the `DOWNWARD_ARC_9IN` ordered tuple + `holder_rotation_angle` + `groove_arcs` in `src/face_plate_layouts.py`). This story replaces that semicircular geometry with the parabola and adds the holder↔holder / screw-hole verification gates.

## Dependent Stories

None.

## Tasks

### Task Sizing

The architect-for-story-planning reviewed the decomposition, sizing, and parallelism of every task:

- **Task 1** is **not** `[Small]`: it is a coordinated multi-function rewrite (not additive) — three functions in `src/face_plate_layouts.py` (`candle_positions` via a new module tuple, `holder_rotation_angle` with a new parabola-tangent formula, `groove_arcs` with a new Bézier triple) plus a full rewrite of `tests/test_downward_arc_layout.py`. Requires reasoning about arc-length parameterization, tangent/rotation math, and Bézier equivalence. Routes to `code-for-story-implementor`.
- **Task 2** is annotated `[Small]`: one file (`src/main.py`), one additive mechanical curve-primitive swap (`ThreePointArc` → `Bezier`) plus a comment update; the holder-rotation call is already generic. Routes to `small-code-for-story-implementor`.
- **Task 3** is **not** `[Small]`: run-only, but 7 subtasks including 3 hard geometric gates (holder↔holder all-pairs across the 36 mounted holders, holder↔connector, screw-hole clearance) requiring intersection-check scripting over the assembled die, regeneration of 20 STEP artifacts, a baseline doc update, and a human visual sign-off. Routes to `code-for-story-implementor`.
- **Task 4** is **not** `[Small]` and is a tech-writer task: a multi-file markdown rewrite (6–7 files forming one semantic unit — every live doc must describe the same parabolic spec) with a cross-task hidden-dependency guard. Routes to the `technical-writer-for-story-implementor` agent, not a code agent.

### Task 1: Rewrite `downward_arc_layout` to the parabolic arch (TDD) — Completed

Architect note (decomposition): at its natural granularity — the red test step is a deliberately failing state, not an independently mergeable deliverable, and splitting the test rewrite from the implementation would split the same two files with no isolation benefit. The task is a coordinated multi-function rewrite (not additive), so it is **not** `[Small]`.

1. Rewrite the downward arc layout to the parabolic arch (test-first) - Not Started
   a. Rewrite `tests/test_downward_arc_layout.py` (full rewrite of the existing file) using Python's stdlib `unittest`, following the conventions of the current file and `tests/test_face_plate_layouts.py` (a `sys.path` insertion at the top so `src/` is importable; `REPO_ROOT` derived from `__file__`). Use the **9-in** face-height constant `TRIANGLE_HEIGHT = 9.0 * INCH_MM * math.sqrt(3) / 2` and the 9-in shamash center `(0.0, 161.17)` (= 9-in height − 36.8). Do **not** add pytest or any package to `requirements.txt`. The tests assert:
      - **Ordered 8-candle positions match the design**: `candle_positions(8)` equals the ordered list `DOWNWARD_ARC_PARABOLIC_9IN` (bottom right → up the right side → over the crown → down the left side → bottom left), compared with `assertAlmostEqual(..., delta=0.1)` (design values are quoted to 3 decimals):
        1. (63.000, 28.000) — bottom right (start)
        2. (50.261, 52.356) — right side, up
        3. (34.534, 74.867) — right side, up
        4. (13.312, 92.008) — top right (just right of crown)
        5. (−13.312, 92.008) — top left (just left of crown)
        6. (−34.534, 74.867) — left side, down
        7. (−50.261, 52.356) — left side, down
        8. (−63.000, 28.000) — bottom left (end)
      - **Count rule (first n of the ordered sequence)**: `candle_positions(n)` equals `list(DOWNWARD_ARC_PARABOLIC_9IN)[:n]` for every n 1–8; specifically `candle_positions(1) == [(63.000, 28.000)]`, `candle_positions(4)[-1] == (13.312, 92.008)`, and `candle_positions(5)[-1] == (−13.312, 92.008)`. This is the continuous over-the-top traversal (same count rule as the current single-arc design).
      - **Spacing minimum**: for every `num_candles` 1–8 **with at least two positions** (`n == 1` has no pairs — guard the test so `min()` is never computed over an empty sequence), the minimum pairwise distance between positions is ≥ 25.35 mm (the 1.0 in / 25.4 mm requirement with 0.05 mm tolerance). The parabolic design gives 26.62 mm for the arc-top pair (holes 4–5); side gaps ≈ 27.3–27.5 mm.
      - **Shamash distance**: for `n = 8`, the minimum distance from the shamash center `(0.0, 161.17)` to any candle position is ≥ 44.4 mm (the relaxed 1.75 in / 44.45 mm requirement). The design gives ~70.43 mm (also ≥ 63.5 mm / 2.5 in).
      - **Edge inset**: every candle center ≥ 0.5 in (12.7 mm) from every edge of the 9-in triangle (keep the existing `test_edge_inset_half_inch`).
      - **Groove arcs**: `groove_arcs(n)` returns the **single quadratic-Bézier control-point triple** `((63.0, 28.0), (0.0, 162.0), (−63.0, 28.0))` for **every** n 1–8 (the exact parabola — a quadratic Bézier *is* a parabola; `P1 = (0, 162)` is the tangent-intersection control point, not a point on the curve, which peaks at `(0, 95)`). `CircularLayout.groove_arcs(8)` returns `[]`.
      - **Holder rotation**: `holder_rotation_angle(cx, cy)` aligns the holder's local +X with the parabola's tangent in traversal direction (bottom-right → crown → bottom-left) and its local +Y with the inboard normal (toward the base). Assert the tangent alignment at the ends (hole 1 ≈ **115.18°**, hole 8 ≈ **244.82°**), mirror symmetry (`angle[i] + angle[7−i] == 360°`), and the 2-inboard/2-outboard split **reformulated against the parabola's inboard normal** at each candle (no circle center; the old radial `DOWNWARD_ARC_CENTER` approach is gone).
      - **Retain the `create_layout` registry tests** from the current file (the registry entry is unchanged, so they remain valid): `create_layout("downward_arc_layout", triangle_height=…)` returns a `DownwardArcLayout` instance, and `create_layout("<unknown>")` raises `ValueError` whose message lists **both** `circular` and `downward_arc_layout`.
      - Run `source venv/bin/activate && python -m unittest discover -s tests -v` — the new tests fail because the layout still returns the semicircle geometry (intended TDD red step; this is not an independent task).
   b. Implement in `src/face_plate_layouts.py` (rewrite of the arc-layout internals; the `circular` layout is untouched):
      - Replace the module constant `DOWNWARD_ARC_9IN` with an ordered tuple `DOWNWARD_ARC_PARABOLIC_9IN` containing the eight coordinates above (hole 1 = bottom right start, up the right side, over the crown, down the left side to the bottom left), with a comment noting: feet `(±63.0, 28.0)` clear the adjacent-face holder collision (threshold ≈ 27–28 mm) and the equatorial connector (~2–3 mm margin; zero-clearance ≈ x = 65 at y = 28); crown `(0, 95)`; the eight points lie on the parabola `y = 28 + 67·(1 − (x/63)²)`.
      - `candle_positions(self, num_candles)` returns `list(DOWNWARD_ARC_PARABOLIC_9IN)[:num_candles]`.
      - `holder_rotation_angle(self, cx, cy)` returns the parabola-tangent angle `degrees(atan2(2·A·cx / XFOOT, −XFOOT))` with `A = 67` and `XFOOT = 63` (drop the `DOWNWARD_ARC_CENTER` radial approach). The exact sign convention is pinned by the invariants asserted in the tests: mirror symmetry (`angle(x) + angle(−x) = 360°`) and 2-inboard/2-outboard vs the parabola's inboard normal.
      - `groove_arcs(self, num_candles)` returns `[((63.0, 28.0), (0.0, 162.0), (−63.0, 28.0))]` — one quadratic-Bézier control-point triple for every n (the existing per-arc sweep in `main.py` is reused, but the curve primitive changes from circular `ThreePointArc` to `Bezier` in Task 2).
      - Keep `__init__(self, triangle_height: float)` storing `triangle_height` but intentionally not using it, with the docstring updated (the parabolic geometry is fixed for the 9-in face).
      - Keep the `"downward_arc_layout"` registry entry (name unchanged) so CLI/export/`--show` keys stay stable.
      - Update the module docstrings/comments to the parabola (feet ±63/28, crown 95, Bézier control point `(0, 162)`).
      - The module must still import only `manora_parameters` and `math` (no `build123d`).
   c. Run `source venv/bin/activate && python -m unittest discover -s tests -v` again — all tests pass (the TDD green step).

### Task 2: Draw the groove with `Bezier` in `src/main.py` — Completed [Small]

Architect note (decomposition): at its natural granularity — one file, one additive curve-primitive swap; cannot be smaller. Sequential after Task 1 (Task 1 changes the groove tuple semantics to the Bézier triple that this task sweeps).

1. Draw the embossed groove as a Bézier - Completed
   a. In `create_face_plate` in `src/main.py`, changed the groove curve primitive from `ThreePointArc(...)` to `Bezier(...)` for the three groove points, and updated the surrounding comment: a single quadratic Bézier **is** the exact parabola, so the `is_frenet=True` sweep still produces one clean uniform groove with no C1 joints (the "shear at the joints" pitfall of the old multi-arc approach does not apply). The holder-rotation call (`layout.holder_rotation_angle`) is unchanged.
   b. Programmatic gate: every `downward_arc_layout` plate is valid, and each plate is strictly lighter than the same-number `circular` plate (the groove removes material); the groove prism z-range is `[plate_thickness − 1.0, plate_thickness]`.
   c. Ran `python src/main.py --layout downward_arc_layout -o /tmp/parab_arc` and `python src/main.py --layout circular -o /tmp/parab_circular` — both completed; `circular` output is unchanged (no grooves). Used temp `/tmp` outdirs so committed `manufacture/*.step` files are not churned.
   d. Worktree commit: `b70f1dc3c55f0d415e826e3475865ebe094131f9`.

### Task 3: Regenerate and verify geometry (run-only) — Completed

Run/record over `manufacture/*.step` and `manufacture/face_plate_baseline.md`; no source edits. Depends on Tasks 1–2.

Architect note (decomposition): **borderline** but at its natural granularity — no natural seam. The three hard geometric gates (subtasks b/c/d) are all sequentially dependent on the single regeneration (subtask a), and the baseline record (subtask e) depends on the bbox/volume measured during regeneration. Splitting would create a sequential chain with zero isolation benefit (all in one worktree anyway). Subtask g (human sign-off) is a checkpoint within the task, surfaced to the user, not a separable handoff. Keep as one run-only task; route to `code-for-story-implementor`.

1. Regenerate manufacture, run the assembly gates, record the parabolic baseline - Not Started
   a. Regenerate the committed `manufacture/` artifacts for **both** layouts and the assembly:
      - `source venv/bin/activate && python src/main.py --layout circular` (default outdir = `manufacture/`) — regenerates `face_plate_circular_1.step` … `face_plate_circular_8.step` plus the shared parts (`regular_candle_holder.step`, `apex_connector.step`, `equator_connector.step`) and `assembly.step`.
      - `source venv/bin/activate && python src/main.py --layout downward_arc_layout` — regenerates `face_plate_downward_arc_layout_1.step` … `face_plate_downward_arc_layout_8.step` plus the shared parts and assembly.
      - Do **not** regenerate, delete, or rename the legacy `manufacture/face_plate_*.step` and `jig_*.step`/`output.step` files — they are historical and outside `main.py`'s artifact set.
   b. **Holder↔holder collision check (critical, new hard gate)**: build all 36 candle-holder solids in their assembly positions (faces carry 1–8 candles: 1+2+…+8 = 36) and pairwise boolean-intersect them; require **0 overlap** across **every** pair — not just the adjacent-face feet. This is the gate that catches the pre-existing defect this plan fixes (the semicircle's feet at `(±59.7, 12.7)` overlapped the adjacent face's foot holders by ≈ 3224–3375 mm³ per pair). If any pair intersects, record the failing face/holder pair and coordinates, and **STOP before recording the baseline**.
   c. **Holder↔connector collision check (critical, hard gate)**: for **each** layout, verify no candle-holder solid intersects any connector solid (reuse the Story003 empirical method: connectors in assembly positions, holders via plate locations, boolean-intersect). Both layouts must pass — the arc-layout start holders at `(±63, 28)` must be clear (~2–3 mm margin; zero-clearance ≈ x = 65 at y = 28). If any intersection is found, record the failing layout and coordinates, and **STOP before recording the baseline**.
   d. **Screw-hole clearance check (new)**: for each bottom (foot) holder, confirm its four M2 screw-hole centers are ≥ 4.5 mm center-to-center from every equatorial-connector M2 screw-hole center (countersink head Ø 4.5 mm; the design gives ≈ 22.5 mm).
   e. Only after the collision gates pass, update `manufacture/face_plate_baseline.md`: keep the existing "9-in post-resize baseline" circular record, and add a **"9-in parabolic-arc baseline"** record for the `downward_arc_layout` plates (bbox/volume measured from the regenerated `face_plate_downward_arc_layout_*.step` files).
   f. `source venv/bin/activate && python src/main.py --layout bogus -o /tmp/parab_bogus` — confirm the error names **both** `circular` and `downward_arc_layout`; then run the full unit suite (`python -m unittest discover -s tests -v`) — green.
   g. **Human visual sign-off gate** (the story's final gate regardless of task numbering — surfaced to the user): run `python src/main.py --show face_plate_8 -o /tmp/parab_show` and `python src/main.py --show face_plate_2 -o /tmp/parab_show` in `ocp_vscode` and inspect the assembly: a **single continuous concave-down parabolic groove** from bottom right over the crown (y ≈ 95) to bottom left, shamash clear, no holder/holder or holder/connector overlap. This is where the crown height (90/92/95) and foot position are finalized with the user. **Group-level revision trigger**: if the user changes the crown or feet at sign-off, the figures in Task 4's doc branch (written in parallel) become stale — revise Task 4's branch to the final geometry **before** merging Group A.

### Task 4: Reconcile memory-bank documentation — Completed

Tech-writer task; routes to the `technical-writer-for-story-implementor` agent, not a code agent. Depends on Task 2 conceptually (documents the implemented feature) and is file-disjoint from Task 3.

Architect note (decomposition): **borderline** but at its natural granularity — each per-file edit is small, but the subtasks form ONE semantic unit: every live doc must describe the same parabolic spec (coordinates, Bézier groove, 26.62/70.4 figures, 9-in face) with no internal inconsistency. Splitting per-file would force each sub-task to re-derive the full spec and re-read the plan, multiplying coordination overhead and raising inconsistency risk with no isolation benefit. This matches the "single coordinated mechanical change across many files — keep as one task" rule. Keep as one writing task; route to `technical-writer-for-story-implementor`.

**Coordination guard**: this task must **not** embed any measured bounding-box/volume figures from Task 3 (embedding them would create a hidden dependency and break the parallel group). All content is derivable from the plan and design docs.

1. Reconcile the memory-bank documentation - Not Started
   a. `memory-bank/design/candle-arrangement-arc.md` — rewrite to the **parabolic** spec: the 9-in face geometry (side 228.6 mm, height 197.97 mm, half-base 114.3 mm), the parabola `y = 28 + 67·(1 − (x/63)²)` with feet `(±63.0, 28.0)` and crown `(0, 95)`, the ordered 8-position coordinates table, the continuous over-the-top count rule (`candle_positions(n) == DOWNWARD_ARC_PARABOLIC_9IN[:n]`), the single quadratic-Bézier groove `((63.0, 28.0), (0.0, 162.0), (−63.0, 28.0))` drawn on every face, the parabola-tangent holder rotation (A = 67, XFOOT = 63), and the constraint table **including the holder↔holder non-intersection and screw-hole clearance rows**. Retain the 7-in two-arc note only as superseded history.
   b. `memory-bank/design/design.md` — update the Candle Arrangement pointer table row and the Face Plate paragraph: "parabolic arch" (not circle), crown `(0, 95)`, spacing **26.62 mm** (was 26.23), shamash **≈ 70.4 mm** (was 95.5).
   c. `memory-bank/requirements.md` — update FR #4 wording ("single concave-down parabolic arch"); Constraint #3 spacing figure (**26.62 mm**) and Constraint #4 arc-top figure (**26.62 mm**); add a note that the foot holders must not intersect across adjacent faces.
   d. `memory-bank/concepts.md` — "Candle Spacing vs. Face Capacity": change "fixed 7-inch" to 9-inch and update the 8-candle pattern to the single parabolic arch.
   e. `resources/chanukah-halacha/candle_arrangement.md` — "Feasibility note (fixed 7-inch faces)" → 9-inch faces.
   f. `memory-bank/context.md` — record the task at start and clear it on completion, per the standard task discipline.
   g. Optional: add a "parabolic arch (9-in, collision-free)" worked example to `memory-bank/arrangement_approach.md` (leave the existing 7-in examples as method history).

### Parallel Execution

- **Group A: Tasks 3 and 4** — File-disjoint and independent. Task 3 writes `manufacture/*.step` (20 regenerated artifacts) and `manufacture/face_plate_baseline.md`; Task 4 writes `memory-bank/design/*.md`, `memory-bank/requirements.md`, `memory-bank/concepts.md`, `memory-bank/context.md`, `resources/chanukah-halacha/candle_arrangement.md`, and optionally `memory-bank/arrangement_approach.md`. Different directories, no shared infrastructure file, no compile-time or semantic dependency. Task 4's content (parabolic spec, layout name, count rule, spacing/shamash figures) comes from the plan and design doc, **not** from Task 3's measurements — Task 4 must not embed Task 3's measured bbox/volume figures (hidden dependency guard). **Residual hazard**: Task 3's human sign-off (subtask g) may invalidate Task 4's figures if the user changes the crown (90/92/95) or feet at sign-off — treat subtask g as a group-level revision trigger (revise Task 4's doc branch to the final geometry BEFORE merging Group A). Contingency: if Task 3's collision gates fail, the story needs rework and the baseline/artifacts must not be recorded.

All other task pairs are sequential: Task 2 depends on Task 1 (Task 1 changes the groove tuple semantics to the Bézier triple that Task 2 sweeps); Group A depends on Tasks 1–2 (Task 3 regenerates from the new code; Task 4 documents the new spec).

### Execution Order

```
        ┌─────────────┐
        │  Task 1     │  (parabolic layout rewrite, TDD — code-for-story-implementor)
        └──────┬──────┘
               ▼
        ┌──────┴──────┐
        │  Task 2     │  (Bézier groove in main.py — [Small], small-code agent)
        └──────┬──────┘
               ▼
     ┌─────────┴──────────┐
     │                    │
┌────┴──────┐   ┌─────────┴────┐
│ Task 3    │   │  Task 4     │
│(manufact.)│   │ (memory-bank)│
└───────────┘   └─────────────┘
   ───────── Group A (parallel): Tasks 3, 4 ─────────
```

Task 1 must be merged before Task 2 starts (Task 2 sweeps the Bézier triple that Task 1 defines). Task 2 must be merged before Group A starts (Task 3 verifies Task 1–2's output; Task 4 documents the implemented feature). Task 3's human visual sign-off gate (subtask g) is the story's **final gate regardless of task numbering** — the user performs the final qualification (crown/foot decision) on the visible result.

### Reintegration

Reintegration instructions refer to the "story branch" generically (the branch the story-implementor selects at runtime via the user configuration).

**Sequential chain (Task 1 → Task 2):**
- Merge order: Task 1 branch first, then Task 2 branch. Task 2's `Bezier` groove sweep and every downstream gate (Task 3's collisions at feet ±63/28, Task 4's spec) assume Task 1's parabolic layout is in the base.
- Integration test: `source venv/bin/activate && python -m unittest discover -s tests -v` — confirms Task 1's rewritten layout tests pass against the post-Task-1 tree (the combined state both downstream tasks build on).
- Watch for conflicts in: `src/face_plate_layouts.py` (touched only by Task 1 within this story) and `src/main.py` (touched only by Task 2 within this story) — both are equally exposed to concurrent parent-repo stories modifying them.

**Group A (Tasks 3, 4):**
- Merge order: any order — use finish-order (the first task to pass review merges first; task-number tiebreaker). The trees are fully disjoint (`manufacture/` vs `memory-bank/` + `resources/`) with no shared infrastructure or generator→consumer relationship. Soft preference (Story003 precedent): merge Task 3 before Task 4 when both pass review, so a diff review of Task 4's docs immediately confirms the hidden-dependency guard held (no measured bbox/volume figures embedded); not required for correctness.
- Integration tests (run from the repo root on the merged story branch):
  - `source venv/bin/activate && python -m unittest discover -s tests -v` — the full unit suite stays green after the group merges.
  - `source venv/bin/activate && python src/main.py --layout downward_arc_layout -o /tmp/integration_parab && source venv/bin/activate && python src/main.py --layout circular -o /tmp/integration_circular` — end-to-end generation for both layouts on the merged branch; `circular` output must be unchanged.
  - Re-run the three Task 3 assembly gates on the merged tree: holder↔holder **0 overlap** across all 36 mounted holders; holder↔connector **0 overlap** both layouts; bottom-holder M2 screw-hole centers ≥ 4.5 mm from every equatorial-connector M2 hole. These are the story's acceptance gates and must hold on the final merged tree, not just in Task 3's worktree.
  - `grep` for stale markers (`7-inch`, `7-in`, `8.287`, `59.713`, `26.23`, `95.5`, `peak (0, 68.0)`) in live docs — zero hits (historical plans/stories/context-history are expected and left intact).
  - Task 3 subtask g (human visual sign-off gate) — the story's final gate regardless of task numbering.
- Watch for conflicts in: `manufacture/*.step` (STEP export entity ordering is nondeterministic between runs/worktrees — spurious diffs to discard, not real conflicts); `memory-bank/context.md` (touched by Task 4 within this story, but it is the project's task-record file — genuine conflict risk at story-branch merge time if the parent repo edits it concurrently); `memory-bank/design/candle-arrangement-arc.md` and `memory-bank/arrangement_approach.md` (only Task 4 here; low risk, shared design docs); `memory-bank/toc.md` and the story file itself (edited by the story-implementor during coordination — keep them out of worktree branches). No lock files involved (Python, stdlib `unittest` only). `venv/` is gitignored and absent from worktrees, so each worktree needs the parent repo's Python environment with build123d installed (see the Story001/Story002 walkthrough lessons: use the parent repo's `venv/bin/python` via its absolute path).

## Test-First Development

This project follows the Logical TDD Lifecycle. The coding task with a natural unit-test target (Task 1) integrates the test-and-implement cycle inside the task: the rewritten failing test file is written first (subtask a, the red step), then the layout internals are rewritten (subtask b), then the tests are run to green (subtask c). Task 1 uses Python's stdlib `unittest` with no new dependency, following the convention established in Story001 (`tests/` directory, `sys.path` insertion, namespace-package discovery). Task 2 is a single-file additive curve-primitive change verified by run-only generation gates (no unit-test target for the build123d sweep). Tasks 3 is run-based verification with programmatic gates: the holder↔holder and holder↔connector checks are hard STOP-on-failure gates that must pass before the baseline is recorded, the screw-hole clearance check and CLI/suite checks run as explicit gates, and the human visual sign-off gate (subtask g) is surfaced to the user. Task 4 is a documentation task with no test target (verified by the stale-marker grep in its acceptance criteria).

## Constraints

- **Minimal/additive**: the die architecture (octahedron, connectors fixed at 1.5-in/2.0-in, holders 0.75-in, taper) is unchanged. Only the `downward_arc_layout` geometry changes. The `circular` layout is **untouched** (slated for later removal). Do **not** touch `src/manora_parameters.py`.
- **No new dependency**: use Python's stdlib `unittest`; do not add pytest or any package to `requirements.txt`.
- **Module purity**: `src/face_plate_layouts.py` must not import `build123d`; only `manora_parameters` and `math`.
- **Design conformance**: positions must match `memory-bank/design/candle-arrangement-arc.md` (as rewritten in Task 4) within 0.1 mm; the layout must keep regular spacing ≥ 1.0 in (25.4 mm) for every candle count.
- **Spacing**: adjacent regular-candle centers ≥ 25.4 mm (assert ≥ 25.35 with the 0.05 tolerance convention) for every candle count.
- **Shamash**: minimum 44.45 mm center-to-center from the shamash (the new design gives ~70.43 mm, also ≥ 63.5 mm / 2.5 in).
- **Feet and connector clearance**: start points at `(±63, 28)`; the assembled-die holder↔connector collision check **must be re-run** (feet widened from ±59.7 to ±63 and raised to y=28).
- **Adjacent-face holder non-intersection (new)**: the bottom (foot) holders must not intersect holders on the adjacent face sharing the bottom edge. Verified by an all-pairs holder↔holder intersection check over the 36 mounted holders (0 overlap).
- **Screw-hole clearance (new)**: each bottom holder's four M2 screw holes must stay ≥ 4.5 mm center-to-center from every equatorial-connector M2 screw hole (countersink head Ø 4.5 mm); design gives ≈ 22.5 mm.
- **Holder fit**: all four 19.05-mm-square holder corners inside the 9-in triangle.
- **Edge inset**: candle centers ≥ 0.5 in (12.7 mm) from every edge (the feet at 28 mm bottom inset satisfy this).
- **Embossed groove**: single continuous 1/8 in (3.175 mm) × 1 mm groove on the **outside** face following the parabola; on every face; shamash never crossed; drawn with `Bezier` (not `ThreePointArc`) in `src/main.py`.
- **Unchanged code**: in `create_face_plate()`, the triangle body, the taper, the connector M2 holes, the starter candle hole, and the holder-rotation call are untouched; only the groove curve primitive changes. Component keys for `--show` remain `face_plate_1` … `face_plate_8`; exports remain `face_plate_circular_<n>.step` and `face_plate_downward_arc_layout_<n>.step`.
- **Documentation rule**: do **not** rewrite frozen historical records (`memory-bank/plans/downward_arc_layout_plan.md`, `memory-bank/plans/adjust_size_and_arc_plan.md`, `memory-bank/stories/Story00*`, and the "Recently Completed" history in `context.md`). Only live, current-state docs are updated.
- **Environment**: the Python virtual environment lives at `venv/`; activate it with `source venv/bin/activate` before running `python` commands. In git worktrees, use the parent repo's `venv` via its absolute path (see the Story001/Story002 walkthrough lessons). Use temp `-o /tmp/...` outdirs for any generation that must not churn the committed `manufacture/*.step` files.
- **Convention followed**: Story001 introduced the `tests/` directory and `unittest`-based tests; this story follows that convention (no new convention changes).

## Intent

The purpose of each task, stated so the goal remains clear even if implementation details change:

- **Task 1** — Rewrite `downward_arc_layout` to the parabolic arch (feet ±63/28, crown 95, parabola-tangent holder rotation, Bézier groove triple), pinned by unit tests written first (TDD red → green).
- **Task 2** — Draw the embossed groove with `Bezier` in `src/main.py` so the groove follows the parabola exactly, keeping the `circular` output unchanged.
- **Task 3** — Regenerate the committed models for both layouts and record the 9-in parabolic baseline, gated on the three assembly checks: holder↔holder non-intersection (new), holder↔connector clearance, and bottom-holder screw-hole clearance (new); then surface the human visual sign-off.
- **Task 4** — Keep the project's design, requirements, concepts, and context documentation consistent with the 9-in parabolic arch, removing all stale 7-inch and superseded-arc references from live docs.

## Acceptance Criteria

- [ ] `tests/test_downward_arc_layout.py` is rewritten (9-in constants, shamash `(0, 161.17)`) and `source venv/bin/activate && python -m unittest discover -s tests -v` passes; the tests pin the 8 ordered parabolic positions, the first-n-of-8 count rule, spacing ≥ 25.35 mm, shamash distance ≥ 44.4 mm for n = 8, edge inset ≥ 0.5 in, the single Bézier groove triple `((63.0, 28.0), (0.0, 162.0), (−63.0, 28.0))` for every n, and the parabola-tangent holder rotation (end values ≈ 115.18°/244.82°, mirror symmetry, 2-inboard/2-outboard vs the parabola normal).
- [ ] `src/face_plate_layouts.py` contains the ordered `DOWNWARD_ARC_PARABOLIC_9IN` tuple (hole 1 = bottom right, feet ±63/28), `candle_positions(n) == list(DOWNWARD_ARC_PARABOLIC_9IN)[:n]`, the parabola-tangent `holder_rotation_angle` (A=67, XFOOT=63, no `DOWNWARD_ARC_CENTER`), `groove_arcs(n)` returning the single Bézier triple, and the unchanged `"downward_arc_layout"` registry entry; the module imports no `build123d`.
- [ ] `src/main.py` draws the groove with `Bezier` (not `ThreePointArc`); `circular` output is unchanged from the Story003 9-in baseline.
- [ ] Every `downward_arc_layout` plate is valid and strictly lighter than its same-number `circular` plate; the groove prism z-range is `[plate_thickness − 1.0, plate_thickness]`.
- [ ] `manufacture/face_plate_circular_*.step` and `manufacture/face_plate_downward_arc_layout_*.step` plus the shared parts and assembly are regenerated; the legacy `face_plate_*.step` and `jig_*.step`/`output.step` files were NOT regenerated or deleted.
- [ ] **Holder↔holder intersection check: 0 overlap across all 36 mounted holders** (the new gate that catches the pre-existing adjacent-face defect).
- [ ] **Holder↔connector intersection check: 0 overlap for both layouts** (feet widened to ±63 and raised to y=28).
- [ ] **Screw-hole clearance check: every bottom holder's M2 holes ≥ 4.5 mm from every equatorial-connector M2 hole.**
- [ ] `manufacture/face_plate_baseline.md` has a "9-in parabolic-arc baseline" record (existing 9-in circular record retained).
- [ ] `python src/main.py --layout bogus` fails with an error naming both `circular` and `downward_arc_layout`; the full unit suite is green.
- [ ] Live docs (`candle-arrangement-arc.md`, `design.md`, `requirements.md`, `concepts.md`, `resources/chanukah-halacha/candle_arrangement.md`) describe the 9-in parabolic arch; a grep for stale markers (`7-inch`, `7-in`, `8.287`, `59.713`, `26.23`, `95.5`, `peak (0, 68.0)`) returns no hits in live docs (historical plans/stories/context-history are expected and left intact); Task 4 embedded no measured bbox/volume figures from Task 3.
- [ ] Human visual sign-off obtained: a single continuous concave-down parabolic groove from bottom right over the crown (y ≈ 95) to bottom left on the outside face, shamash clear, no holder/holder or holder/connector overlap (final qualification by the user; crown height and foot position finalized and recorded).

## Requesting Clarification

If at any point during story construction there is confusion or ambiguity about the goal or how to accomplish it, stop and ask the user for clarification.

## Notes

- The exact parabolic coordinates, count rule, Bézier groove triple, and 9-in face geometry are settled in `memory-bank/plans/parabolic_arch_layout_plan.md` and the design docs; the story's Task 1 rewrite is pinned by the plan (no ambiguity) — a bounded 2-file TDD task.
- **Resolved decisions (confirmed in the plan)**: (1) feet pinned at `(±63.0, 28.0)` mm (clears adjacent-face holders and the equatorial connector, ~2–3 mm connector margin); (2) crown pinned at `y = 95` mm (90 and 92 also feasible; finalized by the user at the Task 3 visual sign-off — if changed, revise Task 4's figures before merging Group A); (3) groove curve is a single quadratic Bézier `((63.0, 28.0), (0.0, 162.0), (−63.0, 28.0))` drawn with `Bezier` in `main.py`; (4) holder rotation is the parabola tangent with invariants preserved (mirror symmetry, 2-inboard/2-outboard); (5) new constraints — adjacent-face holder non-intersection (0 overlap) and bottom-holder screw-hole clearance (≥ 4.5 mm) — are explicit design and verification requirements; (6) doc cleanup scope is live docs only; historical plans/stories/context-history left intact.
- **Traceability**: the holder–holder collision discovery (adjacent-face foot holders overlapping by ≈ 3375 mm³ per pair in the merged semicircle design — 8 pairs; ≈ 3224 mm³ for the parabola with the old feet) and the screw-hole verification (≈ 22.5 mm clearance, safe) are recorded in the plan and should be captured in the docs so the fix's rationale is traceable.
- The layout registry names (`circular`, `downward_arc_layout`) are kept unchanged so CLI/export/`--show` keys stay stable.
- `manufacture/face_plate_baseline.md` keeps the existing 9-in circular record and gains a 9-in parabolic-arc record; the old 7-in record stays as a historical section.
- Story001/Story002 walkthrough lessons apply to this story's worktrees: verify the worktree branch before committing, use the parent repo's `venv` (it is gitignored and absent from worktrees), and use the `worktrees/` symlink for sub-agent paths.
