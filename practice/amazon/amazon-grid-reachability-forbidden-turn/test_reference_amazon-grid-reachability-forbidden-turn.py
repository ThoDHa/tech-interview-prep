"""Reference-parametrized gauntlet for Grid Reachability with a Forbidden Turn.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Turn-Constrained Breadth-First Search reference against cases_full.json.
Every expectation in cases_full.json is oracle-derived, never
hand-computed and never recorded from this reference: the oracle is a
backtracking enumeration of simple paths through the (cell, heading)
state graph, trying straight and the one allowed turn at every state and
succeeding the moment a walk stands on the destination cell, exactly as
the statement's literal move rule reads. It shares no mechanism with the
reference's visited-table breadth-first search. Per the Testing Strategy
rule for non-outlier problems, the oracle script was scratch and was
deleted after freezing; the comparison is a deterministic boolean, so
plain `==` with no canonicalization.

The gauntlet covers the statement's named corners at eye-auditable
sizes: the page's two examples, the one-cell grid minimum, a
start-equals-destination zero-move case, a single row walked straight in
each direction (straight shot and heading away), a single column under
the same pair, a plus-shaped garage of turns where the destination arm
is reachable only under one forbiddenTurn value, a two-by-three grid
where the top-right corner must be crossed twice under different
headings (the case that punishes dropping the heading from the visited
state), a serpentine corridor needing two same-direction turns and its
left-turn mirror, a ring walked from the start cell and a ring descent
down the far edge, an open three-by-three where the top row traps every
east-headed walk whose only turn faces north, and a two-by-two corner
pair distinguishing the two forbiddenTurn values. Scale corners live
here as constructed cases per the Testing Strategy rule that length
corners are constructible or synthesized, never serialized bulk; all
three build their 500-by-500 grids in this module, derive the expected
outcome from the construction, and confirm the derivation rule on an
oracle-frozen analogue:

- test_constructed_open_500_straight_shot_row_zero: an all-open
  500-by-500 grid walked east along row 0 never needs a turn, so the
  destination at the far end is reached; analogue
  single_row_straight_shot.
- test_constructed_open_500_edge_descent_one_left_turn: heading south
  with left turns allowed, the walker descends the left edge straight to
  row 499, turns left once, and runs straight east to
  (499, 499); analogue edge_descent_left_turn_analogue.
- test_constructed_serpentine_500_two_rows_deep: even rows fully open
  and odd rows open only at column 499, walked with right turns: east
  along row 0, south through the single-column joints, west along
  row 2 to (2, 0); analogue serpentine_two_right_turns.

Discrimination record, naming the mutant classes the serialized and
constructed cases catch, every claim verified by applying the mutant to
the reference and running it against all 24 cases (21 frozen plus three
constructed). Dropping the heading from the visited state is caught by
revisit_cell_new_heading alone: the walk must cross the top-right corner
heading east first, where it dead-ends, and only the later crossing
heading north continues west along the top row to the destination.
Allowing both turns (straight plus left and right, a strict superset
of the legal move set) is caught by exactly the four cases whose
destination is unreachable legally but reachable once the forbidden
turn exists: example_2, plus_shape_left_turn_blocked,
open_grid_trapped_on_top_row, and corner_pair_left_forbidden_false;
every case that already reaches the destination cannot flip, since
extra moves never revoke reachability, and the two heading-away
straight shots stay boxed on their row or column under either turn
set. Requiring the
arrival heading to equal initialHeading is caught by example_1,
plus_shape_right_turn_reaches, plus_shape_north_arm_left_turn,
revisit_cell_new_heading, serpentine_two_right_turns,
serpentine_mirrored_left_turns, ring_right_turn_at_start,
ring_right_edge_descent, open_grid_right_turns_reach,
corner_pair_left_allowed_true, edge_descent_left_turn_analogue,
constructed_open_500_edge_descent_one_left_turn, and
constructed_serpentine_500_two_rows_deep (only the zero-move and
straight-shot arrivals keep their initial heading). Straight-only moves
are caught by example_1, plus_shape_right_turn_reaches,
plus_shape_north_arm_left_turn, revisit_cell_new_heading,
serpentine_two_right_turns, serpentine_mirrored_left_turns,
ring_right_turn_at_start, ring_right_edge_descent,
open_grid_right_turns_reach, corner_pair_left_allowed_true,
edge_descent_left_turn_analogue,
constructed_open_500_edge_descent_one_left_turn, and
constructed_serpentine_500_two_rows_deep. Allowing the reverse move as
a third option is caught by the six unreachable-destination cases
example_2, single_row_heading_away, single_column_heading_away,
plus_shape_left_turn_blocked, open_grid_trapped_on_top_row, and
corner_pair_left_forbidden_false, where backing out of a pocket turns a
correct false into a wrong true. Inclusive bounds (`<=`) crash with an
IndexError on example_1, example_2, single_row_straight_shot,
single_row_heading_away, plus_shape_right_turn_reaches,
plus_shape_left_turn_blocked, plus_shape_north_arm_left_turn,
revisit_cell_new_heading, serpentine_two_right_turns,
serpentine_mirrored_left_turns, ring_right_edge_descent,
open_grid_trapped_on_top_row, open_grid_right_turns_reach,
corner_pair_left_forbidden_false, corner_pair_left_allowed_true,
edge_descent_left_turn_analogue,
constructed_open_500_edge_descent_one_left_turn, and
constructed_serpentine_500_two_rows_deep (the escapes never attempt a
move past an edge before answering). Inverting the blocked-cell check
is caught by example_1, single_row_straight_shot,
single_column_straight_shot, plus_shape_right_turn_reaches,
plus_shape_north_arm_left_turn, revisit_cell_new_heading,
serpentine_two_right_turns, serpentine_mirrored_left_turns,
ring_right_turn_at_start, ring_right_edge_descent,
open_grid_right_turns_reach, corner_pair_left_allowed_true,
edge_descent_left_turn_analogue,
constructed_open_500_straight_shot_row_zero,
constructed_open_500_edge_descent_one_left_turn, and
constructed_serpentine_500_two_rows_deep. Checking the destination only
at enqueue time, so the seed is never tested, is caught by
single_cell_grid and start_equals_destination, the two zero-move cases.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")

GRID_SIZE = 500


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().canReachWithTurnRule, case)


def test_constructed_open_500_straight_shot_row_zero():
    grid = ["0" * GRID_SIZE] * GRID_SIZE
    assert reference.Solution().canReachWithTurnRule(grid, [0, 0], [0, GRID_SIZE - 1], 1, "left") is True


def test_constructed_open_500_edge_descent_one_left_turn():
    grid = ["0" * GRID_SIZE] * GRID_SIZE
    assert reference.Solution().canReachWithTurnRule(grid, [0, 0], [GRID_SIZE - 1, GRID_SIZE - 1], 2, "right") is True


def test_constructed_serpentine_500_two_rows_deep():
    open_row = "0" * GRID_SIZE
    joint_row = "X" * (GRID_SIZE - 1) + "0"
    grid = [open_row if row_index % 2 == 0 else joint_row for row_index in range(GRID_SIZE)]
    assert reference.Solution().canReachWithTurnRule(grid, [0, 0], [2, 0], 1, "left") is True
