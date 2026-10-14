"""Make All Elements Distinct — https://www.fastprep.io/problems/amazon-make-all-elements-distinct

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-make-all-elements-distinct.md

An Amazon warehouse manager is responsible for managing inventory and ensuring that each product has a unique identifier. There are n products in the warehouse, where the identifier of the i-th item i

  uv run python amazon_oa/amazon-make-all-elements-distinct/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-make-all-elements-distinct/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def makeAllElementsDistinct(self, n, identifier):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in makeAllElementsDistinct above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().makeAllElementsDistinct(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
