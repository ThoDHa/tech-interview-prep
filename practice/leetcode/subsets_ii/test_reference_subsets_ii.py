"""Reference-parametrized gauntlet for Subsets II.

Any-order output is compared with full canonicalized-set equality on both
sides (sorted(map(sorted, ...)), the pin for the six set problems): the
oracle-derived expectation is written canonicalized in cases_full.json, and
the returned subset list is canonicalized the same way before the
comparison, so subset order and value order within a subset are both free.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


def _canonical(subsets):
    return sorted(sorted(subset) for subset in subsets)


def _check(method, case):
    assert _canonical(method(*case["args"])) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().subsetsWithDup, case)
