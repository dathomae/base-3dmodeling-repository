# Story008: Tooling Generalization

## Goal

Generalize the leftover tooling of this repository template so it no longer references the Chronocone / Go / Gradle projects (or menora-specific candle-arrangement content) and will run correctly in a derived Python repository.

This story covers **Step 7 only** of the base repository setup plan (`memory-bank/plans/base-repository-setup_plan.md`). It edits five tooling files, each in its own task:

- `.kilocode/rules/organization.md` — replace the menora-specific `design/` directory description with a generic one.
- `scripts/add-new-story.pdd.script.md` — drop `chronocone/...` links and the CPL/Go path conventions; replace Go commands with Python equivalents.
- `scripts/story-implementor.pdd.script.md` — drop the CPL/Go/Gradle defaults and path conventions; default `source_root` to the repository root and the build/test commands to Python equivalents.
- `.kilocode/rules/system-rules/system-rules.md` — drop the "Chronocone" reference and the dead link to the non-existent `memory-bank/specifications/patterns/toc.md`.
- `.kilocode/rules/rules-mock/mock.md` — remove the `chronoconev0_frontend` references.

There is no code and no test target. Verification is by grep and by a dry run of story creation in a scratch location, per the plan's Step 7 completion criteria.

A subtlety that shapes the tasks: Step 7 generalizes the very PDD scripts that this story arc's coordination machinery consumes. The changes therefore take effect for **derived repositories** and for story creation that happens after this story (for example, later stories created from this plan arc). This story's own execution continues to be driven by the instructions already loaded into the running sessions, so editing the scripts is safe; the Task 6 dry run exists precisely to confirm the edited `add-new-story` script still works.

## References

Links are relative to the `memory-bank` directory:

- [Base Repository Setup Plan](../plans/base-repository-setup_plan.md)
- [Stories Template](../../resources/templates/stories.md)
- [Add New Story PDD Script](../../scripts/add-new-story.pdd.script.md)
- [Story Implementor PDD Script](../../scripts/story-implementor.pdd.script.md)
- [Organization Rules](../../.kilocode/rules/organization.md)
- [System Rules](../../.kilocode/rules/system-rules/system-rules.md)
- [Mock Persona Rules](../../.kilocode/rules/rules-mock/mock.md)

## Dependencies

- [Story006_base-repo-cleanup.md](Story006_base-repo-cleanup.md) — Not Started (the menora-specific references it removes must be gone before the grep-based verification in this story)
- [Story007_python-structure-and-setup.md](Story007_python-structure-and-setup.md) — Not Started (per the plan's execution order, this story runs after the Python structure is established)

## Dependent Stories

- [Story009_template-verification.md](Story009_template-verification.md) — Not Started (verifies no Chronocone/Go refs remain and a dry-run story creation works)
- [Story010_stories-reset.md](Story010_stories-reset.md) — Not Started (terminal story)

## Tasks

### Task Sizing

The architect-for-story-planning reviewed the decomposition, sizing, and parallelism of every task:

- **Task 1** is annotated `[Small]`: one file (`.kilocode/rules/organization.md`), one concern (a single sentence describing the `design/` directory), mechanical. Routes to `technical-writer-for-story-implementor`.
- **Task 2** is **not** `[Small]`: one file, but a coordinated rewrite of the path-convention guidance and several embedded examples across one document that future story authors follow; requires the agent to reason about what the Python equivalents are and to re-check the whole file for consistency. Routes to `technical-writer-for-story-implementor`.
- **Task 3** is **not** `[Small]`: the deepest of the five edits. It changes the parameter defaulting semantics (removing the CPL-detection branch in Operation 4b), updates the source-path-resolution instructions in Operations 10 and 14, and sweeps examples and notes across the whole document; each region must stay consistent with the new Python defaults. Routes to `technical-writer-for-story-implementor`.
- **Task 4** is annotated `[Small]`: one file (`.kilocode/rules/system-rules/system-rules.md`), one concern (remove one stale section). Routes to `technical-writer-for-story-implementor`.
- **Task 5** is annotated `[Small]`: one file (`.kilocode/rules/rules-mock/mock.md`), one concern (remove the `chronoconev0_frontend` references and generalize the wording). Routes to `technical-writer-for-story-implementor`.
- **Task 6** is **not** `[Small]` and is run-only (no repository edits): the story-level verification task that executes the grep gate, checks the story-implementor defaults, and dry-runs story creation in a scratch location. Depends on Tasks 1-5 being merged. Routes to `technical-writer-for-story-implementor` for the dry run; the story-implementor runs the final gates on the merged story branch.

### Task 1: Generalize the `design/` description in `.kilocode/rules/organization.md` — Completed [Small]

Architect note (decomposition): at its natural granularity, one file and one concern, cannot be smaller. Single sentence rewrite with no cross-file coordination. Routes to `technical-writer-for-story-implementor`.

1. Generalize the memory-bank design-directory description - Completed
   a. In `.kilocode/rules/organization.md`, replace the memory-bank item 8 sentence (currently: "The design directory memory-bank/design/ contains design.md (the overall design and list of parts) plus documents for the candle arrangements (candle-arrangement-circular.md and candle-arrangement-arc.md).") with a project-agnostic description. The design directory holds `design.md` (the overall design and list of parts) and may hold additional project-specific design documents beside it. Do not reference `candle-arrangement-circular.md`, `candle-arrangement-arc.md`, or any menora-specific subsystem (those files are deleted by Story006). Keep the item's numbering and the surrounding style of the list. The wording must stay consistent with the generic `memory-bank/design/design.md` skeleton that Story006 established. - Completed
   b. Grep `.kilocode/rules/organization.md` for `candle-arrangement`, `chanukah`, and `menora`; zero hits in this file. - Completed

### Task 2: Generalize `scripts/add-new-story.pdd.script.md` — Completed

Architect note (decomposition): at its natural granularity, one file, but not a small task. The stale content is spread across the intro paragraph, the step 9 file-path-convention bullet, the step 9a architect link, the step 9e reintegration examples, and the step 14 quality-check wording; the replacement must be coherent (same Python conventions everywhere) because future story authors follow this document. Routes to `technical-writer-for-story-implementor`.

1. Replace the Chronocone/CPL/Go content with repo-root Python conventions - Completed
   a. Fix the two stale `chronocone/...` markdown links to be repo-root-relative: the stories-template link in the intro paragraph (currently `[stories template](chronocone/resources/templates/stories.md)`) and the architect link in step 9a (currently `[architect-for-story-planning's Task Decomposition Review section](chronocone/.kilo/agent/architect-for-story-planning.md)`). Both point into the Chronocone repository layout and do not resolve in this repository. - Completed
   b. Rewrite the "File path convention" bullet in step 9 (currently lines ~53-56) to the Python convention. The current text directs story authors to the CPL/Go layout (`src/chronocone_planning_language`, `src/main/go/` prefixes, `go test ./src/main/go/...`, `go build`). Replace it with: all file paths in task descriptions are relative to the project's `source_root` (where build/test commands run from); for Python projects `source_root` is the repository root (`.`), source files are referenced repo-root-relative (for example `src/scaffold/example.py`), and commands run from `source_root` in module form, for example `python -m pytest` (or `python -m unittest discover -s tests`) and `python -m build`. Non-Python derived projects override `source_root` and the command defaults as documented in the story-implementor PDD script. Drop every CPL/Go/`src/main/go/` mention. - Completed
   c. Replace the remaining Go-flavored examples and wording with Python equivalents: the two reintegration example commands in step 9e (currently `go test ./pkg/evaluator/... -count=1 -timeout 60s` and `go test ./pkg/parser/... ./pkg/formatter/... -count=1 -timeout 60s`) and the task-decomposition-quality example in step 14 (currently "no task should say 'run go test to verify the new types pass' followed by 'now update the consumers'"). Use the Python module form (`python -m pytest`) so the illustrative commands match the conventions this story is establishing. - Completed
   d. Re-read the whole file and confirm none of the stale markers remain: `chronocone`, `chronocone_planning_language`, `gradlew`, `src/main/go`, `go test`, `go build`, `CPL`, `chanukah`, `candle-arrangement`. - Completed

### Task 3: Generalize `scripts/story-implementor.pdd.script.md` — Completed

Architect note (decomposition): at its natural granularity, one file, but the least small task in the story. It changes the *semantics* of parameter defaulting (removing the CPL-detection branch and replacing it with unconditional Python defaults), updates the operational instructions in Operations 4b, 10, and 14, and sweeps examples and notes across the whole document. Every region must agree on the new defaults, so the edit needs whole-file reasoning; it is not a mechanical rename. Routes to `technical-writer-for-story-implementor`.

1. Replace the CPL/Go/Gradle defaults and path conventions with Python defaults - Completed
   a. Fix the stale stories-template link in the intro paragraph (currently `[resources/templates/stories.md](chronocone/resources/templates/stories.md)`) to be repo-root-relative. - Completed
   b. Update the `source_root`, `build_command`, and `test_command` rows of the Parameters table (currently lines ~138-140). Drop the "Auto-detected for CPL stories; prompted if missing for other stories" default and the Chronocone/Gradle example values (`src/chronocone_planning_language`, `./gradlew build`, `./gradlew test`). State that `source_root` defaults to the repository root (`.`), `build_command` to `python -m build`, and `test_command` to `python -m pytest`; a derived non-Python repository overrides the values at the Operation 4b confirmation prompt. - Completed
   c. Rewrite the Operation 4b default-resolution block (currently lines ~189-194). Remove the CPL-detection heuristic ("Determine whether this is a CPL story. If the story file or any of its references mention `chronocone_planning_language`, `CPL`, `CIL`, or `src/chronocone_planning_language`...") and the two-branch CPL/non-CPL defaulting. Replace with: all stories default `source_root` to the repository root, `build_command` to `python -m build`, and `test_command` to `python -m pytest`; if the repository is not a Python project the user supplies the correct values at the confirmation prompt. The Configuration Summary presented to the user is unchanged in shape. - Completed
   d. Update the "Source path resolution" instructions in Operation 10 (coding handoff, currently line ~324) and Operation 14 (writing handoff, currently line ~409). Drop the CPL-specific sentence ("For the CPL project specifically, `source_root` is `src/chronocone_planning_language`; Go packages live under `src/main/go/`...", the `src/main/go/` prefix-repair rule, and the `cd <source_root> && go test ./src/main/go/<pkg>/...` instruction). Replace with the Python convention: for Python projects `source_root` is the repository root (`.`), story paths are repo-root-relative (for example `src/scaffold/example.py`), and Python commands run from `source_root`, for example `cd <source_root> && python -m pytest`. - Completed
   e. Sweep the remaining stale wording outside Operations 4b/10/14: the violation-detection example in the handoff-protocol section (currently line ~69, "Consider running `go test`, `npm test`, or any test runner...") and the setup-script install hints in Operation 7a (line ~248, "e.g., Gradle wrapper, Go modules, npm packages"), Operation 8 (line ~269, "Gradle wrapper, Go modules, etc."), and the Notes section (line ~685, same phrase). Replace the Go/Gradle examples with Python environment hints (for example creating the venv and running `pip install -e .`, which the `.kilo/setup-script.sh` created by Story007 performs). - Completed
   f. Re-read the whole file and confirm none of the stale markers remain: `chronocone`, `chronocone_planning_language`, `gradlew`, `src/main/go`, `go test`, `go build`, `CPL`, `CIL`, `chanukah`, `candle-arrangement`; and confirm the Operation 4b block and the Parameters table both state the Python defaults. - Completed

### Task 4: Remove the stale Chronocone section from `.kilocode/rules/system-rules/system-rules.md` — Completed [Small]

Architect note (decomposition): at its natural granularity, one file and one concern. Path note: the plan Step 7(d) names this file `.kilocode/rules/system-rules.md`; in this repository the master system-rules file lives at `.kilocode/rules/system-rules/system-rules.md` (a directory), which is the path `organization.md` itself uses ("system-rules/system-rules.md"). The file is untouched by any other story in this arc before this one. Routes to `technical-writer-for-story-implementor`.

1. Remove the stale "Design and Implementation Patterns" section - Completed
   a. In `.kilocode/rules/system-rules/system-rules.md`, remove the "Design and Implementation Patterns" paragraph (currently line ~71: "The Chronocone system follows some specific patterns in documentation, design and implemenation. Whenever performing any coding, architecture, planning or documentation activity **Always read the patterns table[`toc.md`](../../../memory-bank/specifications/patterns/toc.md) file first**"). The paragraph references the Chronocone system and links to a `memory-bank/specifications/patterns/toc.md` that does not exist in this repository (the memory-bank layout documented in `organization.md` has no `specifications/patterns/` directory). Remove the whole paragraph; nothing else in the file references it. Do not change any other content of the file. - Completed
   b. Grep `.kilocode/rules/system-rules/system-rules.md` for `chronocone` and `specifications/patterns`; zero hits. - Completed

### Task 5: Clean the Chronocone references from `.kilocode/rules/rules-mock/mock.md` — In Progress [Small]

Architect note (decomposition): at its natural granularity, one file and one concern (generalize the Mock persona rules). The `chronoconev0_frontend` path appears at four sites; all four must be made consistent. Routes to `technical-writer-for-story-implementor`.

1. Generalize the Mock persona rules - In Progress
   a. In `.kilocode/rules/rules-mock/mock.md`, replace the four Chronocone / `chronoconev0_frontend` references with project-agnostic wording that a derived repository can follow without a Chronocone frontend: (1) the responsibilities bullet "Creating high-fidelity UI mocks for Chronocone features (e.g., bitemporal visualizations)" becomes a generic statement about creating high-fidelity UI mocks for the project's features; (2) the "Directory & File Standards" location rule, (3) the "Session Continuity" scan instruction, and (4) the "Mode Entry" notification message all reference `src/chronoconev0_frontend/src/mocks`. Replace that path with a project-agnostic mocks-directory convention (for example a dedicated `src/mocks/` directory at the repository root's source area, or "the project's configured mocks directory"), using the same wording at all four sites. Do not invent project features or reference repository structure that Story006 removed (this template has no frontend package). - Not Started
   b. Grep `.kilocode/rules/rules-mock/mock.md` for `chronocone`; zero hits. - Not Started

### Task 6: Verify the generalized tooling (run-only) — Not Started

Architect note (decomposition): run-only verification; no repository edits. It is the story's gate task and must run after Tasks 1-5 are merged onto the story branch, because its grep checks the combined result and its dry run exercises the edited `add-new-story` script. Routes to `technical-writer-for-story-implementor` for the dry run; the story-implementor performs the final gates on the merged branch.

1. Run the Step 7 verification gates - Not Started
   a. Run the plan's Step 7 grep gate from the repository root, excluding `node_modules`, `.git`, and `.kilo/worktrees`: `grep -rn "chronocone\|chronocone_planning_language\|gradlew\|src/main/go\|go test\|go build\|chanukah\|candle-arrangement"`. Expect zero hits in the five tooling files edited by Tasks 1-5 and in every other non-meta tracked file. Matches confined to this arc's meta-records (the Story006-Story010 story files and `toc.md` entries, and `memory-bank/plans/base-repository-setup_plan.md`) and to the out-of-scope residuals listed in the Notes are expected and acceptable. - Not Started
   b. Confirm `scripts/story-implementor.pdd.script.md` now defaults `source_root` to the repository root and `test_command` to `python -m pytest` (with `build_command` defaulted to `python -m build`), in both the Parameters table and the Operation 4b default-resolution block, and that the file contains no CPL/Go/Gradle/Chronocone references. - Not Started
   c. Dry-run the generalized `scripts/add-new-story.pdd.script.md` in a scratch location outside the repository (for example under `/tmp`). Create a minimal skeleton there: an empty `memory-bank/stories/` directory, a `memory-bank/stories/toc.md` containing an "Active Stories" section, and `resources/templates/stories.md` copied from this repository. Execute the script's procedure with a dummy `story_name` (for example `smoke-test`) through story-file creation, the `toc.md` entry update, and the structural self-checks (script steps 1-14), stopping before the Review-mode handoff (step 15). Note that step 9's sub-agent consultations (9a-9e) are exercised only in simplified form in the scratch repo — the dummy story's task decomposition is trivial and no real codebase exists to analyze; the dry run's purpose is to confirm story-file creation, repo-root-relative Python path conventions, and the `toc.md` update in the edited script, not to reproduce the full architect consultation. Confirm it scans and numbers stories, creates the story file with repo-root-relative Python path conventions and no CPL/Go/Chronocone wording, and updates the scratch `toc.md`; then delete the scratch directory. - Not Started

### Parallel Execution

- **No parallel groups.** Architect-for-story-planning evaluation: the five edit tasks (Tasks 1-5) touch mutually disjoint files and would ordinarily satisfy the file-disjointness test for parallelism. They are nevertheless kept **serial** for two reasons. First, every edited file is an agent-guidance artifact: two PDD scripts (`scripts/`) and three rule files (`.kilocode/rules/`) that the story-implementor router and its sub-agents load and follow while this arc executes. Parallel worktrees would produce divergent guidance snapshots, and the cross-file coherence of the two scripts' Python defaults is a correctness property that only the merged end-state (Task 6) can verify. Second, the "when in doubt, default to serial" rule applies: false parallelism on guidance files that steer the executing machinery is worse than missed parallelism. This follows the narrower Story004 precedent of keeping a coordinated multi-file guidance/documentation change as one unit routed to one agent rather than decomposing per-file; Story004 itself did declare a parallel group elsewhere, so the serial decision here rests on the machinery-coherence and conservative-default grounds above, not on a blanket "guidance changes never parallelize" rule. Task 6 is necessarily last (it verifies the merged result).

### Execution Order

```
┌──────────────┐
│  Task 1      │  (.kilocode/rules/organization.md — [Small])
└──────┬───────┘
       ▼
┌──────────────┐
│  Task 2      │  (scripts/add-new-story.pdd.script.md)
└──────┬───────┘
       ▼
┌──────────────┐
│  Task 3      │  (scripts/story-implementor.pdd.script.md)
└──────┬───────┘
       ▼
┌──────────────┐
│  Task 4      │  (.kilocode/rules/system-rules/system-rules.md — [Small])
└──────┬───────┘
       ▼
┌──────────────┐
│  Task 5      │  (.kilocode/rules/rules-mock/mock.md — [Small])
└──────┬───────┘
       ▼
┌──────────────┐
│  Task 6      │  (verification: grep gate + defaults check + dry run)
└──────────────┘
```

Each task must be merged before the next starts (Tasks 2 and 3 both re-check their file end-to-end for stale markers, and Task 6 verifies the whole merged tree), so the graph is a single sequential chain.

### Reintegration

None, no parallel groups exist; every task is a sequential handoff, so the standard per-task merge applies and no group-level merge order or integration-test targets are needed. The story's real integration gate is Task 6, which the story-implementor runs on the fully merged story branch (all six tasks merged) rather than per task.

Watch for conflicts in: `scripts/*.pdd.script.md` and `.kilocode/rules/**` are agent-guidance files that sibling arc stories or router-configuration maintenance in the parent repository could also touch; keep all five edits inside this story's worktrees and do not let unrelated parent-repo edits to these files land while the story branch is open. The story file and `memory-bank/stories/toc.md` are coordination files edited by the story-implementor and must be kept out of the task worktrees.

## Test-First Development

Not applicable: this story contains no code and no test target. The Logical TDD Lifecycle does not apply. Verification is by (1) per-file greps in Tasks 1-5, (2) the repo-wide grep gate, the defaults check, and the scratch dry run of story creation in Task 6, and (3) the Story009 template-verification story, which later re-runs the whole-tree sweep. Each task's acceptance is the grep/read-back check embedded in its subtasks.

## Constraints

- **Scope**: edit exactly the five tooling files named in plan Step 7. Do **not** modify any other file, including `memory-bank/` documents, `resources/`, the story file, or `toc.md`.
- **Leave as-is**: `kilo.jsonc` (per plan); the `.kilo/agent/*.md` sub-agent definitions (per the plan constraint they are reusable as-is, even though `architect-for-story-planning.md` still carries illustrative Go/Chronocone examples, see Notes); `.kilocode/kilo-code-settings.json` (editor settings artifact, see Notes).
- **Replace, do not delete**: Go-specific instructions are replaced with their Python equivalents, not merely removed. The established defaults are `source_root` = repository root (`.`), `test_command` = `python -m pytest`, and `build_command` = `python -m build`.
- **Consistency**: the two PDD scripts must state the same Python defaults and path conventions; the three rule files must contain no stale references after editing.
- **File paths**: all file paths in task descriptions are repo-root-relative.
- **No code, no new dependency**: pure markdown edits; nothing to install.
- **Dry run hygiene**: the Task 6 dry run must execute in a scratch directory outside the repository and be deleted afterward.
- **Routing**: all writing and run-only tasks route to `technical-writer-for-story-implementor`; no code agent is involved.

## Intent

The purpose of each task, stated so the goal remains clear even if implementation details change:

- **Task 1** — Make `organization.md`'s description of `memory-bank/design/` project-agnostic so a derived repository is not told about removed menora design documents.
- **Task 2** — Make the add-new-story script produce stories for a Python repo rooted at the repository root: correct links, Python path conventions, and Python command examples.
- **Task 3** — Make the story-implementor script treat every repository as Python by default (`source_root` = `.`, `test_command` = `python -m pytest`, `build_command` = `python -m build`) and drop the CPL/Go/Gradle detection and path rules.
- **Task 4** — Remove the stale Chronocone reference and the dead link to the non-existent patterns TOC from the master system-rules file.
- **Task 5** — Remove the `chronoconev0_frontend` assumption from the Mock persona rules so they apply to any derived repository.
- **Task 6** — Prove the generalization: the stale-marker grep is clean outside known out-of-scope residuals, the story-implementor defaults are Python, and the edited add-new-story script still creates a story in a scratch location.

## Acceptance Criteria

- [ ] `.kilocode/rules/organization.md` describes `memory-bank/design/` generically (design.md plus optional project-specific design documents) with no `candle-arrangement`, `chanukah`, or `menora` references.
- [ ] `scripts/add-new-story.pdd.script.md` has no `chronocone`, `chronocone_planning_language`, `gradlew`, `src/main/go`, `go test`, `go build`, `CPL`, `chanukah`, or `candle-arrangement` references; its file-path-convention bullet and examples use the repository-root Python convention (`python -m pytest`, `python -m build`); its two markdown links are repo-root-relative.
- [ ] `scripts/story-implementor.pdd.script.md` defaults `source_root` to the repository root, `build_command` to `python -m build`, and `test_command` to `python -m pytest` in both the Parameters table and Operation 4b; the CPL-detection heuristic and every CPL/Go/Gradle/`src/main/go/` reference and path rule are gone.
- [ ] `.kilocode/rules/system-rules/system-rules.md` contains no "Chronocone" reference and no `specifications/patterns` link; no other content in the file changed.
- [ ] `.kilocode/rules/rules-mock/mock.md` contains no `chronocone` reference; its directory-location, continuity, and mode-entry wording is project-agnostic and internally consistent.
- [ ] The plan's Step 7 grep gate (`chronocone|chronocone_planning_language|gradlew|src/main/go|go test|go build|chanukah|candle-arrangement`, excluding `node_modules`, `.git`, `.kilo/worktrees`) returns zero hits except for the known out-of-scope residuals documented in the Notes (this arc's meta-records, `.kilo/agent/architect-for-story-planning.md` illustrative examples, and `.kilocode/kilo-code-settings.json`).
- [ ] A dry run of the generalized `scripts/add-new-story.pdd.script.md` in a scratch location creates a story file and updates `toc.md` with Python conventions and no CPL/Go/Chronocone wording, and the scratch directory is removed.
- [ ] `kilo.jsonc` and `.kilo/agent/*.md` are unmodified.

## Requesting Clarification

If at any point during story construction there is confusion or ambiguity about the goal or how to accomplish it, stop and ask the user for clarification.

## Notes

- **Plan path shorthand for system-rules**: plan Step 7(d) writes `.kilocode/rules/system-rules.md`, but in this repository the master system-rules file lives at `.kilocode/rules/system-rules/system-rules.md`; Task 4 targets the real path.
- **The arc generalizes its own tooling**: Tasks 2 and 3 edit the PDD scripts that drive this story arc's coordination and future story creation. The running sessions have already loaded their instructions, so editing is safe; the changes take effect for derived repositories and for stories created after this one in the arc. Task 6's dry run confirms the edited add-new-story script still functions, which is the safeguard the plan calls for ("verify by a dry run of story creation").
- **Grep-gate residuals are known and out of scope for Step 7**: after Tasks 1-5, matches for the plan's grep terms remain only in (1) this arc's meta-records, which necessarily name the terms they describe and are removed by the terminal Story010 reset (the plan file is a retained record of the arc), (2) `.kilo/agent/architect-for-story-planning.md`, which contains illustrative Go/Chronocone examples in YAML guidance and which the plan's constraints explicitly leave reusable as-is, and (3) `.kilocode/kilo-code-settings.json`, an editor-settings artifact (tracked, but not a rule or PDD script). The plan's overall "no Chronocone/Go content remains in tracked files" criterion is pursued by the whole arc; Story009 (template-verification) re-runs the whole-tree sweep and resolves or formally exempts these residuals with the user.
- **No `.kilo/agent` edits**: per the plan constraint ("Do not modify `.kilo/agent/*.md` ... unless a path reference in them is demonstrably stale"), this story does not touch `.kilo/agent/*.md` even though `architect-for-story-planning.md` shows Chronocone/Go example content; Task 2 only fixes the *links* to that file from within `add-new-story.pdd.script.md`.
- **`memory-bank/context.md`**: recording this story's start and completion is the story-implementor's coordination responsibility (standard task discipline), not a task-worktree edit. Story006 reset `context.md` to a skeleton, and the five edit tasks are single-file scoped, so no task here writes `context.md`.
- **Traceability**: the exact stale text this story removes is anchored in the target files as they exist when this story starts: the five files are not edited by any earlier story in the arc, so the reference lines cited in the tasks are stable.
