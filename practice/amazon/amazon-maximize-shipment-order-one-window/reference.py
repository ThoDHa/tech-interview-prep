"""Maximize Shipment Order by Sorting One Window — https://www.fastprep.io/problems/amazon-maximize-shipment-order-one-window

Write-up & approaches: ../../../docs/amazon/amazon-maximize-shipment-order-one-window.md

Reference implementation of the write-up's recommended Painted
Agreement Intervals solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-maximize-shipment-order-one-window/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-maximize-shipment-order-one-window/              # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def solve(self, shipmentOrder: List[int], windowSize: int) -> List[int]:
        """Return the lexicographically largest array after sorting exactly
        one window of `windowSize` consecutive values.

        The page's constraint block is unparseable, so this reference
        assumes `1 <= windowSize <= len(shipmentOrder)` and treats
        `shipmentOrder` as a permutation of `1..n`, the statement's one
        explicit structural guarantee. Sorting a window ascending never
        beats the original array: wherever the sorted window first
        differs, it placed the smallest value left in the window. The
        answer therefore keeps the longest possible agreement with the
        original. Each window position `k` is a valid agreement end for
        a start `s` exactly when the values before `k` ascend from `s`,
        no smaller value interrupts before the window ends, and the
        window covers `k`: three interval conditions that precomputed
        descent and next-smaller arrays turn into one interval per `k`.
        Painting those intervals largest-break-first hands every start
        its break; the earliest start with the largest break sorts its
        window. A window with no internal descent sorts to itself, so
        the original array is returned immediately in that case.

        Args:
            shipmentOrder: Permutation of `1..n`.
            windowSize: Window length, `1 <= windowSize <= n`.

        Returns:
            The lexicographically largest obtainable array.

        Time:  O(n log n): linear precompute and interval painting,
               then one O(w log w) sort of the winning window.
        Space: O(n): the position arrays, paint pointers, and the
               result assembly.
        """
        values = shipmentOrder
        count, width = len(values), windowSize

        last_descent_before = [-1] * count
        for position in range(1, count):
            last_descent_before[position] = last_descent_before[position - 1]
            if values[position - 1] > values[position]:
                last_descent_before[position] = position - 1

        for start in range(count - width + 1):
            if last_descent_before[start + width - 1] < start:
                return values

        next_smaller_right = [count] * count
        monotonic_stack: List[int] = []
        for position in range(count):
            while monotonic_stack and values[monotonic_stack[-1]] > values[position]:
                next_smaller_right[monotonic_stack.pop()] = position
            monotonic_stack.append(position)

        break_after = list(range(count))
        next_unpainted = list(range(count + 1))

        def first_unpainted(start: int) -> int:
            while next_unpainted[start] != start:
                next_unpainted[start] = next_unpainted[next_unpainted[start]]
                start = next_unpainted[start]
            return start

        for agreement_end in range(count - 1, 0, -1):
            last_agreed = agreement_end - 1
            low = max(
                last_descent_before[last_agreed] + 1,
                agreement_end - width + 1,
                0,
            )
            high = min(
                last_agreed,
                next_smaller_right[last_agreed] - width,
                count - width,
            )
            start = first_unpainted(low)
            while start <= high:
                break_after[start] = agreement_end
                next_unpainted[start] = start + 1
                start = first_unpainted(start + 1)

        best_start, best_break = 0, 0
        for start in range(count - width + 1):
            if break_after[start] > best_break:
                best_break, best_start = break_after[start], start
        return (
            values[:best_start]
            + sorted(values[best_start : best_start + width])
            + values[best_start + width :]
        )


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
