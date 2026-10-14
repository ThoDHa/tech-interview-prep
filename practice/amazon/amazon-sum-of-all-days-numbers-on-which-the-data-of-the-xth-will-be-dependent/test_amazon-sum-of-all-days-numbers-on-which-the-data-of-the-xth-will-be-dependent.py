"""Tests for Sum of All Days Numbers on Which the Data of the Xth Will Be Dependent — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-sum-of-all-days-numbers-on-which-the-data-of-the-xth-will-be-dependent.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            5,
        ],
        "expected": 8,
    },
]

if len(CASES) == 0:
    pytest.skip("no cases parsed", allow_module_level=True)

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", CASES, ids=_ids(CASES))
def test_solution(case):
    try:
        _check(solution.Solution().sumOfAllDaysNumbers, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
