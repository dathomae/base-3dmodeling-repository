# Story007: Python Structure and Setup

## Goal

Establish the template repository's Python project structure and developer onboarding per **Steps 4–6** of `memory-bank/plans/base-repository-setup_plan.md` (the "Base Repository Setup" plan). This is the coding/setup story of the setup arc (following Story006's cleanup; Steps 1–3 and 7–8 of the plan belong to other stories).

Specifically, this story:

- **Lays down a standard `src/`-layout Python package** under a new placeholder package `src/scaffold/` with a PEP 621 `pyproject.toml`, a trivial build123d `make_box()` example plus a `.step`-exporting CLI, and a matching unit test — the "smoke-test example" that gives any derived repo an immediate end-to-end verification (`setup.sh` → `pytest` → generate a `.step`).
- **Replaces the dependency/install conventions**: `requirements.txt` is deleted (superseded by `pyproject.toml`); the menora project's `venv/bin/activate` + stdlib-`unittest` convention is replaced by a plain **`.venv`** + pip install with **pytest** as the test runner (`python -m pytest`). This is a deliberate **convention change** for the whole repository.
- **Creates `manufacture/`** as the gitignored `.step` output directory (kept tracked via `manufacture/.gitkeep`), writes the repository `.gitignore`, and replaces the GPL-3.0 `LICENSE` with **MIT** text (the `license` field in `pyproject.toml` must match).
- **Adds the two setup scripts**: developer-facing `setup.sh` (creates `.venv`, upgrades pip, `pip install -e .`) and `.kilo/setup-script.sh` (thin wrapper the story-implementor worktree flow already expects for environment bootstrap).
- **Writes the onboarding docs**: `GETTINGSTARTED.md` (full onboarding: deriving a new repo, `setup.sh`, the build123d → `.step` → slicer/CAM methodology, renaming the `scaffold` package, the memory-bank plan/story workflow, and viewing models in `ocp_vscode`) and a **minimal** `README.md` (title, one-line description, pointer to `GETTINGSTARTED.md` only).

Nothing in this story touches `memory-bank/` content, `resources/`, `.kilocode/rules/`, `scripts/`, or `.kilo/agent/*` — those belong to the sibling setup stories. The `scaffold` package is a placeholder that a derived repository renames (documented in `GETTINGSTARTED.md`).

## References

Links are relative to the `memory-bank` directory:

- [Base Repository Setup Plan](../plans/base-repository-setup_plan.md) — Steps 4, 5, and 6 are the authoritative source for this story; Steps 1–3, 7, 8 are covered by sibling stories.
- [Organization rules](../../.kilocode/rules/organization.md) (referenced by the plan for the `manufacture/` directory convention)

## Dependencies

- [Story006_base-repo-cleanup.md](Story006_base-repo-cleanup.md) — Not Started. The repository must be free of the menora project's content before the new Python structure is added, per the plan's execution order. This story's `pyproject.toml`, `.gitignore`, `src/`, and `tests/` must be created on the cleaned, project-agnostic tree.

## Dependent Stories

- [Story009_template-verification.md](Story009_template-verification.md) — Not Started (verifies this story's `setup.sh`/pytest/example output end-to-end from a clean state, per plan Step 8).
- [Story010_stories-reset.md](Story010_stories-reset.md) — Not Started (terminal story; resets `stories/` and `finished-stories/`, removing this arc's meta-stories once complete, per plan Step 3).

## Tasks

### Task Sizing

The architect-for-story-planning reviewed the decomposition, sizing, and parallelism of every task (the plan's Story-Writer Guidance decomposition — Steps 4–6 in one story with the single coding task following test-first — was used as the draft; the architect's decomposition review found **no** task too large and proposed **no** changes):

- **Task 1** is annotated `[Small]`: one new file (`pyproject.toml`), one concern (the PEP 621 packaging manifest), purely additive, contents fully dictated by the plan's settled decisions (src-layout, `build123d` + `pytest` dependencies, MIT license field, `[tool.pytest.ini_options]`). Routes to `small-code-for-story-implementor`.
- **Task 2** is **not** `[Small]`: four distinct repository-level file operations (create `.gitignore`, create `manufacture/.gitkeep`, delete `requirements.txt`, replace `LICENSE` with MIT text) spanning several concerns (ignore rules, output-directory tracking, obsolete-manifest removal, license text). Mechanical and uniform, but multi-file/multi-concern — below the 2-file `[Small]` threshold. Routes to `code-for-story-implementor`.
- **Task 3** is **not** `[Small]`: the test+implementation pair is one coherent TDD lifecycle (write the failing test, implement the package, run to green) and **must not** be split; it creates a new package (`src/scaffold/__init__.py` + `src/scaffold/example.py`) — new code infrastructure — plus `tests/test_example.py`, and requires a real environment bootstrap (`.venv`, dependency install, `pip install -e .`) to run the pytest cycle. Routes to `code-for-story-implementor`.
- **Task 4** is **not** `[Small]`: two new executable shell scripts defining the environment-bootstrap convention (new infrastructure), verified by a run-based gate (`./setup.sh` from a clean state → `.venv` → editable install → pytest green). `setup.sh` and `.kilo/setup-script.sh` are one semantic unit (the wrapper reuses the same install steps), so splitting them would be artificial. Routes to `code-for-story-implementor`.
- **Task 5** is a tech-writer task with **no size annotation** (the `[Small]` tag is a routing mechanism between code agents and would be a misnomer for a writing task). Routes to the `technical-writer-for-story-implementor` agent.

### Task 1: Write `pyproject.toml` (PEP 621 project metadata) — Completed [Small]

Architect note (decomposition/sizing): at its natural granularity — one new file, one concern (the packaging manifest), contents fully settled by the plan. Genuinely `[Small]` (≤ 2 files, additive, single domain, no new abstractions); cannot be smaller. Sequential-before Task 3 only (Task 3's `pip install -e .` and pytest `pythonpath` rely on this file). Its full functional verification (`pip install -e .` succeeding) happens in Tasks 3 and 4 because the `scaffold` package must exist first.

1. Write the PEP 621 packaging manifest — Not Started
   a. Create `pyproject.toml` at the repo root declaring, per the plan's settled decisions and design decisions (see plan "Design decisions" and "Resolved Decisions" 1 and 3):
      - `[build-system]` — `setuptools` backend (e.g., `requires = ["setuptools>=68"]`, `build-backend = "setuptools.build_meta"`).
      - `[project]` metadata — `name = "scaffold"` (the placeholder package name a derived repo renames; documented in `GETTINGSTARTED.md`, Task 5), a one-line description of the placeholder modeling package, `requires-python` set conservatively to a Python version compatible with the installed `build123d` (confirm against `resources/apis/build123d/` install notes; use `>=3.10` unless those notes say otherwise), and `version` (e.g., `0.1.0`).
      - `dependencies = ["build123d", "pytest"]` — **no third-party dependency beyond `build123d` and `pytest`** (plan constraint). Per the plan, pytest is declared as a regular dependency (not an optional extra) so the single editable install in `setup.sh` provides the test runner; this is deliberate (see Notes).
      - The project `license` field set to **MIT** (SPDX), matching the MIT `LICENSE` file written in Task 2 (consistency verified at integration — the two files are in different tasks of the same parallel group; see the Task 2 subtask e note and the Group A reintegration checks).
      - `[tool.setuptools.packages.find]` with `where = ["src"]` so the `scaffold` package is discovered under the `src/` layout.
      - `[tool.pytest.ini_options]` — `testpaths = ["tests"]` and `pythonpath = ["src"]` (pytest ≥ 7), so `python -m pytest` from the repo root discovers the tests and imports the `src/`-layout package without requiring a prior editable install. This is what lets Task 3 run the test-and-implement cycle against the raw tree.
   b. Verify the manifest parses and carries the required fields: run `python -c "import tomllib, pathlib; d = tomllib.loads(pathlib.Path('pyproject.toml').read_text()); assert d['project']['name'] == 'scaffold'; assert set(d['project']['dependencies']) == {'build123d', 'pytest'}; assert 'license' in d['project']"` (tomllib is stdlib on Python 3.11+; adjust the python used for the check as needed). Do **not** run `pip install -e .` here — it would fail because `src/scaffold/` does not exist yet; that gate belongs to Task 3. - Not Started

### Task 2: Repo hygiene — `.gitignore`, `manufacture/.gitkeep`, delete `requirements.txt`, replace `LICENSE` with MIT — Completed

Architect note (decomposition): at its natural granularity — four distinct but trivially small repository-level file operations that form one "finish the repo-level config" pass over plan Step 4 letters d–f. Splitting them into four tasks would create four near-empty worktrees with zero isolation benefit. **Not** `[Small]` (4 files, multi-concern: ignore rules, output-directory tracking, deletion, license text) — route to `code-for-story-implementor`. File-disjoint from Task 1 (Group A).

1. Write the repository hygiene files — Not Started
   a. Create `manufacture/.gitkeep` (empty file) so the `.step` output directory is present in git even though its contents are ignored. - Not Started
   b. Create `.gitignore` at the repo root containing exactly the plan Step 4 letter (d) patterns: `.venv/`, `__pycache__/`, `*.pyc`, `manufacture/*.step`, `.kilo/worktrees/`, `*.egg-info/`, `dist/`, `build/`. Notes: `.venv/` is the new environment location (this story's convention — the menora project used `venv/`); `manufacture/*.step` keeps generated `.step` files out of git (plan design decision; `manufacture/.gitkeep` keeps the directory); `.kilo/worktrees/` keeps story-implementor worktrees untracked (also referenced by plan Step 1 letter (c), which Story006 executes — if Story006 left a partial `.gitignore`, supersede it so the final file contains **all** the patterns above). - Not Started
   c. Delete `requirements.txt` (superseded by `pyproject.toml`; resolved decision 1 — plain `venv` + pip, dependency manifest is `pyproject.toml` only). - Not Started
   d. Replace the `LICENSE` GPL-3.0 text with the standard **MIT** license text (resolved decision 3; MIT is the default, Apache-2.0 the acceptable alternative — if the alternative is chosen, Task 1's `pyproject.toml` license field must be updated to match before Group A merges). Preserve the copyright attribution carried by the existing LICENSE (convert the notice to the MIT form) rather than inventing a holder; if no attributable holder can be determined, stop and request clarification per the Requesting Clarification section. - Not Started
   e. Verify the file state: `git ls-files` no longer lists `requirements.txt` (or it was not tracked and is simply absent from the working tree after deletion); `git status --porcelain`/`git ls-files` shows `manufacture/.gitkeep` present; a grep of `.gitignore` finds each required pattern; the first line of `LICENSE` reads `MIT License` and the permission/liability boilerplate is present. **Cross-file consistency**: the `license` field in Task 1's `pyproject.toml` must equal `MIT` — this is a post-merge check performed when Group A reintegrates (Task 1's manifest and this task's LICENSE are plan-settled to MIT, so no behavioral dependency exists between the two tasks). - Not Started

### Task 3: Add `src/scaffold/` box example with passing test (test-first, TDD) — In Progress

Covers plan Step 4 letters (a) and (b): write `tests/test_example.py` **before** `src/scaffold/` (Logical TDD Lifecycle), then implement, then run to green — all inside this one task.

Architect note (decomposition): at its natural granularity — the red test step is a deliberately failing state, not an independently mergeable deliverable; splitting the test write from the package implementation would split one TDD lifecycle across two tasks with no isolation benefit (the "do not break the test-and-implement cycle into separate tasks" rule). **Not** `[Small]`: lays down the first package infrastructure of the new tree (`src/scaffold/__init__.py`, `src/scaffold/example.py` — a function **and** a CLI in a new package), plus a test file, and its verification requires a real environment bootstrap. Routes to `code-for-story-implementor`.

1. Create the scaffold package, test-first — Not Started
   a. **Red** — write `tests/test_example.py` first (plan Step 4a). Use **pytest** style (plain `def test_...()` functions and `assert`, **not** stdlib `unittest` classes — the new convention; see Notes). The test imports the package (`from scaffold.example import make_box`) and asserts:
      - `make_box()` returns a build123d **`Part`/`Solid`** — assert the result is an instance of build123d's `Part` (a `Solid` subclass, per the plan: "a build123d `Part`/`Solid` with the expected bounding box").
      - **the expected bounding box** — with the default `make_box()` producing a cube of side `10` mm centered at the origin, assert `part.bounding_box().size` is `(10, 10, 10)` in X/Y/Z (and/or the box spans `−5..5` in each axis). Use a tolerance (pytest `approx` or an explicit `assertAlmostEqual`-style delta) because build123d bounding boxes are computed floats; the test and the implementation must agree on the exact default size (10 mm cube is the settled default for this task).
      - Run the suite with `.venv/bin/python -m pytest` — but note the `.venv` environment does not exist until subtask b bootstraps it, so do the red run at the top of subtask b (immediately after the environment is created, before installing dependencies is even required for the collection error to appear). The test is **red**: it fails/errors because `scaffold` does not exist yet (ModuleNotFoundError / collection error). This is the intended TDD red step; it is not an independent task. - Not Started
   b. Bootstrap the test environment (needed to run pytest at all — the repository has no Python environment until this story creates it): create `.venv` with `python3 -m venv .venv`, upgrade pip (`.venv/bin/python -m pip install --upgrade pip`), and install the two declared dependencies directly (`.venv/bin/python -m pip install build123d pytest`) so the runner and the modeling library exist before the package is implemented. (Installing the deps by name is a bootstrap convenience for this task only; Task 4's `setup.sh` formalizes environment creation as a single `pip install -e .`, which resolves the same set from `pyproject.toml`.) `.venv/` is gitignored (Task 2) and never committed. Run the **red** step here (see subtask a): `.venv/bin/python -m pytest` fails/errors because `scaffold` does not exist yet. - Not Started
   c. **Implement** `src/scaffold/__init__.py` and `src/scaffold/example.py` (plan Step 4b):
      - `src/scaffold/example.py` defines `make_box()` — a trivial build123d box builder (e.g., `Box(10, 10, 10)` centered at the origin) returning a `Part` — plus a minimal `argparse` CLI (`main()`) that exports the box to a `.step` file in `manufacture/` by default (`export_step`; build123d's default outdir convention), with an `-o/--outdir` option and an `if __name__ == "__main__":` guard so `python -m scaffold.example` works (the documented CLI for the plan's completion criteria). Output filename: `scaffold_box.step` (deterministic name for the gates).
      - `src/scaffold/__init__.py` — the package marker; keep it minimal (short docstring; a re-export of `make_box` is optional).
      - Only `build123d` is imported for geometry; the module stays a simple, dependency-light example that a derived repo replaces wholesale. - Not Started
   d. Complete the environment and run to **green**: `.venv/bin/python -m pip install -e .` (the editable install — must succeed now that `pyproject.toml` (Task 1) and `src/scaffold/` both exist; this is the plan's `pip install -e .` completion criterion, and it installs `pytest` + `build123d` from the manifest), then run `.venv/bin/python -m pytest` — **all tests pass** (the TDD green step). - Not Started
   e. Run the example CLI end-to-end: `.venv/bin/python -m scaffold.example` (default outdir `manufacture/`) and confirm `manufacture/scaffold_box.step` is written. The file is gitignored (Task 2) so it appears in the working tree but is never committed — that is the intended state (`.step` files are generated artifacts). - Not Started

### Task 4: Write `setup.sh` and `.kilo/setup-script.sh` — Not Started

Covers plan Step 5 letters (a) and (b). Depends on Task 3 (the scripts' verification installs the `scaffold` package and runs its pytest suite, so `src/scaffold/` must already be merged).

Architect note (decomposition): at its natural granularity — two new scripts forming one semantic unit (`.kilo/setup-script.sh` is a thin wrapper around the same install `setup.sh` performs), with a run-based verification gate. **Not** `[Small]`: lays down the environment-bootstrap convention as new executable infrastructure and cannot be verified by inspection alone. Route to `code-for-story-implementor`.

1. Write the two setup scripts — Not Started
   a. Write `setup.sh` (executable; `#!/usr/bin/env bash` with `set -euo pipefail`) at the repo root performing, per plan Step 5a: create the virtual environment with `python3 -m venv .venv` (the **new `.venv` convention** — not the menora project's `venv/`), upgrade pip, then `pip install -e .` (installs the package and its `build123d` + `pytest` dependencies from `pyproject.toml`). End by printing next steps and the model-viewer hint: how to run the tests (`python -m pytest`), run the example (`python -m scaffold.example`), and the `ocp_vscode` hint for viewing models (do **not** install `ocp_vscode` in the script — it is a hint only). The script should invoke `.venv/bin/python` / `.venv/bin/pip` directly (no activation required inside the script). - Not Started
   b. Write `.kilo/setup-script.sh` (executable) as a **thin wrapper around the same install** (plan Step 5b): it must perform the same `.venv` + pip + `pip install -e .` bootstrap that `setup.sh` performs (either by invoking `setup.sh` from the repo root or by replicating its core lines), kept minimal and quiet, because the story-implementor PDD script expects this file to exist for worktree environment setup. - Not Started
   c. Make both files executable (`chmod +x setup.sh .kilo/setup-script.sh`) and run the verification gate: from a state with no `.venv` present (a worktree is clean of `.venv` because it is gitignored), run `./setup.sh` — it creates `.venv`, upgrades pip, editable-installs the package, then `.venv/bin/python -m pytest` passes (the plan's Step 5 completion criterion). Confirm `git status --porcelain` shows no `.venv/` or `.step` entries (both ignored). - Not Started

### Task 5: Write `GETTINGSTARTED.md` and minimal `README.md` — Not Started

Covers plan Step 6 letters (a) and (b). Tech-writer task; routes to the `technical-writer-for-story-implementor` agent, not a code agent. Depends on Task 3 conceptually (documents the implemented feature) and is file-disjoint from Task 4 (Group B).

Architect note (decomposition): at its natural granularity — the two files form ONE semantic unit: the onboarding contract of the template repository. `README.md` is deliberately minimal (title + one-line description + pointer to `GETTINGSTARTED.md`) while `GETTINGSTARTED.md` carries all onboarding content; splitting them would split the pointer from the thing it points to. Keep as one writing task; no size annotation (writing task, routed by type).

**Coordination guard**: Task 5 must not embed any behavior discovered at run-time by Tasks 3–4 beyond what the plan has already settled (setup.sh creates `.venv` and runs `pip install -e .`; the example CLI is `python -m scaffold.example`; the package name is `scaffold`; `.step` outputs land in `manufacture/` and are gitignored). All of these are plan-settled, so the guard is about staying faithful to the plan — if a Group B implementer (Task 4) must deviate from the plan for a working script, revise Task 5's branch to match **before** merging Group B.

1. Write the onboarding documentation — Not Started
   a. Write `GETTINGSTARTED.md` at the repo root documenting, per plan Step 6a: (1) how to create a new repository from this one as a GitHub template; (2) running `setup.sh` (creates `.venv`, installs the package + dependencies, then `python -m pytest` and `python -m scaffold.example`); (3) the build123d → `.step` → slicer/CAM methodology; (4) renaming the `scaffold` package for a new project (and updating the matching `pyproject.toml` `[tool.setuptools.packages.find]`/name references and tests); (5) the memory-bank plan/story workflow used in this repository; and (6) how to view models (`ocp_vscode`). - Not Started
   b. Write `README.md` at the repo root — **minimal**: title, a one-line description of the template repository, and a pointer to `GETTINGSTARTED.md`. It must contain **no onboarding detail** that a derived repo would lose if it replaces the README (plan constraint and resolved decision 4 — all "get back up to speed" content lives in `GETTINGSTARTED.md`). - Not Started
   c. Verify: both files exist at the repo root; `README.md` contains no more than the title, one-line description, and the pointer (review — no onboarding body); `GETTINGSTARTED.md` contains all six required topics from subtask a. - Not Started

### Parallel Execution

- **Group A: Tasks 1 and 2** — File-disjoint and independent. Task 1 writes `pyproject.toml`; Task 2 writes `.gitignore`, creates `manufacture/.gitkeep`, deletes `requirements.txt`, and replaces `LICENSE`. Different files, no shared infrastructure file, no compile-time or semantic dependency (the `license`-field/`LICENSE`-file MIT consistency is a post-merge static check, not a behavioral dependency — both are plan-settled). Each is independently verifiable: Task 1 by a `tomllib` parse check, Task 2 by file-state checks. **Residual hazard**: none beyond the license-match consistency check, which is enforced statically at Group A integration; if either executor must deviate from the plan's settled values (e.g., a different `requires-python`), the deviation is confined to that task's own file and does not invalidate the other's.
- **Group B: Tasks 4 and 5** — File-disjoint and independent. Task 4 writes `setup.sh` and `.kilo/setup-script.sh`; Task 5 writes `GETTINGSTARTED.md` and `README.md`. Different directories, no shared infrastructure file, no compile-time or semantic dependency. Task 4's verification is run-based (fresh `./setup.sh` → pytest green); Task 5's is content-based (six required topics; minimal README). Task 5's content is derived entirely from the plan's settled spec (see its coordination guard), **not** from Task 4's run output — Task 5 must not embed any run-discovered behavior. **Residual hazard**: if Task 4's executor finds the plan's settled setup steps need adjustment to actually work, Task 5's "run setup.sh" description could go stale — treat any such deviation as a group-level revision trigger (revise Task 5's branch to match before merging Group B). Low probability: the plan fully specifies the setup steps.

All other task pairs are sequential: Tasks 3 depends on Group A (Task 3's `pip install -e .` reads Task 1's `pyproject.toml`; Task 3's pytest runs and its `manufacture/` CLI export rely on Task 2's `.gitignore` for `.venv/`/`*.egg-info/` cleanliness and on `manufacture/.gitkeep` for the tracked output directory). Group B depends on Task 3 (Task 4's `setup.sh` editable-installs the `scaffold` package that Task 3 creates and runs its pytest suite; Task 5 documents the implemented feature). These are genuine worktree dependencies, not merely recommended ordering.

### Execution Order

```
        ┌──────────────────────┐        ┌──────────────────────────────┐
        │  Task 1              │        │  Task 2                      │
        │  pyproject.toml      │        │  .gitignore · manufacture/   │
        │  ([Small])           │        │  .gitkeep · requirements.txt │
        └──────────┬───────────┘        │  delete · LICENSE → MIT      │
                   │                    └──────────────┬───────────────┘
                   └────────────── Group A ────────────┘
                          (parallel: Tasks 1, 2)
                                  │
                                  ▼
                   ┌──────────────────────────────┐
                   │  Task 3                      │
                   │  src/scaffold/ + test (TDD)  │
                   └──────────────┬───────────────┘
                                  ▼
        ┌──────────────────────┐        ┌──────────────────────────────┐
        │  Task 4              │        │  Task 5                      │
        │  setup.sh +          │        │  GETTINGSTARTED.md +         │
        │  .kilo/setup-script  │        │  README.md (tech writer)     │
        └──────────────────────┘        └──────────────────────────────┘
           ───────────── Group B (parallel): Tasks 4, 5 ─────────────
```

Group A must be merged before Task 3 starts (Task 3's editable install and pytest/`pythonpath` configuration require Task 1's `pyproject.toml`; its `.venv`/egg-info cleanliness and `manufacture/` export rely on Task 2's `.gitignore` and `manufacture/.gitkeep`). Task 3 must be merged before Group B starts (Task 4 installs and tests the Task 3 package; Task 5 documents the Task 3 feature). Tasks 1 and 2 run in parallel with each other; Tasks 4 and 5 run in parallel with each other.

### Reintegration

Reintegration instructions refer to the "story branch" generically (the branch the story-implementor selects at runtime via the user configuration).

**Group A (Tasks 1, 2):**
- Merge order: any order — use finish-order (the first task to pass review merges first; task-number tiebreaker). The trees are fully disjoint (`pyproject.toml` vs `.gitignore`/`manufacture/.gitkeep`/`requirements.txt`/`LICENSE`) with no shared infrastructure or generator→consumer relationship.
- Integration checks (run from the repo root on the merged story branch):
  - `python -c "import tomllib, pathlib; d = tomllib.loads(pathlib.Path('pyproject.toml').read_text()); assert d['project']['name'] == 'scaffold'; assert 'pytest' in d['project']['dependencies'] and 'build123d' in d['project']['dependencies']"` — the manifest parses after the merge.
  - Static license-match check: the `license` field in `pyproject.toml` equals `MIT` **and** the `LICENSE` file opens with `MIT License` — the cross-file consistency the plan requires.
  - File-state checks: `requirements.txt` absent; `.gitignore` contains every required pattern (`.venv/`, `__pycache__/`, `*.pyc`, `manufacture/*.step`, `.kilo/worktrees/`, `*.egg-info/`, `dist/`, `build/`); `manufacture/.gitkeep` tracked.
  - No test run yet — pytest is not installed until Task 3/4 bootstrap the environment; Group A is verified by parse and file-state gates only.
- Watch for conflicts in: `.gitignore` (written by Task 2 here, but Story006's Step 1c also wants `.kilo/worktrees/` recorded — if Story006 created a partial `.gitignore`, this story's Task 2 supersedes it; coordinate so the final file has all patterns); `LICENSE` and `requirements.txt` (touched only by Task 2 within this story, but equally exposed to concurrent parent-repo edits); `pyproject.toml` (only Task 1). `memory-bank/stories/toc.md` and this story file are coordinator-edited on the base branch — keep them out of worktree branches.

**Group B (Tasks 4, 5):**
- Merge order: any order — use finish-order (task-number tiebreaker). The trees are fully disjoint (`setup.sh` + `.kilo/setup-script.sh` vs `GETTINGSTARTED.md` + `README.md`).
- Integration tests (run from the repo root on the merged story branch):
  - `./setup.sh` — creates `.venv`, upgrades pip, editable-installs the package (from the merged Task 1 manifest and Task 3 package); then `.venv/bin/python -m pytest` is green.
  - `.venv/bin/python -m scaffold.example` — writes `manufacture/scaffold_box.step` (gitignored; confirm presence in the working tree, not in git). This is the story's end-to-end smoke path; a full clean-checkout verification of the same flow is Story009's scope (plan Step 8).
  - Static checks: `README.md` is minimal (title, one-line description, pointer to `GETTINGSTARTED.md` only); `GETTINGSTARTED.md` covers the six required topics from plan Step 6a.
- Watch for conflicts in: `setup.sh` and `.kilo/setup-script.sh` (touched only by Task 4 within this story); `GETTINGSTARTED.md` and `README.md` (touched only by Task 5); `.venv` is gitignored and absent from worktree branches — each worktree creates its own via `./setup.sh` or the manual bootstrap in Task 3, and merge-time verification runs recreate it locally (harmless); `memory-bank/stories/toc.md` and this story file (coordinator-edited — keep them out of worktree branches). No lock files involved (plain venv + pip, no lockfile convention). No conflict is expected on the two shared watch points, but if Story006's cleanup left the tree in a different state than assumed, verify `.gitignore`/`LICENSE`/`requirements.txt` exist as expected before Group A merges.

## Test-First Development

This project follows the Logical TDD Lifecycle. The one coding task with a natural unit-test target (Task 3) integrates the test-and-implement cycle **inside** the task: `tests/test_example.py` is written first (subtask a — the red step: `scaffold` does not exist), the environment is bootstrapped (subtask b), then `src/scaffold/__init__.py` and `src/scaffold/example.py` are implemented (subtask c), then `pip install -e .` and `python -m pytest` run to green (subtask d). The test-and-implement cycle is **not** broken out as separate tasks. Tasks 1–2 are config/writing tasks with no unit-test target (verified by parse and file-state checks). Task 4 is a run-based verification gate (`./setup.sh` from a clean state → `.venv` → editable install → pytest green). Task 5 is a documentation task with no test target (verified by content review against plan Step 6a). All tests use **pytest** (`python -m pytest`) — the new convention — with no dependency beyond the `build123d` and `pytest` already declared in `pyproject.toml`.

## Constraints

- **No new third-party dependency**: the only dependencies are `build123d` and `pytest`, declared in `pyproject.toml` (plan constraint). `requirements.txt` is deleted and not recreated. No `ocp_vscode` install in `setup.sh` (hint only).
- **`src/` layout**: the package lives under `src/scaffold/` with `[tool.setuptools.packages.find] where = ["src"]`; no `sys.path` bootstrap hacks (the plan removes the menora project's bootstrap convention).
- **Convention change (this story)**: plain `venv` + pip with the environment at **`.venv`** (created by `setup.sh`), and **pytest** (`python -m pytest`) as the test runner — this **replaces** the menora project's `venv/bin/activate` + stdlib-`unittest` conventions. All gate commands in this story use `.venv/bin/python -m pytest` (explicit interpreter; no activation required).
- **`.step` outputs are gitignored**: `manufacture/*.step` is in `.gitignore`; `manufacture/.gitkeep` keeps the directory tracked. Generated `.step` files (e.g., `manufacture/scaffold_box.step`) appear in the working tree but are never committed.
- **License consistency**: the `license` field in `pyproject.toml` (Task 1) must match the `LICENSE` file text (Task 2) — MIT by default (Apache-2.0 acceptable alternative; if chosen, both must change together before Group A merges).
- **README stays minimal**: `README.md` is title + one-line description + pointer to `GETTINGSTARTED.md` only; all onboarding lives in `GETTINGSTARTED.md` (plan constraint / resolved decision 4).
- **Do not modify**: `.kilo/agent/*.md`, `.kilocode/rules/*`, `resources/`, `scripts/`, `kilo.jsonc`, or any `memory-bank/` file — those belong to the sibling setup stories (Story006/Story008/Story010) or are reusable as-is.
- **Test command**: `python -m pytest` (not `unittest discover`); pytest is provided by the editable install.
- **Environment/worktrees**: `.venv` is gitignored and absent from worktree branches; each worktree creates its own (via `./setup.sh` or the Task 3 bootstrap). `.kilo/worktrees/` is gitignored.
- **All file paths are repo-root-relative** (e.g., `tests/test_example.py`, `src/scaffold/example.py`, `.kilo/setup-script.sh`, `manufacture/.gitkeep`).

## Intent

The purpose of each task, stated so the goal remains clear even if implementation details change:

- **Task 1** — Give the repository its single dependency/package manifest (`pyproject.toml`, PEP 621): `src/`-layout package discovery, `build123d` + `pytest` as the only dependencies, MIT license field, and the `[tool.pytest.ini_options]` configuration that makes `python -m pytest` work from the repo root against the `src/` layout.
- **Task 2** — Finish the repository-level file state the plan requires: ignore the right generated/environment paths, keep `manufacture/` tracked, retire `requirements.txt`, and replace the GPL-3.0 license with MIT text consistent with the manifest.
- **Task 3** — Provide the runnable, test-covered smoke-test example (a trivial build123d `make_box()` + `.step` CLI in the placeholder `src/scaffold/` package) proven by a pytest test written first, and demonstrate the full `pip install -e .` → `pytest` → generate flow this template exists to enable.
- **Task 4** — Make a new clone runnable with one command (`setup.sh`) and give the story-implementor worktree flow its expected `.kilo/setup-script.sh` bootstrap, both performing the same `.venv` + editable-install steps.
- **Task 5** — Document how a newcomer derives a new repository from this template and starts modeling (`GETTINGSTARTED.md`), while keeping `README.md` minimal so a derived repo can replace it without losing onboarding detail.

## Acceptance Criteria

- [ ] `pyproject.toml` exists at the repo root (PEP 621, setuptools backend): `name = "scaffold"`, `dependencies` = exactly `build123d` + `pytest`, `license` = MIT, `[tool.setuptools.packages.find] where = ["src"]`, and `[tool.pytest.ini_options]` with `testpaths = ["tests"]` and `pythonpath = ["src"]`; the file parses with `tomllib`.
- [ ] `.gitignore` exists containing every required pattern (`.venv/`, `__pycache__/`, `*.pyc`, `manufacture/*.step`, `.kilo/worktrees/`, `*.egg-info/`, `dist/`, `build/`); `manufacture/.gitkeep` is present and tracked.
- [ ] `requirements.txt` is deleted (absent from the working tree and from `git ls-files`).
- [ ] `LICENSE` is MIT text (first line `MIT License`); the `pyproject.toml` license field matches it (MIT).
- [ ] `tests/test_example.py` exists, written before the package, asserting `make_box()` returns a build123d `Part`/`Solid` whose bounding box is the expected 10 mm cube (with tolerance).
- [ ] `src/scaffold/__init__.py` and `src/scaffold/example.py` exist; `example.py` provides `make_box()` and a minimal `argparse` CLI exporting `scaffold_box.step` to `manufacture/` by default; `python -m scaffold.example` is the documented CLI.
- [ ] `pip install -e .` succeeds; `.venv/bin/python -m pytest` passes (red test first, then green after implementation — the TDD cycle completed within Task 3).
- [ ] The example CLI writes a `.step` into `manufacture/` (`manufacture/scaffold_box.step` present in the working tree; gitignored, not committed).
- [ ] `setup.sh` and `.kilo/setup-script.sh` exist and are executable; `setup.sh` (with no `.venv` present) creates `.venv`, upgrades pip, editable-installs the package, and `python -m pytest` passes afterward; `.kilo/setup-script.sh` performs the same install bootstrap.
- [ ] `GETTINGSTARTED.md` exists covering the six topics from plan Step 6a (GitHub-template derivation, `setup.sh`, build123d → `.step` → slicer/CAM methodology, renaming `scaffold`, memory-bank plan/story workflow, `ocp_vscode` viewing); `README.md` exists and is minimal (title, one-line description, pointer to `GETTINGSTARTED.md`, no onboarding body).
- [ ] No dependency beyond `build123d` and `pytest` is introduced; no `memory-bank/`, `resources/`, `scripts/`, `.kilocode/rules/`, or `.kilo/agent/` file was modified; `git status` shows only this story's intended files (plus gitignored `.venv` and `manufacture/*.step` present but untracked).

## Requesting Clarification

If at any point during story construction there is confusion or ambiguity about the goal or how to accomplish it, stop and ask the user for clarification. Known parameters the plan does **not** pin and which may need user input rather than executor invention: the copyright holder line in the MIT `LICENSE` (Task 2d — do not invent one; preserve the existing attribution or ask), the `requires-python` floor and exact build-backend pin in `pyproject.toml` if `resources/apis/build123d/` does not settle them, and any deviation from the plan's settled setup steps discovered while making `setup.sh` actually work (Task 4).

## Notes

- **This story is the coding/setup story of the Base Repository Setup arc**: it covers plan Steps 4–6 only. Steps 1–2 → Story006 (cleanup + memory-bank skeletons), Step 7 → Story008 (tooling generalization), Step 8 → Story009 (end-to-end verification), Step 3 → Story010 (terminal stories reset). The arc's own meta-stories (Story006–Story010) are removed by Story010 once they are complete and moved to `finished-stories/`.
- **Convention change (explicit)**: the menora project's `venv/bin/activate` + stdlib-`unittest` + 90-line pinned `requirements.txt` conventions are replaced here by a plain **`venv` + pip** environment at **`.venv`** created by `setup.sh`, dependency declarations in **`pyproject.toml` only**, and **pytest** (`python -m pytest`) as the test command. Story009 verifies the new convention end-to-end from a clean state; resources/apis/build123d install docs remain the reference for build123d specifics.
- **pytest as a regular dependency is deliberate**: the plan writes `dependencies = ["build123d", "pytest"]` and resolves decision 1 (plain venv + pip) so that the single `pip install -e .` inside `setup.sh` provides the test runner with no extra flag (`pip install -e .[test]`) — unusual for a runtime manifest, but specified by the plan and matched here.
- **Group A's license consistency is a static post-merge check, not a dependency**: `pyproject.toml` (Task 1) and `LICENSE` (Task 2) are plan-settled to MIT independently, so the two tasks can run in parallel; the integration gate verifies they agree.
- **Story numbering**: this arc numbers its stories Story006–Story010 alongside the leftover menora Story004/Story005 until Story010's reset frees the numbering to restart at Story001 (plan resolved decision 9 and Story-Writer Guidance item 5).
- Architect review notes are embedded in each task so the story-implementor understands the sizing/decomposition/parallelism decisions without re-deriving them.
