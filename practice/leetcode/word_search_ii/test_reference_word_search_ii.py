"""Reference-parametrized gauntlet for Word Search II.

The set of found words is order-free, so both sides are compared as
canonicalized lists: the oracle-derived expectation is written sorted in
cases_full.json, and the returned word list is sorted before the
comparison, so any permutation of a correct answer set passes and any
missing, extra, or duplicated word fails.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert sorted(method(*case["args"])) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().findWords, case)
