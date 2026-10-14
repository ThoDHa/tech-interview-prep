"""Group-Relative Policy Advantages — https://www.fastprep.io/problems/amazon-group-relative-policy-advantages

Write-up & approaches: ../../../docs/amazon/amazon-group-relative-policy-advantages.md

Compute group-relative advantages for sampled policy responses. Response i belongs to groupIds[i] and receives the integer reward correctnessRewards[i] + formatRewards[i].

  uv run python amazon_oa/amazon-group-relative-policy-advantages/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-group-relative-policy-advantages/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def groupRelativeAdvantages(self, groupIds, correctnessRewards, formatRewards):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in groupRelativeAdvantages above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().groupRelativeAdvantages(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
