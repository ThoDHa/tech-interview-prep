"""Happy Number — https://leetcode.com/problems/happy-number/

Write-up & approaches: ../../docs/problems/happy_number.md
Canonical reference implementation: the write-up's Floyd's Cycle Detection
solution (tortoise and hare, O(1) space). Your own attempt lives in
solution.py.

A **non-cyclical number** is an integer defined by the following algorithm:

* Given a positive integer, replace it with the sum of the squares of its
  digits.
* Repeat the above step until the number equals `1`, or it **loops infinitely
  in a cycle** which does not include `1`.
* If it stops at `1`, then the number is a **non-cyclical number**.

  uv run python happy_number/reference.py   # replay the example cases
  uv run pytest happy_number/               # run the test sets
"""

from harness import pick_case


class Solution:
    def isHappy(self, n: int) -> bool:
        """Report whether repeated digit-square-sums reach 1 or a cycle.

        Advances a slow runner one successor step and a fast runner two per
        round: inside a cycle the gap closes by one each round and the two
        collide, on the road to 1 the fast runner parks at 1 (its own
        successor), and the exit test tells the two endings apart.

        Args:
            n: Starting value, 1 <= n <= 1000 per the constraint range.

        Returns:
            True when the chain reaches 1, False when it cycles elsewhere.

        Time:  bounded rounds of O(log n) successor computations: three
            digit passes per round, and the runners meet within one cycle
            length (at most 243 values) once both are inside.
        Space: O(1): two runner variables, no visited history.
        """

        def next_number(value: int) -> int:
            total = 0
            while value > 0:
                value, digit = divmod(value, 10)
                total += digit * digit
            return total

        slow = n
        fast = next_number(n)
        while fast != 1 and slow != fast:
            slow = next_number(slow)
            fast = next_number(next_number(fast))
        return fast == 1


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().isHappy(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
