# Chanukah Candle Arrangement — Halachic Practices and Constraints

## 1. Source and Scope

This document captures the halachic practices and constraints that bear on
**how candles are arranged on a Chanukah menorah**. It is distilled from:

- Richard B. Aiken, "Halacha L'Maaseh on Chanuka," Orthodox Union
  (<https://www.ou.org/holidays/practical-halacha-chanuka/>).

Only rules that affect the *geometry, ordering, or structure* of a candle
arrangement are captured here. Halachot about timing, blessings, who lights,
and where the menorah sits are listed in Section 6 only to mark them out of
scope. This material is provided for informational purposes only and is not a
substitute for the consultation of a competent rabbi.

The overarching reason for lighting is *pirsumei nisa* — publicizing the
miracle. The arrangement rules below serve that purpose by making each candle a
clear, distinct, ordered light.

## 2. Summary of Arrangement Rules

| # | Rule | Effect on arrangement |
|---|------|-----------------------|
| 1 | All eight candle holders must be on the **same level** | The eight candles sit at one common height — never a circle, pyramid, or staircase |
| 2 | The menorah itself may be **curved horizontally** | The row may follow a gentle horizontal curve, but never a vertical one |
| 3 | The **shamash** must be clearly not one of the eight | Distinct placement: raised, lowered, off to the side, or centered |
| 4 | Each candle must be **in its own holder** | One candle per holder; no shared wells |
| 5 | There is a **defined left-to-right order** | Setup right-to-left, light left-to-right — the arrangement must make "left-most" unambiguous |
| 6 | **One shamash** serves any number of menorot in one area | A single servant candle per menorah is sufficient |
| 7 | Candles are separate, individual lights | Centers are spaced so flames never merge (project constraint: ≥ 1.0 in) |

## 3. Detailed Rules

### 3.1 All Eight Candles at the Same Level

> "All eight candle holders of a chanuka menorah must be on the same level."

The eight Chanukah candles must sit at a common height above the surface on
which the menorah stands. This is what makes the candles read as "the eight"
versus the shamash. The rule bites when holders are placed at deliberately
different heights (a pyramid, a staircase, or a circle whose *holders* are at
different heights).

**Important for a flat-plate menorah:** the rule constrains the *height of the
holders*, not their 2-D footprint. On a flat surface — such as the horizontal
top face of the die when it rests on a face — every holder lies at the same
height by construction, so the rule is satisfied automatically for any 2-D
pattern (row, arc, circle, or packed field). A pattern only violates the rule
if the holders themselves are at different heights (e.g., a stepped design).

When fewer than eight candles are lit (nights 1–7), the candles in use are a
subset of the eight, so they likewise occupy the same level — automatic on a
flat face.

### 3.2 The Menorah May Be Curved Horizontally

> "The menorah itself may be curved horizontally."

The *plan view* of the candle row may be a gentle horizontal curve (e.g., a
shallow arc as seen from above), but this must never change the candles'
heights. Any curve must stay horizontal — curving up or down would violate
Rule 3.1. A straight row is simply the degenerate (zero-curvature) case.

### 3.3 The Shamash Must Be Clearly Distinct

> "The shamash must be slightly raised or lowered or to the side of the
> menorah or in the center, as long as it clearly is not part of the other
> eight candles."

The shamash (servant candle) is not one of the eight and must be visually and
geometrically unmistakable as such. Acceptable placements: raised, lowered, off
to one side, or in the center — any arrangement that clearly separates it from
the row of eight. The shamash is also the only candle from which the others may
be lit ("do not light other candles from them, except from the shamash").

### 3.4 Candles Must Be in Their Own Holders

> "You may put oil lights directly onto a windowsill or other level surface,
> but candles must be in or on some type of holder."

Every candle occupies a holder of its own. Each candle is an individual,
distinct light; holders are never shared between candles. This also implies the
candles must be separated enough to remain distinct entities (see 3.7).

### 3.5 A Defined Left-to-Right Order

> "Light Chanuka candles from left to right, as you face it, not as it will be
> seen from outside the window. Add the new candle from right to left. For
> example, on the first night, put the candle on the extreme right of the
> menorah."
>
> "Set up the candles starting from the right side of the menorah."
>
> "Light the left-most candle first and proceed to the next candle on the
> right."

The ritual depends on a well-defined left-to-right ordering *from the point of
view of the person facing the menorah*:

- Each night's **new** candle is added on the **left** (accumulation proceeds
  right → left).
- On night one, the single candle sits on the **extreme right**.
- Lighting proceeds **left → right** (newest first, oldest last).

The arrangement must therefore make the left-to-right order unambiguous to the
lighter. A single straight row (or horizontally-curved row) does this
naturally; a circular arrangement does not, because no consistent "left-most"
candle exists.

### 3.6 One Shamash per Area

> "You only need one service (shamash) candle for any amount of Chanuka
> candles/oil lamps (menorot) in the same area."

A single shamash serves the entire menorah. On a die menorah this means one
shamash per face is sufficient, and only the face currently in use needs its
shamash lit.

### 3.7 Separation of Candles — Flames Must Not Merge

The candles are separate, individual lights. They must be spaced so that
flames and holders remain clearly distinct and candles cannot be mistaken for
"part of" one another. The halacha does not prescribe a numeric distance; the
minimum separation is an engineering/design decision.

**Project constraint (not from the OU article):** the centers of adjacent
regular candle holders must be at least **1.0 inch (25.4 mm)** apart. They may
be spaced further apart where a larger spacing yields a more symmetrical
arrangement (see `memory-bank/requirements.md`).

**Project constraint on shamash visibility:** when a fully populated face is
viewed from its base edge toward the point (a low, "through the forest" view),
the shamash must not be occluded by the regular candles. In the single-arch
arrangement this is enforced by separating the innermost candle tops (the
arc-top pair straddling the arch crown) by at least **0.5 inches (12.7 mm)**;
the parabolic-arch design gives 26.62 mm between the arc-top pair (holes 4–5).

## 4. Derived Design Implications for the Octahedral Die Menorah

The die menorah is an octahedron with eight triangular faces; each face holds
1–8 candles plus one shamash near the triangle's point. Applying the rules
above:

| Halachic rule | Design implication for a face plate |
|---------------|--------------------------------------|
| 3.1 Same level | Satisfied automatically: when the die rests on a face, the lit face is horizontal, so every candle on it — in any 2-D pattern (row, arc, circle, packed) — sits at the same height. This rule does not constrain the 2-D layout. |
| 3.2 May curve horizontally | Confirms the 2-D footprint is free: a circle or arc on the flat top face keeps every candle at the same height and is an explicitly permitted "horizontal curve." |
| 3.3 Distinct shamash | The shamash at the triangle's point is clearly separated from the cluster of eight on the face — an acceptable placement (off to the side / raised in the plan view). It must remain visually distinct. |
| 3.4 Own holder | Each candle has its own holder (the 0.75 in square candle holders); already satisfied. |
| 3.5 Left-to-right order | The ritual (night-one candle on the right, add leftward, light left-to-right) needs an unambiguous left-to-right order. A straight row makes this self-evident; an arc keeps a monotonic left-right order; a circle or packed field needs an explicit ordering convention. This is a ritual-clarity constraint, not a "level" constraint. |
| 3.6 One shamash per area | One shamash per face is sufficient; only the lit face's shamash is used. |
| 3.7 Separation | Adjacent holder centers on a face must be ≥ 1.0 in (25.4 mm) apart; spacing may grow to fill the face symmetrically. |

**Net effect:** the same-level halacha imposes no constraint on the 2-D candle
pattern on a face. The face layout is governed instead by (a) the 1.0-inch
minimum spacing, (b) fitting inside the fixed triangular plate, (c) a clearly
distinct shamash that stays visible through the candle forest, and (d) keeping
a usable left-to-right order for the lighting ritual. A straight row is the
clearest form for (d) but is not halachically required.

**Feasibility note (fixed 9-inch faces):** the face plates are an equilateral
triangle 9 in (228.6 mm) on a side (the standard face). The current 8-candle
arrangement is the single concave-down parabolic arch (the `downward_arc_layout`
face layout): all 8 regular candles from the bottom right up the right side,
over the crown at (0, 95), and down the left side to the bottom left, with
adjacent centers 26.62 mm apart (≥ 1.0 in) and the shamash ≈ 70.4 mm from the
nearest regular candle (≥ 1.75 in, also ≥ 63.5 mm). An 8-candle face fits
comfortably, and the foot (bottom) holders of faces sharing a bottom edge do
not intersect in the assembled die. (Earlier capacity studies — straight single
row ≤ 7, horizontal arc ≤ 8–9, full circle ≤ 12, staggered/packed rows ≤ 15,
two symmetric arcs holding 8 at the 1.0-in minimum — were computed at the
former smaller face size and are superseded by the 9-in face; the method and
history are in `memory-bank/arrangement_approach.md`.)

## 5. Related Halachot That Do Not Constrain Per-Face Arrangement

For completeness, these rules from the same source govern lighting *practice*
rather than candle *geometry* and are out of scope for face layout:

- **Timing:** light after dark; burn at least 30 minutes after dark; Friday
  arrangements; latest time (102 minutes before sunrise).
- **Who and how many:** one candle per household per night is the basic
  obligation; extra candles per night and every male lighting is an enhancement;
  women are equally obligated; a wife may light for her husband.
- **Blessings:** *Lehadlik ner shel Chanuka*, *She'asa nisim*,
  *Shehecheyanu*, *Ha'neirot hallalu*; one shamash per area.
- **Use:** no using the candle light for any purpose; no "work" while burning.
- **Placement of the menorah:** light in your own home; outside *Eretz
  Yisrael* place by a window ideally facing the street; once lit the menorah
  may not be turned or moved.

## 6. References

- Aiken, Richard B. "Halacha L'Maaseh on Chanuka." Orthodox Union,
  <https://www.ou.org/holidays/practical-halacha-chanuka/>.
- Project requirement for candle-center spacing:
  `memory-bank/requirements.md` (Constraints section).
