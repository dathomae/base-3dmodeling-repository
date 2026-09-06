# Story010: Stories Reset

## Goal

Reset `memory-bank/stories/` and `memory-bank/finished-stories/` to clean, empty, template-ready skeletons — removing the leftover menora stories and this arc's own completed meta-stories — so the repository is ready to serve as a project-agnostic template.

This is the **TERMINAL story** of the `base-repository-setup` arc and covers **Step 3 only** of `memory-bank/plans/base-repository-setup_plan.md` ("Reset the stories directories (terminal step)"). Per that plan's Story-Writer Guidance item 5 it must run **last**, after every other setup story (Story006–Story009) is complete **and** moved to `finished-stories/`: running it earlier would delete the arc's own in-progress stories. It is pure documentation/deletion work, routes to `technical-writer-for-story-implementor`, and has no TDD.

When this story finishes, `stories/` and `finished-stories/` contain only fresh `toc.md` skeletons, `plans/` contains only this plan, and story numbering is free to restart at Story001.

## References

Links are relative to the `memory-bank` directory:

- [Base Repository Setup Plan](../plans/base-repository-setup_plan.md) (Step 3 is this story's scope; Story-Writer Guidance item 5 defines its position and routing)
- [Requirements](../requirements.md)
- [Design](../design/design.md)
- [Organization rules](../../.kilocode/rules/organization.md) (defines the memory-bank structure the empty skeletons must match)

## Dependencies

This terminal story depends on all four earlier stories of the arc being complete **and** moved to `finished-stories/`:

- [Story006_base-repo-cleanup.md](Story006_base-repo-cleanup.md) — Not Started
- [Story007_python-structure-and-setup.md](Story007_python-structure-and-setup.md) — Not Started
- [Story008_tooling-generalization.md](Story008_tooling-generalization.md) — Not Started
- [Story009_template-verification.md](Story009_template-verification.md) — Not Started

**Note**: this terminal story must run after the others are complete and moved to `finished-stories/`, because running it earlier would delete the arc's own in-progress stories.

## Dependent Stories

None — this is the terminal story of the arc (it removes itself once its work is recorded).

## Tasks

### Task Sizing

The architect-for-story-planning reviewed the decomposition, sizing, and parallelism of every task:

- **Decomposition review**: all four tasks map 1:1 to plan Step 3's lettered sub-steps (a)–(d). No task is `too_large`: none has a self-contained preamble or an intermediate verification cycle. Task 3 (the deletion sweep) is the largest — it reaches across two directories and enforces a strict record-then-self-delete ordering — but the removals are tightly coupled and strictly sequential (each deletion depends on the state left by the previous one, and the Story010 file itself must be the very last thing removed), so there is no natural seam; it stays as one task at its natural granularity.
- **Task 1** is annotated `[Small]`: one file (`memory-bank/stories/toc.md`), a mechanical rewrite to a documented empty skeleton, narrow scope, single concern. Routes to `technical-writer-for-story-implementor` (the `[Small]` annotation reflects intrinsic size only — this story never routes to a code agent).
- **Task 2** is annotated `[Small]`: one file (`memory-bank/finished-stories/toc.md`), identical mechanical rewrite pattern to Task 1. Routes to `technical-writer-for-story-implementor`.
- **Task 3** is **not** `[Small]`: touches 5+ files across two directories, coordinates a destructive sweep with a strict internal ordering rule (self-deletion last), and requires state confirmation before every removal. Routes to `technical-writer-for-story-implementor`.
- **Task 4** is annotated `[Small]`: read-only verification of a single directory (`memory-bank/plans/`), one concern. Routes to `technical-writer-for-story-implementor`.

### Task 1: Rewrite `memory-bank/stories/toc.md` as an empty skeleton — Completed [Small]

Architect note (decomposition): at its natural granularity — one file, a mechanical rewrite to the file's existing structural headers with every entry/row removed; cannot be smaller. `[Small]` by all four sizing rules (1 file; additive/mechanical, no new abstractions; narrow scope; single concern). Routes to `technical-writer-for-story-implementor`.

1. Rewrite `memory-bank/stories/toc.md` to the empty skeleton (plan Step 3 (a)) - Completed
   a. Replace the current contents (header `# Stories - Table of Contents`, intro line, whatever `## Active Stories` entries are present at execution time — the menora Story004/Story005 entries plus this arc's own Story006–Story010 entries — and whatever `## Finished Stories` rows are present) with the empty skeleton: keep the header and the intro line, add an `## Active Stories` heading with **zero entries** beneath it, and an `## Finished Stories` heading whose table keeps only the header row (`| Story File | Description | State |` and the `|------------|-------------|-------|` separator) with **zero data rows**. The result contains no story links and no dangling references. - Completed
   b. Verify: read the rewritten file back; confirm exactly two section headings (`## Active Stories`, `## Finished Stories`) with no entries between them and the table header, and zero `[Story...](...)` links. - Completed

### Task 2: Rewrite `memory-bank/finished-stories/toc.md` as an empty skeleton — Completed [Small]

Architect note (decomposition): at its natural granularity — one file, the same mechanical pattern as Task 1. `[Small]` (1 file, mechanical, single concern). Routes to `technical-writer-for-story-implementor`.

Path note: the finished-stories toc lives at **`memory-bank/finished-stories/toc.md`** — `finished-stories/` is a sibling of `memory-bank/stories/` in the actual repository layout. The plan's Step 3 lettered text uses this actual path; only the plan's proposed-target-structure diagram shows a nested `stories/finished-stories/`. Use the actual layout — do not create or relocate any directory.

1. Rewrite `memory-bank/finished-stories/toc.md` to the empty skeleton (plan Step 3 (b)) - Completed
   a. Replace the current contents (header `# Finished Stories - Table of Contents`, intro line, and whatever `## Finished Stories` data rows are present at execution time — the menora Story001–Story003 rows plus the arc's completed Story006–Story009 rows) with the empty skeleton: keep the header and the intro line, then a `## Finished Stories` table with only the header row (`| Story File | Description | State |` and the separator) and **zero data rows**. - Completed
   b. Verify: read the rewritten file back; confirm zero data rows and zero `[Story...](...)` links. - Completed

### Task 3: Remove all remaining story files (menora stories, arc meta-stories, walkthrough, then this story) — Completed

Architect note (decomposition): **not** `[Small]`. This is a coordinated destructive sweep across two directories (`memory-bank/stories/` and `memory-bank/finished-stories/`) with a strict internal ordering: menora stories first, then the arc's own completed meta-stories, then the walkthrough directory, and finally the completion record. The Story010 file itself is **not** deleted by this task — its physical removal is the last act of the whole story, after Task 4 (see subtask 3d and Constraints). Every removal depends on the state left by the previous removal (and the story file must never be deleted before its work is recorded), so there is no natural seam and no isolation benefit to splitting; the ordering is enforced within one task. Splitting per directory would split a tightly-coupled sequential chain and multiply the risk of deleting a still-needed file. Routes to `technical-writer-for-story-implementor` (pure deletion/record work, run-only, no TDD).

1. Remove all remaining story files (plan Step 3 (c)) - Completed
   a. Remove any remaining **menora** story files: `memory-bank/stories/Story004_parabolic-arch-layout.md` and `memory-bank/stories/Story005_stock-generation-utility.md`, and — if still present — `memory-bank/finished-stories/Story001_face-plate-layout-refactor.md`, `Story002_downward-arc-layout.md`, and `Story003_nine-inch-face-single-arc.md`. These should already have been deleted by Story006 (base-repo-cleanup, plan Step 1 (a)); remove whatever remains in the working tree. Before each removal, list the target directory and confirm the target is a story `.md` file. - Completed
   b. Remove the arc's own completed **meta-stories** from `memory-bank/finished-stories/`: `Story006_base-repo-cleanup.md`, `Story007_python-structure-and-setup.md`, `Story008_tooling-generalization.md`, and `Story009_template-verification.md` (each was moved there by its own completion discipline before this story ran; they must be present and are removed here). - Completed
   c. Remove `memory-bank/stories/walkthrough/` if it is still present (menora-specific walkthrough; plan Step 1 (a) may already have removed it). - Completed
   d. Record this story's completion — add a brief "Recently Completed" entry in `memory-bank/context.md` per the standard task discipline — and then clear that entry so `context.md` returns to the empty-skeleton state that plan Step 2 established (the template-ready end state leaves `context.md` with empty Active Tasks / Recently Completed sections). **Do not delete `Story010_stories-reset.md` in this task.** The physical self-deletion is the **last act of the whole story**, executed by the story-implementor in the main tree only after Task 4 confirms `plans/` — the story file must remain readable through every task (including Task 4). See Constraints ("Self-deletion ordering") and Execution Order. - Completed

### Task 4: Confirm `memory-bank/plans/` contains only `base-repository-setup_plan.md` — Not Started [Small]

Architect note (decomposition): at its natural granularity — read-only verification of one directory, one concern, no file modifications. `[Small]`. Routes to `technical-writer-for-story-implementor`.

1. Confirm `memory-bank/plans/` contains only this plan (plan Step 3 (d)) - Not Started
   a. List `memory-bank/plans/`; expect exactly one entry: `base-repository-setup_plan.md` (the 7 menora plan files were already deleted from the working tree; verify nothing else was reintroduced during the arc). - Not Started
   b. If any other file is present, STOP and report — do not delete anything outside `memory-bank/stories/` and `memory-bank/finished-stories/` without direction; the reset scope is the stories directories, and the `plans/` check is a verification gate, not a deletion license. - Not Started

### Parallel Execution

**None.** This story is pure documentation/deletion work with no parallelization: all rewrites and removals are sequential and interdependent (the toc skeletons must be rewritten before the deletions so no toc ever references a deleted story; the deletions must complete before the final verification; and the Story010 file must be the very last thing removed). Tasks 1 and 2 are file-disjoint in principle (two different toc.md files) but both are trivial single-file rewrites, so parallel worktree overhead would exceed any benefit — the architect's conservative default ("cannot parallelize" when in doubt, and no isolation benefit here) applies, and they stay sequential.

### Execution Order

```
        ┌─────────────┐
        │  Task 1     │  (rewrite stories/toc.md → empty skeleton — [Small])
        └──────┬──────┘
               ▼
        ┌──────┴──────┐
        │  Task 2     │  (rewrite finished-stories/toc.md → empty skeleton — [Small])
        └──────┬──────┘
               ▼
        ┌──────┴──────┐
        │  Task 3     │  (remove menora stories → arc meta-stories → walkthrough → record)
        └──────┬──────┘
               ▼
        ┌──────┴──────┐
        │  Task 4     │  (verify plans/ holds only base-repository-setup_plan.md — [Small])
        └─────────────┘
```

A simple linear graph — one chain, no branches, no parallel groups. Each task's output is the next task's precondition:

- **Task 1 before Task 2**: the parent index (`stories/toc.md`) is emptied first; the finished index is emptied second.
- **Tasks 1–2 before Task 3**: both toc skeletons must be in place before any story file is deleted, so no toc ever references a file that is about to disappear.
- **Task 3 before Task 4**: final verification runs on the post-deletion tree.
- **Subtask 3d**: the completion record is made (and cleared) at the end of Task 3. The physical self-deletion of `Story010_stories-reset.md` is **not** part of Task 3 — it is the very last act of the whole story, executed by the story-implementor in the main tree after Task 4 passes, so the story file remains readable through every task (see Constraints).

### Reintegration

**None — no parallel groups.** All four tasks execute sequentially in the single story worktree/branch; there are no parallel worktrees to merge, so no merge-order, integration-test, or conflict-prone-file analysis applies. The final state is verified once, at Task 4, against the story's Acceptance Criteria.

## Test-First Development

n/a — this story contains no code and has no unit-test target. It is pure documentation and deletion work (plan Story-Writer Guidance item 5 routes it to `technical-writer-for-story-implementor`: "pure docs/deletion, no TDD"). Verification is performed by the per-task checks — reading the rewritten toc.md files back, listing the story directories, and confirming `plans/` contents — and by the story-level Acceptance Criteria, which mirror plan Step 3's completion criteria.

## Constraints

- **Hard ordering gate (dependencies)**: this story must NOT run until Story006–Story009 are complete **and** moved to `memory-bank/finished-stories/`. Running it earlier would delete the arc's own in-progress or not-yet-moved stories.
- **TERMINAL story**: Story010 is the last story of the `base-repository-setup` arc — nothing else in this arc runs after it. Per the plan, story numbering is free to restart at Story001 once this story completes.
- **Scope**: modify only `memory-bank/stories/`, `memory-bank/finished-stories/`, and `memory-bank/context.md` (completion record only). Do **not** modify `.kilocode/rules/organization.md`, `memory-bank/plans/base-repository-setup_plan.md`, or any other file. `memory-bank/plans/` is read-only (verification only).
- **Skeleton conformance**: the two reset toc.md files must match the structure documented in `.kilocode/rules/organization.md` — `stories/` and `finished-stories/` each contain a `toc.md`, and after this story each directory contains **only** its fresh `toc.md`.
- **Actual paths**: `memory-bank/finished-stories/` is a sibling of `memory-bank/stories/`; its toc is at `memory-bank/finished-stories/toc.md`. The plan's Step 3 lettered text uses these actual paths; its proposed-target-structure diagram (nested `stories/finished-stories/`) is superseded by the actual layout. Do not create or relocate directories.
- **Self-deletion ordering**: `Story010_stories-reset.md` is removed only after its work is recorded (Task 3 subtask d) **and** after Task 4 confirms `plans/`. The physical deletion is the very last act of the whole story — the last deletion overall — executed by the story-implementor in the main tree (the story file is a coordination file kept out of task worktrees).
- **No end-of-task move**: the standard "move the completed story to `finished-stories/`" step does NOT apply to this terminal story — the reset deletes the story file instead (there is no finished story to move).
- **Destructive-state care**: deletions are irreversible in the working tree. Before each removal, list the target directory and confirm the target is a story/walkthrough artifact; if the expected file is absent (already deleted by an earlier story), record it as already-removed and continue — do not recreate or restore anything.
- All paths in this story are repo-root-relative except the References section (relative to the `memory-bank` directory, per the story template).

## Intent

- **Task 1** — Reset `memory-bank/stories/toc.md` to a fresh empty skeleton (Active + Finished sections, zero entries) so the stories directory is template-ready and no link points at a to-be-deleted story.
- **Task 2** — Reset `memory-bank/finished-stories/toc.md` to a fresh empty skeleton (Finished table, zero rows) at its actual path, matching the directory's template state.
- **Task 3** — Remove every remaining story artifact — the menora stories, the arc's own completed meta-stories, and the walkthrough directory — and finally the reset story itself, once its completion is recorded, leaving only the two fresh toc skeletons.
- **Task 4** — Confirm `memory-bank/plans/` holds only `base-repository-setup_plan.md`, proving the reset left no stray plan or story state behind.

## Acceptance Criteria

The plan's Step 3 completion criteria, restated as verifiable checks:

- [ ] `memory-bank/stories/` contains only `toc.md`: no `StoryNNN_*.md` files and no `walkthrough/` (verified by directory listing).
- [ ] `memory-bank/finished-stories/` contains only `toc.md` (verified by directory listing).
- [ ] `memory-bank/stories/toc.md` has `## Active Stories` (zero entries) and `## Finished Stories` (table header row only, zero data rows) and contains no `[Story...](...)` links.
- [ ] `memory-bank/finished-stories/toc.md` has `## Finished Stories` (table header row only, zero data rows) and contains no `[Story...](...)` links.
- [ ] `memory-bank/plans/` contains only `base-repository-setup_plan.md`.
- [ ] Every story file is gone: a listing of `memory-bank/stories/` and `memory-bank/finished-stories/` shows exactly the two toc.md files; no `Story*.md` remains anywhere under `memory-bank/` (verified via `find`/`ls`).
- [ ] `Story010_stories-reset.md` itself was the last deletion — its physical removal is the very last act of the whole story, executed by the story-implementor after Task 4 passes and the completion record was made (Task 3 subtask d).
- [ ] `memory-bank/context.md` is in its plan-Step-2 skeleton state (empty Active Tasks / Recently Completed) after the story's temporary completion entry was cleared.
- [ ] Story numbering is free to restart at Story001 (the only remaining stories-path content is the two toc skeletons).

## Requesting Clarification

If at any point during story construction there is confusion or ambiguity about the goal or how to accomplish it, stop and ask the user for clarification.

## Notes

- **Position in the arc**: Story-Writer Guidance item 5 of `memory-bank/plans/base-repository-setup_plan.md` defines this story: "Story `stories-reset` (TERMINAL — last) — Step 3 only. Depends on stories 1–4 being complete and moved to `finished-stories/`. Resets `stories/` and `finished-stories/` to empty skeletons, removing the menora stories and the arc's own meta-stories. Route to `technical-writer-for-story-implementor`; pure docs/deletion, no TDD."
- **Path discrepancy (resolved toward actual)**: the plan's proposed-target-structure diagram nests `finished-stories/` under `stories/` (`memory-bank/stories/finished-stories/toc.md`), but the actual repository layout has `memory-bank/finished-stories/` as a sibling of `memory-bank/stories/`. The plan's Step 3 lettered text (a)–(d) uses the actual paths, and this story follows the actual layout: `memory-bank/finished-stories/toc.md`.
- **What "empty" means per file** (as inspected at story-creation time):
  - `memory-bank/stories/toc.md` currently contains Active entries (Story004–Story010 — the menora stories plus this arc's own) and a Finished table with the Story001–Story003 rows. "Empty" = keep header + intro + `## Active Stories` heading with no entries + `## Finished Stories` heading with the table header row only. At execution time the exact mix may differ (some arc stories may already have been moved to the Finished table by their completion discipline), but the result is always the same: no entries, no data rows.
  - `memory-bank/finished-stories/toc.md` currently contains a Finished table with the Story001–Story003 rows (and will gain the arc's completed Story006–Story009 rows before this story runs). "Empty" = keep header + intro + `## Finished Stories` heading with the table header row only.
- **Completion record**: "once its work is recorded" (plan Step 3 (c)) is realized as a brief `memory-bank/context.md` "Recently Completed" entry that is then cleared, so `context.md` ends in the same empty-skeleton state plan Step 2 established (the plan's target structure requires empty Active Tasks / Recently Completed sections). The story-implementor's final report also records the outcome before the file is deleted.
- **This story's toc entry**: the story was registered in `memory-bank/stories/toc.md` when created, with the description "Reset memory-bank/stories/ and finished-stories/ to empty skeletons, removing the menora stories and this arc's own completed meta-stories (TERMINAL story)." Task 1's rewrite wipes that entry along with everything else — intended.
- **Resolved decisions applied**: plan Resolved Decision 9 (story numbering resets to Story001) and Resolved Decision 10 (stories reset is a terminal story) — both satisfied by this story's execution.
- **Overlap with Story006**: plan Step 1 (a) (inside Story006, `base-repo-cleanup`) already deletes the menora story files and the walkthrough; this story's Task 3 handles whatever remains, so it is idempotent with respect to those earlier deletions. Verify presence before deleting (Constraint: Destructive-state care).
- All paths in this story are repo-root-relative except the References section.