"""Reference-parametrized gauntlet for Maximum Frequency Stack.

Expectations in cases_full.json come from an independent definition-model
oracle, not from this reference: the oracle keeps the literal push
history plus a live frequency map and answers each pop by taking the max
frequency over the map and scanning the stack from the top down for the
first value carrying it, which is the statement's definition (highest
frequency, ties broken toward the most recently pushed). Every case
issues a pop only while the structure is nonempty, so each pop yields
exactly one expected integer and `run_operations` compares the whole
expected result list per operation.
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
    _check(reference.FreqStack, case)
