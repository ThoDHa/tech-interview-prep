"""Reference-parametrized gauntlet for LRU Cache for Query Results.

Expectations in cases_full.json come from an independent definition-model
oracle, not from this reference: the oracle pairs a plain dict of values
with a hand-tracked recency list, touching a key on every successful get
and every put (updates included), evicting the front of the list only on
an insertion that exceeds capacity, and returning -1 for misses without
touching recency. Membership, not a sentinel comparison, decides hits
because stored values may be -1. Each get yields exactly one expected
integer and each put yields None, and `run_operations` compares the
whole expected result list per operation.
"""

import pytest

from harness import load_cases, load_solution, run_operations

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


def _check(design_class, case):
    result = run_operations(design_class, case["operations"], case["arguments"])
    assert result == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.LRUCache, case)
