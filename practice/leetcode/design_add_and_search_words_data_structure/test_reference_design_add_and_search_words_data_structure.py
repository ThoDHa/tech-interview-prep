"""Reference-parametrized gauntlet for Design Add And Search Words Data Structure.

Expectations in cases_full.json come from an independent definition-model
oracle, not from this reference: the oracle keeps a plain list of stored
words and answers each search by scanning every stored word, requiring
equal length and position-wise agreement where the query letter is not the
wildcard `.`. That first-match scan is deterministic, so
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
    _check(reference.WordDictionary, case)
