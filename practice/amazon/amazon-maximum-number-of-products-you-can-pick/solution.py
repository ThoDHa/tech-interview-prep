"""Max Number of Products You can Pick — https://www.fastprep.io/problems/amazon-maximum-number-of-products-you-can-pick

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-maximum-number-of-products-you-can-pick.md

You have an array of products, where each element contains how much product you have

  uv run python amazon_oa/amazon-maximum-number-of-products-you-can-pick/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-maximum-number-of-products-you-can-pick/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maximumProductsPicked(self, products):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maximumProductsPicked above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maximumProductsPicked(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
