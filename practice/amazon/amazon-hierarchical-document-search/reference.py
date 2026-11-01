"""Hierarchical Document Search — https://www.fastprep.io/problems/amazon-hierarchical-document-search

Write-up & approaches: ../../../docs/amazon/amazon-hierarchical-document-search.md

Reference implementation of the write-up's recommended Children-Map
DFS solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-hierarchical-document-search/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-hierarchical-document-search/              # run the test sets
"""

from typing import DefaultDict, List

from harness import pick_case


class Solution:
    def searchDocuments(
        self,
        parents: List[int],
        documentFlags: List[int],
        sizes: List[int],
        documentTypes: List[str],
        root: int,
        minSize: int,
        wantedType: str,
    ) -> List[int]:
        """Return the subtree documents passing the enabled filters, sorted.

        The traversal and the filters are kept separate: `_subtree_nodes`
        yields every node below `root` and knows nothing about documents,
        while `_is_matching_document` knows nothing about the tree. The
        method joins them with the statement's contract: a document
        matches when `sizes[node] > minSize` and either `wantedType` is
        empty (type condition disabled) or the document's type equals it
        case-sensitively. IDs come back in increasing order regardless
        of traversal order.

        Args:
            parents: One parent per node; exactly one entry is -1. Node
                arrays are aligned across the four lists.
            documentFlags: 1 marks a document, 0 a folder.
            sizes: Document sizes; folder entries are ignored.
            documentTypes: Document types; folder entries are ignored.
            root: The folder whose subtree is searched.
            minSize: Inclusive lower bound is `minSize`; only strictly
                greater sizes match.
            wantedType: Required type, case-sensitive; empty disables
                the type condition.

        Returns:
            The matching document IDs in increasing order.

        Time:  O(n + d log d): one pass builds the child map, one DFS
            visits the subtree, and the d matches sort.
        Space: O(n): the child map and the visited-node stack.
        """
        children = self._child_map(parents)
        matches = [
            node
            for node in self._subtree_nodes(children, root)
            if self._is_matching_document(node, documentFlags, sizes, documentTypes, minSize, wantedType)
        ]
        return sorted(matches)

    @staticmethod
    def _child_map(parents: List[int]) -> DefaultDict[int, List[int]]:
        """Group node IDs under their direct parent in one pass.

        Time:  O(n): one entry per node.
        Space: O(n): one list entry per non-root node.
        """
        children: DefaultDict[int, List[int]] = DefaultDict(list)
        for node, parent in enumerate(parents):
            if parent != -1:
                children[parent].append(node)
        return children

    @staticmethod
    def _subtree_nodes(children: DefaultDict[int, List[int]], root: int) -> List[int]:
        """Return every node of the subtree rooted at `root`, root included.

        The explicit stack visits each subtree node once and cannot
        overflow on a deeply nested folder chain.

        Time:  O(subtree): each visited node pushes its children once.
        Space: O(subtree): the stack.
        """
        visited: List[int] = []
        stack = [root]
        while stack:
            node = stack.pop()
            visited.append(node)
            stack.extend(children.get(node, []))
        return visited

    @staticmethod
    def _is_matching_document(
        node: int,
        documentFlags: List[int],
        sizes: List[int],
        documentTypes: List[str],
        minSize: int,
        wantedType: str,
    ) -> bool:
        """Apply the statement's filter contract to one node.

        Time:  O(1): two field reads and up to two comparisons.
        Space: O(1): no state.
        """
        if documentFlags[node] != 1:
            return False
        if sizes[node] <= minSize:
            return False
        return wantedType == "" or documentTypes[node] == wantedType


if __name__ == "__main__":
    # Debug playground: set a breakpoint in searchDocuments above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().searchDocuments(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
