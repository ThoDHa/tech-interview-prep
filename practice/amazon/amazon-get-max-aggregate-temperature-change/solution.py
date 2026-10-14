"""Max Aggregate Temp Change — https://www.fastprep.io/problems/amazon-get-max-aggregate-temperature-change

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-get-max-aggregate-temperature-change.md

Alexa is Amazon's virtual AI assistant. It makes it easy to set up your Alexa-enabled devices, listen to music, get weather updates, and much more. The team is working on a new feature that evaluates 

  uv run python amazon_oa/amazon-get-max-aggregate-temperature-change/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-get-max-aggregate-temperature-change/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def getMaxAggregateTemperatureChange(self, tempChange):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in getMaxAggregateTemperatureChange above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().getMaxAggregateTemperatureChange(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
