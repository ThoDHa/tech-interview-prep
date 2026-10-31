"""Tests for Find Word-Multiset Windows — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-word-multiset-window-search.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                'red',
                'blue',
                'green',
                'blue',
                'red',
            ],
            [
                'blue',
                'red',
            ],
        ],
        "expected": [
            0,
            3,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                'a',
                'a',
                'b',
                'a',
            ],
            [
                'a',
                'a',
            ],
        ],
        "expected": [
            0,
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
        _check(solution.Solution().wordWindowStarts, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
