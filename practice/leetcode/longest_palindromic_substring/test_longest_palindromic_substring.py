"""Tests for Longest Palindromic Substring: your attempt (solution.py) against both case sets.

cases.json (marker `simple`) is the "Run" set; cases_full.json (marker `full`) is
the "Submit" gauntlet. The worked approaches live in
../../docs/problems/longest_palindromic_substring.md.
"""

import pytest

from harness import NotSolved, load_cases, load_solution

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    # The longest palindromic substring is not always unique, so we don't compare
    # against a fixed string. The case stores the expected length; a result is valid
    # when it has that length, is itself a palindrome, and is a substring of the input.
    s = case["args"][0]
    result = method(s)
    assert len(result) == case["expected"]
    assert result == result[::-1]
    assert result in s


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(solution.Solution().longestPalindrome, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.Solution().longestPalindrome, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
