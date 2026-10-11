# [Most Frequent Name](https://www.fastprep.io/problems/amazon-most-frequent-name)

**Easy** | **NN minutes** | **Array, Hash Table, String**

Given a nonempty array of case-sensitive names, return the name that appears most often.

If multiple names have the same maximum frequency, return the lexicographically smallest tied name.

## Examples

### Example 1

**Input:** `names = ["ana","bob","ana"]`

**Output:** `"ana"`

**Explanation:** Case 1 exercises the documented deterministic contract.

### Example 2

**Input:** `names = ["zoe","amy","zoe","amy"]`

**Output:** `"amy"`

**Explanation:** Case 2 exercises the documented deterministic contract.

### Example 3

**Input:** `names = ["solo"]`

**Output:** `"solo"`

**Explanation:** Case 3 exercises the documented deterministic contract.

## Constraints

- `1 <= names.length <= 200000.`
- `1 <= names[i].length <= 100.`
- `Names contain printable ASCII characters and comparisons are case-sensitive.`

## Solutions

### Brute Force

#### Derivation

The most literal reading of the problem counts each name by hand. For every entry in the array, walk the whole array and tally how many times it appears; keep the tally that wins. The tie-break rule (lexicographically smallest among tied names) is applied directly in the comparison: a candidate replaces the current winner when its count is strictly higher, or when the counts tie and the candidate's name sorts earlier:

1. Start with `best_name = names[0]` and `best_count = 0`.
2. For each `candidate_index`, count how many entries equal
   `names[candidate_index]`.
3. Replace the winner when `count > best_count`, or when
   `count == best_count` and `names[candidate_index] < best_name`.
4. Return `best_name`.

#### Walkthrough

Let us run the double scan by hand on Example 2: `names = ["zoe","amy","zoe","amy"]`, the case where the tie-break decides the answer:

```text
candidate 0  "zoe"  count = 2   2 > 0            -> best_name = "zoe",  best_count = 2
candidate 1  "amy"  count = 2   tie, "amy" < "zoe" -> best_name = "amy"
candidate 2  "zoe"  count = 2   tie, "zoe" > "amy" -> keep "amy"
candidate 3  "amy"  count = 2   tie, not < "amy"   -> keep "amy"
```

Every candidate counts to `2`, so the winner is decided purely by the lexicographic comparison: `"amy"` replaces `"zoe"` at candidate 1 and is returned, matching the expected Output for Example 2.

#### Solution

The code is the walkthrough's double scan written down: an outer loop naming a candidate, an inner loop counting it.

```python
from typing import List


class Solution:
    def mostFrequentName(self, names: List[str]) -> str:
        best_name = names[0]
        best_count = 0
        for candidate_index in range(len(names)):
            count = 0
            for other_name in names:
                if other_name == names[candidate_index]:
                    count += 1
            if count > best_count or (
                count == best_count and names[candidate_index] < best_name
            ):
                best_name = names[candidate_index]
                best_count = count
        return best_name
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n² × L)`

For each of the `n` names, the inner scan performs up to `n` string comparisons, and each comparison reads up to `L` characters (the maximum name length), so the length factor multiplies the quadratic pair count.

##### Space Complexity: `O(1)`

Only the winner bookkeeping (`best_name`, `best_count`, and one loop counter) is kept; no structure grows with the input.

#### Key Insights

- The tie-break costs nothing extra here: comparing `(count, name)` in one conditional is the whole contract.
- The quadratic rescan repeats the same counting work once per duplicate, which is harmless at the stated minimum sizes but disqualifying at `n = 200000`.
- No auxiliary structure means no hashing and no ordering assumptions, making this the version to test against.

### Sorting

#### Derivation

The brute force recounts every duplicate from scratch because the array carries no structure. Sorting gives the array the one property frequency counting needs: equal names become adjacent. Once the names are in order, one pass with a `run_length` counter reads each group of duplicates off the array, and the lexicographic tie-break comes from the sort order itself: within a tie, the earliest group in the sorted array already holds the smallest name, so a later group must beat the winner on count alone to replace it:

1. Build `ordered_names = sorted(names)`, grouping duplicates together and
   ordering groups lexicographically.
2. Sweep once with `run_length`, resetting to `1` at each group boundary and
   incrementing within a group.
3. When `run_length > best_count`, record the group's name and length. The
   strict comparison lets earlier (smaller) groups keep ties.
4. Return `best_name`.

#### Walkthrough

Let us sweep the sorted array by hand on Example 1: `names = ["ana","bob","ana"]`, which sorts to `ordered_names = ["ana","ana","bob"]`:

```text
position 0  "ana"  (group start)  run_length = 1
position 1  "ana"  same as before  run_length = 2   2 > 1 -> best_name = "ana", best_count = 2
position 2  "bob"  group boundary  run_length = 1   1 < 2 -> keep "ana"
```

The `"ana"` group of length 2 is the only group to beat the running best, so the function returns `"ana"`, matching the expected Output for Example 1. Had `"bob"` also appeared twice, its group would start after the `"ana"` group in sorted order, fail the strict `run_length > best_count` test at equal length, and `"ana"` would still win the tie without any explicit name comparison.

#### Solution

The code is the walkthrough's single sweep over the sorted groups.

```python
from typing import List


class Solution:
    def mostFrequentName(self, names: List[str]) -> str:
        ordered_names = sorted(names)
        best_name = ordered_names[0]
        best_count = 1
        run_length = 1
        for position in range(1, len(ordered_names)):
            if ordered_names[position] == ordered_names[position - 1]:
                run_length += 1
            else:
                run_length = 1
            if run_length > best_count:
                best_count = run_length
                best_name = ordered_names[position]
        return best_name
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n × L)`

Sorting performs `O(n log n)` comparisons and each compares up to `L` characters; the group sweep afterwards is a single `O(n × L)` pass.

##### Space Complexity: `O(n × L)`

`sorted` materializes a new list holding all `n` names, linear in the input's total character count.

#### Key Insights

- Sorting converts frequency counting into run counting: no hash structure, and the tie-break rides on sort order for free.
- The strict `>` on `run_length` is what encodes "lexicographically smallest on ties": equal-count groups later in sorted order never displace an earlier winner.
- It sits between the quadratic and hashed versions: faster than rescanning, but it pays for an ordering it does not otherwise need and still costs more than one tally pass.

### Hash Map

#### Derivation

Counting does not actually need neighbors or order, only memory: a [hash map](https://en.wikipedia.org/wiki/Hash_table) tallies every name in one pass, answering "how many times have I seen this name?" in constant expected time per lookup. With the tallies built, a second pass over the map's entries applies the winner rule. Python dicts preserve insertion order, so the entries arrive in first-occurrence order, and the tie-break stays an explicit name comparison between the incumbent and the challenger:

1. Build `name_counts` in one pass: `name_counts.get(name, 0) + 1` per entry.
2. Initialize `best_name = names[0]` and `best_count = 0`.
3. Walk `name_counts.items()`; replace the winner when `count > best_count`,
   or when the counts tie and `name < best_name`.
4. Return `best_name`.

#### Walkthrough

Let us tally Example 2, `names = ["zoe","amy","zoe","amy"]`, by hand:

```text
build   "zoe" -> {zoe: 1}
        "amy" -> {zoe: 1, amy: 1}
        "zoe" -> {zoe: 2, amy: 1}
        "amy" -> {zoe: 2, amy: 2}

select  zoe: count 2 > 0            -> best_name = "zoe", best_count = 2
        amy: count 2 tie, "amy" < "zoe" -> best_name = "amy"
```

The tally phase touches each entry once, and the selection phase touches each distinct name once. The tie between `"zoe"` and `"amy"` is broken by the string comparison, and the function returns `"amy"`, matching the expected Output for Example 2. On Example 3, `names = ["solo"]`, the map holds the single entry `{solo: 1}`, which wins with count `1 > 0`, returning `"solo"`.

#### Solution

The code is the walkthrough's two phases: one tally pass, one winner pass.

```python
from typing import List


class Solution:
    def mostFrequentName(self, names: List[str]) -> str:
        name_counts: dict[str, int] = {}
        for name in names:
            name_counts[name] = name_counts.get(name, 0) + 1

        best_name = names[0]
        best_count = 0
        for name, count in name_counts.items():
            if count > best_count or (count == best_count and name < best_name):
                best_name = name
                best_count = count
        return best_name
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × L)` expected

Hashing and comparing each name reads up to `L` characters, and both passes do constant expected work per entry, so the total is linear in the array's character volume.

##### Space Complexity: `O(n × L)`

`name_counts` holds one entry per distinct name, and in the worst case every name is distinct, storing the whole input's characters.

#### Key Insights

- The hash map does the algorithmic work, so the tie-break remains a plain comparison over `(count, name)`: the winner rule from the brute force survives unchanged.
- One pass to build, one pass to choose: the quadratic rescan collapses into dictionary updates.
- This is the pattern to reach for in any "most frequent element" question; only the tie-break clause is problem-specific.

### Counter with Tuple Key

#### Derivation

The hash map version hand-rolls both the tally and the winner selection, and Python's standard library offers each as a one-liner. [Counter](https://docs.python.org/3/library/collections.html#collections.Counter) builds the tally in a single call, and `min` over the keys with a tuple key `(-count, name)` encodes the whole winner rule: the negative count makes the highest count sort first, and the name breaks ties toward the smaller string. The insight being evaluated (frequency selection as an order statistic over a composite key) is derived in full by the hash map version above; this is the same selection with the bookkeeping handed to the library:

1. Build `name_counts = Counter(names)`.
2. Return `min(name_counts, key=lambda name: (-name_counts[name], name))`.

#### Walkthrough

Let us evaluate the tuple key by hand on Example 1, `names = ["ana","bob","ana"]`. The Counter holds `{ana: 2, bob: 1}`, and `min` compares the keys lexicographically:

```text
"ana"  key = (-2, "ana")
"bob"  key = (-1, "bob")
min compares: -2 < -1 -> "ana" wins on count, name never consulted
```

The function returns `"ana"`, matching the expected Output for Example 1. The tie path is just as direct: for Example 2's `{zoe: 2, amy: 2}`, both keys share `-2`, so the comparison falls to the second element and `"amy" < "zoe"` selects `"amy"`.

#### Solution

The code is the composite key written down: one Counter call and one `min`.

```python
from collections import Counter
from typing import List


class Solution:
    def mostFrequentName(self, names: List[str]) -> str:
        name_counts = Counter(names)
        return min(name_counts, key=lambda name: (-name_counts[name], name))
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × L)` expected

Counter hashes each name once and `min` performs one comparison per distinct name, each up to `L` characters.

##### Space Complexity: `O(n × L)`

The Counter stores one entry per distinct name, with the same worst case as the hash map version.

#### Key Insights

- The tuple key `(-count, name)` is the whole contract: sort descending by count, ascending by name, in one comparison.
- Negating the count turns a maximum search into a `min` search, which lets the tie-break ride in the same tuple instead of a two-clause conditional.
- The same composite-key trick generalizes to any lexicographic winner rule (ties by length, by timestamp, by any secondary field).

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n² × L)` - every candidate is counted by rescanning the whole array.
- **Sorting**: `O(n log n × L)` - the sort dominates; the group sweep is one linear pass.
- **Hash Map**: `O(n × L)` expected - one tally pass plus one selection pass, constant expected work per entry.
- **Counter with Tuple Key**: `O(n × L)` expected - the same two phases with the library building the tally.

### Space Complexity

- **Brute Force**: `O(1)` - winner bookkeeping only.
- **Sorting**: `O(n × L)` - the sorted copy of the name list.
- **Hash Map**: `O(n × L)` - one counter entry per distinct name.
- **Counter with Tuple Key**: `O(n × L)` - the Counter holds the same entries.

### Trade-offs

- The brute force is the contract written as code and needs no auxiliary structure, but its rescan repeats identical counting work once per duplicate.
- Sorting buys run counting without hashing and gets the tie-break from the sort order, but pays for an ordering the problem never asks for.
- The hash map is the direct optimal form: one pass to count, one to choose, with the tie-break as an explicit comparison.
- The Counter version moves both the tally and the selection into library calls; shortest to write and review, at the price of the winner logic hiding inside a lambda.

### When to Use Each

- **Brute Force**: tiny inputs or environments without hashing, and as the reference oracle when testing the faster versions.
- **Sorting**: when the output must be sorted anyway or hashing is undesirable.
- **Hash Map (Recommended)**: the interview answer: linear expected time, and the tie-break visible in the code.
- **Counter with Tuple Key**: production or contest code where brevity wins and the composite-key idiom is familiar to readers.

### Optimization Notes

- All linear versions share the same `O(n × L)` bound because string hashing and comparison read up to `L` characters; the name length, not the map mechanics, sets the constant.
- Neither linear version depends on dict iteration order: the hash map's explicit name comparison and the tuple key's name element both fully determine the winner among tied names, so the result is the same whatever order the entries arrive in.
- A single-pass variant that updates `best_name` while tallying is possible but gains nothing: the selection pass is over distinct names, which is the smaller of the two counts in duplicate-heavy inputs.
