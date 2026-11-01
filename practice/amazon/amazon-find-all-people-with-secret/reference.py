"""Find All People with the Secret — https://www.fastprep.io/problems/amazon-find-all-people-with-secret

Write-up & approaches: ../../../docs/amazon/amazon-find-all-people-with-secret.md

Reference implementation of the write-up's recommended Per-Time BFS
on Meeting Groups solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-find-all-people-with-secret/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-find-all-people-with-secret/              # run the test sets
"""

from collections import defaultdict, deque
from typing import DefaultDict, List

from harness import pick_case


class Solution:
    def findAllPeople(self, n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
        """Return everyone who knows the secret after all meetings, ascending.

        A meeting connects its participants only at its own timestamp,
        and sharing inside one timestamp is instantaneous regardless of
        input order, so the timeline decomposes into independent
        time groups processed in increasing order. Within a group, the
        participants and their meeting edges form a small graph; one
        breadth-first sweep seeded with the group members who already
        hold the secret adds exactly the people reachable from them
        through that group's edges, and every person reached joins the
        holders permanently. Sorting the distinct times is the only
        global work.

        Args:
            n: The people, labeled 0 through n - 1.
            meetings: Rows [x, y, time]; unsorted, repeatable, and
                possibly sharing timestamps.
            firstPerson: The person who learns the secret at time 0
                alongside person 0.

        Returns:
            The secret holders after all meetings, in ascending order.

        Time:  O(m log m + n log n): grouping sorts the distinct time
            keys, and each meeting edge is traversed a constant number
            of times inside its group; the final sort of holders is
            comparison-based, O(n log n) in the worst case.
        Space: O(m): the grouped map and per-group adjacency.
        """
        holders = {0, firstPerson}
        by_time: DefaultDict[int, List[List[int]]] = defaultdict(list)
        for person, other, time in meetings:
            by_time[time].append([person, other])

        for time in sorted(by_time):
            edges = by_time[time]
            adjacency: DefaultDict[int, List[int]] = defaultdict(list)
            for person, other in edges:
                adjacency[person].append(other)
                adjacency[other].append(person)

            frontier = deque(member for member in adjacency if member in holders)
            while frontier:
                person = frontier.popleft()
                for neighbor in adjacency[person]:
                    if neighbor not in holders:
                        holders.add(neighbor)
                        frontier.append(neighbor)

        return sorted(holders)


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findAllPeople above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().findAllPeople(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
