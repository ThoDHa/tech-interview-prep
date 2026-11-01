"""Reference-parametrized gauntlet for Longest Equal-Value Run.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Single-Pass Run Counter reference against cases_full.json. Every
expectation in cases_full.json is oracle-derived, never hand-computed
and never recorded from this reference: the oracle enumerates run
boundaries (indices whose value differs from their predecessor), takes
the longest stretch between consecutive boundaries and the array ends,
and shares no mechanism with the reference's rolling counter. The
statement parses with no constraints block, so the gauntlet covers the
corner shapes its statement and example name: single element, one run
spanning the whole array, all-distinct (every run length 1), runs at
the start, middle, and end, ties for the maximum, non-adjacent repeats
of one value across separate runs, signed extreme magnitudes,
randomized arrays, and two 100000-element arrays (one random, one all
equal). Arrays are non-empty by assumption, and the output is a
deterministic integer, so the comparison is plain `==`.
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
    _check(reference.Solution().solve, case)
