"""Reference-parametrized gauntlet for Minimum Cost of Left and Right Propagation.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Kept-Run Greedy reference against cases_full.json. Every expectation in
cases_full.json is oracle-derived, never hand-computed and never
recorded from this reference: the oracle is Dijkstra over operation
sequences exactly as the statement quantifies them (either propagation
at any index, any order, any number of times, first uniform state at
minimum cost, reachable states being constant-prefix / untouched-core /
constant-suffix shapes). It shares no mechanism with the reference's
maximal-run scan. Per the Testing Strategy rule for non-outlier
problems, the oracle script was scratch and was deleted after freezing;
the comparison is a deterministic integer, so plain `==` with no
canonicalization.

The gauntlet covers the statement's named corners at eye-auditable
sizes: the page's three examples, a single element, an already-uniform
array, equal and unequal pairs, a descending pair, a cheap middle, an
expensive middle, a long cheap run in the middle, runs at both ends,
four distinct values, an alternating array, a single peak, a single
valley, an expensive dominant value, runs touching each edge, values at
the 10^9 bound, and a twelve-value mix. Scale corners live here as
constructed cases per the Testing Strategy rule that length corners are
constructible or synthesized, never serialized bulk; all four build
their arrays in this module and derive the expected outcome from the
construction, with each derivation rule confirmed against the oracle on
a brute-force-able analogue before freezing:

- test_constructed_uniform_hundred_thousand_costs_nothing: 100000
  copies of one value are already uniform, the zero-operation rule;
  analogue [7, 7, 7, 7, 7] scores 0.
- test_constructed_two_value_edges_flatten_for_two: `[5] + [1] * 99998
  + [5]` keeps the middle 1-run and flattens one element on each side,
  cost `(1 + 1) * 1 = 2`; analogue [9, 1, 1, 9] scores 2.
- test_constructed_long_right_run_flattens_left_edge_for_one:
  `[2] + [1] * 99999` keeps the trailing 1-run and propagates it left
  across the leading 2, cost `1 * 1 = 1`; analogue [9, 1] scores 1.
- test_constructed_bound_value_pair_flattens_for_one: `[10**9] +
  [1] * 99999` keeps the trailing 1-run, cost `1 * 1 = 1`; analogue
  [10**9, 1] scores 1.

Discrimination record, naming the mutant classes the serialized and
constructed cases catch, every claim verified by applying the mutant
rendering to the reference and running it against all 25 cases
(21 frozen plus four constructed). Scoring a run by its length
(`(right - left + 1) * value`, rewarding long runs instead of charging
for the flattened sides) is caught by example_1, example_2, example_3,
single_element, already_uniform, two_elements_equal, cheap_middle,
expensive_middle, runs_at_both_ends, all_distinct_four,
alternating_small, single_peak, single_valley,
dominant_expensive_value, kept_run_touches_left_edge,
kept_run_touches_right_edge, big_value_corner, twelve_mixed,
constructed_uniform_100000, constructed_two_value_edges,
constructed_long_right_run, and constructed_bound_value_pair (only the
unequal pairs escape: one element each side scores the length either
way). Charging only the left width (`left * value`) is caught by
example_1, example_2, example_3, two_elements_unequal, descending_pair,
cheap_middle, expensive_middle, long_cheap_run_middle,
runs_at_both_ends, all_distinct_four, alternating_small, single_peak,
single_valley, dominant_expensive_value, kept_run_touches_left_edge,
kept_run_touches_right_edge, big_value_corner, twelve_mixed,
constructed_two_value_edges, constructed_long_right_run, and
constructed_bound_value_pair (kept_run_touches_left_edge is caught
through its other runs; only right-edge runs pay nothing on that
side). Charging only the right width (`(count - 1 - right) * value`)
catches the same 21 cases by symmetry. Returning the first run's cost
instead of the minimum is caught by example_1, example_3,
descending_pair, cheap_middle, long_cheap_run_middle,
all_distinct_four, single_valley, dominant_expensive_value,
big_value_corner, twelve_mixed, constructed_two_value_edges,
constructed_long_right_run, and constructed_bound_value_pair (uniform
inputs, example_2, two_elements_unequal, alternating_small,
single_peak, kept_run_touches_left_edge, and
constructed_uniform_100000 have their first run optimal or no cheaper
run). Widening the charge by one (`left + count - right`) is caught by
all 25 cases, uniform inputs included, because even a full-width run
then scores its own value instead of the zero-operation answer.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")

UNIFORM_BOUND = 100000
TWO_VALUE_EDGES_BOUND = 100000
LONG_RIGHT_RUN_BOUND = 100000
BOUND_VALUE_PAIR_BOUND = 100000


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().minimumPropagationCost, case)


def test_constructed_uniform_hundred_thousand_costs_nothing():
    values = [7] * UNIFORM_BOUND
    assert reference.Solution().minimumPropagationCost(values) == 0


def test_constructed_two_value_edges_flatten_for_two():
    values = [5] + [1] * (TWO_VALUE_EDGES_BOUND - 2) + [5]
    assert reference.Solution().minimumPropagationCost(values) == 2


def test_constructed_long_right_run_flattens_left_edge_for_one():
    values = [2] + [1] * (LONG_RIGHT_RUN_BOUND - 1)
    assert reference.Solution().minimumPropagationCost(values) == 1


def test_constructed_bound_value_pair_flattens_for_one():
    values = [10**9] + [1] * (BOUND_VALUE_PAIR_BOUND - 1)
    assert reference.Solution().minimumPropagationCost(values) == 1
