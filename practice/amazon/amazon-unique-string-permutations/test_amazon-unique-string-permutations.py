"""Tests for Unique String Permutations — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-unique-string-permutations.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            'aab',
        ],
        "expected": [
            'aab',
            'aba',
            'baa',
        ],
    },
    {
        "id": 'example_2',
        "args": [
            'xxyy',
        ],
        "expected": [
            'xxyy',
            'xyxy',
            'xyyx',
            'yxxy',
            'yxyx',
            'yyxx',
        ],
    },
    {
        "id": 'example_3',
        "args": [
            'z',
        ],
        "expected": [
            'z',
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
        _check(solution.Solution().uniquePermutations, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
