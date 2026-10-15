"""Reference-parametrized gauntlet for Maximum Sum BST in a Binary Tree.

The generator-emitted test module carries a module-level skip (the
starter is not a single `==`-assertable call), so the sanctioned
reference class lives here instead: the generated module stays
byte-identical and cases_full.json stays falsifiable. Every expectation
in cases_full.json is oracle-derived: recorded from the write-up's
Brute Force (per-candidate bounds validation plus a fresh subtree sum),
an implementation independent of this reference's one-pass report fold.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    from harness import build_tree

    got = reference.Solution().maxSumBST(build_tree(case["args"][0]))
    assert got == case["expected"]
