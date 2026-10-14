"""Merge Triplets to Form Target Triplet — https://leetcode.com/problems/merge-triplets-to-form-target-triplet/

Write-up & approaches: ../../docs/problems/merge_triplets_to_form_target_triplet.md
Reference implementation of the write-up's Greedy Component Flags solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python merge_triplets_to_form_target_triplet/reference.py   # replay the example cases
  uv run pytest merge_triplets_to_form_target_triplet/               # run the test sets
"""

from typing import List

from harness import pick_case


class Solution:
    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:
        """Return whether `target` is obtainable by merging `triplets`.

        Time:  O(n): one pass, a constant number of comparisons per triplet.
        Space: O(1): three flags, regardless of `n`.
        """
        good = [False, False, False]
        for a, b, c in triplets:
            if a > target[0] or b > target[1] or c > target[2]:
                continue
            good[0] = good[0] or a == target[0]
            good[1] = good[1] or b == target[1]
            good[2] = good[2] or c == target[2]
        return all(good)


if __name__ == "__main__":
    # Debug playground: cases.json holds the parsed example cases.
    for case_id in ("example_1", "example_2"):
        case = pick_case(__file__, case_id)
        result = Solution().mergeTriplets(*case["args"])
        print(f"case {case['id']}: args = {case['args']}")
        print(f"expected: {case['expected']}")
        print(f"got:      {result}")
