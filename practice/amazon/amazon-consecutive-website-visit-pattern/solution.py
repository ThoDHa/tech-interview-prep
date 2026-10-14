"""Most Frequent Consecutive Website Pattern — https://www.fastprep.io/problems/amazon-consecutive-website-visit-pattern

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-consecutive-website-visit-pattern.md

You are given three equal-length arrays describing website visits. Entry i contains a username, an integer timestamp, and a website.

  uv run python amazon_oa/amazon-consecutive-website-visit-pattern/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-consecutive-website-visit-pattern/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def mostFrequentConsecutivePattern(self, usernames, timestamps, websites):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in mostFrequentConsecutivePattern above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().mostFrequentConsecutivePattern(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
