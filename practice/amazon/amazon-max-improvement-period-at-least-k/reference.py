"""Best Improvement Period of at Least K Intervals — https://www.fastprep.io/problems/amazon-max-improvement-period-at-least-k

Write-up & approaches: ../../../docs/amazon/amazon-max-improvement-period-at-least-k.md

Reference implementation of the write-up's recommended Cheapest Start
So Far solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-max-improvement-period-at-least-k/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-max-improvement-period-at-least-k/              # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def solve(self, changes: List[int], k: int) -> int:
        """Return the best score of any period of at least k intervals.

        The rule being optimized: a period [i, j] scores
        -changes[i] + changes[i+1] + ... + changes[j], its first change
        subtracted instead of added. With P the prefix sums of changes,
        that score is P[j+1] - (P[i+1] + changes[i]): an end term minus
        a start cost. Ends are walked left to right; each end admits
        exactly one new start (i = end - k + 1) and none ever leaves,
        so the cheapest admissible start cost is a running minimum and
        each end is scored in constant time.

        Args:
            changes: Nonempty list of interval changes; changes[i] may
                be any integer, positive or negative.
            k: Minimum period length, 1 <= k <= len(changes).

        Returns:
            The maximum score over all periods [i, j] with
            j - i + 1 >= k.

        Time:  O(n): one pass builds the prefix array, one pass over
               the ends admits each start and scores each end once.
        Space: O(n): the prefix array; the running minimum and the
               answer are two scalars.
        """
        periods = len(changes)
        prefix = [0] * (periods + 1)
        for t in range(periods):
            prefix[t + 1] = prefix[t] + changes[t]
        best = None
        cheapest = None
        for end in range(k - 1, periods):
            start = end - k + 1
            start_cost = prefix[start + 1] + changes[start]
            if cheapest is None or start_cost < cheapest:
                cheapest = start_cost
            candidate = prefix[end + 1] - cheapest
            if best is None or candidate > best:
                best = candidate
        return best


if __name__ == "__main__":
    # Debug playground: set a breakpoint in solve above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().solve(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
