"""Letter Combinations of a Phone Number: https://leetcode.com/problems/letter-combinations-of-a-phone-number/

Write-up & approaches: ../../docs/problems/letter_combinations_of_a_phone_number.md

Given a string containing digits from `2-9`, return all letter combinations the
number could represent (telephone keypad mapping). Return the answer in any order.

  uv run python letter_combinations_of_a_phone_number/solution.py   # debug one case (see CASE below)
  uv run pytest letter_combinations_of_a_phone_number/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in letterCombinations above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().letterCombinations(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
