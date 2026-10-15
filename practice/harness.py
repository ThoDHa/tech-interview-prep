"""Shared utilities for the grind75 practice harness.

Each problem lives in its own directory with a `solution.py` (your attempt, also
runnable directly for debugging), a `cases.json` / `cases_full.json` (test cases),
and a `test_<slug>.py`. The canonical worked solutions live in the matching
`../docs/leetcode/<slug>.md` write-up, not here. The helpers below marshal
LeetCode-style inputs/outputs (linked lists, binary trees, graphs, design-operation
sequences) and load each problem's `solution.py` under a unique module name so
identically named files never collide.
"""

from __future__ import annotations

import importlib.util
import json
from collections import deque
from pathlib import Path
from typing import Any, List, Optional


class ListNode:
    """Singly linked list node, matching the LeetCode definition."""

    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None) -> None:
        self.val = val
        self.next = next


class TreeNode:
    """Binary tree node, matching the LeetCode definition."""

    def __init__(
        self,
        val: int = 0,
        left: "Optional[TreeNode]" = None,
        right: "Optional[TreeNode]" = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right


def build_linked_list(values: List[int]) -> Optional[ListNode]:
    """Build a linked list from a Python list; empty list yields None."""
    head: Optional[ListNode] = None
    for value in reversed(values):
        head = ListNode(value, head)
    return head


def linked_list_to_list(head: Optional[ListNode]) -> List[int]:
    """Serialize a linked list back to a Python list."""
    out: List[int] = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


def build_linked_list_with_cycle(values: List[int], pos: int) -> Optional[ListNode]:
    """Build a linked list whose tail links back to index `pos` (-1 = no cycle)."""
    if not values:
        return None
    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes[0]


def build_tree(values: List[Optional[int]]) -> Optional[TreeNode]:
    """Build a binary tree from LeetCode level-order form (None = missing node)."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        # The while condition already guarantees i < len(values) for the left child.
        if values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def find_tree_node(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """Locate the TreeNode whose .val equals `val`, for problems taking node refs."""
    if root is None:
        return None
    if root.val == val:
        return root
    return find_tree_node(root.left, val) or find_tree_node(root.right, val)


def tree_to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    """Serialize a binary tree to LeetCode level-order form, trailing Nones trimmed."""
    out: List[Optional[int]] = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


class GraphNode:
    """Undirected graph node (LeetCode `Node` for Clone Graph): val + neighbors."""

    def __init__(self, val: int = 0, neighbors: "Optional[List[GraphNode]]" = None) -> None:
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def build_graph(adj_list: List[List[int]]) -> Optional[GraphNode]:
    """Build a graph from a LeetCode adjacency list (node i is 1-indexed)."""
    if not adj_list:
        return None
    nodes = {i: GraphNode(i) for i in range(1, len(adj_list) + 1)}
    for i, neighbors in enumerate(adj_list, start=1):
        nodes[i].neighbors = [nodes[j] for j in neighbors]
    return nodes[1]


def graph_to_adjacency(node: Optional[GraphNode]) -> List[List[int]]:
    """Serialize a graph back to a LeetCode adjacency list (by ascending val)."""
    if node is None:
        return []
    adjacency: dict = {}
    stack = [node]
    while stack:
        current = stack.pop()
        if current.val in adjacency:
            continue
        adjacency[current.val] = [neighbor.val for neighbor in current.neighbors]
        for neighbor in current.neighbors:
            if neighbor.val not in adjacency:
                stack.append(neighbor)
    return [adjacency[val] for val in sorted(adjacency)]


def run_operations(cls, operations: List[str], arguments: List[list]) -> List[Any]:
    """Run a LeetCode design-problem operation sequence against `cls`.

    `operations[0]` is the constructor (its return is None); each later entry
    calls the named method with its positional `arguments`. Returns the list of
    results aligned with `operations`.
    """
    if not operations or len(operations) != len(arguments):
        raise ValueError("operations and arguments must be non-empty and equal length")
    instance = cls(*arguments[0])
    results: List[Any] = [None]
    for op, args in zip(operations[1:], arguments[1:]):
        results.append(getattr(instance, op)(*args))
    return results


def load_cases(file: str, filename: str = "cases.json") -> List[dict]:
    """Load a case file sitting next to the given problem file."""
    path = Path(file).resolve().parent / filename
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def all_cases(file: str) -> List[dict]:
    """Load cases.json plus cases_full.json (if present) for a problem."""
    cases = load_cases(file, "cases.json")
    if (Path(file).resolve().parent / "cases_full.json").exists():
        cases += load_cases(file, "cases_full.json")
    return cases


def pick_case(file: str, case_id: Optional[str] = None) -> dict:
    """Return one case for the solution.py debug playground.

    Pass a case `id` (see cases.json / cases_full.json) to choose a specific case;
    omit it to get the first. Raises with the available ids if the id is unknown.
    """
    cases = all_cases(file)
    if case_id is None:
        return cases[0]
    for case in cases:
        if case.get("id") == case_id:
            return case
    raise KeyError(f"no case id {case_id!r}; available: {[c.get('id') for c in cases]}")


def load_solution(file: str, filename: str = "solution.py"):
    """Import a problem's solution module under a unique, collision-free name."""
    directory = Path(file).resolve().parent
    path = directory / filename
    module_name = f"{directory.name}_{path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class NotSolved(Exception):
    """Raised by an unsolved practice stub so tests skip instead of failing."""
