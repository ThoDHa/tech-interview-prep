"""Maximum System Memory Capacity — https://www.fastprep.io/problems/amazon-maximum-capacity

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximum-capacity.md

Amazon is optimizing the capacity of a cloud system with n servers. The memory capacity of the i-th server is memory[i].

  uv run python amazon_oa/amazon-maximum-capacity/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximum-capacity/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximumCapacity(self, memory):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximumCapacity above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximumCapacity(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
