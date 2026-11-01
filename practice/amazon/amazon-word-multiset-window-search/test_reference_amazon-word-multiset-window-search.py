"""Reference-parametrized gauntlet for Find Word-Multiset Windows.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Match-Count Sliding Window reference against cases_full.json. Every
expectation in cases_full.json is oracle-derived, never hand-computed
and never recorded from this reference: the oracle is a naive
definition-model scan that sorts each candidate window and the target
and compares the sorted lists, which shares no mechanism with the
reference's count maps and mismatch tally. The output is
statement-ordered (ascending start indices), so the comparison is
plain `==` with no canonicalization.

The gauntlet covers the statement's named corners at eye-auditable
sizes: the page's two examples, the target equal to the whole text in
order and reordered, a single-word target, a target whose multiset
never appears, duplicate multiplicity inside the window, case
sensitivity, a match at the last window, matches at every position,
sparse matches, order-free windows against a reordered target,
forty-character words at the statement's word-length bound, a
high-multiplicity shift where the only match is one slot late, and
empty results. Two scale corners live here as constructed cases per the
Testing Strategy rule that length corners are constructible or
synthesized, never serialized bulk; both build their inputs in this
module and derive every expected outcome from the construction:

- test_constructed_hundred_thousand_text_isolated_tail_match: the text
  alternates [x, y] for 99998 words and ends with [x, x] (100000 words,
  the statement's text-length upper bound); the alternating prefix never
  holds two equal neighbors, so the target [x, x] matches exactly the
  final window and the expected list is [99998].
- test_constructed_hundred_thousand_alternating_text_brackets_both_ends:
  the pure alternating text (100000 words) against the target [x, x]
  can never match, so the answer is [], while the same text against the
  target [x, y] matches at every one of its 99999 windows (each is a
  rotation of the period, and multiset equality is order-free); the
  expected list is range(99999).
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")

PERIOD = ["x", "y"]
PERIOD_REPEATS = 50000


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().wordWindowStarts, case)


def test_constructed_hundred_thousand_text_isolated_tail_match():
    text = PERIOD * (PERIOD_REPEATS - 1) + ["x", "x"]
    assert reference.Solution().wordWindowStarts(text, ["x", "x"]) == [99998]


def test_constructed_hundred_thousand_alternating_text_brackets_both_ends():
    text = PERIOD * PERIOD_REPEATS
    assert reference.Solution().wordWindowStarts(text, ["x", "x"]) == []
    assert reference.Solution().wordWindowStarts(text, ["x", "y"]) == list(range(99999))
