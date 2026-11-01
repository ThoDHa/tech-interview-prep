"""Reference-parametrized gauntlet for Connect N Ropes With Minimum Cost.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Min-Heap with heapq reference against cases_full.json. The statement
defines its procedure literally, so the oracle is an independently
coded implementation of that same smallest-first greedy rather than a
different algorithm: a two-queue merge planner (original ropes sorted
once, merged sums drained from a second FIFO queue, two smallest fronts
per round) that shares no mechanism with the reference's heap. Before
freezing, every small and medium expectation was cross-checked against
a second independent implementation (a re-sorting simulation), so each
frozen value carries three agreeing implementations. The gauntlet
covers the statement's named corners: the single-rope zero cost, one
merge for two ropes, all-equal lengths, the ropes[i] boundaries 1 and
10^4, adversarial descending order, randomized shapes, and
100000-rope arrays including the signed-64-bit total corner. The
output is a deterministic integer, so the comparison is plain `==`.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().minimumRopeConnectionCost, case)
