# Story006: Base Repository Cleanup

## Goal

Remove all menora-project-specific content from the repository (this repo was copied from an eight-sided menora die project) and replace the memory-bank documentation with project-agnostic skeletons, so the repo becomes a clean template for future manufacturing repositories.

This story covers **Steps 1 and 2** of `memory-bank/plans/base-repository-setup_plan.md` only:

- **Step 1** — remove project-specific content and the nested worktree: delete the menora `memory-bank/` files (stories, finished stories, walkthrough, `arrangement_approach.md`, design docs, plan files), delete `resources/chanukah-halacha/`, remove the `.kilo/worktrees/alder-paradox` gitlink and the top-level `worktrees` symlink, and drop the `chanukah-halacha/` row from `resources/toc.md`.
- **Step 2** — replace the memory-bank docs with project-agnostic skeletons: `brief.md`, `requirements.md`, `context.md`, `concepts.md`, `terms.md`, `design/design.md`, and a pruned/generalized `lessons-learned.md` (`bugs.md` is left as-is, already empty).

Out of scope by design (later stories in this arc): Steps 3 (stories reset — terminal `Story010_stories-reset`), 4–6 (Python structure, setup scripts, GETTINGSTARTED/README — `Story007_python-structure-and-setup`), 7 (tooling generalization — `Story008_tooling-generalization`), and 8 (end-to-end verification — `Story009_template-verification`). In particular, this story does **not** create `.gitignore`, `pyproject.toml`, `setup.sh`, `src/`, `tests/`, `README.md`, or `GETTINGSTARTED.md`, and does **not** reset the stories directories.

The 7 menora plan files in `memory-bank/plans/` and the `resources/chanukah-halacha/` directory are **already deleted in the working tree** (uncommitted); the tasks below confirm and capture those deletions in the commit rather than re-creating any content.

## References

Links are relative to the `memory-bank` directory:

- [Base Repository Setup Plan](../plans/base-repository-setup_plan.md)
- [Organization rules](../../.kilocode/rules/organization.md)
- [Story Template](../../resources/templates/stories.md)

## Dependencies

None — this is the first story of the base-repository-setup arc. The repository still contains the menora project's files that every later story assumes are gone, so there is nothing this story waits on.

## Dependent Stories

The later stories of this arc depend on this cleanup (the menora content must be gone and the memory-bank docs must be project-agnostic skeletons before they run):

- [Story007_python-structure-and-setup.md](Story007_python-structure-and-setup.md) — Not Started
- [Story008_tooling-generalization.md](Story008_tooling-generalization.md) — Not Started
- [Story009_template-verification.md](Story009_template-verification.md) — Not Started
- [Story010_stories-reset.md](Story010_stories-reset.md) — Not Started

## Tasks

### Task Sizing

The architect-for-story-planning reviewed the decomposition, sizing, and parallelism of every task:

- **Task 1** is **not** `[Small]`: a large mechanical deletion across ~17 tracked files plus two directories (`memory-bank/stories/walkthrough/`, `resources/chanukah-halacha/`). Per the architect rules, a single coordinated mechanical change across many files stays one task ("large but mechanically uniform"). Routes to `technical-writer-for-story-implementor`.
- **Task 2** is **not** `[Small]`: a git-index operation (gitlink + symlink removal) that requires reasoning about gitlink index semantics, on-disk nested-checkout handling, and the worktree-execution caveat (later tasks run in worktrees under `.kilo/worktrees/`, and the tracked `worktrees` symlink is removed by this task). More than one concern; conservative default "not small". Routes to `code-for-story-implementor` (git-index operation).
- **Task 3** is annotated `[Small]`: one file (`resources/toc.md`), one mechanical row removal, a single concern. Routes to `small-code-for-story-implementor`.
- **Task 4** is **not** `[Small]`: six skeleton files forming one semantic unit — every skeleton must match the structure documented in `.kilocode/rules/organization.md` and use consistent header + placeholder conventions. A coordinated multi-file rewrite kept as one task per the architect rules. Routes to `technical-writer-for-story-implementor`.
- **Task 5** is annotated `[Small]`: one file (`memory-bank/lessons-learned.md`), one concern (make it project-agnostic: keep generic rows, generalize the one menora row). Routes to `small-code-for-story-implementor`.

### Task 1: Delete the menora memory-bank and resources content (plan Step 1a + 1b) — Completed

Architect note (decomposition): a single coordinated mechanical deletion across ~17 tracked files and 2 directories, with the plan's lettered sub-steps 1(a) and 1(b) preserved as subtasks. The 7 plan files and `resources/chanukah-halacha/` are already deleted in the working tree (uncommitted) — this task captures those deletions, it does **not** re-create content. Splitting per-file would create merge conflicts with no isolation benefit; keep as one task. Not `[Small]`.

1. Delete the menora `memory-bank/` files and capture the deletions (plan sub-step 1a) - Not Started
   a. `memory-bank/arrangement_approach.md` — menora candle-arrangement worked example. Delete the file (`git rm`).
   b. `memory-bank/design/candle-arrangement-arc.md` and `memory-bank/design/candle-arrangement-circular.md` — menora-specific design docs. Delete both files.
   c. `memory-bank/design/design.md` — the menora die design. Delete it here (plan lists it under "Delete"); it is re-created as a generic skeleton by Task 4 (plan sub-step 2a) — a delete-and-replace pairing across the two tasks.
   d. `memory-bank/stories/Story004_parabolic-arch-layout.md` and `memory-bank/stories/Story005_stock-generation-utility.md` — menora-specific stories. Delete both files. Do **not** touch `memory-bank/stories/toc.md` (reset by the terminal Story010).
   e. `memory-bank/stories/walkthrough/` — menora-specific walkthrough directory (contains `Story001_face-plate-layout-refactor.md`). Delete the entire directory.
   f. `memory-bank/finished-stories/Story001_face-plate-layout-refactor.md`, `Story002_downward-arc-layout.md`, `Story003_nine-inch-face-single-arc.md` — menora-specific finished stories. Delete all three. Do **not** touch `memory-bank/finished-stories/toc.md` (reset by Story010).
   g. `memory-bank/plans/` — the 7 menora plan files (`adjust_size_and_arc_plan.md`, `downward_arc_layout_plan.md`, `face_plate_layout_plan.md`, `jig_plan.md`, `parabolic_arch_layout_plan.md`, `stabilization_block_plan.md`, `stock_generation_plan.md`) are **already deleted in the working tree**. Stage/capture these deletions (e.g., `git add -u memory-bank/plans/`). Keep `memory-bank/plans/base-repository-setup_plan.md` — it is this arc's plan and must survive. If it is untracked when this task runs (it is new in this arc), stage it explicitly as well: `git add memory-bank/plans/base-repository-setup_plan.md`, so subtask h's `git ls-files` check can pass.
   h. Verify the memory-bank deletions: `git status --short memory-bank/` shows only intended deletions; `git ls-files memory-bank/ | grep -iE "menor|candle|walkthrough|arrangement_approach"` returns nothing; `git ls-files memory-bank/plans/` lists only `base-repository-setup_plan.md` (which subtask g staged).
2. Delete `resources/chanukah-halacha/` and confirm the uncommitted deletions are captured (plan sub-step 1b) - Not Started
   a. `resources/chanukah-halacha/candle_arrangement.md` and `resources/chanukah-halacha/toc.md` are **already deleted in the working tree** (uncommitted). Stage/capture the deletions (e.g., `git add -u resources/chanukah-halacha/`); verify `git ls-files resources/chanukah-halacha/` returns nothing.
   b. Confirm **both** uncommitted deletion sets are captured: `git status --short` shows the 7 plan files and the 2 chanukah-halacha files as staged deletions (not as untracked new files). This is the plan's "confirm the uncommitted working-tree deletions for plans and chanukah-halacha are captured" check.
   c. Do **not** delete or modify anything else under `resources/` — the reusable trees (`apis/build123d/`, `modeling/`, `code_review/`, `writing_resources/`, `templates/`) are preserved per the plan constraints.

### Task 2: Remove the `alder-paradox` gitlink from the git index (plan Step 1c) — Completed [REVISED]

> **USER REVISION (2026-09-05)**: the removal of the tracked top-level `worktrees` symlink is an **error in this story** and has been rescinded. The `worktrees -> .kilo/worktrees` symlink is required for sub-agent worktree paths (`.kilo`-prefixed paths trigger a tool-permissions quirk) and is retained as a tracked file. The only remaining scope is the `.kilo/worktrees/alder-paradox` gitlink removal, which was **already removed from the index on the base branch** by commit `9532a46` and verified by the dispatched sub-agent; no changes were produced and none are merged for this task. Subtasks b/c/f below are superseded by this revision.

Architect note (decomposition): a git-index operation, not a file edit. `.kilo/worktrees/alder-paradox` is tracked as a bare gitlink (index mode `160000`, no `.gitmodules` entry exists, so there is no submodule configuration to clean up). The task requires git index reasoning plus an operational caveat (later story tasks run in worktrees under `.kilo/worktrees/`), so it is not `[Small]`.

1. Remove the alder-paradox gitlink from the git index (plan sub-step 1c, symlink portion rescinded) - Completed
   a. Remove the gitlink: **already done on the base branch** — commit `9532a46` removed the `.kilo/worktrees/alder-paradox` gitlink from the index, and the dispatched sub-agent verified `git ls-files --stage | grep alder-paradox` returns nothing. There is **no `.gitmodules`**, so no submodule-config removal is needed.
   b. ~~Leave the `.kilo/worktrees/` directory itself in place~~ — superseded: `.kilo/worktrees/` remains in place as the story-implementor's worktree root (git-excluded via `.git/info/exclude`).
   c. ~~Remove the symlink: `git rm worktrees`~~ — **RESCINDED by user direction**: the tracked `worktrees -> .kilo/worktrees` symlink is retained (it provides non-dot-directory worktree paths for sub-agents).
   d. Verify (amended): `git ls-files --stage | grep -E "alder-paradox|160000"` returns nothing (no gitlink in the index); `git ls-files --stage | grep "120000"` lists only the retained `worktrees` symlink; `git status --short` is clean.
   e. **Deferred by design**: the plan's Step 1(c) also says "record `.kilo/worktrees/` in `.gitignore`", but no `.gitignore` exists at this point — it is created in plan Step 4(d) (Story007), which already includes `.kilo/worktrees/` in its ignore list. Do **not** create `.gitignore` in this story. (`.kilo/worktrees/` is already excluded locally via `.git/info/exclude`.)
   f. ~~Note for the remainder of the arc~~ — superseded: because the tracked `worktrees` symlink is retained, later task handoffs continue to use `worktrees/<sanitized_feature_branch>-task-N` symlink paths (never `.kilo/...` paths).

### Task 3: Remove the `chanukah-halacha/` row from `resources/toc.md` (plan Step 1d) — Completed [Small]

Architect note (decomposition): one file, one mechanical row removal, single concern — `[Small]`. File-disjoint from Tasks 1 and 2, so it joins Group A.

1. Update `resources/toc.md` - Not Started
   a. Remove the row `| [chanukah-halacha/](chanukah-halacha/) | Halachic practices and constraints relevant to menorah design (candle arrangement) |` from the directory table.
   b. Keep the remaining rows (`apis/`, `code_review/`, `templates/`, `writing_resources/`) unchanged.
   c. Verify: `grep -niE "chanukah|halacha|menorah" resources/toc.md` returns nothing, and the table still lists all four preserved directories.

### Task 4: Write project-agnostic memory-bank skeleton docs (plan Step 2a + 2c) — Not Started

Architect note (decomposition): six skeleton files forming one semantic unit — each must match the structure documented in `.kilocode/rules/organization.md` (brief, requirements, context, concepts, terms, lessons-learned, bugs, design/, stories/ + finished-stories/, plans/) and use consistent header + placeholder conventions. This is the "single coordinated mechanical change across many files — keep as one task" case; splitting per-file would force each subtask to re-derive the full skeleton convention with no isolation benefit. The plan's sub-step 2(c) (leave `bugs.md` as-is) is folded in as a verification subtask. Not `[Small]`.

1. Write the six skeleton docs (plan sub-step 2a) - Not Started
   a. `memory-bank/brief.md` — replace the menora brief (Hanukkah menorah / octahedron die / aluminum milling) with a header plus "fill in project overview / goals / design considerations" placeholders. No menora content may remain.
   b. `memory-bank/requirements.md` — replace the menora requirements with a header plus empty Functional Requirements / Non-Functional Requirements / Constraints sections containing placeholder text. No menora content may remain.
   c. `memory-bank/context.md` — replace the menora task history with the standard header plus empty "Active Tasks" and "Recently Completed" sections.
   d. `memory-bank/concepts.md` — replace the two-project concept rows (bee-house and menora) with the standard header plus an **empty table** (keep the existing header row `| Concept | Description | Related Concepts/Terms |`; remove all data rows). No rows may remain.
   e. `memory-bank/terms.md` — replace the two-project term rows with the standard header plus an **empty table** (keep the existing header row `| Term | Definition |`; remove all data rows). No rows may remain.
   f. `memory-bank/design/design.md` — re-create (the menora version was deleted in Task 1) as a generic skeleton: header, project design placeholder, and parts-list placeholder. No menora content may remain.
2. Verify `bugs.md` is left as-is (plan sub-step 2c) - Not Started
   a. Confirm `memory-bank/bugs.md` is unchanged (already empty: header plus empty table). No edit required; it is preserved as the plan directs.
3. Verify the skeleton set - Not Started
   a. Each of the six files is a valid, self-describing skeleton (header + placeholder); `concepts.md` and `terms.md` contain only header rows; `grep -rniE "menorah|candle|octahedron|manora|chanukah|halacha|hanukkah" memory-bank/brief.md memory-bank/requirements.md memory-bank/context.md memory-bank/concepts.md memory-bank/terms.md memory-bank/design/design.md` returns nothing.

### Task 5: Prune and generalize `memory-bank/lessons-learned.md` (plan Step 2b) — Not Started [Small]

Architect note (decomposition): one file, one concern (make the lessons table project-agnostic) — keep the generic rows and generalize the single menora row. `[Small]`.

1. Prune and generalize `memory-bank/lessons-learned.md` - Not Started
   a. Keep the generic lessons unchanged: "Activate Python Virtual Environment First", "Viewing Parts with ocp_vscode", "Checking Port Before Starting OCP Server", "Consult Modeling Resources", "Verify Worktree Branch Before Committing", "Use the Parent Repo's venv in Git Worktrees", "Use the worktrees Symlink for Sub-Agent Paths".
   b. Generalize the row "Assembled-die checks must cover holder↔holder, not just holder↔connector" into a generic lesson: e.g., "Verify all-pairs part intersection in assemblies" — boolean-intersect every part against every *other* part in an assembly, not just part↔connector pairs, because adjacent parts sharing an edge can overlap in ways a pairwise-with-connector gate misses. Remove all menora-specific terms and figures (menorah, candle-holder, the ≈ 3375 mm³ overlap figure) from the row.
   c. Verify: `grep -niE "menorah|candle|chanukah|halacha" memory-bank/lessons-learned.md` returns nothing, and the table retains only the generic lessons.

### Parallel Execution

- **Group A: Tasks 1, 2, 3** — File-disjoint and independent. Task 1 deletes `memory-bank/*` and `resources/chanukah-halacha/*`; Task 2 removes two git-index entries (`.kilo/worktrees/alder-paradox` gitlink, `worktrees` symlink); Task 3 edits `resources/toc.md`. No shared file, no shared infrastructure file, no semantic dependency, and each is independently verifiable (`git ls-files` checks for Tasks 1–2, a grep for Task 3). **Residual hazard**: Task 2 removes the tracked `worktrees` symlink that sub-agents conventionally use for paths (see the lessons-learned row); Task 1 does not depend on that symlink (it runs in its own worktree accessed via the paths the story-implementor assigns), but the story-implementor should sequence the Group A worktree handoffs so later handoffs do not rely on the removed symlink — see the Reintegration and Notes sections.
- **Group B: Tasks 4, 5** — File-disjoint and independent. Task 4 writes the six skeleton docs (+ verifies `bugs.md`); Task 5 rewrites `memory-bank/lessons-learned.md`. Disjoint files, no semantic dependency (both are "make memory-bank project-agnostic" but neither consumes the other's output), each independently verifiable by grep.

All other pairs are sequential: Group A must merge before Group B starts — Task 4 re-creates `memory-bank/design/design.md` that Task 1 deleted (delete-and-replace pairing), and conceptually the repo's menora content must be gone before the replacement skeletons are written.

### Execution Order

```
   ┌───────────────────────────────────────────────────────────────┐
   │               Group A (parallel): Tasks 1, 2, 3               │
   │                                                               │
   │  ┌────────────────┐   ┌────────────────┐   ┌────────────────┐ │
   │  │     Task 1     │   │     Task 2     │   │     Task 3     │ │
   │  │ delete menora  │   │ gitlink +      │   │ resources/     │ │
   │  │ memory-bank +  │   │ symlink removal│   │ toc.md row     │ │
   │  │ resources      │   │ (git-index)    │   │ removal        │ │
   │  │ content        │   │                │   │ [Small]        │ │
   │  └────────────────┘   └────────────────┘   └────────────────┘ │
   └───────────────────────────────┬───────────────────────────────┘
                                   ▼
   ┌───────────────────────────────────────────────────────────────┐
   │               Group B (parallel): Tasks 4, 5                  │
   │                                                               │
   │  ┌────────────────────────┐      ┌────────────────────────┐   │
   │  │         Task 4         │      │         Task 5         │   │
   │  │ skeleton memory-bank   │      │ prune + generalize     │   │
   │  │ docs (6 files +        │      │ lessons-learned.md     │   │
   │  │ bugs.md verify)        │      │ [Small]                │   │
   │  └────────────────────────┘      └────────────────────────┘   │
   └───────────────────────────────────────────────────────────────┘
```

Group A must be merged before Group B starts (Task 4 re-creates `design/design.md` deleted by Task 1). Within Group A, merge in any order (finish-order with task-number tiebreaker is fine; see Reintegration). This story's final gates are the story-level grep and `git ls-files` checks in Acceptance Criteria.

### Reintegration

Reintegration instructions refer to the "story branch" generically (the branch the story-implementor selects at runtime via the user configuration).

**Group A (Tasks 1, 2, 3):**
- Merge order: any order — Task 1 (`memory-bank/` deletions) and Task 3 (`resources/toc.md`) are disjoint; **Task 2 produces no changes to merge** (its gitlink removal was already on the base branch and its symlink-removal portion was rescinded). Soft preference: merge Task 1 first so the "menora content is gone" state the story-level checks assert is established before the smaller tasks land; not required for correctness.
- Integration checks (run from the repo root on the merged story branch):
  - `git ls-files | grep -iE "menor|candle|chanukah|halacha|walkthrough|arrangement_approach"` — returns nothing (no menora files tracked).
  - `git ls-files --stage | grep -E "alder-paradox|160000"` — returns nothing (no gitlink in the index); `git ls-files --stage | grep "120000"` lists only the retained `worktrees` symlink (REVISED — symlink retention per user direction).
  - `git ls-files memory-bank/plans/` — lists only `base-repository-setup_plan.md`.
  - `grep -niE "chanukah|halacha|menorah" resources/toc.md` — returns nothing.
  - `git status --short` — shows only intended changes (no stray files, nothing untracked from the deletions).
- No unit tests exist in this repo (pure documentation/deletion story), so the integration "test" is the verification set above; nothing else to run.

**Group B (Tasks 4, 5):**
- Merge order: any order — Task 4's six skeleton files and Task 5's `lessons-learned.md` are fully disjoint.
- Integration checks (run from the repo root on the merged story branch):
  - `grep -rniE "menorah|candle|octahedron|manora|chanukah|halacha|hanukkah" memory-bank/brief.md memory-bank/requirements.md memory-bank/context.md memory-bank/concepts.md memory-bank/terms.md memory-bank/lessons-learned.md memory-bank/design/design.md memory-bank/bugs.md` — returns nothing.
  - Manual review: each skeleton is valid and self-describing per `.kilocode/rules/organization.md`; `concepts.md`/`terms.md` contain only header rows; `bugs.md` unchanged.

**Conflict-prone files (both groups):**
- `memory-bank/stories/toc.md`, `memory-bank/finished-stories/toc.md`, and this story file — edited by the story-implementor during coordination; keep them out of worktree branches (they are reset/replaced by Story010).
- `resources/toc.md` — touched only by Task 3 within this story; low risk unless a concurrent parent-repo story edits it.
- `.kilo/agent-manager.json` — untracked local state file; not in scope, never commit it.
- No lock files involved (markdown-only repo; package manifests arrive in Story007). All tasks in this story are pure docs/deletion, so there is no environment or venv dependency.

## Test-First Development

No TDD applies to this story: it is a pure documentation/deletion story with no code and no test targets (the repo currently has no `tests/` directory or package manifest — those arrive in Story007). Verification is entirely via the grep, `git ls-files`, `git status`, and skeleton-validity gates in the Acceptance Criteria. Per the Logical TDD Lifecycle, tasks with no unit-test target are verified by run-only gates; `memory-bank/bugs.md` is already empty and is intentionally left that way.

## Constraints

- **Scope guard**: cover only plan Steps 1–2. Do **not** perform any Step 3–8 work: do not reset the stories directories, do not create `.gitignore`/`pyproject.toml`/`setup.sh`/`src/`/`tests/`/`README.md`/`GETTINGSTARTED.md`/`manufacture/`, do not delete `requirements.txt` or replace `LICENSE`, and do not generalize the PDD scripts or rule files.
- **Capture, don't re-create**: the 7 menora plan files in `memory-bank/plans/` and `resources/chanukah-halacha/` are already deleted in the working tree (uncommitted). Tasks must confirm/capture those deletions in the commit — never re-create the deleted content.
- **Do not modify `.kilo/agent/*.md`** (the story-implementor sub-agent definitions) — they are reusable as-is.
- **Preserve reusable resources**: `resources/apis/build123d/`, `resources/modeling/`, `resources/code_review/`, `resources/writing_resources/`, `resources/templates/` are kept untouched; only menora-specific `resources/chanukah-halacha/` is removed.
- **Memory-bank skeletons must match the structure documented in `.kilocode/rules/organization.md`** (brief, requirements, context, concepts, terms, lessons-learned, bugs, design/, stories/ + finished-stories/, plans/).
- **Deferred files stay deferred**: `memory-bank/stories/toc.md` and `memory-bank/finished-stories/toc.md` are reset by the terminal Story010 (plan Step 3); `.kilocode/rules/organization.md`'s menora `design/` description is generalized in Story008 (plan Step 7a). Do not touch them here.
- **`.gitignore` does not exist yet**: the plan's intent to record `.kilo/worktrees/` in `.gitignore` is fulfilled when Story007 creates `.gitignore` (plan Step 4d, which already lists `.kilo/worktrees/`). Do not create `.gitignore` in this story.
- **Story numbering resets to Story001** after the menora stories are cleared (Story010 terminal reset); this story must not renumber anything.
- **Preserve the plan**: `memory-bank/plans/base-repository-setup_plan.md` is kept as the arc's authority; `memory-bank/bugs.md` is left as-is.
- **Environment**: all commands run from the repo root (the story-implementor convention in this project). No Python environment is needed for any task in this story.

## Intent

The purpose of each task, stated so the goal remains clear even if implementation details change:

- **Task 1** — Remove every menora-specific file from `memory-bank/` and `resources/` so the repository no longer contains any menora stories, plans, design docs, walkthrough, or `chanukah-halacha` content, capturing the pre-existing uncommitted deletions in the commit.
- **Task 2** — [REVISED] Remove the leftover `alder-paradox` gitlink from the git index so the template no longer references another project's worktree, while keeping `.kilo/worktrees/` itself functional as the story-implementor's worktree root. The top-level `worktrees` symlink is **retained** (the story's original symlink-removal scope was an error — the symlink provides non-dot-directory worktree paths for sub-agents).
- **Task 3** — Remove the `chanukah-halacha/` row from `resources/toc.md` so the resources table no longer points at deleted content.
- **Task 4** — Replace the menora memory-bank docs with project-agnostic, self-describing skeletons (brief, requirements, context, concepts, terms, design) so a new repository can fill them in, and confirm `bugs.md` stays as-is.
- **Task 5** — Make `lessons-learned.md` project-agnostic by keeping the generic lessons and generalizing the one menora-specific row, so the lessons remain reusable across many kinds of builds.

## Acceptance Criteria

- [ ] Task 1: `memory-bank/arrangement_approach.md`, `memory-bank/design/candle-arrangement-arc.md`, `memory-bank/design/candle-arrangement-circular.md`, `memory-bank/design/design.md`, `memory-bank/stories/Story004_parabolic-arch-layout.md`, `memory-bank/stories/Story005_stock-generation-utility.md`, `memory-bank/stories/walkthrough/`, `memory-bank/finished-stories/Story001_face-plate-layout-refactor.md`, `Story002_downward-arc-layout.md`, and `Story003_nine-inch-face-single-arc.md` are deleted; the 7 menora plan files and `resources/chanukah-halacha/` uncommitted deletions are captured in the commit (staged as deletions, not re-created); `git ls-files memory-bank/plans/` lists only `base-repository-setup_plan.md`.
- [ ] Task 2: [REVISED] `git ls-files --stage` shows no `.kilo/worktrees/alder-paradox` gitlink (mode `160000`) and still lists the `worktrees` symlink (mode `120000`) as a retained tracked file; `.kilo/worktrees/` itself remains on disk (git-excluded); no `.gitmodules` was created or edited (none exists); `.gitignore` was not created (deferred to Story007).
- [ ] Task 3: `resources/toc.md` has no `chanukah-halacha/` row and still lists `apis/`, `code_review/`, `templates/`, and `writing_resources/`.
- [ ] Task 4: `brief.md`, `requirements.md`, `context.md`, `concepts.md`, `terms.md`, and `design/design.md` are valid, self-describing skeletons (header + placeholder); `concepts.md`/`terms.md` contain only header rows; `memory-bank/bugs.md` is unchanged (empty).
- [ ] Task 5: `lessons-learned.md` retains only generic lessons, and the menora assembly-collision row is generalized into a generic "verify all-pairs part intersection in assemblies" lesson with no menora terms or figures.
- [ ] Story-level grep (plan Step 1 completion criteria, scoped to the content this story owns): `grep -rniE "menorah|candle|octahedron|manora|chanukah|halacha|hanukkah" memory-bank/brief.md memory-bank/requirements.md memory-bank/context.md memory-bank/concepts.md memory-bank/terms.md memory-bank/lessons-learned.md memory-bank/bugs.md memory-bank/design/design.md resources/` returns **zero hits**. Files legitimately excluded by design: `memory-bank/plans/base-repository-setup_plan.md` (the arc plan), `memory-bank/stories/` and `memory-bank/finished-stories/toc.md` (reset by Story010), `.kilocode/rules/organization.md` and the PDD scripts/rule files (generalized in Story008), and this arc's own story files.
- [ ] Story-level `git ls-files` (plan Step 1 completion criteria, revised): no menora story/plan/design files, no `resources/chanukah-halacha/` files, no `alder-paradox` gitlink; the tracked `worktrees` symlink is retained.
- [ ] Story-level `git status --short` on the merged story branch shows only intended changes; nothing unrelated was deleted or added.

## Requesting Clarification

If at any point during story construction there is confusion or ambiguity about the goal or how to accomplish it, stop and ask the user for clarification. Known plan ambiguities that have been resolved here: (1) `.gitignore` does not exist, so the Step 1(c) `.gitignore` record for `.kilo/worktrees/` is deferred to Story007 (plan Step 4d) rather than created in this story; (2) the Step 1 grep criterion cannot be satisfied repo-wide until the terminal Story010 and Story008 have run, so it is scoped to the content this story owns, with the deferred files listed explicitly.

## Notes

- The exact deletion list and skeleton content are settled in `memory-bank/plans/base-repository-setup_plan.md` (Impacted Files tables, Steps 1–2, and the Story-Writer Guidance item 1) — no ambiguity about what to delete or what each skeleton should contain.
- **Uncommitted working-tree deletions**: the 7 menora plan files and `resources/chanukah-halacha/` (2 files) were already deleted before this story began. Every task touching them must capture the deletions in the commit (`git add -u` / `git rm` staging) and verify via `git ls-files` — never re-create content.
- **Delete-and-replace pairing**: `memory-bank/design/design.md` is deleted in Task 1 (plan Step 1a) and re-created as a skeleton in Task 4 (plan Step 2a). Group B must therefore run after Group A.
- **Git-index operation (Task 2, REVISED)**: `.kilo/worktrees/alder-paradox` is a bare gitlink (no `.gitmodules`) that was already removed from the index on the base branch. The `worktrees` symlink is a tracked file that is **retained** (removal rescinded by user direction). `.kilo/worktrees/` itself is the story-implementor's worktree root and remains on disk (git-excluded via `.git/info/exclude`).
- **Operational caveat (REVISED)**: the lessons-learned row "Use the worktrees Symlink for Sub-Agent Paths" tells sub-agents to use the `worktrees/` symlink because `.kilo`-prefixed paths can trigger a tool-permissions quirk. Because the tracked `worktrees` symlink is retained, all task handoffs in this story use `worktrees/<sanitized_feature_branch>-task-N` symlink paths and sub-agents are instructed never to resolve or use `.kilo/worktrees/...` real paths.
- **Deferred by design**: `memory-bank/stories/toc.md` and `memory-bank/finished-stories/toc.md` still reference the menora stories after this story completes — that is expected; Story010 (terminal, plan Step 3) resets them. `.kilocode/rules/organization.md` still mentions the menora `design/` docs by name — Story008 (plan Step 7a) generalizes it.
- `resources/toc.md` is the only table of contents this story updates; the stories tocs are Story010's scope.
- No code, no tests, no new dependencies, and no environment setup are involved in this story; the acceptance gates are the grep, `git ls-files`, `git status`, and skeleton-validity checks listed above.
