"""Tests for Use Minimum Tokens — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-use-minimum-tokens.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                2,
                4,
                1,
                3,
            ],
            [
                [
                    5,
                    7,
                ],
            ],
        ],
        "expected": [
            2,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                5,
                1,
                1,
                4,
            ],
            [
                [
                    5,
                    7,
                ],
                [
                    4,
                    10,
                ],
                [
                    7,
                    9,
                ],
            ],
        ],
        "expected": [
            1,
            3,
            5,
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
        _check(solution.Solution().useMinimumTokens, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
