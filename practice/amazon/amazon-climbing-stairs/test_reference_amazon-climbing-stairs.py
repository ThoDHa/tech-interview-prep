"""Reference-parametrized gauntlet for Climbing Stairs.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Space-Optimized Bottom-Up DP reference against cases_full.json. Every
expectation in cases_full.json is oracle-derived, never hand-computed
and never recorded from this reference: the oracle evaluates the
combinatorial closed form, summing C(n - a, a) over a = 0 .. n // 2 (a
climb with `a` two-step moves and `n - 2a` one-step moves arranges `a`
identical doubles among `n - a` moves), which shares no mechanism with
the reference's rolling-pair recurrence. The gauntlet enumerates every
n in the constraint range 1 <= n <= 45, so each named corner is a
boundary value of the enumeration. The output is a deterministic
integer, so the comparison is plain `==` with no canonicalization.
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
    _check(reference.Solution().climbStairs, case)
