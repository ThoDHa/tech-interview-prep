"""Reference-parametrized gauntlet for Recent Advertisement Click Counts.

Expectations in cases_full.json come from an independent definition-model
oracle, not from this reference: the oracle keeps each advertisement's
full click history forever and answers every count by scanning the whole
log for timestamps inside the inclusive interval
[timestamp - 60 * kMinutes + 1, timestamp], which is the literal
definition of the window. Every case uses nondecreasing timestamps and
counts only after the constructor, so each count yields exactly one
expected integer and `run_operations` compares the whole expected result
list per operation.
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
    _check(reference.AdClickCounter, case)
