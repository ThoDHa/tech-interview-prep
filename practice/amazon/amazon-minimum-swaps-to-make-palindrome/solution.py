"""Get Max Stability — https://www.fastprep.io/problems/amazon-minimum-swaps-to-make-palindrome

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-minimum-swaps-to-make-palindrome.md

Example output is a placeholder. Please ignore it.

  uv run python amazon_oa/amazon-minimum-swaps-to-make-palindrome/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-minimum-swaps-to-make-palindrome/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def minSwapsToMakePalindrome(self, s):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in minSwapsToMakePalindrome above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().minSwapsToMakePalindrome(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
