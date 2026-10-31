"""Tests for Lazy Merge of Sorted Event Streams — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/amazon/amazon-lazy-event-stream-merge.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = [
    {
        "id": 'example_1',
        "args": [
            [
                [
                    1,
                    4,
                    4,
                ],
                [
                    1,
                    2,
                    9,
                ],
                [],
                [
                    3,
                ],
            ],
        ],
        "expected": [
            1,
            1,
            2,
            3,
            4,
            4,
            9,
        ],
    },
    {
        "id": 'example_2',
        "args": [
            [
                [],
                [
                    -3,
                    -1,
                ],
                [
                    -3,
                    0,
                ],
            ],
        ],
        "expected": [
            -3,
            -3,
            -1,
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
        _check(solution.Solution().mergeEventStreams, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
