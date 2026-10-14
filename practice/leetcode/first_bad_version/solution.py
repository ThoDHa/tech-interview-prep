"""First Bad Version: https://leetcode.com/problems/first-bad-version/

Write-up & approaches: ../../docs/problems/first_bad_version.md

Versions `[1, 2, ..., n]` turn bad from some point on; given the API
`isBadVersion(version)`, find the first bad version with the fewest calls.

  uv run python first_bad_version/solution.py   # debug one case (see CASE below)
  uv run pytest first_bad_version/              # run the test sets
"""

from harness import NotSolved, pick_case


# The isBadVersion API is provided by LeetCode. Here we simulate it: every
# version >= `bad` is bad. Tests set `bad` per case before calling the solution.
bad = 0


def isBadVersion(v: int) -> bool:
    return v >= bad


class Solution:
    def firstBadVersion(self, n: int) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in firstBadVersion above, then run this
    # file. The case is {args: [n, bad], expected: first_bad}; we point the
    # module-level `bad` at the case's bad version before calling, just like the
    # test harness does.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    bad = case["args"][1]
    result = Solution().firstBadVersion(case["args"][0])
    print(f"case {case['id']}: n = {case['args'][0]}, bad = {case['args'][1]}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
