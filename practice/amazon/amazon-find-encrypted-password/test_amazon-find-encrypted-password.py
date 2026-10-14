"""Tests for Find Encrypted Password — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-find-encrypted-password.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            'babab',
        ],
        "expected": 'abbba',
    },
    {
        "id": 'example_2',
        "args": [
            'yxxy',
        ],
        "expected": 'xyyx',
    },
    {
        "id": 'example_3',
        "args": [
            'ded',
        ],
        "expected": 'ded',
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
        _check(solution.Solution().findEncryptedPassword, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
