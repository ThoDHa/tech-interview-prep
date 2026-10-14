"""Product Category Group Sizes — https://www.fastprep.io/problems/amazon-product-category-groups

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-product-category-groups.md

You are given a list of products and a list of pairs. Each pair means the two products belong to the same category. Category membership is transitive: if product A is in the same category as B, and B 

  uv run python amazon_oa/amazon-product-category-groups/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-product-category-groups/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def productCategoryGroupSizes(self, products, pairs):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in productCategoryGroupSizes above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().productCategoryGroupSizes(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
