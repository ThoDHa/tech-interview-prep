"""Tests for Get Max Programs — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-get-max-programs.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                5,
                2,
                1,
                4,
                2,
            ],
            2,
            6,
        ],
        "expected": 4,
    },
    {
        "id": 'example_2',
        "args": [
            [
                4,
                2,
                3,
                4,
                1,
            ],
            1,
            4,
        ],
        "expected": 1,
    },
    {
        "id": 'example_3',
        "args": [
            [
                1,
                2,
                3,
                1,
                1,
            ],
            3,
            3,
        ],
        "expected": 5,
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
        _check(solution.Solution().getMaxPrograms, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
