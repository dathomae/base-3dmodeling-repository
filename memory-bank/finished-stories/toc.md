# Finished Stories - Table of Contents

This directory contains completed story files for the project. Each story listed here has been fully implemented.

## Finished Stories

| Story File | Description | State |
|------------|-------------|-------|
| [Story001_face-plate-layout-refactor.md](Story001_face-plate-layout-refactor.md) | Refactor the face-plate builder so candle-hole placement is driven by a pluggable layout strategy, adding a --layout CLI option with circular as the default. | Done |
| [Story002_downward-arc-layout.md](Story002_downward-arc-layout.md) | Add the `downward_arc_layout` face-plate candle arrangement (two symmetric circular arcs, 4 per side) with its continuous embossed arc line, per the arc design doc, with unit tests and verification. | Done |
| [Story003_nine-inch-face-single-arc.md](Story003_nine-inch-face-single-arc.md) | Enlarge the face plates to 9-inch equilateral triangles for all layouts and revise the downward_arc_layout to a single concave-down circular arc carrying all 8 candles. | Done |
| [Story008_tooling-generalization.md](Story008_tooling-generalization.md) | Generalize the PDD scripts and rule files: drop Chronocone/Go references, set Python defaults (python -m pytest/build), and update organization.md and mock.md. | Done |
| [Story006_base-repo-cleanup.md](Story006_base-repo-cleanup.md) | Remove all menora-specific content (stories, plans, design docs, chanukah-halacha, alder-paradox gitlink) and replace memory-bank docs with project-agnostic skeletons. | Done |
| [Story007_python-structure-and-setup.md](Story007_python-structure-and-setup.md) | Establish the Python src/-layout package (pyproject.toml + scaffold example + test), setup scripts, MIT LICENSE, and GETTINGSTARTED/README; delete requirements.txt. | Done |
| [Story009_template-verification.md](Story009_template-verification.md) | Verify the template end-to-end from a clean state: ./setup.sh succeeds, python -m pytest passes, the example CLI emits a .step, and git status is clean. | Done |
