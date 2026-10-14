"""Count Faults (Faulty Binding 101 😁) — https://www.fastprep.io/problems/amazon-count-faults

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-count-faults.md

There are n servers with IDs s1, s2, ..., sn. You are given an array logs in chronological order. Each entry has the form "<server_id> <status>", where status is either success or error.

  uv run python amazon_oa/amazon-count-faults/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-count-faults/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def countFaults(self, n, logs):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in countFaults above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().countFaults(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
