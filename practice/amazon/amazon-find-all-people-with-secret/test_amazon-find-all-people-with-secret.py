"""Tests for Find All People with the Secret — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-find-all-people-with-secret.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            6,
            [
                [
                    2,
                    3,
                    5,
                ],
                [
                    1,
                    2,
                    5,
                ],
                [
                    4,
                    5,
                    6,
                ],
            ],
            1,
        ],
        "expected": [
            0,
            1,
            2,
            3,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            5,
            [
                [
                    2,
                    3,
                    1,
                ],
                [
                    1,
                    2,
                    2,
                ],
                [
                    3,
                    4,
                    3,
                ],
            ],
            1,
        ],
        "expected": [
            0,
            1,
            2,
        ],
    },
    {
        "id": 'example_3',
        "args": [
            4,
            [],
            3,
        ],
        "expected": [
            0,
            3,
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
        _check(solution.Solution().findAllPeople, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
