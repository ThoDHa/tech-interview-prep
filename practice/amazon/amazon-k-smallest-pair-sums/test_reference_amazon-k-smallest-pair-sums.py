"""Reference-parametrized gauntlet for Find K Pairs with Smallest Sums.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Min-Heap Row Merge reference against cases_full.json. Every expectation
in cases_full.json is oracle-derived, never hand-computed and never
recorded from this reference: the oracle is the exhaustive pair
enumeration below, sorting every (sum, i, j) tuple and slicing k, which
shares no mechanism with the reference's k-way heap merge. Per the D3
ruling this oracle stays alive: every run re-derives each expectation
and cross-checks the reference against it. The statement fixes the
output to nondecreasing sums and leaves the order within a sum tie
free; the page pins ascending (i, j) as the tie convention, and oracle
and reference both produce it (tuple sort key, and heap tuple
comparison, respectively), so the comparison is plain `==` with no
canonicalization.

The gauntlet covers the statement's named corners at eye-auditable
sizes: the page's two examples, k = 1, k equal to every pair, single
arrays, duplicated rows and columns, negative values, sums at the
int32 extremes (-2 * 10^9 included), equal sums from two different
rows tying in emitted order, a zero-sum pair, one row spanning all k,
one column, a gap between sums, a mixed-sign tie, k equal to all pairs
with internal ties, near-int32 values without ties, duplicated heads
across four rows, a tail-heavy instance, a zero-headed row, k beyond
the row count (the min(n, k) seed bound), and negative duplicate
heads. Scale corners live here as constructed cases per the Testing
Strategy rule that length corners are constructible or synthesized,
never serialized bulk:

- test_constructed_hundred_thousand_duplicated_rows: 100000 rows of 7
  against 100000 columns of -7, the statement's array-size bounds;
  every pair sums to 0, so k = 100 returns 100 copies of [7, -7].
- test_constructed_wide_column_beyond_head_window: one row against
  100000 ascending columns from -50000 to 49999; the single row offers
  columns in order, so k = 5 returns the five smallest column values.
- test_constructed_seeded_random_agrees_with_oracle: one seeded
  randomized representative (60 by 60 sorted arrays, values in
  [-50, 50], k = 40) cross-checked against the alive oracle's full
  enumeration of its 3600 pairs.

Discrimination record, naming the mutant classes the serialized cases
catch, each claim verified by running the mutant against every case:
a tie broken by column before row (sort and heap key (sum, j, i)) is
caught by all_pairs, int32_extremes, tie_two_rows, zero_sum_pair,
gap_sums, mixed_sign_tie, k_equals_all_with_ties,
alternating_duplicates, and tail_heavy; seeding only row 0 (a
one-stream merge) is caught by example_2, all_pairs, duplicates_left,
negatives, int32_extremes, tie_two_rows, one_column_two_rows,
mixed_sign_tie, k_equals_all_with_ties, big_values_no_tie,
alternating_duplicates, tail_heavy, zero_head_row, k_beyond_row_count,
and negative_duplicate_heads; dropping the next-column push (each row
contributes one pair) is caught by example_1, all_pairs,
duplicates_left, negatives, int32_extremes, tie_two_rows,
zero_sum_pair, one_row_many_columns, gap_sums, mixed_sign_tie,
k_equals_all_with_ties, alternating_duplicates, tail_heavy,
k_beyond_row_count, and negative_duplicate_heads; returning k + 1
pairs is caught by every case; and a row tie broken by descending row
index, applied to the seed and the pushes alike, is caught by
all_pairs, int32_extremes, tie_two_rows, zero_sum_pair, gap_sums,
mixed_sign_tie, k_equals_all_with_ties, alternating_duplicates, and
tail_heavy.
"""

import random

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


class SortedPairEnumeration:
    """The oracle: every index pair enumerated, sorted by (sum, i, j), sliced k."""

    @staticmethod
    def k_smallest_pairs(nums1, nums2, k):
        ranked = sorted(
            (nums1[row] + nums2[column], row, column)
            for row in range(len(nums1))
            for column in range(len(nums2))
        )
        return [[nums1[row], nums2[column]] for _, row, column in ranked[:k]]


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().kSmallestPairs, case)


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_oracle_agrees_with_frozen_expectation(case):
    assert SortedPairEnumeration.k_smallest_pairs(*case["args"]) == case["expected"]


def test_constructed_hundred_thousand_duplicated_rows():
    nums1 = [7] * 100000
    nums2 = [-7] * 100000
    expected = [[7, -7]] * 100
    assert reference.Solution().kSmallestPairs(nums1, nums2, 100) == expected


def test_constructed_wide_column_beyond_head_window():
    nums1 = [5]
    nums2 = list(range(-50000, 50000))
    expected = [[5, -50000], [5, -49999], [5, -49998], [5, -49997], [5, -49996]]
    assert reference.Solution().kSmallestPairs(nums1, nums2, 5) == expected


def test_constructed_seeded_random_agrees_with_oracle():
    generator = random.Random(20261101)
    nums1 = sorted(generator.randint(-50, 50) for _ in range(60))
    nums2 = sorted(generator.randint(-50, 50) for _ in range(60))
    assert (
        reference.Solution().kSmallestPairs(nums1, nums2, 40)
        == SortedPairEnumeration.k_smallest_pairs(nums1, nums2, 40)
    )
