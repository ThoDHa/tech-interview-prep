"""Reference-parametrized gauntlet for Maximize Shipment Order by Sorting One Window.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Painted Agreement Intervals reference against cases_full.json. Every
expectation in cases_full.json is oracle-derived, never hand-computed
and never recorded from this reference: the oracle is the brute-force
window simulation (sort a copy at every start, keep the lexicographically
largest result; the original array is a candidate only when some window
sorts to itself), which shares no mechanism with the reference's descent
and next-smaller precomputations. The scratch oracle script was deleted
after freezing; the output is a deterministic list, so the comparison is
plain `==` with no canonicalization.

The gauntlet covers the statement's named corners at eye-auditable
sizes: the page's example, a single element, a window covering the
whole array, unit windows that can change nothing, a sorted window and
a fully sorted array (both return the original), an all-descending
array where every window hurts, the longest-agreement rule, a tie
preferring the earlier window, a tie producing one result, the final
window's sort winning, a wide window minimizing damage, descents at
both edges, a valley touched from both sides, a peak approached from
both sides, an agreement landing in the second window, a mixed
twelve-value permutation, and an earliest start whose agreement prefix
is strictly longer than the next start's (the case that catches the
smallest-covering-break mutant and the latest-start tie flip). Scale
corners live here as constructed cases per the Testing Strategy rule
that length corners are constructible or synthesized, never serialized
bulk; all four build their inputs in this
module and derive the expected outcome from the construction, with each
derivation rule confirmed against the brute-force oracle at
brute-force-able analogue scales before freezing:

- test_constructed_reverse_hundred_thousand_sorts_last_pair: a fully
  descending permutation of 1..100000 with windowSize 2 has no
  agreement anywhere, so every candidate breaks at its own first
  position and the latest break wins: the final pair [2, 1] sorts and
  every earlier value keeps its place, giving
  `[100000, 99999, ..., 3, 1, 2]`. (The brute-force oracle at
  n = 4 through 8 confirms the latest-start rule for this corner.)
- test_constructed_identity_pair_buried_in_descents: a descending run
  of 100000 values with one adjacent ascent created by a swap has a
  sorted window across that ascent, so the original array is returned
  unchanged.
- test_constructed_full_window_at_hundred_thousand_sorts_everything:
  windowSize equal to the array length leaves one candidate, so the
  evens-then-odds permutation comes back fully sorted.
- test_constructed_unit_windows_at_hundred_thousand_change_nothing:
  windowSize 1 makes every window a sorted singleton, so the original
  permutation is returned unchanged.

Discrimination record, naming the mutant classes the serialized and
constructed cases catch, every claim below verified by applying the
mutant rendering to the reference and running all 22 cases (18 frozen
plus four constructed) against the frozen expectations. Breaking
ranking ties toward the latest start (update on `>=` instead of `>`)
is caught by example_1 and earliest_start_longest_agreement, whose two
starts tie at the same painted break. Defaulting
unpainted breaks to 0 instead of the start's own position is caught by
every_window_hurts, longest_agreement_wins, final_window_sort_wins,
wide_window_minimal_damage, peak_from_both_sides, all_descending_four,
and constructed_reverse_hundred_thousand_sorts_last_pair. Dropping the
sorted-window early-out is caught by
constructed_identity_pair_buried_in_descents alone: on the identity
cases the painted winner stays a sorted window whose sort is the
identity, so the output is unchanged; only the buried-ascent corner
shifts the argmax to a damaged window. Giving every start its smallest
covering break instead of its largest, in either rendering (painting
increasing-k with the skip structure, or decreasing-k with plain
overwrites), is caught by earliest_start_longest_agreement alone: the
earliest start covers two agreement ends while the later start covers
only its own break, so smallest-serving demotes the earliest start
from the tie and the argmax flips to the later window; the other 21
cases leave the argmax unchanged. Relaxing the
next-smaller bound to `next_smaller_right[last_agreed] - width + 1`
(letting an agreement end claim a window position that holds a smaller
value) is caught by final_window_sort_wins and peak_from_both_sides.
Sorting the winning window in descending order is caught by every case
except the six identity returns (single_element,
unit_windows_change_nothing, sorted_window_returns_original,
sorted_array_returns_original,
constructed_identity_pair_buried_in_descents, and
constructed_unit_windows_at_hundred_thousand_change_nothing, whose
expected outputs are the input). Ranking by earliest break instead of
latest is caught by example_1, every_window_hurts,
longest_agreement_wins, tie_prefers_earlier_window,
final_window_sort_wins, wide_window_minimal_damage, valley_two_sides,
peak_from_both_sides, single_agreement_in_second_window,
all_descending_four, mixed_damage_twelve, and
constructed_reverse_hundred_thousand_sorts_last_pair. Scanning starts
only through `count - width` exclusive, dropping the last window from
both the early-out scan and the ranking scan, is caught by
every_window_hurts, longest_agreement_wins, final_window_sort_wins,
wide_window_minimal_damage, peak_from_both_sides,
single_agreement_in_second_window, all_descending_four,
mixed_damage_twelve, and
constructed_reverse_hundred_thousand_sorts_last_pair (the single-window
and identity corners are not caught: with the last window dropped their
remaining candidates still produce the same output).
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")

REVERSE_BOUND = 100000
IDENTITY_DESCENT_COUNT = 100000
FULL_WINDOW_BOUND = 100000
UNIT_WINDOW_BOUND = 100000


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().solve, case)


def test_constructed_reverse_hundred_thousand_sorts_last_pair():
    values = list(range(REVERSE_BOUND, 0, -1))
    expected = list(range(REVERSE_BOUND, 2, -1)) + [1, 2]
    assert reference.Solution().solve(values, 2) == expected


def test_constructed_identity_pair_buried_in_descents():
    values = list(range(IDENTITY_DESCENT_COUNT, 0, -1))
    ascent_position = IDENTITY_DESCENT_COUNT // 2
    values[ascent_position], values[ascent_position + 1] = (
        values[ascent_position + 1],
        values[ascent_position],
    )
    assert reference.Solution().solve(values, 2) == values


def test_constructed_full_window_at_hundred_thousand_sorts_everything():
    values = list(range(2, FULL_WINDOW_BOUND + 1, 2)) + list(
        range(1, FULL_WINDOW_BOUND + 1, 2)
    )
    assert reference.Solution().solve(values, FULL_WINDOW_BOUND) == list(
        range(1, FULL_WINDOW_BOUND + 1)
    )


def test_constructed_unit_windows_at_hundred_thousand_change_nothing():
    values = list(range(2, UNIT_WINDOW_BOUND + 1, 2)) + list(
        range(1, UNIT_WINDOW_BOUND + 1, 2)
    )
    assert reference.Solution().solve(values, 1) == values
