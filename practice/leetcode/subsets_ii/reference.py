"""Subsets II — https://leetcode.com/problems/subsets-ii/

Write-up & approaches: ../../docs/problems/subsets_ii.md
Reference implementation of the write-up's Sorted Backtracking solution,
kept next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python subsets_ii/reference.py   # debug one case (see below)
  uv run pytest subsets_ii/               # run the test sets
"""

from typing import List


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        """Return every distinct subset of `nums` in any order.

        Sorts `nums` so equal values sit side by side, then walks the
        subset backtracking tree over indices: every node records a copy
        of `current_subset`, and inside one loop level a value whose
        identical left neighbor was passed over is skipped, so each
        emitted subset takes a prefix of every run of equal values and
        no subset is ever produced twice.

        Args:
            nums: Integers, possibly with duplicates; 1 <= len(nums) <= 11,
                each value in [-20, 20].

        Returns:
            All distinct subsets. The order of the subsets, and of the
            values inside each subset, is arbitrary; equal values appear
            in sorted order because the input is sorted first.

        Time:  O(2^n x n): one O(n) copy per node of the deduplicated
            tree, which holds exactly one node per distinct subset, at
            most 2^n of them.
        Space: O(2^n x n) for the result plus O(n) recursion depth.
        """
        nums = sorted(nums)
        result: List[List[int]] = []

        def backtrack(start_index: int, current_subset: List[int]) -> None:
            result.append(current_subset[:])
            for i in range(start_index, len(nums)):
                if i > start_index and nums[i] == nums[i - 1]:
                    continue
                current_subset.append(nums[i])
                backtrack(i + 1, current_subset)
                current_subset.pop()

        backtrack(0, [])
        return result


if __name__ == "__main__":
    # Debug playground: set a breakpoint in subsetsWithDup above, then run this
    # file. cases.json is empty (any-order output), so a literal example
    # stands in.
    nums = [1, 2, 1]
    result = Solution().subsetsWithDup(nums)
    print(f"args = nums {nums}")
    print(f"got: {sorted(map(sorted, result))}")
