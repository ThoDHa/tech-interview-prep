"""Reference-parametrized gauntlet for Tallest Billboard.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Bottom-Up Difference DP reference against cases_full.json. Every
expectation in cases_full.json is oracle-derived, never hand-computed
and never recorded from this reference: the oracle is the exhaustive
assignment enumeration below, walking every rod's three roles (left,
right, unused) as a two-half meet in the middle so the statement's
20-rod bound stays affordable, and it shares no mechanism with the
reference's difference DP. Per the D3 ruling this oracle stays alive:
every run re-derives each expectation and cross-checks the reference
against it. The output is a deterministic integer, so the comparison is
plain `==` with no canonicalization.

The gauntlet covers the statement's named corners at eye-auditable
sizes: the page's two examples, a single rod, an equal pair, a three-rod
build, duplicated rods, an odd total that still levels, unused rods
beside a pair, a big rod swallowed by a swap, two distinct assignments
tying on the optimum, rod lengths at the 1000 bound, four and five rods
at the 1000 bound, a mixed instance, unit rods, a 999/1000/1 triple, an
instance with no positive split, the reversed example order, a pair
beside an unusable odd rod, a twelve-rod mixed instance, and a tall rod
among eleven lights. Scale corners live here as constructed cases per
the Testing Strategy rule that length corners are constructible or
synthesized, never serialized bulk; all three build their rod lists in
this module and are cross-checked by the alive oracle at full size:

- test_constructed_twenty_unit_rods_level_at_ten: 20 unit rods, the
  statement's count bound: ten per side, level at 10.
- test_constructed_twenty_rods_at_total_bound: 20 rods of 250, the
  statement's total-length bound of 5000: ten per side, level at 2500.
- test_constructed_twenty_mixed_rods_use_ten_of_twenty: ten rods of 1
  and ten of 499 (total 5000): five 499s plus five 1s per side levels
  at 2500, using only ten of the twenty rods.

Discrimination record, naming the mutant classes the serialized cases
catch, each claim verified by running the mutant against every case:
a shorter-side write of `shorter + rod` instead of
`shorter + min(difference, rod)` (overpaying a swap) is caught by
every positive-answer case, from example_1 through
tall_single_among_lights, and by all three constructed corners; a
taller-side write of `shorter + rod` instead of `shorter` is caught by
the same span (the two mutants survive only example_2, single_rod,
primes_never_level, and no_split_possible, whose optima build without
stacking onto an occupied side); dropping the skip transition (every
rod must be placed) is caught by example_2, single_rod,
primes_never_level, odd_total_still_levels, unused_rods, two_ways_tie,
five_at_total_bound, no_split_possible, gap_after_exact, and
tall_single_among_lights; reading the answer from
`best_shorter[total]` instead of `best_shorter[0]` is caught by every
positive-answer case; initializing unreachable differences to `0`
instead of the `-1` sentinel (phantom empty supports) is caught by
example_1, example_2, three_builds, quadruple_duplicates,
primes_never_level, odd_total_still_levels, unused_rods,
swap_makes_pair, two_ways_tie, four_big, five_at_total_bound,
mixed_uneven, unit_rods_even, no_split_possible, reversed_example,
gap_after_exact, twelve_mixed, tall_single_among_lights, and all three
constructed corners; and dropping the `shorter < 0` guard so the
sentinel propagates into writes is caught by example_1,
quadruple_duplicates, primes_never_level, unused_rods,
swap_makes_pair, two_ways_tie, four_big, five_at_total_bound,
mixed_uneven, unit_rods_even, no_split_possible, reversed_example,
gap_after_exact, twelve_mixed, tall_single_among_lights, and all three
constructed corners.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


class AssignmentEnumeration:
    """The oracle: exhaustive role enumeration via two-half meet in the middle.

    Each half's every (left_sum, right_sum) outcome is enumerated exactly,
    keeping the tallest left_sum per difference; a full assignment levels
    when the halves' differences cancel, and its common sum is the two
    left sums added. Exact over all 3**len(rods) outcomes.
    """

    @staticmethod
    def _half_table(rods):
        states = [(0, 0)]
        for rod in rods:
            next_states = []
            for left_sum, right_sum in states:
                next_states.append((left_sum, right_sum))
                next_states.append((left_sum + rod, right_sum))
                next_states.append((left_sum, right_sum + rod))
            states = next_states
        best_left = {}
        for left_sum, right_sum in states:
            difference = left_sum - right_sum
            if left_sum > best_left.get(difference, -1):
                best_left[difference] = left_sum
        return best_left

    @classmethod
    def tallest_level(cls, rods):
        first = cls._half_table(rods[: len(rods) // 2])
        second = cls._half_table(rods[len(rods) // 2 :])
        best = 0
        for difference, left_sum in second.items():
            partner = first.get(-difference)
            if partner is not None and partner + left_sum > best:
                best = partner + left_sum
        return best


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().tallestBillboard, case)


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_oracle_agrees_with_frozen_expectation(case):
    assert AssignmentEnumeration.tallest_level(*case["args"]) == case["expected"]


def test_constructed_twenty_unit_rods_level_at_ten():
    rods = [1] * 20
    expected = 10
    assert reference.Solution().tallestBillboard(rods) == expected
    assert AssignmentEnumeration.tallest_level(rods) == expected


def test_constructed_twenty_rods_at_total_bound():
    rods = [250] * 20
    expected = 2500
    assert reference.Solution().tallestBillboard(rods) == expected
    assert AssignmentEnumeration.tallest_level(rods) == expected


def test_constructed_twenty_mixed_rods_use_ten_of_twenty():
    rods = [1] * 10 + [499] * 10
    expected = 2500
    assert reference.Solution().tallestBillboard(rods) == expected
    assert AssignmentEnumeration.tallest_level(rods) == expected
