"""All About Medians — https://www.fastprep.io/problems/amazon-medians

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-medians.md

A new Amazon intern encountered a challenging task. Currently, the intern has n integers, where the value of the ith element is represented by the array element nums[i]. The intern is curious to play 

  uv run python amazon_oa/amazon-medians/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-medians/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def medians(self, nums, k):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in medians above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().medians(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
