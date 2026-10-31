"""Find All People with the Secret — https://www.fastprep.io/problems/amazon-find-all-people-with-secret

Write-up & approaches: ../../../docs/amazon/amazon-find-all-people-with-secret.md

There are n people labeled from 0 to n - 1. At time 0, person 0 shares a secret with firstPerson.

  uv run python amazon/amazon-find-all-people-with-secret/solution.py   # debug one case (see CASE below)
  uv run pytest amazon/amazon-find-all-people-with-secret/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def findAllPeople(self, n, meetings, firstPerson):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findAllPeople above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findAllPeople(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
