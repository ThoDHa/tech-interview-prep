"""Tests for LRU Cache for Query Results — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-lru-query-result-cache.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = []

if len(CASES) == 0:
    pytest.skip("design-operation example for amazon-lru-query-result-cache is not `==`-assertable", allow_module_level=True)

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", CASES, ids=_ids(CASES))
def test_solution(case):
    try:
        _check(solution.Solution().runQueryCache, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
