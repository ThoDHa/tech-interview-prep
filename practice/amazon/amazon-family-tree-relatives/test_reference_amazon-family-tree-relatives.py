"""Reference-parametrized gauntlet for Family Tree Relatives.

Every expectation in cases_full.json is oracle-derived, never
hand-computed and never recorded from this reference: the oracle
computes both people's full ancestor closures recursively with
memoization (each person counting as their own ancestor, exactly as
the statement defines relatives) and tests the closures for a
non-empty intersection, which shares no mechanism with the reference's
early-exit frontier walk that stops at the first shared ancestor. The
output is one boolean, so the comparison is plain `==` with no
canonicalization. The band covers the statement's named corners:
equality of the two queries, people with no recorded parents, direct
and multi-generation ancestor pairs, siblings and half-siblings (two
recorded parents, the statement's maximum), cousins and double
cousins, the coparents-without-shared-ancestor trap, an outside parent
joining a blood family without relating to it, disconnected families,
and a seeded random band of shuffled-label families with up to two
parents per person. The statement sets no population bound (its
constraint block is unparsed on the page), so no length corner is
named; one constructed deep chain is still exercised here to pin the
walk's shape at scale, with its expectation following from the
construction:

- test_constructed_line_of_20000_people_stays_linear: a single
  parent-per-child line of 20000 people (label p<i> born from p<i-1>).
  Every earlier label is an ancestor of every later one, so an
  ancestor-descendant pair must return True and two people of one
  disjoint second line must return False.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")

LINE_POPULATION = 20_000


def _ids(cases):
    return [case["id"] for case in cases]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().solve, case)


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


def test_constructed_line_of_20000_people_stays_linear():
    relations = [[f"p{person - 1}", f"p{person}"] for person in range(1, LINE_POPULATION)]
    solve = reference.Solution().solve
    assert solve(relations, "p0", f"p{LINE_POPULATION - 1}") is True
    assert solve(relations, f"p{LINE_POPULATION - 1}", "p0") is True
    assert solve(relations, "p7", f"p{LINE_POPULATION // 2}") is True
    second_line = [[f"q{person - 1}", f"q{person}"] for person in range(1, LINE_POPULATION)]
    assert solve(relations + second_line, f"p{LINE_POPULATION - 1}", f"q{LINE_POPULATION - 1}") is False
