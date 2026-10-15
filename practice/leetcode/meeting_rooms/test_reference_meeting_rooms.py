"""Reference-parametrized gauntlet for Meeting Rooms.

Expectations in cases_full.json come from an independent definition oracle,
not from this reference: the oracle tests every pair of `[start, end)`
intervals for a conflict, which exists exactly when each meeting starts
before the other ends (`a_start < b_end and b_start < a_end`), and stores
the negation as the attendability expectation: a schedule is attendable
exactly when no pair conflicts. Intervals arrive as `[start, end]` pairs in
cases_full.json and are marshalled to the reference's `Interval` objects
here; the boolean expectation is exact.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


def _build_intervals(pairs):
    return [reference.Interval(start, end) for start, end in pairs]


def _check(case):
    schedule = reference.Solution()
    intervals = _build_intervals(case["arguments"][1][0])
    assert schedule.canAttendMeetings(intervals) == case["expected"][1]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(case)
