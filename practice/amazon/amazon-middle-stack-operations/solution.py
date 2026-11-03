"""Stack with Constant-Time Middle Queries — https://www.fastprep.io/problems/amazon-middle-stack-operations

Write-up & approaches: ../../../docs/amazon/amazon-middle-stack-operations.md

Process a sequence of stack operations. Each operation is ["push", value], ["pop"], ["top"], or ["middle"]. Values are signed decimal integers encoded as strings.

  uv run python amazon/amazon-middle-stack-operations/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-middle-stack-operations/              # run the test sets
"""

from typing import Optional

from harness import NotSolved, pick_case, run_operations


class MiddleStack:
    def __init__(self) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def push(self, value: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def pop(self) -> Optional[int]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def top(self) -> Optional[int]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def middle(self) -> Optional[int]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a MiddleStack method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(MiddleStack, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement MiddleStack's methods first")
