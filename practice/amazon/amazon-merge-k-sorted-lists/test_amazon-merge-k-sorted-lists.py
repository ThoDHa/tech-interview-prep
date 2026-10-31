"""Tests for Merge k Sorted Lists — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-merge-k-sorted-lists.md.
"""

import pytest

from harness import NotSolved, build_linked_list, linked_list_to_list, load_cases, load_solution

CASES = load_cases(__file__, "cases.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    heads = [build_linked_list(values) for values in case["args"][0]]
    assert linked_list_to_list(method(heads)) == case["expected"]


@pytest.mark.parametrize("case", CASES, ids=_ids(CASES))
def test_solution(case):
    try:
        _check(solution.Solution().mergeKLists, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
