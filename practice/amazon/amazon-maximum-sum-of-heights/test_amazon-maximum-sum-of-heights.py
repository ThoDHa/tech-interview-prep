"""Tests for Maximum Sum of Heights — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-maximum-sum-of-heights.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                5,
                3,
                4,
                1,
                1,
            ],
        ],
        "expected": 13,
    },
    {
        "id": 'example_2',
        "args": [
            [
                6,
                5,
                3,
                9,
                2,
                7,
            ],
        ],
        "expected": 22,
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
        _check(solution.Solution().maximumSumOfHeights, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
