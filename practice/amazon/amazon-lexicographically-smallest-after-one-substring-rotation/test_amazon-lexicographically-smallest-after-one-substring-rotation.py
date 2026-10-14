"""Tests for Lexicographically Smallest After One Substring Rotation — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-lexicographically-smallest-after-one-substring-rotation.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            'baca',
        ],
        "expected": 'abac',
    },
    {
        "id": 'example_2',
        "args": [
            'cba',
        ],
        "expected": 'acb',
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
        _check(solution.Solution().smallestStringAfterOneRotation, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
