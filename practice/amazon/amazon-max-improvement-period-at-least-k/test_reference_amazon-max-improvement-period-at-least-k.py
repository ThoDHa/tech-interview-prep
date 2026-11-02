"""Reference-parametrized gauntlet for Best Improvement Period of at Least K Intervals.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Cheapest Start So Far reference against cases_full.json. Every
expectation in cases_full.json is oracle-derived, never hand-computed
and never recorded from this reference: the oracle enumerates every
qualifying period and scores each directly from the pinned rule (the
first interval's change subtracted, the rest added) through slice sums,
sharing no mechanism with the reference's prefix array and running
minimum. Expectations were frozen from that oracle and the scratch
script deleted; the score is a bare integer, so the comparison is plain
`==` with no canonicalization.

The scoring rule itself is pinned from the page example's explanation,
the only statement authority: the scaffold's formula line and its
constraints block did not survive the parse, and both scores the
explanation computes (10 for [1, 4], 3 for [0, 4]) fix the rule as
-changes[i] + changes[i+1] + ... + changes[j]. The gauntlet covers the
rule's corners at eye-auditable sizes: the page's example, k equal to n
(only the whole array qualifies), k = 1, a single interval, all
positive, all negative with k = 1 and k = 2, a period that gains by
starting on a decline, all zeros, a decline-then-swing, an optimum that
starts on the largest decline, two decline starts, k = n - 1,
monotone rises and falls, a trap where a too-short window would beat
every qualifying one, and period scores at +-10^9 magnitude per
interval. Scale corners live here as constructed cases per the Testing
Strategy rule that length corners are constructible or synthesized,
never serialized bulk; all three derive their expected outcome from the
construction (the scaffold states no constraints, so these sizes are
chosen, not statement-derived):

- test_constructed_hundred_thousand_all_declines: 100000 copies of -1
  with k = 2; a period of length L scores 2 - L, so the best is the
  shortest qualifying period and the answer is 0.
- test_constructed_hundred_thousand_all_gains_k_half: 100000 copies of
  1 with k = 50000; a period scores L - 2, so the whole array wins and
  the answer is 99998.
- test_constructed_giant_decline_then_gains: one decline of -1000000
  followed by 99999 gains of 1 with k = 2; starting on the decline and
  running to the last interval scores 1099999, and starting anywhere
  later is bounded by 99997, so the construction's value stands.

Discrimination record, naming the mutant classes the serialized cases
catch, each claim verified by running the mutant against every case:
dropping the first-interval flip (scoring plain window sums) is caught
by every case except flat_zeros, where both rules score 0; excluding
exactly-length-k windows (admitting starts only at end - k) is caught
by k_equals_n, single_element, all_negative, decline_then_swing,
k_n_minus_one, decreasing, short_period_trap,
large_magnitude_negative_score, large_magnitude_positive_score,
constructed_hundred_thousand_all_declines, and
constructed_hundred_thousand_all_gains_k_half; admitting periods one
shorter than k is caught by k_equals_n, k_one, single_element,
all_positive, all_negative, all_negative_k_two, start_decline_gain,
short_period_trap, large_magnitude_negative_score, and
constructed_hundred_thousand_all_declines; preferring the most
expensive start instead of the cheapest is caught by example_1, k_one,
all_positive, all_negative, start_decline_gain, decline_then_swing,
decline_start_best, two_decline_starts, k_n_minus_one, increasing,
decreasing, short_period_trap,
constructed_hundred_thousand_all_gains_k_half, and
constructed_giant_decline_then_gains; shifting the end term to
prefix[end] is caught by every case except flat_zeros, where both
terms score 0; and admitting each new start one end late (scoring
before the update, which leaves every exactly-length-k window
unscored) is caught by all_negative, all_negative_k_two,
decline_then_swing, k_equals_n, k_n_minus_one,
large_magnitude_negative_score, large_magnitude_positive_score,
short_period_trap, single_element, and
constructed_hundred_thousand_all_declines.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().solve, case)


def test_constructed_hundred_thousand_all_declines():
    assert reference.Solution().solve([-1] * 100000, 2) == 0


def test_constructed_hundred_thousand_all_gains_k_half():
    assert reference.Solution().solve([1] * 100000, 50000) == 99998


def test_constructed_giant_decline_then_gains():
    changes = [-1000000] + [1] * 99999
    assert reference.Solution().solve(changes, 2) == 1099999
