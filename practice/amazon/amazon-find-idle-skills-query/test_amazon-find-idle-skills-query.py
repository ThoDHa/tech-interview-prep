"""Tests for Find Idle Skill Query — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-find-idle-skills-query.md.
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
                    3,
                ],
                [
                    2,
                    6,
                ],
                [
                    1,
                    5,
                ],
            ],
            [
                10,
                11,
            ],
            5,
        ],
        "expected": [
            1,
            2,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            6,
            [
                [
                    3,
                    2,
                ],
                [
                    4,
                    3,
                ],
                [
                    2,
                    6,
                ],
                [
                    6,
                    3,
                ],
            ],
            [
                3,
                2,
                6,
            ],
            2,
        ],
        "expected": [
            3,
            5,
            5,
        ],
    },
    {
        "id": 'example_3',
        "args": [
            6,
            [
                [
                    3,
                    2,
                ],
                [
                    4,
                    3,
                ],
                [
                    2,
                    6,
                ],
                [
                    6,
                    3,
                ],
            ],
            [
                1,
                2,
                3,
                4,
                5,
                6,
            ],
            1,
        ],
        "expected": [
            6,
            5,
            3,
            4,
            6,
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
        _check(solution.Solution().getStaleSkillCount, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
