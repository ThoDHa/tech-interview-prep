"""Group Students — https://www.fastprep.io/problems/amazon-group-students

Write-up & approaches: ../../../docs/problems/amazon_oa/amazon-group-students.md

Amazon Technical Academy (ATA) provides in-demand, technical training to current Amazon employees looking to broaden their skill sets. ATA has admitted a group of n prospective trainees with varying s

  uv run python amazon_oa/amazon-group-students/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/amazon-group-students/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def groupStudents(self, levels, maxSpread):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in groupStudents above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().groupStudents(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
