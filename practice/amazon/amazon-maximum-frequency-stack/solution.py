"""Maximum Frequency Stack — https://www.fastprep.io/problems/amazon-maximum-frequency-stack

Write-up & approaches: ../../../docs/amazon/amazon-maximum-frequency-stack.md

Design a stack-like data structure that supports push and pop.

  uv run python amazon/amazon-maximum-frequency-stack/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-maximum-frequency-stack/              # run the test sets
"""

from harness import NotSolved, pick_case, run_operations


class FreqStack:
    def __init__(self) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def push(self, value: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def pop(self) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a FreqStack method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(FreqStack, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement FreqStack's methods first")
