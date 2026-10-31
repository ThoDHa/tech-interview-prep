"""Hierarchical Document Search — https://www.fastprep.io/problems/amazon-hierarchical-document-search

Write-up & approaches: ../../../docs/amazon/amazon-hierarchical-document-search.md

Source note: The report asks for an extensible folder search library with size and type filters. Tree serialization, matching conventions, and ordering are practice assumptions. Conservative editorial

  uv run python amazon/amazon-hierarchical-document-search/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-hierarchical-document-search/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def searchDocuments(self, parents, documentFlags, sizes, documentTypes, root, minSize, wantedType):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in searchDocuments above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().searchDocuments(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
