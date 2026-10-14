"""Min Operation — https://www.fastprep.io/problems/amazon-min-operation

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-min-operation.md

The manager of an Amazon warehouse needs to ship n products from different locations, the location of the ith product is represented by an array locations[i]. The manager is allowed to perform one ope

  uv run python amazon_oa/amazon-min-operation/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-min-operation/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minOperation(self, m, locations):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minOperation above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minOperation(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
