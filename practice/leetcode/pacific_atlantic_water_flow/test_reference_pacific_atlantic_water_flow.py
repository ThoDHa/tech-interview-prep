"""Reference-parametrized gauntlet for Pacific Atlantic Water Flow.

The set of both-ocean cells is order-free, so the returned `[row, column]`
pairs are sorted (outer order only; a coordinate pair's row/column order is
meaningful) and compared against the oracle-derived expectation, which is
written sorted in cases_full.json. Any permutation of a correct cell set
passes; a missing, extra, or row/column-swapped cell fails.
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
    _check(reference.Solution().pacificAtlantic, case)
