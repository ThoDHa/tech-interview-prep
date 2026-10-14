"""K Closest Points to Origin: https://leetcode.com/problems/k-closest-points-to-origin/

Write-up & approaches: ../../../docs/leetcode/k_closest_points_to_origin.md

Given an array of points `points[i] = [xi, yi]` and an integer `k`, return the
`k` points closest to the origin `(0, 0)` by Euclidean distance, in any order.

  uv run python k_closest_points_to_origin/solution.py     # debug one case (see CASE below)
  uv run pytest k_closest_points_to_origin/                # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """

        """
            What do I want to do?
            create a new list, and keep on finding the closest one and then once I get k items
            That's the brute force solution.


            Maxheap, where you use the minimum heap of the python library, where we add till k items
            then start doing replace. heapq, it's a max heap so how do you turn it to a min heap?


            QuickSelect, just uses the a partial quick sort, to sort the first k elements, but how?
            Only do left side if mid is less then k, then right if mid is greater than k.
            it keeps on sorting, till mid mid is k, then it's it.

            Just use built sorting algorithm.

            x1*x1 + y1*y1

        """


        k_list: List[List[int]] = []
        points = points.copy()
        for _ in range(k):

            best = 0
            best_dist = self.dist(points[best])
            for i in range(1, len(points)):
                curr_dist = self.dist(points[i])
                if curr_dist < best_dist:
                    best_dist = curr_dist
                    best = i
            k_list.append(points.pop(best))
        return k_list

    def dist(self, point: List[int]) -> int:
        return point[0]*point[0] + point[1]*point[1]

if __name__ == "__main__":
    # Debug playground: set a breakpoint in kClosest above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().kClosest(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
