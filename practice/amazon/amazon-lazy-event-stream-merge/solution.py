"""Lazy Merge of Sorted Event Streams — https://www.fastprep.io/problems/amazon-lazy-event-stream-merge

Write-up & approaches: ../../../docs/amazon/amazon-lazy-event-stream-merge.md

Implement a forward iterator that merges event streams from earliest timestamp to latest. Each stream is already sorted. Do not load all events into the memory used for merging.

  uv run python amazon/amazon-lazy-event-stream-merge/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-lazy-event-stream-merge/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def mergeEventStreams(self, streams):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in mergeEventStreams above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().mergeEventStreams(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
