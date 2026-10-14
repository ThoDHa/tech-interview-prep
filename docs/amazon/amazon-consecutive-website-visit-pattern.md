# [Most Frequent Consecutive Website Pattern](https://www.fastprep.io/problems/amazon-consecutive-website-visit-pattern)

**Medium** | **NN minutes** | **Array, Hash Table, Sorting, String**

You are given three equal-length arrays describing website visits. Entry i contains a username, an integer timestamp, and a website.

For each user, sort visits by timestamp; when timestamps are equal, keep their original input order. Every three adjacent visits in that per-user order form a consecutive website pattern. A user contributes at most once to the count of any distinct pattern, even if that pattern occurs several times for the user.

Return the three websites in the pattern seen by the greatest number of distinct users. If several patterns have the same count, return the lexicographically smallest three-element sequence. If no user has at least three visits, return an empty array.

## Examples

### Example 1

**Input:** `usernames = ["amy","amy","amy","ben","ben","ben"]`, `timestamps = [1,2,3,1,2,3]`, `websites = ["home","cart","pay","home","cart","pay"]`

**Output:** `["home","cart","pay"]`

**Explanation:** Both users have the consecutive pattern [home, cart, pay], so it has two distinct-user supporters.

### Example 2

**Input:** `usernames = ["a","a","a","b","b","b"]`, `timestamps = [3,1,2,1,2,3]`, `websites = ["z","a","z","a","z","z"]`

**Output:** `["a","z","z"]`

**Explanation:** User a produces [a, z, z], and user b produces the same pattern. Sorting is performed within each user rather than on the global input.

### Example 3

**Input:** `usernames = ["a","a","b"]`, `timestamps = [1,2,1]`, `websites = ["x","y","z"]`

**Output:** `[]`

**Explanation:** No user has three visits, so no consecutive triple exists.

## Constraints

- `0 <= usernames.length <= 5000.`
- `usernames.length == timestamps.length == websites.length.`
- `Usernames and websites contain 1 to 30 lowercase English letters.`
- `0 <= timestamps[i] <= 10^9.`
- `Input rows may be globally unordered; equal timestamps for one user retain input order.`

## Solutions

### Sort Rows and Scan Runs

#### Derivation

The problem mixes two levels: visits must be regrouped per user and ordered by time, yet the input arrives as three parallel arrays in arbitrary order. The shortest path to a working answer flattens the arrays into rows and hands the grouping and ordering work to the sort. Python's sort is [stable](https://en.wikipedia.org/wiki/Sorting_algorithm#Stability), so sorting rows by `(username, timestamp)` keeps the required original input order among a user's equal timestamps, and afterward every user's visits form one contiguous run in row-major order.

One duty remains: a pattern's count is the number of distinct users whose runs contain it, not the number of occurrences. A map from pattern to the set of users that produced it does the deduplication, and the winner is the pattern whose set is largest, ties broken by the lexicographically smallest tuple:

1. Zip the three arrays into `rows` of `(username, timestamp, website)` and sort
   them with `key = lambda row: (row[0], row[1])`.
2. Walk the sorted rows in runs of equal username: a run spans `[run_start, run_end)`.
3. Inside each run, take every consecutive triple at `first`, `first + 1`,
   `first + 2`, form `pattern` from the three website entries, and add the run's
   username to `pattern_users[pattern]`.
4. Scan `pattern_users` for the pattern with the largest supporter set, breaking
   ties by smallest tuple.
5. Return the winner as a list, or an empty list when no pattern exists.

#### Walkthrough

Example 2 shows both mechanisms, the per-user sort and the run scan: `usernames = ["a","a","a","b","b","b"]`, `timestamps = [3,1,2,1,2,3]`, `websites = ["z","a","z","a","z","z"]`. The zipped rows and the stable sort by `(username, timestamp)`:

```text
input rows                       sorted rows
(a, 3, z)   --\                   (a, 1, a)
(a, 1, a)     |                   (a, 2, z)
(a, 2, z)   --/                   (a, 3, z)
(b, 1, a)   --\                   (b, 1, a)
(b, 2, z)     |  one stable sort  (b, 2, z)
(b, 3, z)   --/                   (b, 3, z)
```

The sort regrouped user a's shuffled visits into timestamp order while user b's rows were already ordered. Two runs follow, each of length 3, so each run offers exactly one consecutive triple:

```text
run a: [run_start=0, run_end=3)
  first=0: websites a, z, z -> pattern (a, z, z)
           pattern_users = {(a,z,z): {a}}
run b: [run_start=3, run_end=6)
  first=3: websites a, z, z -> pattern (a, z, z)
           pattern_users = {(a,z,z): {a, b}}
```

User b lands in the same supporter set as user a, so `(a, z, z)` counts two distinct users. The scan over `pattern_users` finds a single candidate with the maximum count, and the function returns `["a", "z", "z"]`, matching the expected Output for Example 2. (Example 1 runs identically and produces `["home", "cart", "pay"]` with two supporters.)

#### Solution

The code is the stable sort, the run scan, and the supporter-set deduplication from the walkthrough.

```python
from typing import Dict, List, Optional, Set, Tuple


class Solution:
    def mostFrequentConsecutivePattern(
        self, usernames: List[str], timestamps: List[int], websites: List[str]
    ) -> List[str]:
        rows = sorted(
            zip(usernames, timestamps, websites),
            key=lambda row: (row[0], row[1]),
        )
        row_count = len(rows)
        pattern_users: Dict[Tuple[str, str, str], Set[str]] = {}

        run_start = 0
        while run_start < row_count:
            run_end = run_start
            while run_end < row_count and rows[run_end][0] == rows[run_start][0]:
                run_end += 1
            for first in range(run_start, run_end - 2):
                pattern = (rows[first][2], rows[first + 1][2], rows[first + 2][2])
                pattern_users.setdefault(pattern, set()).add(rows[first][0])
            run_start = run_end

        best_pattern: Optional[Tuple[str, str, str]] = None
        best_count = 0
        for pattern, supporters in pattern_users.items():
            if (best_pattern is None
                    or best_count < len(supporters)
                    or (best_count == len(supporters) and pattern < best_pattern)):
                best_pattern = pattern
                best_count = len(supporters)

        if best_pattern is None:
            return []
        return list(best_pattern)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting `n` rows dominates; the run scan touches each row once, and the winner scan processes at most `n` distinct patterns, each supporter-set lookup `O(1)` on average.

##### Space Complexity: `O(n)`

The sorted row list and the pattern-to-supporters map, whose total content is bounded by the number of rows.

#### Key Insights

- A stable sort by `(username, timestamp)` resolves both the regrouping and the equal-timestamp rule in one comparison key; the tie rule costs no extra code.
- Counting distinct users rather than occurrences is the trap: without the supporter set, a user repeating one pattern twice would inflate its count.
- The lexicographic tie-break falls out of comparing website tuples, since Python orders tuples of strings element by element.

### Per-User Buckets with Contribution Deduplication

#### Derivation

The single global sort works, but it interleaves two concerns: it reorders rows that belong to different users even though the problem's ordering rule never crosses users. Grouping first, then sorting each user's small visit list by timestamp, keeps every operation local to one user and mirrors the statement's phrasing directly. The stable sort of each bucket preserves input order among equal timestamps exactly as required. Deduplication also moves closer to its cause: instead of accumulating supporter sets and taking their sizes at the end, each user declares its patterns once in a local `contributed` set and increments the shared `pattern_counts` tally at most once per pattern:

1. Group rows into `visits_by_user`, a map from username to `(timestamp, website)`
   pairs, with `defaultdict(list)`.
2. Sort each user's list by timestamp; stability keeps input order on ties.
3. For each user, collect `contributed`, the set of patterns its consecutive
   triples form; a pattern entering `contributed` for the first time increments
   `pattern_counts[pattern]`.
4. Scan `pattern_counts` for the highest count, ties broken by smallest pattern
   tuple.
5. Return the winner as a list, or an empty list when the map is empty.

#### Walkthrough

Example 1, `usernames = ["amy","amy","amy","ben","ben","ben"]`, `timestamps = [1,2,3,1,2,3]`, `websites = ["home","cart","pay","home","cart","pay"]`. The grouping pass builds two buckets:

```text
visits_by_user = {
  amy: [(1, home), (2, cart), (3, pay)]
  ben: [(1, home), (2, cart), (3, pay)]
}
```

Both buckets are already in timestamp order, so the sorts move nothing. Each bucket then contributes its consecutive triples:

```text
amy: visits[0..2] -> pattern (home, cart, pay)
     not in contributed -> contributed = {(home,cart,pay)}
     pattern_counts = {(home,cart,pay): 1}
ben: visits[0..2] -> pattern (home, cart, pay)
     not in contributed -> contributed = {(home,cart,pay)}
     pattern_counts = {(home,cart,pay): 2}
```

Each user advanced the tally exactly once, so `(home, cart, pay)` holds a count of two. The winner scan finds one candidate and the function returns `["home", "cart", "pay"]`, matching the expected Output for Example 1.

The deduplication beat needs a longer per-user list to appear. Extend amy to six visits with `timestamps = [1,2,3,4,5,6]`, `websites = ["home","cart","pay","home","cart","pay"]`, a tailored input in the shape of Example 1's first user: the run yields triples at offsets 0 through 3, and offset 3 reproduces offset 0's pattern:

```text
offset 0: (home, cart, pay)  new      -> pattern_counts = {...: 1}
offset 1: (cart, pay, home)  new      -> contributed grows, count 1
offset 2: (pay, home, cart)  new      -> contributed grows, count 1
offset 3: (home, cart, pay)  already in contributed -> no increment
```

Amy's repeated pattern advanced the tally once, not three times, which is exactly the "contributes at most once" rule of the statement.

#### Solution

The code is the bucket pass, the per-user stable sort, and the `contributed` deduplication from the walkthrough.

```python
from collections import defaultdict
from typing import DefaultDict, Dict, List, Optional, Set, Tuple


class Solution:
    def mostFrequentConsecutivePattern(
        self, usernames: List[str], timestamps: List[int], websites: List[str]
    ) -> List[str]:
        visits_by_user: DefaultDict[str, List[Tuple[int, str]]] = defaultdict(list)
        for username, timestamp, website in zip(usernames, timestamps, websites):
            visits_by_user[username].append((timestamp, website))

        pattern_counts: Dict[Tuple[str, str, str], int] = {}
        for visits in visits_by_user.values():
            visits.sort(key=lambda visit: visit[0])
            contributed: Set[Tuple[str, str, str]] = set()
            for first in range(len(visits) - 2):
                pattern = (
                    visits[first][1],
                    visits[first + 1][1],
                    visits[first + 2][1],
                )
                if pattern not in contributed:
                    contributed.add(pattern)
                    pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

        best_pattern: Optional[Tuple[str, str, str]] = None
        best_count = 0
        for pattern, count in pattern_counts.items():
            if (best_pattern is None
                    or best_count < count
                    or (best_count == count and pattern < best_pattern)):
                best_pattern = pattern
                best_count = count

        if best_pattern is None:
            return []
        return list(best_pattern)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Every row is grouped once and appears in exactly one bucket sort; the sorts cost `O(sum of m log m)` over bucket sizes `m`, bounded by `O(n log n)`, and the triple scans and winner scan are linear.

##### Space Complexity: `O(n)`

The buckets, the contributed sets, and the pattern tally together hold one entry per row or per distinct pattern, both bounded by `n`.

#### Key Insights

- Grouping before sorting expresses the statement's rule ("sort visits per user") with no global key trickery, and it sorts only within users instead of shuffling unrelated rows.
- The `contributed` set scopes the once-per-user rule to where it applies, so the shared tally stays a plain counter and the winner scan needs no set-size arithmetic.
- The empty-array outcome needs no special case: no bucket reaching three visits produces no patterns, the map stays empty, and the `best_pattern is None` branch returns `[]`.

## Comparison of Solutions

### Time Complexity

- **Sort Rows and Scan Runs**: `O(n log n)` - one global sort of `n` rows dominates the run and winner scans.
- **Per-User Buckets with Contribution Deduplication**: `O(n log n)` - sorting inside buckets costs the same asymptotics with smaller constants on balanced users.

### Space Complexity

- **Sort Rows and Scan Runs**: `O(n)` - the sorted row list plus the pattern-to-supporters map.
- **Per-User Buckets with Contribution Deduplication**: `O(n)` - the buckets plus the contributed sets and the tally.

### Trade-offs

- **Sort Rows and Scan Runs**: one sort and one scan read cleanly, but the supporter sets keep usernames alive per pattern, and the grouping structure lives only implicitly in run boundaries.
- **Per-User Buckets with Contribution Deduplication**: mirrors the statement rule by rule and deduplicates at the source, at the cost of one more data structure (the `contributed` set) per user.

### When to Use Each

- **Sort Rows and Scan Runs**: when a single pass over sorted data feels natural and you can state the stability argument confidently.
- **Per-User Buckets with Contribution Deduplication (Recommended)**: the interview default: each step corresponds to one sentence of the problem statement, which makes correctness easy to argue under pressure.

### Optimization Notes

- Both versions are comparison-sort bound; replacing the global sort with a bucketed group-then-sort does not beat `O(n log n)` asymptotically but sorts smaller lists, which is faster in practice when users have few visits each.
- `visits.sort(key=lambda visit: visit[0])` sorts tuples by timestamp only; sorting on the bare tuples would also order by website on ties, silently violating the keep-input-order rule.
- The winner scan compares tuples directly for the tie-break; a `min` over `(-count, pattern)` keys is a tidier equivalent if you prefer key functions to explicit branches.
- Example 3's outcome (`[]`) is worth asserting in any test set: it exercises the no-triple path through both implementations.
