"""Reference-parametrized gauntlet for Fill One Exact-Length Binary Window.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Prefix Sums reference against cases_full.json. Every expectation in
cases_full.json is oracle-derived, never hand-computed and never
recorded from this reference: the oracle is a naive definition-model
rebuild that constructs the filled string for every candidate window and
counts its ones, which shares no mechanism with the reference's prefix
sums. The output is a deterministic integer, so the comparison is plain
`==` with no canonicalization.

The statement ships no parsed constraint block (the page's placeholder
stands), so the gauntlet fixes the domain the statement's own wording
implies: a nonempty binary string and a window length from 1 through
len(log), the range in which "choose exactly one contiguous substring of
length k" is possible. The cases cover the page's example, all-ones and
all-zeros strings, the window length equal to the string length (the
single-window boundary), k = 1, single-character strings, split zero
runs, a window that swallows an all-ones block, windows forced over
existing ones, the maximum zero run exactly covered, several optimal
windows, and trailing ones left untouched. Two scale corners live here
as constructed cases per the Testing Strategy rule that length corners
are constructible or synthesized, never serialized bulk; both build
their strings in this module and derive every expected outcome from the
construction:

- test_constructed_alternating_string_best_window_holds_one_zero: the
  string alternates 01 for 50000 characters, so every length-2 window
  holds exactly one zero and the total ones is 50000: the answer is
  50001, and the same string at k = 1 answers 50001 as well, one zero
  per window either way.
- test_constructed_half_zero_block_and_half_one_block: 50000 zeros
  followed by 50000 ones, at k = 25000: the best window sits inside the
  zero block and adds 25000 ones to the block's 50000, so the answer is
  75000, pinning that windows need not touch the ones at all.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")

HALF_LENGTH = 50000


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().solve, case)


def test_constructed_alternating_string_best_window_holds_one_zero():
    alternating = "01" * HALF_LENGTH
    assert reference.Solution().solve(alternating, 2) == HALF_LENGTH + 1
    assert reference.Solution().solve(alternating, 1) == HALF_LENGTH + 1


def test_constructed_half_zero_block_and_half_one_block():
    blocked = "0" * HALF_LENGTH + "1" * HALF_LENGTH
    assert reference.Solution().solve(blocked, HALF_LENGTH // 2) == HALF_LENGTH + HALF_LENGTH // 2
