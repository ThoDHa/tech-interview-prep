"""Package Dependency Order — https://www.fastprep.io/problems/amazon-package-dependency-order

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-package-dependency-order.md

You are given package dependency pairs and a target package. Each pair [package, dependency] means the package depends on that dependency.

  uv run python amazon_oa/amazon-package-dependency-order/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-package-dependency-order/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def packageInstallOrder(self, dependencies, target):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in packageInstallOrder above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().packageInstallOrder(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
