"""Available Recipes from Initial Supplies — https://www.fastprep.io/problems/amazon-available-recipes-from-supplies

Write-up & approaches: ../../../docs/amazon/amazon-available-recipes-from-supplies.md

You are given distinct recipe names in recipes. Row ingredients[i] lists everything needed to make recipes[i]. An ingredient can be an initial supply, another recipe, or a name that is unavailable.

  uv run python amazon/amazon-available-recipes-from-supplies/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-available-recipes-from-supplies/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findAvailableRecipes(self, recipes, ingredients, supplies):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findAvailableRecipes above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findAvailableRecipes(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
