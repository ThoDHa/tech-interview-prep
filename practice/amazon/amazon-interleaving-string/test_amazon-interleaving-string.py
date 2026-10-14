"""Tests for Interleaving String — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-interleaving-string.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            'aabcc',
            'dbbca',
            'aadbbcbcac',
        ],
        "expected": True,
    },
    {
        "id": 'example_2',
        "args": [
            'aabcc',
            'dbbca',
            'aadbbbaccc',
        ],
        "expected": False,
    },
    {
        "id": 'example_3',
        "args": [
            '',
            '',
            '',
        ],
        "expected": True,
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
        _check(solution.Solution().isInterleave, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
