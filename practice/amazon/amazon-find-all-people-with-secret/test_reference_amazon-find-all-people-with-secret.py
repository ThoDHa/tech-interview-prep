"""Reference-parametrized gauntlet for Find All People with the Secret.

The statement requires the answer sorted in ascending order, so the
comparison is plain `==` with no canonicalization; the frozen
expectations are written in that order. Every expectation in
cases_full.json is oracle-derived, never hand-computed and never
recorded from this reference: the oracle is a timestamp-swept fixpoint
simulation per the statement's definition (process each distinct time
in increasing order; within a time, sweep that time's meetings until a
full pass teaches nobody, so instantaneous sharing is independent of
input order), which shares no mechanism with the reference's per-time
BFS over a built adjacency. The band covers the statement's named
corners: the minimum population with and without meetings, meetings
among non-holders, whole chains spreading inside one timestamp (in
sorted and unsorted input order), backward-time immunity, repeated
pairs that only connect once a holder arrives, duplicate rows, star
bursts, disconnected components, the time bounds 1 and 10^9, a high
firstPerson label, and a seeded random band of small unsorted meeting
lists. The statement's scale corners (n = 10^5, m = 10^5) stay out of
the JSON and are constructed here, where the expectations follow from
the construction:

- test_constructed_meeting_chain_of_100000_spreads_to_everyone: people
  i and i + 1 meet at time i + 1 for i in 0..99998, a rising-time
  chain off person 0. Each meeting hands the secret to exactly one new
  person, so every label 0..99999 ends up a holder and the expected
  answer is the full ascending range.
- test_constructed_blocked_meetings_leave_the_initial_holders: 100000
  meetings shuffled among people 2..99999 at rising times, never
  touching person 0 or firstPerson 1. No meeting ever has a holder, so
  the answer stays [0, 1].
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")

SCALE_POPULATION = 100_000


def _ids(cases):
    return [case["id"] for case in cases]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().findAllPeople, case)


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


def test_constructed_meeting_chain_of_100000_spreads_to_everyone():
    population = SCALE_POPULATION
    meetings = [[person, person + 1, person + 1] for person in range(population - 1)]
    assert len(meetings) == SCALE_POPULATION - 1
    assert reference.Solution().findAllPeople(population, meetings, 1) == list(range(population))


def test_constructed_blocked_meetings_leave_the_initial_holders():
    population = SCALE_POPULATION
    meetings = [
        [2 + (index % (population - 2)), 2 + ((index * 7 + 3) % (population - 2)), index + 1]
        for index in range(population)
    ]
    meetings = [[x, y, t] if x != y else [y, (y + 1) % (population - 2) + 2, t] for x, y, t in meetings]
    assert reference.Solution().findAllPeople(population, meetings, 1) == [0, 1]
