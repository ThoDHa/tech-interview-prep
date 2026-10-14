"""Find Largest Set of Onion Bags — https://www.fastprep.io/problems/amazon-find-largest-set-of-onion-bags

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-largest-set-of-onion-bags.md

You are shopping online for some bags of onion. Each listing displays the number of onions that the bag contains. You want to buy a perfect set of onion bags from the entire search results list, onion

  uv run python amazon_oa/amazon-find-largest-set-of-onion-bags/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-largest-set-of-onion-bags/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findLargestSet(self, onionBags):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findLargestSet above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findLargestSet(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
