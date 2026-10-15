"""Reference-parametrized gauntlet for Dynamic Prefix Search Collection.

Expectations in cases_full.json come from an independent definition-model
oracle, not from this reference: the oracle keeps the words in a set,
answers each search by filtering the whole collection through
`word.startswith(prefix)`, sorting the matches, and slicing the first
three, which is the literal definition of the request (duplicates are
free because a set add is idempotent). Every case issues at least one
search, so each search yields exactly one expected row and
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
    _check(reference.PrefixSearchCollection, case)
