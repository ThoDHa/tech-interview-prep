"""Reference-parametrized gauntlet for Dynamic Kth Largest Queries.

Expectations in cases_full.json come from an independent definition-model
oracle, not from this reference: the oracle keeps the whole multiset of
values (initial plus inserted) and answers each find by sorting ascending
and indexing from the top (`ascending[-k]`), which is the direct
definition of the kth largest. Every case keeps the multiset at or above
`k` elements before each find, so each find yields exactly one expected
integer and `run_operations` compares the whole expected result list per
operation.
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
    _check(reference.DynamicKthLargest, case)
