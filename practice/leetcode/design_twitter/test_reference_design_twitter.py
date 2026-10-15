"""Reference-parametrized gauntlet for Design Twitter.

Expectations in cases_full.json come from an independent definition-model
oracle, not from this reference: the oracle stores every post as a
(clock order, author, tweet id) tuple and answers each feed by rescanning
all posts, keeping the author's own tweets plus everyone in the follow set,
sorting newest-first, and truncating to 10. The global clock increments once
per postTweet regardless of user, self-follow is a no-op, and unfollowing a
missing edge is a no-op, so every operation sequence has exactly one
expected result list and `run_operations` compares it per operation.
"""

import pytest

from harness import load_cases, load_solution, run_operations

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


def _check(design_class, case):
    result = run_operations(design_class, case["operations"], case["arguments"])
    assert result == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Twitter, case)
