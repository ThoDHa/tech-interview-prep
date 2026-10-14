"""Tests for Construct a Tree from Level-Order and Inorder Traversals — your attempt (solution.py) against cases.json.

The worked approaches live in ../../../docs/problems/amazon_oa/amazon-construct-tree-level-inorder.md.
"""

import pytest

from harness import NotSolved, load_solution

CASES = []

if len(CASES) == 0:
    pytest.skip("tree output for amazon-construct-tree-level-inorder is not `==`-assertable: the method returns a TreeNode, which never equals a list", allow_module_level=True)

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", CASES, ids=_ids(CASES))
def test_solution(case):
    try:
        _check(solution.Solution().buildTree, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
