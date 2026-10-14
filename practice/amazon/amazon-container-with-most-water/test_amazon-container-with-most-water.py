"""Tests for Container With Most Water — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-container-with-most-water.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                1,
                8,
                6,
                2,
                5,
                4,
                8,
                3,
                7,
            ],
        ],
        "expected": 49,
    },
    {
        "id": 'example_2',
        "args": [
            [
                1,
                1,
            ],
        ],
        "expected": 1,
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
        _check(solution.Solution().maxArea, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
