"""Number of Islands II — https://www.fastprep.io/problems/amazon-number-of-islands-ii

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-number-of-islands-ii.md

Start with an m by n grid containing only water. For each distinct position [row, col] in positions, turn that cell into land and append the current number of islands to the result.

  uv run python amazon_oa/amazon-number-of-islands-ii/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-number-of-islands-ii/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def numIslands2(self, m, n, positions):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in numIslands2 above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().numIslands2(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
