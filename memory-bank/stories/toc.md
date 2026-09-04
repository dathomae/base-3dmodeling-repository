# Stories - Table of Contents

This directory contains story files for the project. Each story represents a planned piece of work.

## Active Stories

**[Story004_parabolic-arch-layout.md](Story004_parabolic-arch-layout.md)** — _Not Started_
: Replace the downward_arc_layout semicircular arc with a collision-free concave-down parabolic arch (feet ±63/28, crown y=95) on the 9-in face and reconcile the 7-in/stale-arc docs.

**[Story005_stock-generation-utility.md](Story005_stock-generation-utility.md)** — _Not Started_
: Generate .step models of the milling stock (0.75in/1.5in/2in square bar and 12in half-square face plate) for 3D-print CAM testing, and extract INCH_MM into a shared common module.

## Finished Stories

| Story File | Description | State |
|------------|-------------|-------|
| [Story001_face-plate-layout-refactor.md](../finished-stories/Story001_face-plate-layout-refactor.md) | Refactor the face-plate builder so candle-hole placement is driven by a pluggable layout strategy, adding a --layout CLI option with circular as the default. | Done |
| [Story002_downward-arc-layout.md](../finished-stories/Story002_downward-arc-layout.md) | Add the `downward_arc_layout` face-plate candle arrangement (two symmetric circular arcs, 4 per side) with its continuous embossed arc line, per the arc design doc, with unit tests and verification. | Done |
| [Story003_nine-inch-face-single-arc.md](../finished-stories/Story003_nine-inch-face-single-arc.md) | Enlarge the face plates to 9-inch equilateral triangles for all layouts and revise the downward_arc_layout to a single concave-down circular arc carrying all 8 candles. | Done |
