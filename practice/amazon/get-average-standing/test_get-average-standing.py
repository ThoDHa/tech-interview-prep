"""Tests for Get Average Standing — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/get-average-standing.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            3,
            [
                [
                    1,
                    1,
                    100,
                ],
                [
                    1,
                    2,
                    200,
                ],
                [
                    2,
                    1,
                    500,
                ],
            ],
        ],
        "expected": [
            [
                -1,
                -1,
            ],
            [
                1,
                1,
            ],
            [
                2,
                1,
            ],
        ],
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
        _check(solution.Solution().getAverageStanding, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
