# [Design Twitter](https://leetcode.com/problems/design-twitter/)

**Medium** | **25 minutes** | **Hash Table, Linked List, Design, Heap (Priority Queue)**

**Pattern:** [Heap / Priority Queue](../patterns/heap/intuition.md), [Data-Structure Design](../patterns/design/intuition.md)

**Algorithm:** [Heap (data structure)](https://en.wikipedia.org/wiki/Heap_(data_structure)) · [K-way merge](https://en.wikipedia.org/wiki/K-way_merge_algorithm) · [Hash table](https://en.wikipedia.org/wiki/Hash_table)

**Practice:** [`practice/leetcode/design_twitter/solution.py`](../../practice/leetcode/design_twitter/solution.py)

Implement a simplified version of Twitter which allows users to post tweets, follow/unfollow each other, and view the `10` most recent tweets within their own news feed.

Users and tweets are uniquely identified by their IDs (integers).

Implement the following methods:

* `Twitter()` Initializes the twitter object.
* `void postTweet(int userId, int tweetId)` Publish a new tweet with ID `tweetId` by the user `userId`. You may assume that each `tweetId` is unique.
* `List<Integer> getNewsFeed(int userId)` Fetches at most the `10` most recent tweet IDs in the user's news feed. Each item must be posted by users who the user is following or by the user themself. Tweets IDs should be **ordered from most recent to least recent**.
* `void follow(int followerId, int followeeId)` The user with ID `followerId` follows the user with ID `followeeId`.
* `void unfollow(int followerId, int followeeId)` The user with ID `followerId` unfollows the user with ID `followeeId`.

## Examples

### Example 1

**Input:** `["Twitter", "postTweet", [1, 10], "postTweet", [2, 20], "getNewsFeed", [1], "getNewsFeed", [2], "follow", [1, 2], "getNewsFeed", [1], "getNewsFeed", [2], "unfollow", [1, 2], "getNewsFeed", [1]]`

**Output:** `[null, null, null, [10], [20], null, [20, 10], [20], null, [10]]`

**Explanation:** Twitter twitter = new Twitter();
twitter.postTweet(1, 10); // User 1 posts a new tweet with id = 10.
twitter.postTweet(2, 20); // User 2 posts a new tweet with id = 20.
twitter.getNewsFeed(1);   // User 1's news feed should only contain their own tweets -> [10].
twitter.getNewsFeed(2);   // User 2's news feed should only contain their own tweets -> [20].
twitter.follow(1, 2);     // User 1 follows user 2.
twitter.getNewsFeed(1);   // User 1's news feed should contain both tweets from user 1 and user 2 -> [20, 10].
twitter.getNewsFeed(2);   // User 2's news feed should still only contain their own tweets -> [20].
twitter.unfollow(1, 2);   // User 1 unfollows user 2.
twitter.getNewsFeed(1);   // User 1's news feed should only contain their own tweets -> [10].

## Constraints

- `1 <= userId, followerId, followeeId <= 500`
- `0 <= tweetId <= 10^4`
- All the tweets have **unique** IDs.
- At most `3 * 10^4` calls will be made to `postTweet`, `getNewsFeed`, `follow`, and `unfollow`.
- A user cannot follow themself.

## Deriving the Solution

Nothing in the input orders tweets by ID: an ID only promises uniqueness. The one order the problem defines is the order `postTweet` calls arrive, so every solution starts by stamping each tweet with a monotonically increasing counter at posting time and keeping each user's timeline in stamp order. After that, `getNewsFeed(userId)` is always the same question, "which are the 10 largest stamps among the authors `userId` follows, plus their own?", and the solutions differ only in how they run that selection.

1. **Start literal.** On each `getNewsFeed` call, flatten every tweet of every
   followed author into one candidate pool, then take the newest ten by hand:
   each of ten rounds scans the pool for the largest stamp, appends the winner
   to the feed, and removes it, at `O(C)` per feed for `C` candidate tweets:
   see [Brute Force](#brute-force).
2. **Spot the waste.** The candidates are `A` already-sorted timelines, and the
   newest tweet not yet fed always sits at some author's timeline head: keep one
   cursor per author and repeatedly emit whichever cursor holds the newest
   stamp, materializing no candidate pool at all. At most ten emissions, each
   found by one linear scan over the cursors: see
   [Repeated Maximum Scan](#repeated-maximum-scan).
3. **Reach for the k-way merge.** "Repeatedly take the newest head of several
   sorted streams" is the merge step of a [k-way merge](https://en.wikipedia.org/wiki/K-way_merge_algorithm),
   and a min-heap of stream heads finds each next element in `O(log A)` instead
   of a fresh scan: see [Min-Heap K-Way Merge](#min-heap-k-way-merge).
4. **Delegate the ordering.** The ranking the by-hand rounds perform is exactly
   what the language's sort provides in one call, at `O(C log C)` per feed: see
   [Flatten and Sort](#flatten-and-sort).
5. **Let the library select.** `heapq.nlargest(10, candidates)` packages exactly
   this top-10 selection, keeping its working set at 10 entries while it sweeps
   the candidates once: see
   [Bounded Heap Selection](#bounded-heap-selection).

## Solutions

### Brute Force

#### Derivation

The most literal reading of `getNewsFeed` is "collect the authors' tweets, then read off the ten newest". `postTweet` appends each tweet to its author's timeline, so the timelines are chronological; stamping each entry with the global counter's value at posting time makes "newest" a plain numeric comparison on that stamp. The comparison key is the stamp, never the `tweetId`: IDs carry no order, and ranking by ID would silently misorder the feed. The selection itself stays hand-rolled, acting the feed out emission by emission: scan for the largest stamp, take that tweet, remove it, and repeat:

1. `__init__` keeps `tweets`, a map from `userId` to its chronological list of
   `(count, tweetId)` entries, `followees`, a map from follower to a set of
   followees, and `count`, starting at `0`.
2. `postTweet` increments `count` and appends `(count, tweetId)` to
   `tweets[userId]`.
3. `getNewsFeed` unions `followees[userId]` with `{userId}` into `authors`,
   flattens every author's timeline into `candidates`, then runs `feed_size`
   rounds: each round scans `candidates` for the largest stamp, tracking it in
   `newest_index`, appends the winner's `tweetId` to `feed`, and pops the
   winner from `candidates`.
4. `follow` adds to the `followees` set, refusing a self-edge, and `unfollow`
   discards from it.

#### Walkthrough

Trace Example 1. Each entry shows the state after the call; `getNewsFeed` lines show the union into `authors`, the flattened `candidates`, the winner each round takes, and the feed it builds:

```text
postTweet(1, 10)   tweets = {1: [(1, 10)]}
postTweet(2, 20)   tweets = {1: [(1, 10)], 2: [(2, 20)]}
getNewsFeed(1)     authors = [1]       candidates = [(1, 10)]          round 1 takes (1, 10)                         feed = [10]
getNewsFeed(2)     authors = [2]       candidates = [(2, 20)]          round 1 takes (2, 20)                         feed = [20]
follow(1, 2)       followees = {1: {2}}
getNewsFeed(1)     authors = [1, 2]    candidates = [(1, 10), (2, 20)] round 1 takes (2, 20), round 2 takes (1, 10)  feed = [20, 10]
getNewsFeed(2)     authors = [2]       candidates = [(2, 20)]          round 1 takes (2, 20)                         feed = [20]
unfollow(1, 2)     followees = {1: {}}
getNewsFeed(1)     authors = [1]       candidates = [(1, 10)]          round 1 takes (1, 10)                         feed = [10]
```

Each tweet entry is `(count, tweetId)`: tweet `10` was posted first and carries stamp `1`, tweet `20` carries stamp `2`. Before the follow, user `1`'s feed is its own tweet; after `follow(1, 2)` the union widens to `[1, 2]` and the round scans take stamp `2` (tweet `20`) first and stamp `1` (tweet `10`) second, producing the expected `[20, 10]`; `unfollow` narrows the union back and the feed returns to `[10]`, matching the expected Output. Example 1's pools are too small to reach the round loop's cap: the two-candidate call's round 3 finds `candidates` empty and the `break` guard ends the loop there with the feed already complete. The cap itself needs a tailored input: with twelve tweets in `candidates`, round 10 takes the tenth newest and `range(feed_size)` ends the loop there, two candidates never read.

#### Solution

The code is the flatten and the scan-take-remove rounds from the walkthrough.

```python
from collections import defaultdict
from typing import List


class Twitter:
    def __init__(self) -> None:
        self.tweets: dict[int, list[tuple[int, int]]] = defaultdict(list)
        self.followees: dict[int, set[int]] = defaultdict(set)
        self.count = 0

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.count += 1
        self.tweets[userId].append((self.count, tweetId))

    def getNewsFeed(self, userId: int) -> List[int]:
        feed_size = 10
        authors = self.followees[userId] | {userId}
        candidates = [tweet for author in authors for tweet in self.tweets[author]]
        feed: List[int] = []
        for _ in range(feed_size):
            if not candidates:
                break
            newest_index = 0
            for index in range(1, len(candidates)):
                if candidates[index][0] > candidates[newest_index][0]:
                    newest_index = index
            feed.append(candidates.pop(newest_index)[1])
        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId != followeeId:
            self.followees[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.followees[followerId].discard(followeeId)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(C)` per `getNewsFeed`

Where `C` is the total number of tweets posted by the authors in the feed. The flatten touches all `C` candidates once, and each of the ten rounds scans and pops within a pool of at most `C` entries, a constant number of linear passes; `postTweet`, `follow`, and `unfollow` are `O(1)` average set and list operations.

##### Space Complexity: `O(C)` per `getNewsFeed`

`candidates` materializes every tweet of every followed author, regardless of how few survive the ten rounds.

#### Key Insights

- The stamp counter, not the `tweetId`, defines recency; deriving order from IDs is the classic bug here because IDs only promise uniqueness.
- Every feed pays to look at the authors' whole histories, although each author's timeline is already sorted by construction.
- Taking the winners one at a time needs no ordering of the losers, but every round re-scans a pool that shrank by only one; the later solutions attack that pool two ways: the next two never materialize it, and the last two hand the ordering or the bounded selection to the standard library.

### Repeated Maximum Scan

#### Derivation

The brute force flattens every candidate into one pool and re-scans that pool for every emission. But each timeline is stamp-ordered, so the newest tweet not yet fed is always at some author's cursor head, and the pool never needs to exist: the feed can be produced by ten rounds of one question, "which author's cursor holds the newest stamp?" Each round answers it with a linear scan over the cursors, emits the winner, and retreats that one cursor:

1. Build `cursors`, one entry per author, pointing at each timeline's last index
   (its newest tweet); an empty timeline starts at `-1`, already exhausted.
2. For each of at most 10 slots: scan `cursors` for the maximum stamp
   `tweets[author][cursor][0]`, tracking it in `newest_count` and its author in
   `newest_author`.
3. When no live cursor remains, stop early; otherwise append the winner's
   `tweetId` to `feed` and decrement that author's cursor.

#### Walkthrough

Example 1 never shows a cursor retreating, so take a tailored input: user `1` follows users `2` and `3`; the post order is `1` posts `40`, `2` posts `20`, `3` posts `30`, `2` posts `10`, `3` posts `50`, so the stamps are `1..5` in that order and the IDs deliberately do not follow it. Each row shows the cursors at the start of a round as `author: (count, tweetId)`, with `done` marking an exhausted cursor:

```text
round 1   cursors = {1: (1, 40), 2: (4, 10), 3: (5, 50)}   max stamp 5, author 3   emit 50
round 2   cursors = {1: (1, 40), 2: (4, 10), 3: (3, 30)}   max stamp 4, author 2   emit 10
round 3   cursors = {1: (1, 40), 2: (2, 20), 3: (3, 30)}   max stamp 3, author 3   emit 30
round 4   cursors = {1: (1, 40), 2: (2, 20), 3: done}      max stamp 2, author 2   emit 20
round 5   cursors = {1: (1, 40), 2: done, 3: done}         max stamp 1, author 1   emit 40
```

Each round retreats exactly one cursor, the one that won, and the feed comes out `[50, 10, 30, 20, 40]`: the five tweets in stamp order, descending, even though the IDs bounce around, which is the stamp discipline doing its job. With fewer than ten tweets in total the cursors all hit `done` and the loop stops early.

#### Solution

```python
from collections import defaultdict
from typing import List


class Twitter:
    def __init__(self) -> None:
        self.tweets: dict[int, list[tuple[int, int]]] = defaultdict(list)
        self.followees: dict[int, set[int]] = defaultdict(set)
        self.count = 0

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.count += 1
        self.tweets[userId].append((self.count, tweetId))

    def getNewsFeed(self, userId: int) -> List[int]:
        feed_size = 10
        authors = self.followees[userId] | {userId}
        cursors = {author: len(self.tweets[author]) - 1 for author in authors}
        feed: List[int] = []
        for _ in range(feed_size):
            newest_author = None
            newest_count = 0
            for author, cursor in cursors.items():
                if cursor >= 0 and self.tweets[author][cursor][0] > newest_count:
                    newest_count = self.tweets[author][cursor][0]
                    newest_author = author
            if newest_author is None:
                break
            feed.append(self.tweets[newest_author][cursors[newest_author]][1])
            cursors[newest_author] -= 1
        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId != followeeId:
            self.followees[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.followees[followerId].discard(followeeId)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(A)` per `getNewsFeed`

Where `A` is the number of authors in the feed. Building `cursors` is one pass over the authors, and the loop runs at most 10 rounds, each scanning at most `A` cursors; with the feed size fixed at 10, the total is a constant number of linear passes.

##### Space Complexity: `O(A)` per `getNewsFeed`

One cursor entry per author, and nothing else grows with history length.

#### Key Insights

- The candidates are never materialized: the scan touches only the `A` cursor heads, so authors with long histories cost nothing extra.
- Stopping when every cursor is exhausted returns short feeds correctly, which a slice-based approach gets only by luck.
- The repeated argmax over cursors is the whole cost; the next solution hands exactly that job to a heap, the way a k-way merge does.

### Min-Heap K-Way Merge

#### Derivation

The scan forgets each round's comparisons and re-scans every author to find the next newest. But emitting the running maximum of several sorted streams is precisely the merge step of a [k-way merge](https://en.wikipedia.org/wiki/K-way_merge_algorithm), and the standard tool there is a min-heap of stream heads: seed it with one head per stream, then pop the overall newest and push that stream's next element. Python's `heapq` is a min-heap and must pop the most recent tweet first, so the counts are stored negated. Each heap entry carries its timeline index, so the previous tweet of the popped author is reachable without a scan:

1. Union `followees[userId]` with `{userId}` into `authors`.
2. Seed `heads` with `(-count, author, tweetId, index)` for each author whose
   timeline is non-empty, taking its last entry, then `heapify`.
3. While `heads` is non-empty and `feed` holds fewer than 10: pop the smallest
   tuple, append its `tweetId` to `feed`, and when `index > 0` push
   `(-count, author, previousId, index - 1)` for the timeline entry before it.
4. Return `feed`.

#### Invariant

The heap `heads` always holds, for each author with tweets left, exactly that author's newest tweet not yet added to `feed`; therefore the largest count in `heads` is the next tweet the feed must emit:

$$ \text{next emit} = \operatorname*{arg\,max}_{\,(-c,\; a,\; t,\; i)\, \in\, \text{heads}} \; c $$

```text
heads     = one (negated count, author, tweetId, index) per author
            with tweets left, each the author's newest unfed tweet
next emit = the entry whose count is largest = whose negated count is smallest
```

Every branch preserves it. Seeding adds each author's last timeline entry, which is its newest tweet. Popping removes the largest count and appends it to `feed`, so that entry is no longer unfed; the push of the entry at `index - 1` restores the "newest unfed" fact for that author, because the timeline is stamp-ordered so index `index - 1` is exactly the next one down. Exhausted authors simply drop out of the heap. At exit, `feed` holds the tweets popped in descending count order, the 10 newest (or all there are), which is the contract.

#### Walkthrough

Reuse the tailored input from the previous walkthrough: user `1` follows users `2` and `3`; the post order is `40, 20, 30, 10, 50` by IDs `1..5` as stamps. The seed heapifies one head per author, then each row is one loop iteration; the `heads` lists are CPython's real heap arrays after the pop and push, whose interior order is an artifact of sifting, with only the pop order meaningful:

```text
seed     heapify -> [(-5, 3, 50, 1), (-4, 2, 10, 1), (-1, 1, 40, 0)]
pop 50   feed = [50]                    heads = [(-4, 2, 10, 1), (-1, 1, 40, 0), (-3, 3, 30, 0)]
pop 10   feed = [50, 10]                heads = [(-3, 3, 30, 0), (-1, 1, 40, 0), (-2, 2, 20, 0)]
pop 30   feed = [50, 10, 30]            heads = [(-2, 2, 20, 0), (-1, 1, 40, 0)]
pop 20   feed = [50, 10, 30, 20]        heads = [(-1, 1, 40, 0)]
pop 40   feed = [50, 10, 30, 20, 40]    heads = []
```

The pops descend by count, `5, 4, 3, 2, 1`, so the feed is `[50, 10, 30, 20, 40]`, the same result the scan produced, with each replacement pushed by the popped entry's `index - 1` instead of found by a fresh scan.

#### Solution

```python
import heapq
from collections import defaultdict
from typing import List


class Twitter:
    def __init__(self) -> None:
        self.tweets: dict[int, list[tuple[int, int]]] = defaultdict(list)
        self.followees: dict[int, set[int]] = defaultdict(set)
        self.count = 0

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.count += 1
        self.tweets[userId].append((self.count, tweetId))

    def getNewsFeed(self, userId: int) -> List[int]:
        feed_size = 10
        authors = self.followees[userId] | {userId}

        heads = []
        for author in authors:
            timeline = self.tweets[author]
            if timeline:
                count, tweetId = timeline[-1]
                heads.append((-count, author, tweetId, len(timeline) - 1))
        heapq.heapify(heads)

        feed: List[int] = []
        while heads and len(feed) < feed_size:
            _, author, tweetId, index = heapq.heappop(heads)
            feed.append(tweetId)
            if index > 0:
                count, previousId = self.tweets[author][index - 1]
                heapq.heappush(heads, (-count, author, previousId, index - 1))
        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId != followeeId:
            self.followees[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.followees[followerId].discard(followeeId)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(A + 10 log A)` per `getNewsFeed`

Where `A` is the number of authors in the feed. Seeding touches each author once and `heapify` is `O(A)`; the loop performs at most 10 rounds, each one `O(log A)` pop plus `O(log A)` push. The `heapify` term dominates for large `A`, but the per-emission cost drops from the scan's fresh `O(A)` pass to `O(log A)`.

##### Space Complexity: `O(A)` per `getNewsFeed`

The heap holds at most one entry per author, regardless of how long each author's history is.

#### Key Insights

- Negating the counts turns a min-heap into a newest-first pop order; the author and timeline index ride along so each pop can push that author's next tweet in `O(1)`.
- The heap stays at `A` entries no matter how long the histories are, and at most 10 pops happen per feed.
- Against the scan, the win is the per-emission cost: `O(log A)` replacement instead of an `O(A)` re-scan, while both share the `O(A)` setup.

### Flatten and Sort

#### Derivation

The approaches above produced the newest-first order themselves, stamp by stamp. Once `candidates` exists, that ordering is exactly what the language's sort provides: `sorted(candidates, reverse=True)` ranks the entries by descending stamp in one call, and the first ten are the feed. This approach delegates the ranking instead of running rounds by hand, trading the brute force's ten per-emission passes for one full comparison sort:

1. Build `candidates` exactly as the brute force does.
2. `sorted(candidates, reverse=True)` puts the newest stamp first.
3. Slice the first ten, strip the stamps, and return the IDs.

#### Walkthrough

Trace Example 1. Each entry shows the state after the call; `getNewsFeed` lines show the union into `authors`, the flattened `candidates`, the newest-first ordering, and the stamps stripped:

```text
postTweet(1, 10)   tweets = {1: [(1, 10)]}
postTweet(2, 20)   tweets = {1: [(1, 10)], 2: [(2, 20)]}
getNewsFeed(1)     authors = [1]       candidates = [(1, 10)]          newest-first -> [(1, 10)]            feed = [10]
getNewsFeed(2)     authors = [2]       candidates = [(2, 20)]          newest-first -> [(2, 20)]            feed = [20]
follow(1, 2)       followees = {1: {2}}
getNewsFeed(1)     authors = [1, 2]    candidates = [(1, 10), (2, 20)] newest-first -> [(2, 20), (1, 10)]   feed = [20, 10]
getNewsFeed(2)     authors = [2]       candidates = [(2, 20)]          newest-first -> [(2, 20)]            feed = [20]
unfollow(1, 2)     followees = {1: {}}
getNewsFeed(1)     authors = [1]       candidates = [(1, 10)]          newest-first -> [(1, 10)]            feed = [10]
```

Each tweet entry is `(count, tweetId)`: tweet `10` was posted first and carries stamp `1`, tweet `20` carries stamp `2`. Before the follow, user `1`'s feed is its own tweet; after `follow(1, 2)` the union widens to `[1, 2]` and the sort puts stamp `2` (tweet `20`) first, producing the expected `[20, 10]`; `unfollow` narrows the union back and the feed returns to `[10]`, matching the expected Output.

#### Solution

The code is the flatten and the delegated ranking from the walkthrough.

```python
from collections import defaultdict
from typing import List


class Twitter:
    def __init__(self) -> None:
        self.tweets: dict[int, list[tuple[int, int]]] = defaultdict(list)
        self.followees: dict[int, set[int]] = defaultdict(set)
        self.count = 0

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.count += 1
        self.tweets[userId].append((self.count, tweetId))

    def getNewsFeed(self, userId: int) -> List[int]:
        feed_size = 10
        authors = self.followees[userId] | {userId}
        candidates = [tweet for author in authors for tweet in self.tweets[author]]
        newest_first = sorted(candidates, reverse=True)[:feed_size]
        return [tweetId for _, tweetId in newest_first]

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId != followeeId:
            self.followees[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.followees[followerId].discard(followeeId)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(C log C)` per `getNewsFeed`

Where `C` is the total number of tweets posted by the authors in the feed. The flatten touches all `C` candidates and the descending sort comparison-sorts all of them, although only ten survive the slice.

##### Space Complexity: `O(C)` per `getNewsFeed`

`candidates` materializes every tweet of every followed author, and the sorted copy holds the entries again.

#### Key Insights

- The delegation is shorthand, not a new mechanism: the stamp discipline and the newest-first ranking were already derived by hand in the approaches above.
- Sorting all `C` candidates orders entries the slice never reads, the waste a bounded selection avoids.
- The sorted call is what `heapq.nlargest` below improves on: same result, working set capped at ten.

### Bounded Heap Selection

#### Derivation

The merge manages its heap by hand because it must keep `A` streams flowing. The feed only needs 10 survivors, and that exact selection is `heapq.nlargest(10, candidates)`: it seeds a min-heap with the first 10 candidates, sweeps the rest evicting the root whenever a candidate is strictly newer, and returns the 10 survivors sorted descending. The working set stays at 10 entries; the candidate list it sweeps is the brute force's flatten, which is the cost left on the table:

1. Build `candidates` exactly as the brute force does.
2. `heapq.nlargest(feed_size, candidates)` returns the 10 largest
   `(count, tweetId)` tuples, newest first.
3. Strip the stamps and return the IDs.

#### Walkthrough

Take a tailored single-author overload: one user posts 12 tweets with IDs `[5, 11, 8, 2, 14, 6, 1, 13, 3, 12, 9, 4]`, so the candidates are the `(count, tweetId)` pairs below. `heapify` leaves the first 10 in place because a sorted prefix already satisfies the heap property; each later post evicts the root only when it is strictly newer:

```text
seed   candidates 1..10  heapify ->
        [(1, 5), (2, 11), (3, 8), (4, 2), (5, 14), (6, 6), (7, 1), (8, 13), (9, 3), (10, 12)]
post (11, 9)  root (1, 5) < candidate   evict (1, 5)
        heap = [(2, 11), (4, 2), (3, 8), (8, 13), (5, 14), (6, 6), (7, 1), (11, 9), (9, 3), (10, 12)]
post (12, 4)  root (2, 11) < candidate  evict (2, 11)
        heap = [(3, 8), (4, 2), (6, 6), (8, 13), (5, 14), (12, 4), (7, 1), (11, 9), (9, 3), (10, 12)]
sort survivors descending ->
        [(12, 4), (11, 9), (10, 12), (9, 3), (8, 13), (7, 1), (6, 6), (5, 14), (4, 2), (3, 8)]
feed = [4, 9, 12, 3, 13, 1, 6, 14, 2, 8]
```

The two overflow posts evicted stamps `1` and `2`, the only tweets that fell out of the newest 10, and the final descending sort reads straight off the survivors: the feed is the 10 newest IDs, `[4, 9, 12, 3, 13, 1, 6, 14, 2, 8]`, stamps `12` down to `3`.

#### Solution

```python
import heapq
from collections import defaultdict
from typing import List


class Twitter:
    def __init__(self) -> None:
        self.tweets: dict[int, list[tuple[int, int]]] = defaultdict(list)
        self.followees: dict[int, set[int]] = defaultdict(set)
        self.count = 0

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.count += 1
        self.tweets[userId].append((self.count, tweetId))

    def getNewsFeed(self, userId: int) -> List[int]:
        feed_size = 10
        authors = self.followees[userId] | {userId}
        candidates = [tweet for author in authors for tweet in self.tweets[author]]
        return [tweetId for _, tweetId in heapq.nlargest(feed_size, candidates)]

    def follow(self, followerId: int, followeeId: int) -> None:
        if followerId != followeeId:
            self.followees[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.followees[followerId].discard(followeeId)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(C)` per `getNewsFeed`

Where `C` is the total number of tweets posted by the authors in the feed. The flatten is `O(C)`, and the sweep performs at most one `O(log 10)` heap replacement per candidate, a constant per step, so the selection stays linear.

##### Space Complexity: `O(C)` per `getNewsFeed`

`candidates` materializes every followed tweet, while the selection's own working set is capped at 10 entries.

#### Key Insights

- `heapq.nlargest(k, xs)` matches the Flatten and Sort approach above in result but keeps its working set at `k` entries, evicting through a conditional root replacement instead of re-sorting.
- The `C`-sized flatten is the remaining waste; avoiding it requires walking the per-author timelines, which is what the merge solution does.
- The internal evictions remove exactly the tweets that fall out of the newest 10, the same bookkeeping the merge's capped heap performs, handed to the library.

## Comparison of Solutions

`A` is the number of authors in the feed (followees plus the user themself); `C` is the total number of tweets those authors have posted.

### Time Complexity

- **Brute Force**: `O(C)` - flatten plus ten scan-and-remove rounds over the candidate pool.
- **Repeated Maximum Scan**: `O(A)` - at most ten linear passes over the `A` cursors.
- **Min-Heap K-Way Merge**: `O(A + 10 log A)` - `O(A)` to heapify one head per author, then at most ten `O(log A)` pops.
- **Flatten and Sort**: `O(C log C)` - flatten plus a full descending sort of all `C` candidates.
- **Bounded Heap Selection**: `O(C)` - linear flatten plus a sweep whose heap work is constant per candidate.

### Space Complexity

- **Brute Force**: `O(C)` - the full candidate pool.
- **Repeated Maximum Scan**: `O(A)` - one cursor per author.
- **Min-Heap K-Way Merge**: `O(A)` - one heap entry per author.
- **Flatten and Sort**: `O(C)` - the candidate list plus the sorted copy.
- **Bounded Heap Selection**: `O(C)` - the full candidate list, plus a selection heap capped at 10.

### Trade-offs

- **Brute Force**: Needs nothing beyond scans and a list, but every emission re-scans a pool holding the authors' entire histories.
- **Repeated Maximum Scan**: Never materializes candidates, so history length is irrelevant, but each emission re-scans every author.
- **Min-Heap K-Way Merge**: The scan's mechanism with the argmax handed to a heap; a little more machinery (negated counts, timeline indices) buys `O(log A)` emissions and the standard shape that scales with the feed cap.
- **Flatten and Sort**: The shortest statement of the flatten reading, but it orders every candidate when only ten survive.
- **Bounded Heap Selection**: The shortest capped implementation, but it flattens all `C` candidates to hand them to the library.

### When to Use Each

- **Brute Force**: A first working version while the API settles, or feeds so small the pool is irrelevant.
- **Repeated Maximum Scan**: When avoiding any candidate buffer matters and author counts stay modest.
- **Min-Heap K-Way Merge** (recommended): The default; per-author histories stay unmaterialized and each of the ten emissions costs `O(log A)` instead of a fresh scan.
- **Flatten and Sort**: When the candidates are at hand anyway and a one-line ordering reads clearer than selection rounds.
- **Bounded Heap Selection**: When the candidate set is known to be small anyway, or when brevity beats the buffer.

### Optimization Notes

- The stamp must be assigned in `postTweet`, not reconstructed later: tweet IDs carry no order, and any scheme that sorts or compares IDs misorders feeds.
- The brute force's flatten can be capped soundly: no author can contribute more than 10 tweets to a feed, so walking only each timeline's last 10 entries (`timeline[-feed_size:]`) bounds `C` at `10 * A` without changing the result.
- The heap entry's timeline index is what makes the successor push `O(1)`; re-locating the previous tweet by searching the timeline would add a factor the index avoids.
- Production feeds invert this cost model: writes push the tweet into each follower's precomputed feed (fan-out on write) so reads are a slice, and the read-time merge here is the fallback for celebrities and dormant followers, where fanning out on write is too expensive.
