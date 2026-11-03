"""Environment Variable Store and Substitution — https://www.fastprep.io/problems/amazon-environment-variable-substitution

Write-up & approaches: ../../../docs/amazon/amazon-environment-variable-substitution.md

Process a sequence of environment-variable operations:

  uv run python amazon/amazon-environment-variable-substitution/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-environment-variable-substitution/              # run the test sets
"""

from harness import NotSolved, pick_case, run_operations


class EnvironmentStore:
    def __init__(self) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def set(self, key: str, value: str) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def get(self, key: str) -> str | None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def parse(self, text: str) -> str:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in an EnvironmentStore method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(EnvironmentStore, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement EnvironmentStore's methods first")
