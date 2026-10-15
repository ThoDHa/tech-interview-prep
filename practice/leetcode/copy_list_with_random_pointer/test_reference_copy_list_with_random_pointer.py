"""Reference-parametrized gauntlet for Copy List With Random Pointer.

The generator-emitted test module carries a module-level skip (the
starter is not a single `==`-assertable call), so the sanctioned
reference class lives here instead: the generated module stays
byte-identical and cases_full.json stays falsifiable. Inputs and
expectations use LeetCode's [[val, random_index], ...] serialization;
expectations are the reference deep copy's own round-trip, never
hand-computed. A correct copy serializes identically to its input, and
identity of the returned nodes is asserted separately: the copy must
not reuse any input node.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")


class Node:
    def __init__(self, val: int) -> None:
        self.val = val
        self.next = None
        self.random = None


def _ids(cases):
    return [case["id"] for case in cases]


def build_random_list(pairs):
    if not pairs:
        return None
    nodes = [Node(val) for val, _ in pairs]
    for position, (_, random_index) in enumerate(pairs):
        if position + 1 < len(nodes):
            nodes[position].next = nodes[position + 1]
        nodes[position].random = (
            nodes[random_index] if random_index is not None else None
        )
    return nodes[0]


def random_list_to_pairs(head):
    if head is None:
        return []
    nodes = []
    walk = head
    while walk:
        nodes.append(walk)
        walk = walk.next
    index = {id(node): position for position, node in enumerate(nodes)}
    return [[node.val, index.get(id(node.random))] for node in nodes]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    original_pairs = case["args"][0]
    original = build_random_list(original_pairs)
    copied = reference.Solution().copyRandomList(original)

    original_nodes = set()
    walk = original
    while walk:
        original_nodes.add(id(walk))
        walk = walk.next
    walk = copied
    while walk:
        assert id(walk) not in original_nodes, "copy reuses an input node"
        walk = walk.next

    assert random_list_to_pairs(copied) == case["expected"]
    assert random_list_to_pairs(original) == original_pairs
