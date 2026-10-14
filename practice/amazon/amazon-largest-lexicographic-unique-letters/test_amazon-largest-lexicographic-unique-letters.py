"""Tests for Remove Duplicate Letters for the Largest Result — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-largest-lexicographic-unique-letters.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            'bcabc',
        ],
        "expected": 'cab',
    },
    {
        "id": 'example_2',
        "args": [
            'cbacdcbc',
        ],
        "expected": 'cbad',
    },
    {
        "id": 'example_3',
        "args": [
            'bbcaac',
        ],
        "expected": 'bca',
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
        _check(solution.Solution().largestUniqueLetters, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
