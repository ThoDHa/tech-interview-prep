"""Merge Triplets to Form Target Triplet — https://leetcode.com/problems/merge-triplets-to-form-target-triplet/

Write-up & approaches: ../../docs/problems/merge_triplets_to_form_target_triplet.md

You are given a 2D array of integers `triplets`, where `triplets[i] = [ai, bi, ci]` represents the `ith` **triplet**. You are also given an array of integers `target = [x, y, z]` which is the triplet 

  uv run python merge_triplets_to_form_target_triplet/solution.py   # debug one case (see CASE below)
  uv run pytest merge_triplets_to_form_target_triplet/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def mergeTriplets(self, triplets, target):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in mergeTriplets above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().mergeTriplets(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
