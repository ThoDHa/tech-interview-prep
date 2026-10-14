"""Get Max Servers — https://www.fastprep.io/problems/amazon-find-maximum-number-of-servers

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-find-maximum-number-of-servers.md

Source note: 2026-07-02 — This problem duplicates Server Selection. Sighting dates were merged into this fuller official-source version, which remains the recommended practice page.

  uv run python amazon_oa/amazon-find-maximum-number-of-servers/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-find-maximum-number-of-servers/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaxServers(self, powers):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaxServers above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaxServers(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
