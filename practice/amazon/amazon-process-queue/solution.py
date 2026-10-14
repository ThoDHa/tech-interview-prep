"""Process Queue — https://www.fastprep.io/problems/amazon-process-queue

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-process-queue.md

You are given an array wait with elements that represent processes where each element in the array denotes the amount on time that process can wait before needing to be removed. Each second, the next 

  uv run python amazon_oa/amazon-process-queue/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-process-queue/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def processQueue(self, wait):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in processQueue above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().processQueue(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
