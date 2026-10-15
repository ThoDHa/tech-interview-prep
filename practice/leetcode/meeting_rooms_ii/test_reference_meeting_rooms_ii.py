"""Reference-parametrized gauntlet for Meeting Rooms II.

Expectations in cases_full.json come from an independent definition oracle,
not from this reference: the oracle measures the deepest simultaneous
occupancy directly, counting for every meeting start how many
`[start, end)` intervals cover that instant and taking the maximum, which
is the minimum room count by definition. Intervals arrive as
`[start, end]` pairs in cases_full.json and are marshalled to the
reference's `Interval` objects here; the integer expectation is exact.
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
    scheduler = reference.Solution()
    intervals = _build_intervals(case["arguments"][1][0])
    assert scheduler.minMeetingRooms(intervals) == case["expected"][1]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(case)
