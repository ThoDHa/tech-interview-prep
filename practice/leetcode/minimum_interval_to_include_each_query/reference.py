"""Minimum Interval to Include Each Query — https://leetcode.com/problems/minimum-interval-to-include-each-query/

Write-up & approaches: ../../docs/problems/minimum_interval_to_include_each_query.md
Reference implementation of the write-up's Min-Heap Sweep solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python minimum_interval_to_include_each_query/reference.py   # replay the example cases
  uv run pytest minimum_interval_to_include_each_query/               # run the test sets
"""

import heapq
from typing import List

from harness import pick_case


class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        """Return the shortest covering interval's size per query, else -1.

        Time:  O(n log n + q log q + (n + q) log n): sorts plus one push and
            at most one pop per interval against a heap bounded by n.
        Space: O(n + q): the heap holds at most n pairs, the indexed queries
            one pair per query.
        """
        sorted_intervals = sorted(intervals)
        indexed_queries = sorted((query, i) for i, query in enumerate(queries))

        heap: List[tuple] = []
        output = [-1] * len(queries)
        ptr = 0
        for query, original_index in indexed_queries:
            while ptr < len(sorted_intervals) and sorted_intervals[ptr][0] <= query:
                left, right = sorted_intervals[ptr]
                heapq.heappush(heap, (right - left + 1, right))
                ptr += 1
            while heap and heap[0][1] < query:
                heapq.heappop(heap)
            if heap:
                output[original_index] = heap[0][0]
        return output


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example case.
    case = pick_case(__file__, "example_1")
    result = Solution().minInterval(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
