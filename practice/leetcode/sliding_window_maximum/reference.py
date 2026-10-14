"""Sliding Window Maximum — https://leetcode.com/problems/sliding-window-maximum/

Write-up & approaches: ../../docs/problems/sliding_window_maximum.md
Reference implementation of the write-up's Monotonic Deque solution.

You are given an array of integers `nums` and an integer `k`. There is a sliding window of size `k` that starts at the left edge of the array. The window slides one position to the right until it reaches the right edge of the array.

  uv run python sliding_window_maximum/reference.py   # debug one case (see CASE below)
  uv run pytest sliding_window_maximum/              # run the test sets
"""

from collections import deque

from harness import pick_case


class Solution:
    def maxSlidingWindow(self, nums, k):
        """Return the window maximum for each of the n - k + 1 windows.

        Maintains a deque of indices whose values are strictly decreasing:
        the front is always the current window's maximum. Each index is
        appended once and removed at most once, so the sweep is linear.

        Args:
            nums: List of window values, 1 <= len(nums).
            k: Window size, 1 <= k <= len(nums).

        Returns:
            List of len(nums) - k + 1 maxima, one per window position.

        Time:  O(n): every index enters and leaves the deque at most once.
        Space: O(k): the deque never holds more than k indices.
        """
        window = deque()
        result = []
        for i, value in enumerate(nums):
            while window and nums[window[-1]] <= value:
                window.pop()
            window.append(i)
            if window[0] <= i - k:
                window.popleft()
            if i >= k - 1:
                result.append(nums[window[0]])
        return result


if __name__ == "__main__":
    # Debug playground: set a breakpoint in maxSlidingWindow above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().maxSlidingWindow(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
