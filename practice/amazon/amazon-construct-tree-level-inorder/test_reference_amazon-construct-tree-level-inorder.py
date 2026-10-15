"""Reference-parametrized gauntlet for Construct a Tree from Level-Order
and Inorder Traversals.

The generator-emitted test module carries a module-level skip (the
starter is not a single `==`-assertable call), so the sanctioned
reference class lives here instead: the generated module stays
byte-identical and cases_full.json stays falsifiable. Every expectation
in cases_full.json is oracle-derived: recorded from the write-up's
Brute Force Partition (inorder window rescans), an implementation
independent of this reference's dictionary lookups. The reconstructed
tree is serialized with tree_to_list, which pins the full structure,
not merely the value set.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


def _ids(cases):
    return [case["id"] for case in cases]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    from harness import tree_to_list

    got = tree_to_list(reference.Solution().buildTree(list(case["args"][0]), list(case["args"][1])))
    assert got == case["expected"]
