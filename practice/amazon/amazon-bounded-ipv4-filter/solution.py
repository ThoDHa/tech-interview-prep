"""Bounded IPv4 Filter — https://www.fastprep.io/problems/amazon-bounded-ipv4-filter

Write-up & approaches: ../../../docs/amazon/amazon-bounded-ipv4-filter.md

Source note: The report specifies three IPv4 pool operations, a 128-entry limit, and a small Linux environment. Initial state, full-pool behavior, and input conventions are specified for practice. The

  uv run python amazon/amazon-bounded-ipv4-filter/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-bounded-ipv4-filter/              # run the test sets
"""

from harness import NotSolved, pick_case, run_operations


class IPv4Pool:
    def __init__(self) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def add_ip(self, address: str) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def remove_ip(self, address: str) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def check_ip(self, address: str) -> bool:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in an IPv4Pool method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(IPv4Pool, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement IPv4Pool's methods first")
