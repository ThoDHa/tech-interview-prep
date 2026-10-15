"""Reference-parametrized gauntlet for Alien Dictionary.

Correctness-property validation, not membership: the validator replays the
input's adjacent word pairs and accepts a returned letter order exactly
when every differing pair is consistent with it, every pair is prefix-
consistent, and the order covers each input letter exactly once. The ""
expectation additionally pins the impossible cases verbatim.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


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


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().solve, case)
