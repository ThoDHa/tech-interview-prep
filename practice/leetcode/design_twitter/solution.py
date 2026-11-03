"""Design Twitter — https://leetcode.com/problems/design-twitter/

Write-up & approaches: ../../../docs/leetcode/design_twitter.md

Implement a simplified version of Twitter which allows users to post tweets, follow/unfollow each other, and view the `10` most recent tweets within their own news feed. Users and tweets are uniquely 

  uv run python leetcode/design_twitter/solution.py   # debug one case (see CASE below)
  uv run pytest leetcode/design_twitter/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case, run_operations


class Twitter:
    def __init__(self) -> None:
        # Initialize empty state here; methods below raise until implemented.
        pass

    def postTweet(self, userId: int, tweetId: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def getNewsFeed(self, userId: int) -> List[int]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def follow(self, followerId: int, followeeId: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved

    def unfollow(self, followerId: int, followeeId: int) -> None:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in a Twitter method, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "empty_constructor_only"
    case = pick_case(__file__, CASE)
    print(f"case {case['id']}: operations = {case['operations']}")
    print(f"arguments: {case['arguments']}")
    print(f"expected:  {case['expected']}")
    try:
        result = run_operations(Twitter, case["operations"], case["arguments"])
        print(f"got:       {result}")
    except NotSolved:
        print("got:       implement Twitter's methods first")
