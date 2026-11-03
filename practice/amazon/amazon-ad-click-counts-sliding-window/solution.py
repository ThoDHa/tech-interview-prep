"""Recent Advertisement Click Counts — https://www.fastprep.io/problems/amazon-ad-click-counts-sliding-window

Write-up & approaches: ../../../docs/amazon/amazon-ad-click-counts-sliding-window.md

You receive a finite sequence of advertisement click and count operations. Each operation is one of:

  uv run python amazon/amazon-ad-click-counts-sliding-window/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-ad-click-counts-sliding-window/              # run the test sets
"""

from harness import NotSolved, pick_case, run_operations


class AdClickCounter:
    def __init__(self, k_minutes: int) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def click(self, ad_id: str, timestamp: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def count(self, ad_id: str, timestamp: int) -> int:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in an AdClickCounter method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(AdClickCounter, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement AdClickCounter's methods first")
