"""Top K Frequent Elements — https://leetcode.com/problems/top-k-frequent-elements/

Write-up & approaches: ../../docs/problems/top_k_frequent_elements.md

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements within the array. The test cases are generated such that the answer is always **unique**. You may return the out

  uv run python top_k_frequent_elements/solution.py   # debug one case (see CASE below)
  uv run pytest top_k_frequent_elements/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def solve(self, *args):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
