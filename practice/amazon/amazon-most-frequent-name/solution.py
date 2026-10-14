"""Most Frequent Name — https://www.fastprep.io/problems/amazon-most-frequent-name

Write-up & approaches: ../../../docs/amazon/amazon-most-frequent-name.md

Given a nonempty array of case-sensitive names, return the name that appears most often.

  uv run python amazon_oa/amazon-most-frequent-name/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-most-frequent-name/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def mostFrequentName(self, names):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in mostFrequentName above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().mostFrequentName(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
