"""Next Greater Element I — https://www.fastprep.io/problems/amazon-next-greater-element-i

Write-up & approaches: ../../../docs/amazon/amazon-next-greater-element-i.md

Reference implementation of the write-up's recommended Monotonic Stack
solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-next-greater-element-i/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-next-greater-element-i/              # run the test sets
"""

from typing import Dict, List

from harness import pick_case


class Solution:
    def nextGreaterElement(self, query: List[int], reference: List[int]) -> List[int]:
        """Return each query value's first greater value to its right in
        `reference`, or -1 when none exists.

        Sweeps `reference` once with a decreasing stack of values still
        waiting for a greater neighbor. Each arriving value pops and
        answers every waiting value smaller than itself, then joins the
        stack, so `greater_map` collects the next greater value of every
        element that has one. Queries read `greater_map` in query order.

        Args:
            query: Values to answer, each guaranteed to appear in
                `reference`; the arrays hold distinct integers.
            reference: The sequence the "to its right" relation is
                defined on.

        Returns:
            One answer per query value, in query order.

        Time:  O(m + n): the sweep pushes and pops each of the m
            reference values at most once, and each of the n queries is
            one dictionary read.
        Space: O(m): the stack and `greater_map` hold at most one entry
            per reference value.
        """
        greater_map: Dict[int, int] = {}
        waiting: List[int] = []
        for value in reference:
            while waiting and waiting[-1] < value:
                greater_map[waiting.pop()] = value
            waiting.append(value)
        return [greater_map.get(value, -1) for value in query]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in nextGreaterElement above, then
    # run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().nextGreaterElement(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
