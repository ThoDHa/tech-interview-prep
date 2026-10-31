"""Latest-Timestamp Key-Value Store — https://www.fastprep.io/problems/amazon-latest-timestamp-key-value-store

Write-up & approaches: ../../../docs/amazon/amazon-latest-timestamp-key-value-store.md

Source note: The source reports set(timestamp,key,value) and get(key) returning the greatest-timestamp value. This exercise uses a finite operation sequence with authored tie handling, missing-key out

  uv run python amazon/amazon-latest-timestamp-key-value-store/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-latest-timestamp-key-value-store/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def latestTimestampValues(self, operations, keys, values, timestamps):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in latestTimestampValues above, then run this file.
    CASE = None
    if CASE is None:
        print("no cases authored yet; add cases to cases.json or cases_full.json, then set CASE to an id")
    else:
        case = pick_case(__file__, CASE)
        result = Solution().latestTimestampValues(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
