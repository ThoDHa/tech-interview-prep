"""Tests for Longest Repeating Character Replacement — your attempt (solution.py) against cases.json.

The worked approaches live in ../../docs/problems/longest_repeating_character_replacement.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            'XYYX',
            2,
        ],
        "expected": 4,
    },
    {
        "id": 'example_2',
        "args": [
            'AAABABB',
            1,
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
        _check(solution.Solution().characterReplacement, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
