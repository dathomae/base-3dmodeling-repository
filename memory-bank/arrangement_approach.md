# Candle Arrangement Optimization Approach

How the face-plate candle arrangements for the menorah die were explored and
solved with numeric optimization (`scipy.optimize`). This document records the
method so future agents can reuse it: the geometric modeling, the optimization
formulation, the solving/validation discipline, the pitfalls encountered, and
worked examples with real numbers from this project.

## 1. The Problem Class

We must place candle-holder centers on a fixed equilateral triangular face
plate (side 7 in / 177.8 mm, height 153.98 mm, half-base 88.9 mm — size fixed
by manufacturing equipment) subject to a set of constraints, while maximizing
or measuring some quantity:

- **Minimum regular-candle spacing** (has been 1.6 in, 1.35 in, and finally
  1.0 in = 25.4 mm between adjacent centers).
- **Shamash constraints** (fixed position at the point; either a minimum
  distance, a multiple-of-spacing rule, or a distance to maximize).
- **Equatorial-connector clearance** (the start holder block must not collide
  with the connector at the bottom vertex).
- **All holder blocks fully inside the triangle.**
- **A shape family** (smooth circular/parabolic/catenary arcs, or an
  unconstrained monotonic curve).

The objective is usually a **max-min**: maximize the smallest pairwise distance
(max spacing), or maximize the shamash-to-nearest-candle distance subject to a
fixed spacing.

The approach has three pillars:

1. **Exact geometric modeling** — encode the feasible region and constraints
   precisely (linear where possible), including the true holder footprint.
2. **The epigraph (slack-variable) formulation** — turn a nonsmooth max-min
   objective into a smooth constrained optimization.
3. **Multi-start SLSQP + strict verification** — solve from many random
   feasible starts, then independently re-check the result.

## 2. Exact Geometric Modeling

### Coordinate system

Face base along `y = 0`, triangle point at `(0, 153.98)`; the face is symmetric
about `x = 0`. Candle centers are `(x, y)` in mm.

### Holder-fit as linear constraints

The holder is a 0.75 in (19.05 mm) square, axis-aligned in face coordinates
(half-width `hw = 9.525 mm`). It is fully inside the triangle iff **all four of
its corners** satisfy the triangle's three edge inequalities:

```
y ≥ 0
154·x + 88.9·y ≤ 13690.6     (right edge)
−154·x + 88.9·y ≤ 13690.6    (left edge)
```

**Important**: a center-inset margin (`center is 9.525 mm from each edge`) is
*not* sufficient near corners — the holder's far corner can poke outside even
when the center is "inset." Always check the four corners.

### Connector clearance as a linear constraint

The equatorial connector occupies a corner triangle on the face's inner
surface: apex at the vertex `(88.9, 0)`, base edge from `(69.85, 0)` to
`(50.80, 33.0)`. Requiring the start holder's nearest corner to stay 3 mm
inboard of the connector's slanted base edge reduces to a single linear
half-plane on the center:

```
33·x + 19.05·y ≤ 2172.2 − 38.1·clearance_mm     (right side)
```

(with `clearance_mm = 3` giving `≤ 2057.9`). Each mm of clearance subtracts
38.1 (the normal length) from the constant.

### Symmetry reduction

Arrangements are symmetric about `x = 0`, so only the right side is
parametrized and the left side is the mirror `(−x, y)`. This halves the
variables and guarantees symmetry.

## 3. Parametrizing the Arrangement

### Smooth circular arc (primary family)

A circular arc is parametrized by its start point `S`, end point `T`, and a
sagitta `b` (signed bulge). The circle through `S` and `T` with sagitta `b`:

```
c  = |T − S|
R  = (c²/4 + b²) / (2b)                 # circle radius
d  = R − b                              # center offset from chord midpoint
center = M − sign(b) · n · d            # n = unit perpendicular to chord
```

Then `N` points are placed **evenly by arc length** (even angle spacing on a
circle = even arc length):

```python
def arc_points(S, T, sagitta, n):
    c = dist(S, T)
    ux, uy = (T[0]-S[0])/c, (T[1]-S[1])/c
    nx, ny = -uy, ux
    M = ((S[0]+T[0])/2, (S[1]+T[1])/2)
    R = (c*c/4 + sagitta**2) / (2*sagitta)
    d = R - sagitta
    Cx, Cy = M[0] - nx*d, M[1] - ny*d          # bulge sign fixed per family
    a0 = angle of S about (Cx,Cy); a1 = angle of T about (Cx,Cy)
    # ensure the minor-arc sweep passes through the intended bulge
    return [(Cx + R*cos(a0 + (a1-a0)*t/(n-1)),
             Cy + R*sin(a0 + (a1-a0)*t/(n-1))) for t in range(n)]
```

### Other smooth families

- **Parabola**: a quadratic Bezier `P(t) = (1−t)²S + 2t(1−t)C + t²E`; choose the
  control point `C` so the curve passes through a chosen mid-bulge point.
- **Catenary**: `y = a·cosh((x−x0)/a) + y0` solved through the three points
  (start, bulge, end) with `scipy.optimize.root`.
- For any non-analytic curve, use **numeric arc-length reparametrization**:
  sample the curve finely, build the cumulative arc length, and interpolate to
  the `N` equal-arc-length positions.

### General (point-based) arrangements

For unconstrained exploration, parametrize the `N` points directly with
monotonicity constraints (`y` increasing, `x` decreasing along each arc) to
keep the intended rising shape.

## 4. The Epigraph (Max–Min) Formulation

A max-min objective (maximize the minimum pairwise distance) is nonsmooth.
Replace it with a smooth constrained problem using a slack variable `t`:

```
variables: point coordinates + t
maximize:  t
subject to: dist(pi, pj) ≥ t   for all pairs (i, j)
```

All other constraints (holder fit, connector clearance, shamash distance,
monotonicity, top-zone bound) are added as additional inequalities. This is
the standard epigraph trick and it works well with SLSQP.

When the spacing is *fixed* and another quantity is to be maximized (e.g., the
shamash-to-nearest distance at a fixed 1.0 in spacing), use the distance
constraints with the fixed spacing and maximize the other quantity directly.

## 5. Solving: Multi-Start SLSQP

Recommended solver: **`scipy.optimize.minimize(method='SLSQP')`** with
constraints as an array-valued inequality function (`≥ 0`), run from **many
random feasible starting points**, keeping the best strictly-feasible result.

```python
import numpy as np, random
from scipy.optimize import minimize

def cons(X):
    # return np.array of constraint residuals, all >= 0 at feasibility
    ...

def obj(X):
    return -X[-1]            # maximize t = last variable

best = None
for _ in range(300):
    X0 = random_feasible_start()          # rejection-sample the feasible region
    res = minimize(obj, X0, method='SLSQP', bounds=bnds,
                   constraints={'type': 'ineq', 'fun': cons},
                   options={'maxiter': 3000, 'ftol': 1e-12})
    X = res.x
    if all(cons(X) >= -1e-5) and better_than(best, X):
        best = X
```

Why SLSQP + many starts instead of `differential_evolution` with a penalty:
the DE+penalty approach was tried and was unreliable — an additive penalty
weight is not always large enough to dominate the objective (infeasible points
with inflated `t` could "win"), and it repeatedly returned infeasible or
suboptimal results. The epigraph + SLSQP + multi-start was both more accurate
and easier to verify.

## 6. Validation Discipline

1. **Strict feasibility**: after each solve, verify `all(cons(X) >= -1e-5)`
   (and tighter, `1e-6`, for the final answer).
2. **Independent re-check**: recompute holder fit with the corner-based test
   and re-derive all pairwise distances from the raw coordinates; never trust
   the solver's internal constraint values alone.
3. **Binding constraints**: at a tight optimum all binding constraints should be
   active to numerical tolerance (e.g., every consecutive spacing equals the
   spacing, and the shamash distance equals its bound). This confirms the
   optimum is balanced, not prematurely stopped.
4. **Floating-point tolerance**: 3-decimal coordinates round the true optimum,
   so a spacing that should be exactly 25.40 mm can come out 25.399 or 25.401.
   Assert `>= 25.35` (or compare with a 0.05 mm delta), not `>= 25.4`.

## 7. Sensitivity Analysis

A single optimum is less useful than knowing **which design levers move the
answer**. For each relevant parameter, re-solve over a sweep and report the
optimum:

- Shamash height (moving the shamash toward the tip increases achievable
  spacing / separation).
- Connector clearance (each mm inboard costs a little spacing).
- The required spacing itself (determines which patterns fit a face).

Sensitivity tables made the design trade-offs concrete (see examples below) and
turned "is it feasible?" into "how much does each knob cost?"

## 8. Ground-Truth Extraction

The final optimized coordinates are the **ground truth** for the implementation.
Because they come from a constraint optimization (no simple closed form), the
implementation **hard-codes** them (e.g., `DOWNWARD_ARC_PARABOLIC_9IN` in
`src/manora/face_plate_layouts.py`) rather than reconstructing them, and unit tests
assert they match the design doc within 0.1 mm.

## 9. Worked Examples from This Project

### Pattern capacity at a given minimum spacing

For a candidate spacing, ask "how many candles fit per pattern?" using the
same machinery (or simple chords):

| Pattern | ≥ 1.6 in | ≥ 1.35 in | ≥ 1.0 in |
|---------|----------|-----------|----------|
| Straight row | 4 | 5 | 7 |
| Horizontal arc spanning the base | 6–7 | 7–8 | 8–9 |
| Full circle (largest that fits, r ≈ 51 mm) | 7 | 9 | 12 |
| Staggered / packed rows | 10 | 12 | 15 |

This drove the decision that the 8-candle face needs a 2-D arrangement, and
showed the 1.0 in minimum makes 8 candles fit comfortably in every pattern.

### Smooth-arc maximum spacing (arc tops near the top of the bottom 2/3)

Maximize the min spacing for two symmetric 4-candle arcs:

| Curve family | Max min spacing |
|--------------|-----------------|
| Circular | 36.2 mm = 1.43 in |
| Parabolic | 36.0 mm = 1.42 in |
| Catenary | 34.5 mm = 1.36 in |

Conclusion: at a 1.35 in requirement a circular arc fits; at 1.6 in it does
not. (Distinguish "smooth arc" from "any monotonic curve" — the latter, allowed
to run along the base first, reached 41.3 mm / 1.63 in, but that is an
L-shape, not an arc.)

### Shamash separation rules (shamash at its current position, y ≈ 117.2)

Maximize the regular spacing such that the shamash is a fixed multiple of the
spacing from its nearest candle:

| Rule | Max spacing | Arc-top height |
|------|-------------|----------------|
| 1.5× | 31.9 mm (1.26 in) | 47 % of face height |
| 2× | 29.6 mm (1.17 in) | 39 % |
| 3× | 24.4 mm (0.96 in) | 29 % |

Sensitivity to the shamash height at the 1.5× rule (y = 117 → 31.9 mm,
y = 135 → 34.4 mm, y = 153 → 36.5 mm) showed the shamash height is a strong
design lever.

### Max shamash separation at a fixed 1.0 in spacing

With the spacing fixed at 25.4 mm, maximize the shamash-to-nearest distance:

| Connector clearance | Max separation |
|---------------------|----------------|
| 0 mm | 66.3 mm = 2.61 in |
| 2 mm | 65.5 mm = 2.58 in |
| 3 mm | 65.1 mm = 2.56 in |

The arc-top candles are the nearest to the shamash; the start candles sit
exactly at the connector-clearance limit. This produced the final design:
arc starts at (±56.862, 9.525), arc tops at (±12.700, 53.295), spacing exactly
25.40 mm, shamash 65.14 mm away — recorded in
`memory-bank/design/candle-arrangement-arc.md` and hard-coded as
`DOWNWARD_ARC_RIGHT` per the plan in `memory-bank/plans/downward_arc_layout_plan.md`.

### 9-in parabolic arch (Story004, current)

The 7-in two-arc result above and the 9-in single circular arc of Story003 (a
semicircle: center (0, 12.7), radius 59.7 mm, peak (0, 72.4), ends (±59.7,
12.7)) are superseded by the **parabolic arch** adopted as the current
`downward_arc_layout` design. The parabola was chosen to reclaim the dead space
under the semicircle's low crown (which left ≈ 89 mm to the shamash) and to move
the feet away from the shared bottom edge, fixing the adjacent-face foot-holder
collision found in the assembled die:

- **Parabola**: `y = 28 + 67·(1 − (x/63)²)`, feet `(±63.0, 28.0)`, crown
  `(0, 95)` — `y = 28` clears the adjacent-face collision (threshold ≈ 27–28
  mm); `x = 63` clears the equatorial connector by ~2–3 mm (zero-clearance
  ≈ `x = 65` at `y = 28`).
- **8 ordered positions** (hole 1 = bottom right start, up the right side, over
  the crown, down the left side to the bottom-left end), placed evenly by arc
  length:
  1. (63.000, 28.000) &nbsp; 2. (50.261, 52.356) &nbsp; 3. (34.534, 74.867) &nbsp; 4. (13.312, 92.008)
  5. (−13.312, 92.008) &nbsp; 6. (−34.534, 74.867) &nbsp; 7. (−50.261, 52.356) &nbsp; 8. (−63.000, 28.000)
- **Constraint check**: the minimum adjacent chord is **26.62 mm** (arc-top
  pair `(±13.312, 92.008)`; side gaps ≈ 27.3–27.5 mm), ≥ 25.4 mm; the shamash at
  `(0, 161.17)` is ≈ 70.4 mm from its nearest candle (holes 4/5; ≥ 44.45 mm,
  also ≥ 63.5 mm); the start holders at `(±63, 28)` leave ~2–3 mm empirical
  clearance to the equatorial connectors; **adjacent-face holder
  non-intersection: 0 overlap across all 36 mounted holders**; bottom-holder
  M2 screw holes are ≈ 22.5 mm center-to-center from every equatorial-connector
  M2 hole (≥ 4.5 mm); all four holder corners sit inside the 9-in triangle, with
  the feet at 28 mm bottom inset (≥ 12.7 mm edge inset).
- The count rule is `candle_positions(n) == DOWNWARD_ARC_PARABOLIC_9IN[:n]` — a
  continuous over-the-top traversal — and the embossed groove is the single
  quadratic Bézier `((63.0, 28.0), (0.0, 162.0), (−63.0, 28.0))` (the control
  point `(0, 162)` is the tangent intersection, not on the curve; the groove
  peaks at `(0, 95)`), drawn on every face. Recorded in
  `memory-bank/design/candle-arrangement-arc.md` and hard-coded as
  `DOWNWARD_ARC_PARABOLIC_9IN` per the plan in
  `memory-bank/plans/parabolic_arch_layout_plan.md`.

## 10. Pitfalls and Lessons

1. **Infeasible start point.** The arc start was initially `(68.4, 9.525)` —
   0.02 mm outside the corner-based holder fit (its far corner poked out), and
   every derived arc inherited the failure. Check the seed points themselves.
2. **Center-inset margin is wrong near corners.** Use the four-corner holder
   test, not "center at least hw from each edge."
3. **Two notions of "level".** The halachic "same level" rule means height
   above the display surface (satisfied automatically when the die rests on a
   face), not the face-local `y`-coordinate. Conflating them invalidated an
   early analysis.
4. **The 2/3-height endpoint is a trap.** Two candles (one per arc) cannot both
   sit at `y = 102.65` on the 7 in face — the triangle is only ~30 mm wide
   there inside the holder margins, far less than any 1.0+ in spacing. The
   innermost pair is limited to `y ≈ 92.8` at a 1.0 in spacing. Always check
   the *available width at the chosen height*.
5. **DE + additive penalty is unreliable.** The penalty weight must dominate
   the objective, and it often did not; DE returned infeasible or suboptimal
   points. Prefer epigraph + SLSQP + multi-start.
6. **Free endpoints exploit the geometry.** Without a shape constraint, the
   optimizer produces an "arc" that runs along the base first (an L-shape) to
   inflate spacing. Enforce monotonicity (and smoothness) to keep the intended
   family.
7. **"Smooth arc" vs "any monotonic curve" differ.** Report the answer for the
   specific family asked about.
8. **Rounded constants drift below minima.** 3-decimal coordinates round the
   exact optimum; use a small tolerance in assertions.
9. **The optimum is only as good as the constraints.** Sensitivity sweeps are
   how you discover which constraint actually binds (here: along-arc spacing,
   the arc-top pair, and the shamash distance all bound the final design).

## 11. Practical Tips for Applying Effectively

1. **Set up scipy** in a virtualenv (the system Python is PEP-668 managed):
   `python3 -m venv /tmp/kilo/scipy-venv && /tmp/kilo/scipy-venv/bin/pip install scipy numpy`
   and run scripts with `/tmp/kilo/scipy-venv/bin/python`.
2. **Model linearly wherever possible** (holder fit, connector clearance,
   top-zone bound) — it makes SLSQP fast and robust.
3. **Use symmetry** (mirror the right side) to halve variables.
4. **Bounds should match the feasible region** (e.g., `y ∈ [hw, top]`, `x ∈
   [0, half_base]`) to keep starts reasonable.
5. **Generate random feasible starts** by rejection sampling the feasible
   region, not uniform box samples.
6. **Run enough starts** (200–500); keep the best *strictly feasible* result.
7. **Verify independently** after solving: corner-based fit, exact distances,
   and confirm the binding constraints are active.
8. **Do the sensitivity sweep** before finalizing — it reveals the design
   levers and tells you which parameter to change if the current answer is not
   good enough.
9. **Extract and hard-code the optimum** as ground truth for implementation,
   and pin it with unit tests against the design doc.
10. **Record the family, constraints, and numbers in the design doc** so the
    optimized coordinates are reproducible (see
    `memory-bank/design/candle-arrangement-arc.md`).
