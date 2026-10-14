"""Design Twitter — https://leetcode.com/problems/design-twitter/

Write-up & approaches: ../../docs/problems/design_twitter.md
Reference implementation of the write-up's Min-Heap K-Way Merge solution, kept
next to the harness so authored cases stay falsifiable. Your own attempt
lives in solution.py.

  uv run python design_twitter/reference.py   # replay the example
  uv run pytest design_twitter/               # run the test sets
"""

import heapq
from collections import defaultdict
from typing import List


class Twitter:
    def __init__(self) -> None:
        """Start an empty Twitter with no tweets and no follow edges.

        Time:  O(1): two empty containers and a zeroed counter.
        Space: O(1): nothing stored yet beyond the containers themselves.
        """
        self.tweets: dict[int, list[tuple[int, int]]] = defaultdict(list)
        self.followees: dict[int, set[int]] = defaultdict(set)
        self.count = 0

    def postTweet(self, userId: int, tweetId: int) -> None:
        """Stamp `tweetId` with the next position on the global clock and
        append it to `userId`'s timeline, keeping the timeline chronological.

        Time:  O(1) average: one counter increment, one dict lookup, one
            list append.
        Space: O(1) per call: one (count, tweetId) entry stored.
        """
        self.count += 1
        self.tweets[userId].append((self.count, tweetId))

    def getNewsFeed(self, userId: int) -> List[int]:
        """Return the at most 10 most recent tweetIds posted by `userId` or
        anyone `userId` follows, newest first.

        Time:  O(A + 10 log A) per feed for A followed authors: heapify the
            A newest-unread heads in O(A), then at most 10 rounds of one
            O(log A) pop plus one O(log A) push.
        Space: O(A): the heads heap holds at most one entry per author.
        """
        feed_size = 10
        authors = self.followees[userId] | {userId}

        # Seed the heap with each author's newest tweet. Counts are negated
        # because heapq is a min-heap and the most recent (largest) count
        # must pop first; each entry carries its timeline index so the next
        # older tweet is reachable on pop.
        heads: list[tuple[int, int, int, int]] = []
        for author in authors:
            timeline = self.tweets[author]
            if timeline:
                count, tweet_id = timeline[-1]
                heads.append((-count, author, tweet_id, len(timeline) - 1))
        heapq.heapify(heads)

        feed: List[int] = []
        while heads and len(feed) < feed_size:
            _, author, tweet_id, index = heapq.heappop(heads)
            feed.append(tweet_id)
            if index > 0:
                count, previous_id = self.tweets[author][index - 1]
                heapq.heappush(heads, (-count, author, previous_id, index - 1))
        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        """Make `followerId` follow `followeeId`; self-follows are ignored.

        Time:  O(1) average: one set add.
        Space: O(1) per new edge: one set entry.
        """
        if followerId != followeeId:
            self.followees[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        """Make `followerId` stop following `followeeId`; a missing edge is
        a no-op.

        Time:  O(1) average: one set discard.
        Space: O(1): no retained state beyond the edge's removal.
        """
        self.followees[followerId].discard(followeeId)


if __name__ == "__main__":
    # Debug playground: cases.json is empty (multi-method starter), so
    # Example 1's operation sequence stands in.
    twitter = Twitter()
    operations = [
        ("postTweet", (1, 10)),
        ("postTweet", (2, 20)),
        ("getNewsFeed", (1,)),
        ("getNewsFeed", (2,)),
        ("follow", (1, 2)),
        ("getNewsFeed", (1,)),
        ("getNewsFeed", (2,)),
        ("unfollow", (1, 2)),
        ("getNewsFeed", (1,)),
    ]
    print("Twitter()")
    for method, args in operations:
        result = getattr(twitter, method)(*args)
        print(f"{method}{args} -> {result}")
