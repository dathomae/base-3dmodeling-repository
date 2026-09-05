# Story009: Template Verification

## Goal

Verify the template end-to-end from a clean state: `./setup.sh` succeeds, `python -m pytest` passes, the example CLI emits a `.step`, and `git status` is clean.

This is the run-and-verify story that closes out the base-repository setup arc. It is **plan Step 8** of `memory-bank/plans/base-repository-setup_plan.md` (Story-Writer Guidance item 4, `template-verification`). It executes only after the prior stories have merged their deliverables: Story006 (Steps 1–2) removed the menora-specific content and skeletonized `memory-bank/`, Story007 (Steps 4–6) established the Python project structure and the setup scripts, and Story008 (Step 7) generalized the tooling. Story009 then proves that the merged result works **as a fresh clone would** — the template-level acceptance gate for the whole plan.

The story is verification-only: it makes **no source or documentation edits** to the template. The plan's four lettered sub-steps (8a–8d) are decomposed into four sequential gate tasks, each approximating a fresh-clone run from a clean state. A gate that fails indicates a defect in an earlier story's deliverable; the failure is recorded precisely and reported, **not** fixed in place. The only tracked change this story may legitimately introduce is the standard task record in `memory-bank/context.md` (entered at start, completed/cleared at end).

## References

Links are relative to the `memory-bank` directory:

- [Base Repository Setup Plan](../plans/base-repository-setup_plan.md) — authoritative source; Step 8 is this story; Steps 3 (Story010) and the overall completion criteria bound its acceptance criteria.
- [GETTINGSTARTED.md](../../GETTINGSTARTED.md) — created in Story007 (plan Step 6); documents the example CLI invocation that Task 3 must use.
- [Story format template](../../resources/templates/stories.md)

## Dependencies

- [Story006_base-repo-cleanup.md](Story006_base-repo-cleanup.md) — Not Started (verifies no menora/Chronocone content remains in tracked files)
- [Story007_python-structure-and-setup.md](Story007_python-structure-and-setup.md) — Not Started (this story runs setup.sh/pytest/example-CLI, which Story007 creates)
- [Story008_tooling-generalization.md](Story008_tooling-generalization.md) — Not Started (verifies the grep for Chronocone/Go hits is clean)

Story009 runs `./setup.sh`, `python -m pytest`, and the example CLI that Story007 creates, and it re-sweeps the content that Stories 006 and 008 already verified. None of its gates can pass — or even be meaningfully attempted — until those three stories are complete and merged.

## Dependent Stories

- [Story010_stories-reset.md](Story010_stories-reset.md) — Not Started (terminal story; depends on all stories 1-4 being complete)

## Tasks

### Task Sizing

The architect-for-story-planning reviewed the decomposition, sizing, and parallelism of every task:

- **Task 1** is **not** `[Small]`: a run-only gate with environment reasoning (fresh-worktree clean-state preparation, neutralizing any bootstrap-created `.venv`, interpreting `./setup.sh` output, and verifying `.gitignore` behavior). It is a gate whose failure semantics matter — a defect in Story007's `setup.sh` must be reported, not worked around.
- **Task 2** is **not** `[Small]`: a run-only gate that re-establishes the environment and interprets the full pytest result (exit code, pass count, collection errors). No code is authored, so the small-code agent's "additive change" profile does not apply.
- **Task 3** is **not** `[Small]`: a run-only gate that must discover the documented CLI invocation (from Story007's `GETTINGSTARTED.md`), run it, and verify both the `.step` artifact and the `manufacture/*.step` gitignore rule.
- **Task 4** is **not** `[Small]`: a review-and-record task with a five-part checklist (`git status`, `git ls-files` present/absent audit, two content sweeps with documented exclusion scoping, and the `memory-bank/context.md` record). It is writing/review work, not code, and routes to the `technical-writer-for-story-implementor` agent.
- **No `[Small]` annotations anywhere**: none of the four tasks is a small code change, and the architect rule is "when in doubt, do NOT mark `[Small]`." Tasks 1–3 route to `code-for-story-implementor` (the Story004 precedent routes run-only verification gates to the code agent); Task 4 routes to `technical-writer-for-story-implementor`.

### Task 1: Run `./setup.sh` from a clean state and verify the environment (plan 8a) — Completed

Architect note (decomposition): at its natural granularity — a single run-and-verify gate. The subtasks flow linearly (prepare clean state → run setup → verify environment → verify gitignore hygiene → STOP-on-failure reporting) with no self-contained preamble and no intermediate verification cycle worth splitting; splitting the preparation from the run would create an artificial seam with zero isolation benefit. **Not `[Small]`** (environment reasoning, gate semantics, 5 subtasks). Routes to `code-for-story-implementor`.

1. Run `./setup.sh` from a clean state and verify the resulting environment - Completed
   a. Establish the clean state: this task executes in a fresh worktree created from the story's feature branch (which carries the merged Story006–Story008 template state). Confirm the worktree contains no `.venv/`, `__pycache__/`, `*.egg-info/`, or `manufacture/*.step`, and that `git status --porcelain` is empty. If the story-implementor's worktree bootstrap (`.kilo/setup-script.sh`, created by Story007) pre-created a `.venv` before delegation, remove it (`rm -rf .venv`) so that `./setup.sh` is exercised as a genuine first run. `.venv` is gitignored, so this is an environment operation, not a tracked-content edit. - Completed
   b. Run `./setup.sh` from the worktree root (the repo root; all paths in this story are repo-root-relative) and capture the full output, e.g. `./setup.sh 2>&1 | tee /tmp/story009-task1-setup.log`. The command must exit 0. - Completed
   c. Verify the created environment: `.venv/` exists; `.venv/bin/python --version` runs; `.venv/bin/python -c "import scaffold, build123d"` succeeds (the editable install from `pyproject.toml` is importable); `.venv/bin/python -m pytest --version` runs (pytest is installed as a declared dependency); and `./setup.sh` printed its documented next-steps message. - Completed
   d. Verify first-run hygiene: `git status --porcelain` still reports no changes after the run, and `git check-ignore -v .venv/` prints the `.venv/` rule from the `.gitignore` Story007 wrote — proving `.venv/`, `__pycache__/`, and `*.egg-info/` are all ignored and that a fresh `./setup.sh` does not dirty the tree. - Completed
   e. STOP-on-failure: if any check in b–d fails, record the exact command, the observed output, and the expected result; do **not** modify any tracked file to make the gate pass. A failing `./setup.sh` is a defect in Story007's deliverable — report it to the story-implementor, which stops the story and surfaces it to the user. - Completed

### Task 2: Run `python -m pytest` and confirm the suite is green (plan 8b) — Completed

Architect note (decomposition): at its natural granularity — a single run-and-verify gate sequentially dependent on Task 1's semantics (pytest is meaningless on a tree whose setup failed). Because `.venv` is gitignored, environment state does not carry between task worktrees, so the task re-establishes the environment itself — this also re-verifies `./setup.sh` reproducibility from clean state. **Not `[Small]`**. Routes to `code-for-story-implementor`.

1. Run the full test suite and confirm it passes from a clean environment - Completed
   a. Re-establish the clean environment exactly as in Task 1 subtasks a–b: fresh worktree from the story's feature branch, no `.venv/` residue (remove it if the bootstrap created one), then `./setup.sh` must exit 0 again. - Completed
   b. Run the project test command from the repo root: `.venv/bin/python -m pytest` (equivalently `source .venv/bin/activate && python -m pytest`). This is the template's `test_command` (the generalized default the story-implementor uses for Python stories). - Completed
   c. Interpret the result as a gate: exit code 0 and a passing summary — at least the tests Story007 wrote in `tests/test_example.py` (the `make_box()` bounding-box assertions) must be collected and pass, with zero failures, zero errors, and zero collection errors. Record the exact pass/fail counts from the summary line. - Completed
   d. STOP-on-failure per Task 1 subtask e: a red suite here is a defect in Story007's package, test, or `pyproject.toml` — record the failing test names and output, do not edit any file to make the suite green, and report. - Completed

### Task 3: Run the example CLI and confirm a `.step` lands in `manufacture/` (plan 8c) — Completed

Architect note (decomposition): at its natural granularity — a single run-and-verify gate sequentially dependent on Tasks 1–2 (the CLI requires the installed package and a passing baseline). It re-establishes the environment (clean-state reproducibility), runs the documented example CLI, and checks both the artifact and the `manufacture/*.step` gitignore rule. **Not `[Small]`**. Routes to `code-for-story-implementor`.

1. Run the example CLI and confirm it emits a `.step` into `manufacture/` - Completed
   a. Re-establish the clean environment exactly as in Task 1 subtasks a–b: fresh worktree, no `.venv/` residue, `./setup.sh` exits 0. - Completed
   b. Identify the documented example CLI from Story007's deliverables: plan Step 4 pins the default form `python -m scaffold.example`; `GETTINGSTARTED.md` (created in Story007, plan Step 6) records the exact invocation. If GETTINGSTARTED documents a different command, use that documented form. Run it from the repo root with the venv python: `.venv/bin/python -m scaffold.example`. - Completed
   c. Confirm the CLI emitted a `.step`: exactly the expected new non-empty `.step` file exists under `manufacture/` (its name is whatever Story007's `src/scaffold/example.py` export logic defines — read the actual name from the CLI output/docs rather than assuming one), and the file begins with the STEP header `ISO-10303-21;`. - Completed
   d. Confirm the artifact is generated output, not tracked content: `git status --porcelain` shows no `manufacture/*.step` entry, and `git check-ignore -v manufacture/<name>.step` prints the `manufacture/*.step` rule — this exercises the plan decision that `.step` outputs are gitignored while `manufacture/.gitkeep` keeps the directory. - Completed
   e. STOP-on-failure per Task 1 subtask e: a missing/invalid `.step` is a defect in Story007's example — record and report, do not fix. - Completed

### Task 4: Review `git status`/`git ls-files` and the content sweeps; record the outcome (plan 8d) — Completed

Architect note (decomposition): at its natural granularity — the five subtasks form ONE semantic unit: a single final-state audit of the merged template (status review, file-set audit, menora-family sweep, Chronocone/Go-family sweep) that closes with the story's only tracked change (the `memory-bank/context.md` record). Splitting per-file would force each subtask to re-derive the exclusion scoping below with no isolation benefit. This is a writing/review task — it ends by authoring a memory-bank record — so it routes to `technical-writer-for-story-implementor`, **not** a code agent. **Not `[Small]`** (multi-part checklist, grep scoping reasoning, 5 subtasks). Sequentially last: it audits the tree that Tasks 1–3 exercised.

1. Audit the final merged tree and record the verification outcome - Completed
   a. **`git status` review**: in a fresh worktree of the story's final feature-branch state, run `git status --porcelain` and `git status`. Expected: no modified tracked content and no untracked, non-ignored files. The only tracked change this story legitimately introduces is the record written in subtask e (`memory-bank/context.md`); story-file/toc status updates are managed by the story-implementor in the main tree, outside worktrees. Any other change means Story006–008 leakage or an incomplete `.gitignore` — list each finding with its path, and do not fix silently. - Completed
   b. **`git ls-files` audit**: verify the expected template file set is present and the forbidden set is absent:
      - Present (spot-check the full set): `pyproject.toml`, `setup.sh`, `.kilo/setup-script.sh`, `README.md`, `GETTINGSTARTED.md`, `.gitignore`, `LICENSE`, `src/scaffold/__init__.py`, `src/scaffold/example.py`, `tests/test_example.py`, `manufacture/.gitkeep`, the memory-bank skeletons (`brief.md`, `requirements.md`, `context.md`, `concepts.md`, `terms.md`, `lessons-learned.md`, `bugs.md`, `design/design.md`, `stories/toc.md`, `stories/finished-stories/toc.md`), and `resources/toc.md`.
      - Absent: `requirements.txt` (superseded by `pyproject.toml`); any path under `resources/chanukah-halacha/`; menora-era files (`memory-bank/arrangement_approach.md`, `memory-bank/design/candle-arrangement-*.md`, `memory-bank/stories/Story00[1-5]*`, `memory-bank/stories/finished-stories/Story00[1-3]*`, the 7 menora plan files); `.kilo/worktrees/alder-paradox`; the `worktrees` symlink.
      - `git ls-files -s` shows no gitlink entries (mode `160000`) — the `alder-paradox` nested repository is gone. - Completed
    c. **Menora-family content sweep**: over the must-be-clean surface — `README.md`, `GETTINGSTARTED.md`, `pyproject.toml`, `setup.sh`, `.gitignore`, `LICENSE`, `kilo.jsonc`, `.kilo/setup-script.sh`, and the directories `src/`, `tests/`, `resources/`, `scripts/`, `.kilocode/rules/`, `memory-bank/design/`, plus the memory-bank live docs `brief.md`, `requirements.md`, `context.md`, `concepts.md`, `terms.md`, `lessons-learned.md`, `bugs.md` — run `grep -rniE 'menorah|candle|octahedron|manora|chanukah|halacha|hanukkah'` and require **zero hits**. Excluded from the sweep (documented in Notes): the arc's coordination artifacts (`memory-bank/stories/**`, `memory-bank/stories/finished-stories/**`, `memory-bank/plans/base-repository-setup_plan.md`), `.kilo/agent/**` (retained as-is by plan constraint), and environment/git internals (`.git/`, `.kilo/worktrees/`, `.venv/`, `node_modules/`). - Completed
     d. **Chronocone/Go-family content sweep**: over the same must-be-clean surface and with the same exclusions, run `grep -rnE 'chronocone|chronocone_planning_language|gradlew|src/main/go|go test|go build|chronoconev0_frontend'` and require **zero hits**. The sweep is defined by the positive surface list in subtask c, so files outside that list are not scanned — in particular `.kilocode/kilo-code-settings.json` (a Kilo editor-config file that retains its Chronocone/Go command-allowlist entries and is retained as-is) and `.kilo/agent/**` are intentionally out of the must-be-clean surface, matching the exclusion Story008 documents for its Step 7 verification. Do not extend the sweep repo-wide, or it will trip on those retained files. - Completed
    e. **Record the outcome**: update `memory-bank/context.md` per the standard task discipline — Story009 was entered as an Active Task at the start of the story; once all four gates pass, mark the verification complete with a one-line summary of what passed (setup.sh, pytest, example `.step`, clean status/sweeps) and clear the active entry. This is the story's only intended tracked change; commit it. - Completed

### Parallel Execution

**None — sequential verification gates.** The architect-for-story-planning analysis: every task is a hard gate whose *success is a prerequisite for the next gate's meaning*, not merely for its file state — pytest is only meaningful after `./setup.sh` succeeds, the example CLI only after the package is installed and the baseline is green, and the final tree audit only after Tasks 1–3 have exercised the tree. Running any later gate while an earlier gate failed would defeat the gate semantics (a red suite or missing `.step` would be explainable by the earlier failure and the defect would be masked). The tasks also share the same verification discipline and, indirectly, the same tree state. Per the architect rules ("when in doubt, default to serial"; false parallelism is worse than missed parallelism), there are **no parallel groups**.

### Execution Order

```
Story006 + Story007 + Story008 merged (the template under test)
                            │
                            ▼
        ┌───────────────────────────────┐
        │  Task 1 — ./setup.sh gate     │  (plan 8a — code-for-story-implementor)
        └───────────────┬───────────────┘
                        ▼
        ┌───────────────────────────────┐
        │  Task 2 — pytest gate         │  (plan 8b — code-for-story-implementor)
        └───────────────┬───────────────┘
                        ▼
        ┌───────────────────────────────┐
        │  Task 3 — example-CLI .step   │  (plan 8c — code-for-story-implementor)
        └───────────────┬───────────────┘
                        ▼
        ┌───────────────────────────────┐
        │  Task 4 — git review + record │  (plan 8d — technical-writer-for-story-implementor)
        └───────────────────────────────┘
```

The four gates run strictly in order 1 → 2 → 3 → 4. **Stop-on-failure semantics**: if any gate fails, the story-implementor does not proceed to the next gate; the failing task's recorded diagnostics are surfaced to the user, and the remaining tasks are treated as blocked (a verification-only story does not fix the template it is auditing — remediation belongs to the responsible earlier story or a follow-up). No human visual sign-off is required for this story; every gate is programmatic and its pass/fail is determined by the commands and checks in the task.

### Reintegration

**None — no parallel groups.** The story is a single sequential chain, so there are no parallel worktree branches to merge in an order or integration-test jointly. Notes for the sequential merges:

- Tasks 1–3 typically introduce **no tracked changes** (they create only gitignored artifacts — `.venv/`, `__pycache__/`, `manufacture/*.step`), so their worktree merges may be no-ops; the sub-agents should report results rather than force commits.
- Task 4's only tracked change is the `memory-bank/context.md` record.
- Watch for conflicts in: `memory-bank/context.md` — the project's shared task-record file, touched by Task 4 here and by concurrent parent-repo story activity; and the story file + `toc.md`, which the story-implementor edits in the main tree (keep them out of worktree branches). No lock files or package manifests are touched by any task.

## Test-First Development

**n/a — verification-only story.** Story009 introduces no functionality, so the Logical TDD Lifecycle does not apply and no tests are written or modified in any task. The code under verification (`src/scaffold/example.py` + `tests/test_example.py`) was already built test-first inside Story007 (plan Step 4: "write `tests/test_example.py` first"); this story simply re-runs the resulting suite end-to-end as the template's acceptance gate. The gates themselves are the story's "tests": Task 1 asserts `setup.sh` succeeds from clean state, Task 2 asserts the suite is green, Task 3 asserts a `.step` is produced and ignored, and Task 4 asserts the final tree is clean.

## Constraints

- **Verification-only**: do not create, modify, or delete any tracked template file. The sole exception is the standard task record in `memory-bank/context.md` (Task 4 subtask e). Environment artifacts (`.venv/`, `__pycache__/`, `manufacture/*.step`, `/tmp` logs) are not tracked content and may be created/removed freely.
- **No fixing in place**: a failing gate is reported with exact commands and observed-vs-expected output; the executor must NOT edit source, tests, docs, or scripts to make a gate pass. Remediation belongs to the responsible earlier story (Story006/007/008) or a follow-up story, decided by the user.
- **Clean state per gate**: every gate task starts from a fresh worktree with no `.venv/`, `__pycache__/`, `*.egg-info/`, or `manufacture/*.step`; any bootstrap-created `.venv` is removed before the task's own `./setup.sh` run so each gate approximates a fresh clone.
- **Source root**: `source_root` is the repository root (`.`); every command runs from the worktree root and every path is repo-root-relative. The Python environment is `.venv` (not the menora-era `venv/`); invoke Python as `.venv/bin/python` or via `source .venv/bin/activate`.
- **Exact commands**: `./setup.sh` (not `.kilo/setup-script.sh`) is the script under test; `python -m pytest` is the project test command; the example CLI is the form documented in `GETTINGSTARTED.md`, defaulting to `python -m scaffold.example` (plan Step 4). Do not invent a different CLI name.
- **`.step` outputs are never committed**: `manufacture/*.step` is gitignored; verifying that it stays out of `git status` is itself part of the acceptance criteria (the plan's `.gitignore` is under test).
- **Sweep scope**: the Task 4 content sweeps cover the must-be-clean surface only, excluding the coordination/historical artifacts that legitimately retain references to the removed projects (the arc's story files and `base-repository-setup_plan.md`), `.kilo/agent/**` (the plan's constraint: reusable sub-agent definitions are kept as-is), and `.kilocode/kilo-code-settings.json` (Kilo editor config retaining its command allowlist; kept as-is). Do not extend the sweeps repo-wide.
- **No new dependency, no build**: nothing is added to `pyproject.toml`; no package is built. `build123d` and `pytest` come from Story007's declared dependencies.
- **Environment for worktrees**: do not rely on `.venv` carrying between task worktrees (gitignored, so absent); each gate that needs the package re-runs `./setup.sh`.

## Intent

The purpose of each task, stated so the goal remains clear even if implementation details change:

- **Task 1** — Prove that `./setup.sh` alone bootstraps a fresh checkout: it exits 0, creates `.venv`, installs the editable `scaffold` package with `build123d`/`pytest`, and leaves `git status` clean (the `.gitignore` works).
- **Task 2** — Prove that the Story007 test suite is green from a clean state under the template's declared test command, with no failures, errors, or collection errors.
- **Task 3** — Prove that the documented example CLI runs from the installed package and emits a valid `.step` into `manufacture/` that stays out of version control.
- **Task 4** — Prove the final merged tree is the intended template: `git status` shows only intended changes, `git ls-files` contains exactly the expected files and none of the forbidden ones, the menora- and Chronocone/Go-family content sweeps are clean over the live deliverable surface, and the story's verification outcome is recorded in `memory-bank/context.md`.

## Acceptance Criteria

These criteria match plan Step 8's completion criteria ("from a clean state, `./setup.sh` succeeds, `python -m pytest` is green, the example CLI emits a `.step`, and `git status` shows only intended changes") and the plan's overall completion criteria:

- [ ] **`./setup.sh` succeeds from a clean state** (Task 1): starting with no `.venv/`, `__pycache__/`, `*.egg-info/`, or `manufacture/*.step`, `./setup.sh` exits 0, creates `.venv/`, the editable `scaffold` package imports alongside `build123d` via `.venv/bin/python`, and `git status --porcelain` shows no tracked changes afterward (`.venv/` confirmed gitignored via `git check-ignore`).
- [ ] **`python -m pytest` is green** (Task 2): the full suite run via `.venv/bin/python -m pytest` from the repo root exits 0 with the Story007 tests (`tests/test_example.py`) collected and passing — zero failures, errors, or collection errors.
- [ ] **The example CLI emits a `.step`** (Task 3): the documented example CLI (default `python -m scaffold.example`) writes a non-empty `.step` file beginning with `ISO-10303-21;` into `manufacture/`; the artifact does not appear in `git status` and `git check-ignore -v` reports the `manufacture/*.step` rule.
- [ ] **`git status` shows only intended changes** (Task 4a): the final state has no modified tracked content and no untracked non-ignored files beyond the story's own `memory-bank/context.md` record.
- [ ] **`git ls-files` audit passes** (Task 4b): the expected template file set is present (pyproject.toml, setup.sh, `.kilo/setup-script.sh`, README.md, GETTINGSTARTED.md, .gitignore, LICENSE, src/scaffold/, tests/, manufacture/.gitkeep, memory-bank skeletons, resources/toc.md) and the forbidden set is absent (requirements.txt, chanukah-halacha/, menora story/plan/design files, the alder-paradox gitlink, the worktrees symlink); no `160000` gitlink entries remain.
- [ ] **Content sweeps are clean** (Task 4c/d): over the must-be-clean surface, the menora-family grep (`menorah|candle|octahedron|manora|chanukah|halacha|hanukkah`, case-insensitive) and the Chronocone/Go-family grep (`chronocone|chronocone_planning_language|gradlew|src/main/go|go test|go build|chronoconev0_frontend`) both return **zero hits** (coordination/historical artifacts and `.kilo/agent/**` excluded per the Constraints).
- [ ] **Outcome recorded** (Task 4e): `memory-bank/context.md` reflects Story009's start and completion per the standard task discipline, with a one-line summary of the passed gates.

## Requesting Clarification

If at any point during story construction there is confusion or ambiguity about the goal or how to accomplish it, stop and ask the user for clarification.

## Notes

- **Clean-state execution model**: each gate task runs in a fresh worktree created from the story's feature branch, so every gate is an independent fresh-clone approximation. Because `.venv` and `manufacture/*.step` are gitignored, environment state does not carry between task worktrees; Tasks 2 and 3 therefore re-run `./setup.sh` (Task 1's procedure) before their own gate — this also re-verifies that `./setup.sh` is reproducible from clean state.
- **Bootstrap hazard**: the story-implementor's worktree flow runs `.kilo/setup-script.sh` in each new worktree before delegation (it reuses Story007's install steps). If it pre-creates `.venv`, Task 1 (and each later gate) must remove it first so the script genuinely under test — `./setup.sh` — is exercised as a first run. A `setup.sh` that only works on top of `.kilo/setup-script.sh` would otherwise slip through.
- **Grep-scope convention**: the Task 4 sweeps cannot be run over the whole repository at Story009 time — the arc's own coordination artifacts legitimately mention the removed projects: this very story file, the other Story00x files, and `memory-bank/plans/base-repository-setup_plan.md` document the removals and retain terms like "menora", "Chronocone", and "candle-arrangement" by design. Story004 established the same convention ("historical plans/stories are expected and left intact"). Likewise `.kilo/agent/*.md` is retained as-is by the plan's constraint ("Do not modify `.kilo/agent/*.md`") and still contains Chronocone/Go *examples* illustrating how the reusable sub-agents reason — it is not part of the must-be-clean surface. If a sweep hit appears in the must-be-clean surface, report it with file/line context for triage; do not auto-fix.
- **Generic-word caution**: `octahedron` (menora-family pattern) is also a generic solid-geometry term. If the only hits are clearly generic geometry references inside reusable resources, flag them for user triage against the plan's intent (removing *menora-specific* content) rather than modifying reusable resources.
- **Verification record**: `memory-bank/context.md` is the single intended tracked change. Per the story-implementor's status protocol, the story file's task statuses and `toc.md` are updated by the story-implementor in the main tree, never inside a task worktree.
- **No committed artifacts**: the `.step` produced in Task 3 is a generated artifact and must never be committed; it is deleted with the worktree when the task's branch is cleaned up. The `manufacture/` directory itself remains tracked via `manufacture/.gitkeep`.
- **Relationship to the arc**: Story009 is the plan's end-to-end acceptance gate (Story-Writer Guidance item 4). When it passes, Story010 (`stories-reset`, plan Step 3 — the terminal story) can run: it resets `stories/` and `finished-stories/` to empty skeletons and removes the arc's own meta-stories, including this one.
