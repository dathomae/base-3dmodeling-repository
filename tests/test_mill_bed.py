"""Tests for the scaffold.mill_bed mounting-hole pattern."""

from scaffold.mill_bed import (
    BOTTOM_OFFSET,
    COLUMNS,
    LEFT_OFFSET,
    LOWER_LEFT_Y,
    ROWS,
    X_SPACING,
    Y_SPACING,
    mounting_hole_locations,
)


def test_returns_35_holes():
    """The bed has a 7 × 5 grid: 35 mounting holes."""
    assert len(mounting_hole_locations()) == COLUMNS * ROWS


def test_x_positions_match_seven_columns():
    """Distinct x positions are the 7 columns spaced 41 mm apart from 26 mm."""
    xs = sorted({x for x, _ in mounting_hole_locations()})
    assert xs == [LEFT_OFFSET + X_SPACING * i for i in range(COLUMNS)]


def test_regular_rows_spaced_46_mm():
    """The five regular rows start at 16 mm and step by 46 mm."""
    ys = sorted({y for _, y in mounting_hole_locations()})
    regular_rows = [y for y in ys if y != LOWER_LEFT_Y]
    assert regular_rows == [BOTTOM_OFFSET + Y_SPACING * j for j in range(ROWS)]


def test_lower_left_exception():
    """The lower-left hole is at (26, 38), not (26, 16)."""
    locations = mounting_hole_locations()
    assert (LEFT_OFFSET, LOWER_LEFT_Y) in locations
    assert (LEFT_OFFSET, BOTTOM_OFFSET) not in locations


def test_bottom_row_has_six_holes():
    """The bottom row holds 6 holes (the leftmost was moved up to y=38)."""
    bottom = [(x, y) for x, y in mounting_hole_locations() if y == BOTTOM_OFFSET]
    assert len(bottom) == COLUMNS - 1


def test_exception_is_24_mm_below_second_row():
    """The exception hole is 24 mm below the first hole of the second row."""
    second_row_y = BOTTOM_OFFSET + Y_SPACING
    assert second_row_y - LOWER_LEFT_Y == 24.0
