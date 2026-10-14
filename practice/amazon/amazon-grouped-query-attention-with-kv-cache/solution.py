"""Grouped-Query Attention with a KV Cache — https://www.fastprep.io/problems/amazon-grouped-query-attention-with-kv-cache

Write-up & approaches: ../../../docs/amazon/amazon-grouped-query-attention-with-kv-cache.md

Compute one projection-free grouped-query scaled dot-product attention pass using an existing key-value cache plus newly generated key and value rows.

  uv run python amazon_oa/amazon-grouped-query-attention-with-kv-cache/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-grouped-query-attention-with-kv-cache/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def groupedQueryAttentionWithCache(self, query, cachedKey, cachedValue, newKey, newValue, queryHeads, kvHeads):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in groupedQueryAttentionWithCache above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().groupedQueryAttentionWithCache(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
