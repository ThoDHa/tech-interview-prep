"""Tests for Encode and Decode Strings — your attempt (solution.py) against cases.json.

The worked approaches live in ../../docs/problems/encode_and_decode_strings.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = []

if len(CASES) == 0:
    pytest.skip("multi-method starter (encode, decode) is not a single `==`-assertable call for encode_and_decode_strings", allow_module_level=True)

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
