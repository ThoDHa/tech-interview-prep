"""Get Max Information Gain — https://www.fastprep.io/problems/amazon-get-max-information-gain

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-max-information-gain.md

Data analysts at Amazon are analyzing a data set of n strings in the array 

  uv run python amazon_oa/amazon-get-max-information-gain/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-max-information-gain/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaxInformationGain(self, dataSet, max_common_features):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaxInformationGain above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaxInformationGain(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
