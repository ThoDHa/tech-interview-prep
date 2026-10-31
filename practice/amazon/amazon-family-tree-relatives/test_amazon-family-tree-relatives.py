"""Tests for Are Two People Relatives in a Family Tree? — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-family-tree-relatives.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                [
                    'ann',
                    'bob',
                ],
                [
                    'ann',
                    'cat',
                ],
                [
                    'bob',
                    'dan',
                ],
                [
                    'cat',
                    'eve',
                ],
            ],
            'dan',
            'eve',
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
        _check(solution.Solution().solve, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
