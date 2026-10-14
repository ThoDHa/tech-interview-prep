"""Tests for Match Strings — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-match-strings.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                'code',
                'coder',
            ],
            [
                'co*d',
                'co*er',
            ],
        ],
        "expected": [
            'NO',
            'YES',
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                'hackerrank',
                'hackerrnak',
            ],
            [
                'hac*rank',
                'hac*rank',
            ],
        ],
        "expected": [
            'YES',
            'NO',
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
        _check(solution.Solution().matchStrings, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
