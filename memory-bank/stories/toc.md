# Stories - Table of Contents

This directory contains story files for the project. Each story represents a planned piece of work.

## Active Stories

**[Story004_parabolic-arch-layout.md](Story004_parabolic-arch-layout.md)** — _Not Started_
: Replace the downward_arc_layout semicircular arc with a collision-free concave-down parabolic arch (feet ±63/28, crown y=95) on the 9-in face and reconcile the 7-in/stale-arc docs.

**[Story005_stock-generation-utility.md](Story005_stock-generation-utility.md)** — _Not Started_
: Generate .step models of the milling stock (0.75in/1.5in/2in square bar and 12in half-square face plate) for 3D-print CAM testing, and extract INCH_MM into a shared common module.

**[Story006_base-repo-cleanup.md](Story006_base-repo-cleanup.md)** — _Done_
: Remove all menora-specific content (stories, plans, design docs, chanukah-halacha, alder-paradox gitlink) and replace memory-bank docs with project-agnostic skeletons.

**[Story007_python-structure-and-setup.md](Story007_python-structure-and-setup.md)** — _Not Started_
: Establish the Python src/-layout package (pyproject.toml + scaffold example + test), setup scripts, MIT LICENSE, and GETTINGSTARTED/README; delete requirements.txt.

**[Story008_tooling-generalization.md](Story008_tooling-generalization.md)** — _Not Started_
: Generalize the PDD scripts and rule files: drop Chronocone/Go references, set Python defaults (python -m pytest/build), and update organization.md and mock.md.

**[Story009_template-verification.md](Story009_template-verification.md)** — _Not Started_
: Verify the template end-to-end from a clean state: ./setup.sh succeeds, python -m pytest passes, the example CLI emits a .step, and git status is clean.

**[Story010_stories-reset.md](Story010_stories-reset.md)** — _Not Started_
: Reset memory-bank/stories/ and finished-stories/ to empty skeletons, removing the menora stories and this arc's own completed meta-stories (TERMINAL story).

## Finished Stories

| Story File | Description | State |
|------------|-------------|-------|
| [Story001_face-plate-layout-refactor.md](../finished-stories/Story001_face-plate-layout-refactor.md) | Refactor the face-plate builder so candle-hole placement is driven by a pluggable layout strategy, adding a --layout CLI option with circular as the default. | Done |
| [Story002_downward-arc-layout.md](../finished-stories/Story002_downward-arc-layout.md) | Add the `downward_arc_layout` face-plate candle arrangement (two symmetric circular arcs, 4 per side) with its continuous embossed arc line, per the arc design doc, with unit tests and verification. | Done |
| [Story003_nine-inch-face-single-arc.md](../finished-stories/Story003_nine-inch-face-single-arc.md) | Enlarge the face plates to 9-inch equilateral triangles for all layouts and revise the downward_arc_layout to a single concave-down circular arc carrying all 8 candles. | Done |
