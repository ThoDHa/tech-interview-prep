"""Tests for Alien Dictionary: your attempt (solution.py) against both case sets.

The worked approaches live in ../../../docs/leetcode/alien_dictionary.md.
"""

import pytest

from harness import NotSolved, load_cases, load_solution

SIMPLE = load_cases(__file__, "cases.json")
FULL = SIMPLE + load_cases(__file__, "cases_full.json")

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _pair_ordered(first, second, place):
    for first_letter, second_letter in zip(first, second):
        if first_letter != second_letter:
            return place[first_letter] < place[second_letter]
    return len(first) <= len(second)


def _is_valid_order(order, words):
    letters = {letter for word in words for letter in word}
    if len(order) != len(letters) or set(order) != letters:
        return False
    place = {letter: position for position, letter in enumerate(order)}
    return all(
        _pair_ordered(first, second, place) for first, second in zip(words, words[1:])
    )


def _check(method, case):
    order = method(*case["args"])
    if case["expected"] == "":
        assert order == ""
    else:
        assert order != "" and _is_valid_order(order, case["args"][0])


@pytest.mark.simple
@pytest.mark.parametrize("case", SIMPLE, ids=_ids(SIMPLE))
def test_solution_simple(case):
    try:
        _check(solution.Solution().solve, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")


@pytest.mark.full
@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_solution_full(case):
    try:
        _check(solution.Solution().solve, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
