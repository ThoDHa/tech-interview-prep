"""Find The Duplicate Number — https://leetcode.com/problems/find-the-duplicate-number/

Write-up & approaches: ../../docs/problems/find_the_duplicate_number.md
Reference implementation of the write-up's Floyd's Cycle Detection solution.

You are given an array of integers `nums` containing `n + 1` integers. Each integer in `nums` is in the range `[1, n]` inclusive. There is exactly one repeated integer in `nums`, and every other integer appears at most once. Return the repeated integer.

  uv run python find_the_duplicate_number/reference.py   # debug one case (see CASE below)
  uv run pytest find_the_duplicate_number/              # run the test sets
"""

from harness import pick_case


class Solution:
    def findDuplicate(self, nums):
        """Return the single repeated value without modifying `nums`.

        Treats each index `i` as a node pointing to index `nums[i]`; the
        duplicate value is the entrance of the cycle this forms. Phase one
        advances a slow pointer one hop and a fast pointer two hops until
        they meet inside the cycle. Phase two resets `slow` to index 0 and
        advances both one hop at a time: they meet again exactly at the
        cycle entrance, the duplicate.

        Args:
            nums: `n + 1` integers, each in `1..n`, with exactly one value
                repeated (possibly more than twice).

        Returns:
            The repeated value.

        Time:  O(n): both phases advance the two pointers a linear number
            of hops combined.
        Space: O(1): two index variables; the array is only read.
        """
        slow = fast = 0
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        slow = 0
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        return slow


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findDuplicate above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().findDuplicate(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
