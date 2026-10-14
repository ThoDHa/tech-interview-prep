"""E-commerce Notification Router — https://www.fastprep.io/problems/amazon-ecommerce-notification-router

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-ecommerce-notification-router.md

Implement the routing decision for a batch of e-commerce notifications. For notification i, preferredChannels[i] is the user's preferred channel and priorities[i] is either NORMAL or URGENT.

  uv run python amazon_oa/amazon-ecommerce-notification-router/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-ecommerce-notification-router/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def routeNotifications(self, preferredChannels, priorities):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in routeNotifications above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().routeNotifications(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
