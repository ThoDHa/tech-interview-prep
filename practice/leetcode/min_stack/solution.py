"""Min Stack: https://leetcode.com/problems/min-stack/

Write-up & approaches: ../../../docs/leetcode/min_stack.md

Design a stack that supports push, pop, top, and retrieving the minimum element
in constant time.

  uv run python min_stack/solution.py     # debug one case (see CASE below)
  uv run pytest min_stack/                # run the test sets
"""

from harness import NotSolved, pick_case, run_operations


class MinStack:
    def __init__(self) -> None:
        # Initialize empty state here; methods below raise until implemented.
        self.stack: list[tuple[int, int]] = []

    def push(self, val: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        """
        current_min = val
        if self.stack:
            current_min = min(current_min, self.getMin())
        current_min = val if not self.stack else min(val, self.stack[-1][1])
        self.stack.append((val, current_min))

    def pop(self) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        self.stack.pop()

    def top(self) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        return self.stack[-1][0]

    def getMin(self) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        return self.stack[-1][1]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a MinStack method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(MinStack, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement MinStack's methods first")
