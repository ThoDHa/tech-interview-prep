"""Maximum Concurrent Processes (Bar Raiser Round) — https://www.fastprep.io/problems/amazon-max-concurrent-processes

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-max-concurrent-processes.md

🍇 FastPrep match note: This version is based on a reported Amazon SDE2 full-time onsite Bar Raiser round prompt and should match the core task about 90-95%: given process running intervals, return the

  uv run python amazon_oa/amazon-max-concurrent-processes/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-max-concurrent-processes/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def maxConcurrentProcesses(self, intervals):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxConcurrentProcesses above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxConcurrentProcesses(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
