"""Get Operations — https://www.fastprep.io/problems/amazon-get-operations

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-operations.md

There are n processes. The i-th process has resource[i] number of resources. All the resource[i] are distinct. The CPU wants the processes to be arranged in increasing order of their resource[i]. The 

  uv run python amazon_oa/amazon-get-operations/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-operations/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getOperations(self, resource):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getOperations above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getOperations(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
