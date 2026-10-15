"""Reference-parametrized gauntlet for Stack with Constant-Time Middle
Queries.

Expectations in cases_full.json come from an independent definition-model
oracle, not from this reference: the oracle keeps the pushed values in a
plain Python list and answers each query by definition: pop removes and
returns the last value, top reads the last value, and middle reads the
bottom-anchored slot `(len - 1) // 2`, which is the exact center for odd
sizes and the lower middle (closer to the bottom) for even sizes. Empty
stack queries expect None, the harness form of the statement's EMPTY
sentinel. Every pop, top, and middle therefore yields exactly one
expected value or None, and `run_operations` compares the whole expected
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
    _check(reference.MiddleStack, case)
