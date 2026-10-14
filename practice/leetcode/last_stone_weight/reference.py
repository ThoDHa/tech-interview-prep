"""Last Stone Weight — https://leetcode.com/problems/last-stone-weight/

Write-up & approaches: ../../docs/problems/last_stone_weight.md

Canonical reference implementation: the write-up's optimal approach (a max-heap
simulation via negated weights), kept next to the harness so authored cases
stay falsifiable. Your own attempt lives in solution.py.

  uv run python last_stone_weight/reference.py   # debug one case (see CASE below)
  uv run pytest last_stone_weight/               # run the test sets
"""

import heapq

from harness import pick_case


class Solution:
    def lastStoneWeight(self, stones):
        """Smash the two heaviest stones until at most one remains.

        Negating every weight turns Python's min-heap into a max-heap, so
        each smash pops the two heaviest stones in O(log n) and pushes back
        their difference when one survives; heapq provides only a min-heap,
        and negation restores max-heap behavior at no extra cost.

        Time:  O(n log n): heapify is O(n) and each of up to n - 1 smashes
               pops twice and pushes once, at O(log n) each.
        Space: O(n): the negated copy of the weights; the heap replaces the
               input list rather than growing beyond it.
        """
        heap = [-stone for stone in stones]
        heapq.heapify(heap)
        while len(heap) > 1:
            first = -heapq.heappop(heap)
            second = -heapq.heappop(heap)
            if first != second:
                heapq.heappush(heap, -(first - second))
        return -heap[0] if heap else 0


if __name__ == "__main__":
    # Debug playground: set a breakpoint in lastStoneWeight above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().lastStoneWeight(*case["args"])
    print(f"case {case['id']}: expected = {case['expected']}")
    print(f"got:      {result}")
