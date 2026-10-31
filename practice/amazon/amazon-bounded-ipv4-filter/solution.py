"""Bounded IPv4 Filter — https://www.fastprep.io/problems/amazon-bounded-ipv4-filter

Write-up & approaches: ../../../docs/amazon/amazon-bounded-ipv4-filter.md

Source note: The report specifies three IPv4 pool operations, a 128-entry limit, and a small Linux environment. Initial state, full-pool behavior, and input conventions are specified for practice. The

  uv run python amazon/amazon-bounded-ipv4-filter/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-bounded-ipv4-filter/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def processIpOperations(self, operations, addresses):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in processIpOperations above, then run this file.
    CASE = None
    if CASE is None:
        print("no cases authored yet; add cases to cases.json or cases_full.json, then set CASE to an id")
    else:
        case = pick_case(__file__, CASE)
        result = Solution().processIpOperations(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
