"""Tests for First Unique Character in a Stream — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-first-unique-character-stream.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            'aabc',
        ],
        "expected": 'a#bb',
    },
    {
        "id": 'example_2',
        "args": [
            'zz',
        ],
        "expected": 'z#',
    },
    {
        "id": 'example_3',
        "args": [
            'abc',
        ],
        "expected": 'aaa',
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
        _check(solution.Solution().firstUniqueAfterEach, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
