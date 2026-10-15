"""Reference-parametrized gauntlet for Detect Squares.

Expectations in cases_full.json come from an independent enumeration
oracle, not from this reference: the oracle stores points as a list and
answers each count by walking every index triple of stored points and
counting the (diagonal, two side corners) assignments that complete an
axis-aligned square with the query point as the fourth corner. Working on
indices makes duplicates count separately, matching the problem's
multiplicity semantics, and the enumeration is deterministic, so
`run_operations` compares the whole expected result list per operation.
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
    _check(reference.CountSquares, case)
