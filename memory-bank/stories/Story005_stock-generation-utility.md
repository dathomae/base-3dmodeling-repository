# Story005: Stock Generation Utility

## Goal

Create a stock-generation utility in `src/stock/` that emits `.step` models of the four raw-stock pieces the menorah is milled from, so they can be 3D-printed at 100% infill and used to verify the CAM milling programs on plastic before cutting metal:

| Stock piece | Cross-section / shape | Length / thickness | mm equivalent | Model shape |
|---|---|---|---|---|
| Candle-holder bar | 3/4 in (0.75") square | 12 in | 19.05 × 19.05 × 304.8 | square bar (`Box`) |
| Apex-connector bar | 2 in square | 12 in | 50.8 × 50.8 × 304.8 | square bar (`Box`) |
| Equator-connector bar | 1.5 in square | 12 in | 38.1 × 38.1 × 304.8 | square bar (`Box`) |
| Face-plate stock | 12 × 12 in square **cut in half diagonally** (right isosceles triangle) | 0.05 in | legs 304.8 mm, thickness 1.27 mm | triangular prism (sketch + `extrude`) |

The diagonal cut of the 12×12-in square is a separate pre-mill operation, so the mill stock is one half — a right-isosceles triangle with legs 12 in (304.8 mm) and 0.05 in (1.27 mm) thickness. The full square is **not** generated.

The story also:

- **Extracts the shared `INCH_MM` unit constant** into a common definitions module (`src/common.py`). `INCH_MM = 25.4` is currently defined inside `src/manora/manora_parameters.py` and imported from there by `src/manora/generate_manora.py`, `src/jigs/jig.py`, and `src/jigs/stabilization_block.py`. It is a unit-conversion constant, not menorah-specific, so it belongs in a shared module. The refactor is behavior-preserving: no generated geometry changes, and the existing 26-test unit suite is the regression gate.
- **Reconciles the stale stock documentation** so the memory-bank spec matches the actual stock (0.05-in plate, 12×12-in diagonal halves, 1.5-in equator-connector bar, 12-in bar lengths). The equator connector is milled from **1.5 in** square bar (the code already uses `equatorial_connector_width = 1.5 * INCH_MM`); only the apex connector uses 2-in square bar. The design docs currently say "2 inch" for both — this story fixes that.

All dimensions are **exact nominal** — the stock models carry no FDM compensation and no clearance/tolerance (unlike the jigs). They are geometric stand-ins for the aluminum stock, 3D-printed at 100% infill for CAM verification. The `.step` files are natively in mm (build123d convention). The user's FDM build volume (325 × 325 × 350 mm) accommodates every piece, including the largest (the 304.8 mm half-square face-plate stock and 304.8 mm bars).

## References

Links are relative to the `memory-bank` directory:

- [Stock Generation Plan](../plans/stock_generation_plan.md)
- [Requirements](../requirements.md)
- [Design](../design/design.md)
- [Brief](../brief.md)

## Dependencies

None — the stock utility is independent of the candle-layout work (Story004); it only requires the already-merged `src/` package structure (the `src/manora/`, `src/jigs/`, and `src/stock/` packages with package-qualified imports, the `sys.path` bootstrap convention in entry points and tests, and the empty `src/stock/__init__.py`) and build123d.

## Dependent Stories

None.

## Tasks

### Task Sizing

The architect-for-story-planning reviewed the decomposition, sizing, and parallelism of every task (the recommended decomposition from the plan's Story-Writer Guidance was used as the draft; the architect's decomposition review found **no** task too large and proposed **no** changes):

- **Task 1** is **not** `[Small]`: a behavior-preserving cross-package refactor touching 6 files across 3 directories (one new shared module, one definition→re-export swap, three one-line import re-points, and one new regression test). Large but mechanically uniform — a single coordinated import change with no isolation benefit to splitting. Routes to `code-for-story-implementor`.
- **Task 2** is annotated `[Small]`: two new files (a pure-constants module whose six values are dictated verbatim by the plan, plus a `unittest` pinning each constant). No logic, no abstractions, single concern, template-faithful to the established pure-Python-module + stdlib-`unittest` convention. The TDD red state is a module-missing import error, not an intermediate behavioral cycle. Routes to `small-code-for-story-implementor`.
- **Task 3** is **not** `[Small]` (the plan's guidance labeled it small; the architect **refuted** that): a single new file, but it lays down the stock package's first real code infrastructure — five builders plus an argparse CLI mirroring two 400+ line reference scripts — and its correctness rests on an ad-hoc run-based bbox/volume gate with **no unit-test target** (the agent's own judgment of nominal-vs-round-tripped geometry). Routes to `code-for-story-implementor`, not `small-code`. Still a single cohesive handoff — do **not** decompose (builders and CLI belong in one module).
- **Task 4** is **not** `[Small]`: a run-only artifact-generation and verification task (4 generated `.step` artifacts, bbox/volume gates, human visual sign-off) with no source/test files; the `[Small]` code-edit routing model does not fit it. Routes to `code-for-story-implementor`.
- **Task 5** is a tech-writer task with **no size annotation** (the `[Small]` tag is a routing mechanism between code agents and would be a misnomer for a writing task). Routes to the `technical-writer-for-story-implementor` agent.

### Task 1: Extract `INCH_MM` into `src/common.py` and update imports — Completed

Architect note (decomposition): at its natural granularity. A defensible artifact-free split exists at the "create `common.py` + `manora_parameters` re-export" boundary, but the halves would be trivially small and the change is a single coordinated mechanical import re-point across files where splitting buys zero isolation while costing a worktree, a merge, and a sequential handoff. Large but mechanically uniform — keep as one task routed to `code-for-story-implementor` (never `small-code`).

1. Extract the shared unit constant into `src/common.py` (test-first refactor) - Not Started
   a. Write `tests/test_common.py` (new file, stdlib `unittest`, following the existing test conventions: a `sys.path` insertion at the top so `src/` is importable; `REPO_ROOT` derived from `__file__`). The test imports `common`, `manora.manora_parameters`, and `INCH_MM` from `common` (the derived-constant assertion uses that import) — the literal `25.4` appears only once, as the expected value, so the implementor does not reintroduce a literal elsewhere. The tests assert:
      - `common.INCH_MM == 25.4` — the shared constant's source of truth.
      - `manora.manora_parameters.INCH_MM == 25.4` — the re-export survives (backward compatibility for any legacy `from manora.manora_parameters import INCH_MM` import).
      - `manora.manora_parameters.CANDLE_HOLE_DEPTH_MM == 0.6 * INCH_MM` — regression that the refactor did not disturb the manora constants that derive from `INCH_MM` (both sides compute the identical float expression, so exact equality is safe).
      - Run `source venv/bin/activate && python -m unittest discover -s tests -v` — the new test is **red** because `common` does not exist yet (intended TDD red step; this is not an independent task). - Not Started
   b. Create `src/common.py` with `INCH_MM = 25.4` and a short docstring noting it is the inch→mm conversion shared by all packages. This is the natural future home for other cross-package constants; it starts with `INCH_MM` only. - Not Started
   c. In `src/manora/manora_parameters.py`, replace the local `INCH_MM = 25.4` definition with `from common import INCH_MM`. The name stays resolvable as `manora_parameters.INCH_MM` (re-export), so `CANDLE_HOLE_DEPTH_MM = 0.6 * INCH_MM` and the other in-module derivations keep working. M2 hardware constants (`M2_TAP_SHANK_DIAMETER_MM`, etc.) stay in `manora_parameters.py` — they are menorah-specific. - Not Started
   d. Change the `INCH_MM` import in the three entry-point scripts to import it from its source of truth, `from common import INCH_MM`:
      - `src/manora/generate_manora.py` — remove `INCH_MM` from its `manora_parameters` tuple import (keep the other names from that import).
      - `src/jigs/jig.py` — remove `INCH_MM` from its `manora_parameters` tuple import and keep the `M2_TAP_SHANK_DIAMETER_MM` (and any other hardware) import from `manora_parameters`.
      - `src/jigs/stabilization_block.py` — replace its standalone `from manora.manora_parameters import INCH_MM` with `from common import INCH_MM`. - Not Started
   e. Run `source venv/bin/activate && python -m unittest discover -s tests -v` again — all green: the existing 26 tests plus the new `tests/test_common.py` (the TDD green step; also the behavior-preserving regression gate). - Not Started

### Task 2: Add `src/stock/stock_parameters.py` (TDD) — Completed [Small]

Architect note (decomposition): at its natural granularity — two new files, one concern, one coherent TDD lifecycle; cannot be smaller. Sequential after Task 1 (imports `common.INCH_MM`).

1. Add the stock dimension constants, test-first - Not Started
   a. **Red** — write `tests/test_stock_parameters.py` (stdlib `unittest`, `sys.path` bootstrap as in the existing tests) asserting each constant equals its inch nominal × `INCH_MM` (import `INCH_MM` from `common` in the test):
      - `CANDLE_HOLDER_BAR_SIDE_MM == 0.75 * INCH_MM`
      - `APEX_CONNECTOR_BAR_SIDE_MM == 2.0 * INCH_MM`
      - `EQUATOR_CONNECTOR_BAR_SIDE_MM == 1.5 * INCH_MM`
      - `BAR_LENGTH_MM == 12.0 * INCH_MM`
      - `FACE_PLATE_SQUARE_SIDE_MM == 12.0 * INCH_MM`
      - `FACE_PLATE_THICKNESS_MM == 0.05 * INCH_MM`
      - Run the suite — red (the module does not exist yet). - Not Started
   b. **Green** — create `src/stock/stock_parameters.py`, a pure-constants module (imports only `common` — no `build123d`, no `manora`; this mirrors the "pure Python, unit-testable" convention used by `face_plate_layouts.py`), holding the six constants above with unit suffixes, converted from the inch nominal:
      ```python
      from common import INCH_MM

      CANDLE_HOLDER_BAR_SIDE_MM = 0.75 * INCH_MM      # 3/4 in square bar
      APEX_CONNECTOR_BAR_SIDE_MM = 2.0 * INCH_MM      # 2 in square bar
      EQUATOR_CONNECTOR_BAR_SIDE_MM = 1.5 * INCH_MM   # 1.5 in square bar
      BAR_LENGTH_MM = 12.0 * INCH_MM                  # 12 in long bars
      FACE_PLATE_SQUARE_SIDE_MM = 12.0 * INCH_MM      # 12 in square plate
      FACE_PLATE_THICKNESS_MM = 0.05 * INCH_MM        # 0.05 in thick plate
      ```
      - Run the suite — green. - Not Started

### Task 3: Add `src/stock/generate_stock.py` — Completed

Architect note (decomposition/sizing): at its natural granularity — one new greenfield file; splitting builders from the CLI would require a partial, non-runnable module (an artificial intermediate artifact). **Not** `[Small]`: it lays down the stock package's first code infrastructure (five builders + an argparse CLI mirroring two large reference scripts), and with no unit-test target its acceptance rests on the agent's own run-based bbox/volume gate. Route to `code-for-story-implementor`.

1. Implement the stock generator CLI entry point - Not Started
   a. Implement `create_square_bar(side_mm, length_mm) -> Part` — a `Box(side_mm, side_mm, length_mm)` centered at the origin, length along Z. Then the three thin wrappers using the package constants: `create_candle_holder_stock()` (19.05 × 19.05 × 304.8), `create_apex_connector_stock()` (50.8 × 50.8 × 304.8), `create_equator_connector_stock()` (38.1 × 38.1 × 304.8). - Not Started
   b. Implement `create_face_plate_stock() -> Part` — a right-isosceles triangle sketch in the XY plane with vertices `(0,0)`, `(FACE_PLATE_SQUARE_SIDE_MM, 0)`, `(0, FACE_PLATE_SQUARE_SIDE_MM)` (right angle at the origin, legs along +X/+Y), extruded +Z by `FACE_PLATE_THICKNESS_MM`. Orientation is a plain, deterministic default (bars centered; right-angle corner at the origin); the user sets the WCS in the CAM profile, so no datum features are required. - Not Started
   c. Implement `main()` matching the `src/manora/generate_manora.py` / `src/jigs/jig.py` convention: `argparse` with `-o`/`--outdir` (default `manufacture`) and `-s`/`--show`; the `sys.path` bootstrap rooted at `src/`; the `ocp_vscode` import guarded by try/except; a component dict mapping `candle_holder` → `create_candle_holder_stock()`, `apex_connector` → `create_apex_connector_stock()`, `equator_connector` → `create_equator_connector_stock()`, `face_plate` → `create_face_plate_stock()`; and `export_step` for each of the four output files (`stock_candle_holder.step`, `stock_apex_connector.step`, `stock_equator_connector.step`, `stock_face_plate.step`). The stdout contract mirrors the reference scripts: a per-component "Generating `<name>` …" progress line as each solid is built and exported, followed by a final success summary naming the outdir and the files written — so the run gate has visible confirmation of which files were produced. An unknown `-s` component must error gracefully and list the available names. The `stock_` prefix distinguishes the raw-stock solids from the existing finished-part files (`regular_candle_holder.step`, `apex_connector.step`, `equator_connector.step`, `face_plate_*.step`) already in `manufacture/`. - Not Started
   d. Run-based gate (generation to a **temp** outdir so committed `manufacture/` files are not churned): `source venv/bin/activate && python src/stock/generate_stock.py -o /tmp/stock`, then load each `.step` with build123d's `import_step` and verify the bounding-box sizes match `19.05 × 19.05 × 304.8`, `50.8 × 50.8 × 304.8`, `38.1 × 38.1 × 304.8`, and the face plate (legs 304.8 mm, thickness 1.27 mm), and that the volumes equal the nominal products (`side² × length`, and `(304.8² / 2) × 1.27` for the triangle). STEP re-imports round-trip through the OCCT kernel, so compare with **tolerance** (`assertAlmostEqual`-style, abs delta ≈ 1e-6) — never exact equality. Bars are centered at the origin; the triangle's right-angle corner is at the origin. - Not Started
   e. Verify `-s face_plate` and `-s bogus` behave like the existing scripts: show the component when `ocp_vscode` is available, and error gracefully on an unknown name listing the available component names (`candle_holder`, `apex_connector`, `equator_connector`, `face_plate`). - Not Started

### Task 4: Regenerate `manufacture/stock_*.step` and verify (run-only) — Completed

Run/record over `manufacture/`; no source edits. Depends on Task 3 (the generator must be merged).

Architect note (decomposition): at its natural granularity — a linear generate → gate → sign-off flow over generated artifacts with no source files. The only conceivable split (automation+gates vs. the human visual sign-off) fails the natural-seam test: the sign-off is not independently handoffable to a sub-agent and depends on the gates passing first. Keep as one run-only task routed to `code-for-story-implementor`.

1. Generate the four stock solids into `manufacture/` and verify them - Not Started
   a. Run `source venv/bin/activate && python src/stock/generate_stock.py` (default outdir = `manufacture/`) — produces `manufacture/stock_candle_holder.step`, `manufacture/stock_apex_connector.step`, `manufacture/stock_equator_connector.step`, and `manufacture/stock_face_plate.step`. - Not Started
   b. Confirm the four files exist and pass the bbox/volume gates from Task 3 (load each with `import_step`; bars 19.05/50.8/38.1 mm square × 304.8 mm long; face plate legs 304.8 mm, thickness 1.27 mm; volumes equal the nominal products), compared with tolerance (abs delta ≈ 1e-6) to account for STEP round-tripping. - Not Started
   c. **Human visual sign-off gate**: inspect the four stock solids in `ocp_vscode` (`python src/stock/generate_stock.py -s <component> -o /tmp/stock_show`) — a thin 304.8 mm right-isosceles-triangle plate (1.27 mm thick) and three 304.8 mm square bars of 19.05/50.8/38.1 mm cross-section — and confirm correct shape and orientation (bars centered; triangle right-angle corner at the origin). This is the story's final geometric gate regardless of task numbering, surfaced to the user. The stock spec is settled (no numeric decision is open at sign-off, unlike Story004's crown/foot decision), so a sign-off finding cannot invalidate Task 5's doc content — the only possible outcome needing follow-up is a shape/orientation bug, which would be fixed in the generator (Task 3) before the story completes. - Not Started

### Task 5: Reconcile stock documentation — Completed

Tech-writer task; routes to the `technical-writer-for-story-implementor` agent, not a code agent. Depends on Tasks 1–3 conceptually (documents the implemented stock spec) and is file-disjoint from Task 4.

Architect note (decomposition): at its natural granularity — each per-file edit is small, but the subtasks form ONE semantic unit: every live doc must describe the same stock spec (0.05-in plate, 12×12 diagonal halves, 0.75/1.5/2-in bars, 12-in lengths) with no internal inconsistency. Splitting per-file would multiply coordination overhead and raise inconsistency risk with no isolation benefit. This matches the "single coordinated mechanical change across many files — keep as one task" rule. Keep as one writing task.

**Coordination guard**: this task must **not** embed any measured bounding-box/volume figures from Task 4 (embedding them would create a hidden dependency and break the parallel group). All content is derivable from the plan's settled stock spec — the stock specification is settled in `memory-bank/plans/stock_generation_plan.md`, not derived from the run.

1. Reconcile the memory-bank stock documentation - Not Started
   a. `memory-bank/requirements.md` — Non-Functional Requirement #2 "Stock Material": faces from **0.05 in** plate cut into **12×12 in squares, then halved diagonally** (one half per face); candle holders from **0.75 in square bar**; apex connectors from **2 in square bar**; equator connectors from **1.5 in square bar**; all bars **12 in long**. Optionally note the plastic stock is 3D-printed at 100% infill for CAM verification. Also reconcile **every** remaining stale reference in the file so the acceptance grep passes — in particular Constraint #2 "Material Yield" currently says the 8 sides must fit within the "12 inch by 48 inch aluminum plate", which is stale once the plate stock is the 12×12-in square halved diagonally; reword the yield statement against the settled stock spec (each 9-in face milled from one diagonal half of a 12×12-in square of 0.05-in plate). - Not Started
   b. `memory-bank/design/design.md` — face-plate "Thickness: 0.1 inches" → **0.05 inches** (1.27 mm); equator-connector "Material: 2 inch square aluminum bar stock" → **1.5 inch** square aluminum bar stock (38.1 mm). The apex connector keeps its 2-in square bar material. - Not Started
   c. `memory-bank/brief.md` — "Key Design Considerations" Material bullet: the 0.5-in holder bar → **0.75 in**, the 0.1-in plate → **0.05 in**, and the 12×48 sheet → **12×12-in squares halved diagonally** (one half per face). - Not Started
   d. `memory-bank/context.md` — record the start of this task and clear it on completion, per the standard task discipline. - Not Started
   e. Grep the live docs for the contiguous stale markers (`0.1 inch`, `0.5 inch square`, `12 inch by 48 inch`) — zero hits. The equator-connector "2 inch" marker is **qualified**, not grep-visible: `design.md` renders the equator material as "2 inch (50.8 mm) square", so the executable check is that the **Equator Connector** part's Material line reads **1.5 inch** (subtask b), while the Apex Connector's 2-inch material legitimately remains. Frozen historical records (`memory-bank/plans/*`, `memory-bank/stories/*`, and the "Recently Completed" history in `context.md`) are expected to retain the old figures and are left intact. - Not Started

### Parallel Execution

- **Group A: Tasks 4 and 5** — File-disjoint and independent. Task 4 writes the four new `manufacture/stock_*.step` artifacts (verified absent today; no other task writes to `manufacture/` — Task 3 exports to a temp dir only). Task 5 writes `memory-bank/requirements.md`, `memory-bank/design/design.md`, `memory-bank/brief.md`, and `memory-bank/context.md`. No shared infrastructure file, no compile-time or semantic dependency. Task 5's content (stock spec, dimensions, doc figures) comes from the settled plan, **not** from Task 4's measurements — Task 5 must not embed Task 4's measured bbox/volume figures (hidden dependency guard, enforced by a static grep). Each task is independently verifiable: Task 4 via bbox/volume gates + human visual sign-off; Task 5 via the stale-marker grep. **Residual hazard**: unlike Story004, there is no open numeric decision at Task 4's sign-off that could invalidate Task 5's figures, so no group-level revision trigger exists — the only sign-off outcome needing follow-up is a shape/orientation bug, which is fixed in the generator before the story completes. Contingency: if Task 4's gates fail, the artifacts must not be recorded and the generator (Task 3) needs rework.
- All other task pairs are sequential: Task 2 depends on Task 1 (`stock_parameters.py` does `from common import INCH_MM`, and `src/common.py` does not exist at the base commit); Task 3 depends on Task 2 (`generate_stock.py` imports the constants from `stock_parameters`, which does not exist at the base commit); Group A depends on Task 3 (Task 4 runs the Task 3 generator; Task 5 documents the implemented feature). These are genuine worktree compile-time dependencies, not merely recommended ordering.

### Execution Order

```
        ┌─────────────┐
        │  Task 1     │  (extract INCH_MM into src/common.py — code-for-story-implementor)
        └──────┬──────┘
               ▼
        ┌──────┴──────┐
        │  Task 2     │  (src/stock/stock_parameters.py TDD — [Small], small-code agent)
        └──────┬──────┘
               ▼
        ┌──────┴──────┐
        │  Task 3     │  (src/stock/generate_stock.py — code-for-story-implementor)
        └──────┬──────┘
               ▼
     ┌─────────┴──────────┐
     │                    │
┌────┴──────┐   ┌─────────┴────┐
│ Task 4    │   │  Task 5     │
│(manufact.)│   │ (memory-bank)│
└───────────┘   └─────────────┘
   ───────── Group A (parallel): Tasks 4, 5 ─────────
```

Task 1 must be merged before Task 2 starts (Task 2 imports `common.INCH_MM`). Task 2 must be merged before Task 3 starts (Task 3 imports the `stock_parameters` constants). Task 3 must be merged before Group A starts (Task 4 runs Task 3's generator; Task 5 documents the implemented feature). Task 4's human visual sign-off gate (subtask c) is the story's **final geometric gate** — surfaced to the user for the final qualification of the stock solids' shape and orientation.

### Reintegration

Reintegration instructions refer to the "story branch" generically (the branch the story-implementor selects at runtime via the user configuration).

**Sequential chain (Task 1 → Task 2 → Task 3):**
- Merge order: Task 1 branch first, then Task 2, then Task 3. Each downstream task's branch imports a module that does not exist at the base commit (`src/common.py` for Task 2, `src/stock/stock_parameters.py` for Task 3), so each must build on the merged state of its predecessor — worktrees branched from the shared base cannot resolve those imports.
- Integration test: after each merge, run `source venv/bin/activate && python -m unittest discover -s tests -v` — confirms the growing tree (Task 1's `test_common.py`, then Task 2's `test_stock_parameters.py`) stays green on the combined state the next task builds on.
- Watch for conflicts in: `src/common.py`, `src/stock/stock_parameters.py` (each created once, by a single task within this story — no intra-story conflict), `src/manora/manora_parameters.py`, `src/manora/generate_manora.py`, `src/jigs/jig.py`, `src/jigs/stabilization_block.py` (touched only by Task 1 within this story, but equally exposed to concurrent parent-repo stories touching them), and the shared `tests/` directory (the parent repo's test files could gain concurrent edits).

**Group A (Tasks 4, 5):**
- Merge order: any order — use finish-order (the first task to pass review merges first; task-number tiebreaker). The trees are fully disjoint (`manufacture/stock_*.step` vs `memory-bank/*.md`) with no shared infrastructure or generator→consumer relationship.
- Integration tests (run from the repo root on the merged story branch):
  - `source venv/bin/activate && python -m unittest discover -s tests -v` — the full unit suite stays green after the group merges (Tasks 4–5 touch no code, so this is a no-op pass confirming the merges did not disturb the code chain).
  - `source venv/bin/activate && python src/stock/generate_stock.py -o /tmp/stock` — end-to-end generation on the merged branch; confirm the four solids pass the bbox/volume gates (bars 19.05/50.8/38.1 mm square × 304.8 mm; face plate legs 304.8 mm, thickness 1.27 mm). **Do not** textual-diff the fresh export against the committed `manufacture/stock_*.step` files — STEP export entity ordering is nondeterministic between runs, so spurious diffs are expected; the bbox/volume gates are the comparison oracle.
  - The Task 4 human visual sign-off gate (subtask c) — the story's final geometric gate regardless of task numbering.
- Watch for conflicts in: `memory-bank/context.md` (modified by Task 5 in its branch; the story-implementor also updates it on the base branch per the memory-bank task-record discipline during Tasks 1–3 — defer base-branch `context.md` writes until after Task 5's branch merges, or expect a coordinator-resolved merge conflict on this file); `memory-bank/stories/toc.md` and the Story005 story file (coordinator-edited on the base branch — instruct Task 4 and Task 5 branches to leave these untouched so they never enter a worktree branch); `manufacture/*.step` (only Task 4 writes the four new `stock_`-prefixed files, which do not collide with the existing finished-part files — but re-running the generator during merge verification produces nondeterministic entity-ordering diffs, so export to `/tmp/stock` rather than regenerating over committed artifacts); the shared `tests/` directory (neither Group A task touches it, but it is a merge watch point if concurrent parent-repo stories add test files in the same window). No lock files involved (Python, stdlib `unittest` only). `venv/` is gitignored and absent from worktrees — every verification run inside a worktree must use the parent repo's `venv` via its absolute path (see the Story001/Story002 walkthrough lessons); never recreate a venv inside a worktree.

## Test-First Development

This project follows the Logical TDD Lifecycle. The coding tasks with a natural unit-test target integrate the test-and-implement cycle inside the task:

- **Task 1** (refactor) writes the new `tests/test_common.py` first (subtask a — the red step: `common` does not exist), then creates `src/common.py`, swaps the definition for the `manora_parameters` re-export, re-points the three entry-point imports, and runs the suite to green (subtask e). The existing 26-test suite is the behavior-preservation regression gate for the refactor.
- **Task 2** follows the full red → implement → green TDD cycle as one unit: `tests/test_stock_parameters.py` first (red — the module does not exist), then the pure-constants module, then the suite to green.
- **Task 3** is a single greenfield generator file with **no unit-test target** (the build123d geometry is verified by run-only generation): its acceptance rests on the run-based bbox/volume gate in subtask d and the `-s`/unknown-component CLI checks in subtask e, not on the regression suite.
- **Task 4** is run-based verification with programmatic gates (bbox/volume) plus the human visual sign-off gate (subtask c) surfaced to the user.
- **Task 5** is a documentation task with no test target (verified by the stale-marker grep in its acceptance criteria).

All new tests use Python's stdlib `unittest` with the established `sys.path`-bootstrap convention (no new dependency added to `requirements.txt`).

## Constraints

- **Exact nominal dimensions**: the stock models have no FDM hole compensation and no clearance/tolerance. They are geometric stand-ins for the aluminum stock (3D-printed at 100% infill for CAM verification). The face-plate stock is **one diagonal half** of a 12×12-in square (right-isosceles triangle, legs 304.8 mm, thickness 1.27 mm) — the full square is not generated (cut off-mill).
- **No new dependency**: stdlib `unittest` only; build123d is already a project dependency. Do not add pytest or any package to `requirements.txt`.
- **Module purity**: `src/stock/stock_parameters.py` imports only `common` (no `build123d`, no `manora`); `src/common.py` has no imports. This mirrors the "pure Python, unit-testable" convention used by `face_plate_layouts.py`.
- **Refactor is behavior-preserving**: moving `INCH_MM` must not change any generated geometry; the existing 26-test suite is the regression gate. `manora_parameters.INCH_MM` must stay resolvable (re-export) so any legacy import keeps working; M2 hardware constants stay in `manora_parameters.py`.
- **CLI convention**: `generate_stock.py` matches the `generate_manora.py`/`jig.py` convention — `-o`/`--outdir` (default `manufacture`), `-s`/`--show`, `sys.path` bootstrap, guarded `ocp_vscode` import, graceful "unknown component" error listing available names.
- **Datum/orientation**: no special datum features on the stock models; the user sets the WCS in the CAM profile. Deterministic default orientation only (bars centered at the origin; triangle right-angle corner at the origin).
- **Documentation rule**: do **not** rewrite frozen historical records (`memory-bank/plans/*`, `memory-bank/stories/*`, and the "Recently Completed" history in `context.md`). Only live, current-state docs are updated.
- **Environment**: the Python virtual environment lives at `venv/`; activate it with `source venv/bin/activate` before running `python` commands. In git worktrees, use the parent repo's `venv` via its absolute path (see the Story001/Story002 walkthrough lessons). Use temp `-o /tmp/...` outdirs for any generation that must not churn the committed `manufacture/*.step` files.
- **Convention followed**: Story001 introduced the `tests/` directory and `unittest`-based tests; this story follows that convention. **Organizational extension (stated)**: `src/common.py` is the first shared top-level module outside the three packages (`manora`, `jigs`, `stock`) — this extends the src-rooted layout without changing package conventions: the existing `sys.path` bootstrap rooted at `src/` already makes the bare `common` name importable, and package-specific constants remain local to their packages.

## Intent

The purpose of each task, stated so the goal remains clear even if implementation details change:

- **Task 1** — Give the shared inch→mm unit constant a single source of truth (`src/common.py`) and make every consumer import it from there, with the `manora_parameters` re-export preserving backward compatibility and the existing suite proving the refactor changed no geometry.
- **Task 2** — Pin the stock package's dimension constants (0.75/2.0/1.5-in bar sides, 12-in bar length, 12-in square / 0.05-in face-plate stock) by unit tests written first, so the generator builds on verified, pure-Python constants.
- **Task 3** — Provide the single CLI entry point (`src/stock/generate_stock.py`) that builds and exports the four raw-stock solids (three square bars and the half-square face-plate prism) to `.step`, verified by bbox/volume gates against the exact nominal dimensions.
- **Task 4** — Regenerate the persistent `manufacture/stock_*.step` artifacts from the merged generator and verify them against the same bbox/volume gates, ending with the user's visual sign-off of the four stock solids.
- **Task 5** — Keep the project's requirements, design, brief, and context documentation consistent with the actual stock (0.05-in plate halved diagonally from 12×12-in squares, 0.75/1.5/2-in square bars, 12-in lengths), removing all stale figures from the live docs while leaving frozen historical records intact.

## Acceptance Criteria

- [ ] `src/common.py` exists with `INCH_MM = 25.4`; `src/manora/manora_parameters.py` imports (not defines) it and still resolves `manora_parameters.INCH_MM` (re-export); `src/manora/generate_manora.py`, `src/jigs/jig.py`, and `src/jigs/stabilization_block.py` import `INCH_MM` from `common`; the M2 hardware constants remain in `manora_parameters.py`.
- [ ] `tests/test_common.py` exists and asserts `common.INCH_MM == 25.4`, `manora_parameters.INCH_MM == 25.4`, and `manora_parameters.CANDLE_HOLE_DEPTH_MM == 0.6 * INCH_MM`.
- [ ] `source venv/bin/activate && python -m unittest discover -s tests -v` passes — existing 26 tests plus `test_common.py` and `test_stock_parameters.py` green.
- [ ] `src/stock/stock_parameters.py` imports only `common` and its six constants equal their inch nominals × `INCH_MM`; `tests/test_stock_parameters.py` pins each one (written first, red → green).
- [ ] `python src/stock/generate_stock.py -o /tmp/stock` emits `stock_candle_holder.step`, `stock_apex_connector.step`, `stock_equator_connector.step`, and `stock_face_plate.step`.
- [ ] Bounding-box/volume gates (via `import_step`): bars 19.05/50.8/38.1 mm square × 304.8 mm long; face plate legs 304.8 mm, thickness 1.27 mm; volumes equal the nominal products (`side² × length`; `(304.8² / 2) × 1.27` for the triangle) — compared with tolerance (abs delta ≈ 1e-6), never exact equality, because STEP re-imports round-trip through the OCCT kernel.
- [ ] `manufacture/stock_*.step` regenerated (default outdir) and match the same gates.
- [ ] `-s` shows a component (when `ocp_vscode` is available) and `-s bogus` errors gracefully listing the component names (`candle_holder`, `apex_connector`, `equator_connector`, `face_plate`).
- [ ] Live docs (`requirements.md` NFR #2 and the Material Yield constraint, `design.md`, `brief.md`) reflect 0.05-in plate / 12×12-in diagonal halves / 1.5-in equator bar / 12-in bar lengths; a grep for the contiguous stale markers (`0.1 inch`, `0.5 inch square`, `12 inch by 48 inch`) returns no hits in live docs, and the **Equator Connector** Material line in `design.md` reads **1.5 inch** (the 2-inch marker is qualified — `design.md` renders it "2 inch (50.8 mm) square", so it is not grep-visible, and the Apex Connector's 2-inch material legitimately remains); historical plans/stories/context-history are expected and left intact; Task 5 embedded no measured bbox/volume figures from Task 4.
- [ ] Human visual sign-off obtained: the four stock solids (three 304.8 mm square bars of 19.05/50.8/38.1 mm cross-section and a thin 1.27 mm right-isosceles-triangle plate with legs 304.8 mm) have correct shape and orientation (bars centered; triangle right-angle corner at the origin).

## Requesting Clarification

If at any point during story construction there is confusion or ambiguity about the goal or how to accomplish it, stop and ask the user for clarification.

## Notes

- The stock specification is **settled** in `memory-bank/plans/stock_generation_plan.md` (no open questions): bar stock 12 in long for all three cross-sections; equator connector milled from 1.5-in square bar (2-in square is apex-only; the code already agrees, the docs are fixed here); face plate 0.05 in thick as one diagonal half of a 12×12-in square (the full square is not generated — the diagonal cut is off-mill); no datum features (the user sets the WCS in the CAM profile); `src/common.py` starts with `INCH_MM` only; exact nominal dimensions with no FDM compensation or clearance on the stock models.
- The equator connector's 2-in→1.5-in correction and the face-plate thickness 0.1→0.05-in correction are doc-only fixes in Task 5 — the generator code already uses `equatorial_connector_width = 1.5 * INCH_MM`, and the stock constants in Task 2 encode the corrected spec.
- Component keys for `-s`/`--show` (`candle_holder`, `apex_connector`, `equator_connector`, `face_plate`) and export names (`stock_*.step`) are new names; the `stock_` prefix distinguishes the raw-stock solids from the existing finished-part files already in `manufacture/`.
- The four generated artifacts are new files — no existing `manufacture/` file is regenerated, deleted, or renamed by this story (unlike Story004's regen tasks, which churned the whole artifact set).
- Task 3's `[Small]` label was removed at the architect's sizing review (new package infrastructure, no unit-test target, run-gate verification). Task 2 keeps `[Small]`. Task 5 carries no size annotation (a writing task routed by type to `technical-writer-for-story-implementor`).
- Organizational extension: this story introduces the first shared top-level module under `src/` (`src/common.py`); it is consistent with the src-rooted `sys.path` convention (see the Constraints section) and is not a package-convention change.
- Architect review notes are embedded in each task so the story-implementor understands the sizing/decomposition decisions without re-deriving them.
- Story001/Story002 walkthrough lessons apply to this story's worktrees: verify the worktree branch before committing, use the parent repo's `venv` (it is gitignored and absent from worktrees), and use the `worktrees/` symlink for sub-agent paths.
