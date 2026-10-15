"""Reference-parametrized gauntlet for Find Median from Data Stream.

Expectations in cases_full.json come from an independent definition-model
oracle, not from this reference: the oracle keeps the whole multiset of
added values and answers each median query by sorting ascending and
reading the middle (float of the sole middle element for odd counts, the
arithmetic mean of the two middle values divided by 2.0 for even counts),
which is the direct definition of the median. Every case keeps at least
one value stored before each median query, so every query yields exactly
one expected float and `run_operations` compares the whole expected
result list per operation.
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
    _check(reference.MedianFinder, case)
