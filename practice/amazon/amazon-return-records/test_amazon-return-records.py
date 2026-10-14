"""Tests for Return Records — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-return-records.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                'register user05 qwerty',
                'login user05 qwerty',
                'logout user05',
            ],
        ],
        "expected": [
            'Registered Successfully',
            'Logged In Successfully',
            'Logged Out Successfully',
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                'register david david123',
                'register adam 1Adam1',
                'login david david123',
                'login adam 1adam1',
                'logout david',
            ],
        ],
        "expected": [
            'Registered Successfully',
            'Registered Successfully',
            'Logged In Successfully',
            'Login Unsuccessfully',
            'Logged Out Successfully',
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
        _check(solution.Solution().returnRecords, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
