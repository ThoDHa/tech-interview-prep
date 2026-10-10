"""LRU Cache for Query Results — https://www.fastprep.io/problems/amazon-lru-query-result-cache

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-lru-query-result-cache.md

Maintain a cache with positive integer capacity. Process each operation atomically in the supplied completed serialization order:

  uv run python amazon_oa/amazon-lru-query-result-cache/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-lru-query-result-cache/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def runQueryCache(self, capacity, operations):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in runQueryCache above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().runQueryCache(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
