"""Are Two People Relatives in a Family Tree? — https://www.fastprep.io/problems/amazon-family-tree-relatives

Write-up & approaches: ../../../docs/amazon/amazon-family-tree-relatives.md

Reference implementation of the write-up's recommended Early-Exit
Ancestor Walk solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-family-tree-relatives/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-family-tree-relatives/              # run the test sets
"""

from collections import deque
from typing import DefaultDict, List

from harness import pick_case


class Solution:
    def solve(self, relations: List[List[str]], first: str, second: str) -> bool:
        """Return whether two people share at least one ancestor.

        Each person counts as one of their own ancestors, so `first`'s
        ancestor set is seeded with `first` itself and grown by walking
        parent edges until the frontier drains. The second walk then
        starts at `second` (also its own ancestor) and returns True at
        the first person the first walk already recorded; it can stop
        there because every later person on that walk is a strictly
        higher ancestor, so the first hit is as deep as any can be.

        Args:
            relations: Rows `[parent, child]`; a child may have up to
                two recorded parents.
            first: One queried person.
            second: The other queried person.

        Returns:
            True when the two share at least one ancestor (including
            the case `first == second`), False otherwise.

        Time:  O(people + relations): each person enters an ancestor
            frontier at most once per walk.
        Space: O(people + relations): the parent map and the first
            walk's ancestor set.
        """
        parents_of: DefaultDict[str, List[str]] = DefaultDict(list)
        for parent, child in relations:
            parents_of[child].append(parent)

        ancestors_of_first = {first}
        frontier = deque([first])
        while frontier:
            person = frontier.popleft()
            for parent in parents_of[person]:
                if parent not in ancestors_of_first:
                    ancestors_of_first.add(parent)
                    frontier.append(parent)

        visited = {second}
        frontier = deque([second])
        while frontier:
            person = frontier.popleft()
            if person in ancestors_of_first:
                return True
            for parent in parents_of[person]:
                if parent not in visited:
                    visited.add(parent)
                    frontier.append(parent)
        return False


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
