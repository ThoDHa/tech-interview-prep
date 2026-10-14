"""Letter Combinations of a Phone Number: https://leetcode.com/problems/letter-combinations-of-a-phone-number/

Write-up & approaches: ../../../docs/leetcode/letter_combinations_of_a_phone_number.md

Given a string containing digits from `2-9`, return all letter combinations the
number could represent (telephone keypad mapping). Return the answer in any order.

  uv run python letter_combinations_of_a_phone_number/solution.py   # debug one case (see CASE below)
  uv run pytest letter_combinations_of_a_phone_number/              # run the test sets
"""

from collections import deque
from typing import List

from harness import NotSolved, pick_case


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """

        if not digits:
            return []
        digit_to_letters = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "pqrs",
            "8": "tuv",
            "9": "wxyz",
        }

        queue = deque([""])

        for digit in digits:
            letters = digit_to_letters[digit]
            for _ in range(len(queue)):
                current = queue.popleft()
                for letter in letters:
                    queue.append(current + letter)
        return list(queue)


if __name__ == "__main__":
    # Debug playground: set a breakpoint in letterCombinations above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().letterCombinations(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
