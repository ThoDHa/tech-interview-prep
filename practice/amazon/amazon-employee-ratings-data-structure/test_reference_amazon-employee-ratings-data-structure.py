"""Reference-parametrized gauntlet for Employee Ratings Management System.

Expectations in cases_full.json come from an independent definition-model
oracle, not from this reference: the oracle keeps the ratings in a plain
Python list, appending on append, popping the current index on delete
(shifting later indices left), and answering each query with
`max(ratings)` paired with `ratings.index(max_rating)`, whose first-match
semantics is exactly the earliest current index the statement requests.
Every case issues a query only while at least one rating exists and uses
valid deletion indices, so each query yields exactly one expected
[maxRating, index] row and `run_operations` compares the whole expected
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
    _check(reference.EmployeeRatings, case)
