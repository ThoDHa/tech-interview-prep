"""Reference-parametrized gauntlet for Search a Row and Column Sorted Matrix.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Staircase Search from the Top-Right Corner reference against
cases_full.json. Every expectation in cases_full.json is oracle-derived,
never hand-computed and never recorded from this reference: the oracle
is the write-up's rung-one full scan, which shares no mechanism with the
reference's corner elimination (the scan reads every cell, the walk
reads at most m + n - 1). Expectations were frozen from that oracle and
the scratch script deleted; the output is a bare boolean, so the
comparison is plain `==` with no canonicalization.

The gauntlet covers the statement's named corners at eye-auditable
sizes: the page's two examples, single-cell hit and miss, single row
and single column hit and miss, a hit at the -10^9 value floor and at
the 10^9 ceiling, misses in gaps just inside both range ends, an
all-equal matrix hit and miss, duplicates crossing rows, an
anti-row-major instance where the target's flat position defeats a
row-major binary search, row blocks that start below the previous
row's end with a hit and a gap miss, negative interleaved values, and
hits at the bottom-left and top-left corners. Scale corners live here
as constructed cases per the Testing Strategy rule that length corners
are constructible or synthesized, never serialized bulk; all four build
their matrices in this module and derive every expected outcome from
the construction:

- test_constructed_three_hundred_square_anti_row_major: the 300 by 300
  statement bound as matrix[i][j] = i + 1000 * j, whose rows start
  below the previous row's end everywhere; the bottom-right corner's
  own value must be found, the top-left's must be found, and a value
  between row starts (500, unreachable because row indices stop at
  299) must be missed.
- test_constructed_single_row_of_three_hundred: one row of 300 values
  at the column bound; the walk degenerates to a line and must find
  the last value and miss the gap beside it.
- test_constructed_single_column_of_three_hundred: 300 rows of one
  value at the row bound; the walk degenerates the other way.
- test_constructed_all_max_duplicates: 300 by 300 copies of 10^9, the
  duplicate and range-ceiling corners at scale; the value must be
  found and -10^9 missed.

Discrimination record, naming the mutant classes the serialized cases
catch, each claim verified by running the mutant against every case:
inverting both moves (down on too-large, left on too-small) is caught
by example_1, single_row_hit, single_column_hit, value_floor_hit,
value_ceiling_hit, duplicates_across_rows_hit, anti_row_major_hit,
row_blocks_hit, negatives_interleaved, bottom_left_hit, top_left_hit,
constructed_anti_row_major_bottom_right, constructed_anti_row_major_top_left,
and constructed_single_column_bottom; replacing the walk with a flat
row-major binary search is caught by anti_row_major_hit and
bottom_left_hit (the constructed 300-square survives it: a flat
row-major binary search still finds its bottom-right and top-left
values and still misses 500); seeding the walk at row 1
(skipping the first row) is caught by single_cell_hit, single_row_hit,
value_floor_hit, top_left_hit, constructed_anti_row_major_top_left,
and constructed_single_row_bottom; seeding the walk at column
len(matrix[0]) crashes on every case (IndexError before any
comparison); dropping the column >= 0 half of the walk condition walks
off the left edge through negative indices and is caught by
single_cell_miss, single_column_miss, value_floor_gap_miss,
duplicates_across_rows_miss, row_blocks_miss, and
constructed_all_max_miss; and advancing both down and left when the
candidate is too small is caught by example_1, single_column_hit,
value_ceiling_hit, anti_row_major_hit, negatives_interleaved,
bottom_left_hit, constructed_anti_row_major_bottom_right, and
constructed_single_column_bottom.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")

VALUE_CEILING = 1000000000
VALUE_FLOOR = -1000000000
SIDE_BOUND = 300


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().searchMatrix, case)


def test_constructed_three_hundred_square_anti_row_major():
    grid = [[row_index + 1000 * column_index for column_index in range(SIDE_BOUND)] for row_index in range(SIDE_BOUND)]
    assert reference.Solution().searchMatrix(grid, grid[SIDE_BOUND - 1][SIDE_BOUND - 1]) is True
    assert reference.Solution().searchMatrix(grid, grid[0][0]) is True
    assert reference.Solution().searchMatrix(grid, 500) is False


def test_constructed_single_row_of_three_hundred():
    single_row = [list(range(0, 300000, 1000))]
    assert reference.Solution().searchMatrix(single_row, 299000) is True
    assert reference.Solution().searchMatrix(single_row, 299001) is False


def test_constructed_single_column_of_three_hundred():
    single_column = [[row_index] for row_index in range(SIDE_BOUND)]
    assert reference.Solution().searchMatrix(single_column, 299) is True
    assert reference.Solution().searchMatrix(single_column, 300) is False


def test_constructed_all_max_duplicates():
    max_grid = [[VALUE_CEILING] * SIDE_BOUND for _ in range(SIDE_BOUND)]
    assert reference.Solution().searchMatrix(max_grid, VALUE_CEILING) is True
    assert reference.Solution().searchMatrix(max_grid, VALUE_FLOOR) is False
