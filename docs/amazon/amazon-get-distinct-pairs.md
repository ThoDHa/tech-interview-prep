# [Get Distinct Pairs](https://www.fastprep.io/problems/amazon-get-distinct-pairs)

**Easy** | **NN minutes** | **Hash Table, Two Pointers**

A financial strategist at Amazon Web Services (AWS) is analyzing a collection of profitable investments, each represented by an integer array. Every value in the array indicates the annual gain of a particular investment. The strategist's goal is to identify all unique investment pairs whose combined annual returns exactly match a given target value.



Unique pairs are defined as combinations that vary by at least one element (i.e., their values are not at the exact same positions or do not have identical values in identical positions).



Given the array of gains, compute the number of unique investment pairs whose sum equals the specified target return.

## Examples

### Example 1

**Input:** `stocksProfit = [5, 7, 9, 13, 11, 6, 6, 3, 3]`, `target = 12`

**Output:** `3`

**Explanation:** There are four pairs whose combined gains equal the target return of 12. However, since the array includes duplicate values of 3, there are two versions of the pair (9, 3): one between positions 2 and 7, and another between positions 2 and 8. But only one of these can be counted to maintain uniqueness.

Therefore, the valid and unique pairs are:



(5, 7)(3, 9)(6, 6)

We return 3.

## Constraints

- `1 ≤ n ≤ 5 x 10^5`
- `0 ≤ investmentReturns[i] ≤ 10^9`
- `0 ≤ goal ≤ 5 x 10^9`

## Solutions

### Brute Force with a Seen-Pair Set

#### Derivation

The most literal reading checks every pair of positions. The position pair, not the value pair, is the unit of enumeration, because uniqueness is defined over values: two different position pairs holding the same values count once. So the scan collects value pairs into a set, normalizing each hit as `(smaller_gain, larger_gain)` so that `(3, 9)` and `(9, 3)` land on one key, and the set's final size is the answer:

1. Loop `first_position` over the array, and `second_position` over the
   positions after it, so no position pair is tried twice.
2. Read `first_gain` and `second_gain` from the two positions.
3. When `first_gain + second_gain == target`, add
   `(min(first_gain, second_gain), max(first_gain, second_gain))` to
   `found_pairs`.
4. Return `len(found_pairs)`.

#### Walkthrough

Trace the scan on Example 1: `stocksProfit = [5, 7, 9, 13, 11, 6, 6, 3, 3]`, `target = 12`. Each row is one `first_position`; the inner scan over later positions is summarized:

```text
first_position 0 (5):  7 at position 1           -> add (5, 7)
first_position 1 (7):  needs 5, none later       -> no addition
first_position 2 (9):  3 at positions 7 and 8    -> add (3, 9);
                       second hit repeats the same key, the set absorbs it
first_position 3 (13): needs -1, impossible      -> no addition
first_position 4 (11): needs 1, none later       -> no addition
first_position 5 (6):  6 at position 6           -> add (6, 6)
first_position 6 (6):  needs 6, none later       -> no addition
first_position 7 (3):  needs 9, none later       -> no addition
```

`found_pairs` ends as `{(5, 7), (3, 9), (6, 6)}` and the function returns `3`, matching the expected Output for Example 1. The row for `first_position 2` is where uniqueness does its work: the statement's two versions of `(9, 3)` both fire, and only the first one changes the set.

#### Solution

The code is the double scan with the normalized key.

```python
from typing import List


class Solution:
    def getDistinctPairs(self, stocksProfit: List[int], target: int) -> int:
        gain_count = len(stocksProfit)
        found_pairs = set()

        for first_position in range(gain_count):
            for second_position in range(first_position + 1, gain_count):
                first_gain = stocksProfit[first_position]
                second_gain = stocksProfit[second_position]
                if first_gain + second_gain == target:
                    found_pairs.add(
                        (min(first_gain, second_gain),
                         max(first_gain, second_gain))
                    )

        return len(found_pairs)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Every position pair is inspected once: `n` outer choices with up to `n` inner ones.

##### Space Complexity: `O(n)`

`found_pairs` holds at most one entry per distinct value pair, bounded by the number of distinct gains.

#### Key Insights

- Uniqueness lives entirely in the normalized key: the scan may find `(9, 3)` many times, and the set is what collapses them to one.
- Restricting the inner loop to positions after `first_position` keeps every position pair ordered, which halves the work without losing any pair.
- Correct and simple, but with `n` up to `5 * 10^5` the quadratic scan is unusable in the OA; the order-based and memory-based solutions below remove it.

### Sort and Two Pointers

#### Derivation

The brute force re-examines every position pair even though only sums matter. Sorting the gains gives the sums an order to exploit: with one pointer at each end of the sorted list, a sum below the target can only grow by advancing the left pointer, a sum above it can only shrink by retreating the right pointer, and the sweep visits each position once. The one trap is duplicates: after recording a hit, both pointers must slide past every copy of the values just paired, or the same value pair would be recorded again from its duplicate positions:

1. Build `sorted_gains`, a sorted copy of `stocksProfit`.
2. Set `left_position = 0` and `right_position` to the last index.
3. While `left_position < right_position`: compute `pair_sum`. When it is
   below the target, advance `left_position`; when above, retreat
   `right_position`.
4. On an exact hit, add the normalized
   `(sorted_gains[left_position], sorted_gains[right_position])` (already
   in ascending order) to `found_pairs`, then skip every duplicate of
   `sorted_gains[left_position]` forward and every duplicate of
   `sorted_gains[right_position]` backward.
5. Return `len(found_pairs)`.

#### Walkthrough

Trace the sweep on Example 1, whose gains sort to `sorted_gains = [3, 3, 5, 6, 6, 7, 9, 11, 13]`:

```text
left 0 (3), right 8 (13):  16 > 12 -> right 7
left 0 (3), right 7 (11):  14 > 12 -> right 6
left 0 (3), right 6 (9):   12 ==   -> add (3, 9); skip duplicates:
                                     left advances past the second 3 to 2
                                     right retreats to 5
left 2 (5), right 5 (7):   12 ==   -> add (5, 7); left 3, right 4
left 3 (6), right 4 (6):   12 ==   -> add (6, 6); left 4, right 3
left 4 >= right 3 -> stop
```

Three hits, three keys: `found_pairs = {(3, 9), (5, 7), (6, 6)}` and the function returns `3`, matching the expected Output for Example 1. The first hit's skip is the decisive beat: without sliding `left_position` past the second `3`, the next comparison would pair that duplicate with `9` and re-add the same key.

#### Solution

The code is the converging sweep with the duplicate skip on each hit.

```python
from typing import List


class Solution:
    def getDistinctPairs(self, stocksProfit: List[int], target: int) -> int:
        sorted_gains = sorted(stocksProfit)
        found_pairs = set()

        left_position = 0
        right_position = len(sorted_gains) - 1
        while left_position < right_position:
            pair_sum = (sorted_gains[left_position]
                        + sorted_gains[right_position])
            if pair_sum < target:
                left_position += 1
            elif pair_sum > target:
                right_position -= 1
            else:
                found_pairs.add((sorted_gains[left_position],
                                 sorted_gains[right_position]))
                left_gain = sorted_gains[left_position]
                right_gain = sorted_gains[right_position]
                while (left_position < right_position
                       and sorted_gains[left_position] == left_gain):
                    left_position += 1
                while (left_position < right_position
                       and sorted_gains[right_position] == right_gain):
                    right_position -= 1

        return len(found_pairs)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

The sort dominates; the sweep advances one of the pointers on every iteration, so it makes at most `n - 1` steps.

##### Space Complexity: `O(n)`

The sorted copy of the gains, plus `found_pairs` for the distinct value pairs.

#### Key Insights

- Order replaces search: the sorted array lets one comparison decide which pointer moves, collapsing the quadratic scan to a linear sweep plus a sort.
- The duplicate skip after each hit is the uniqueness mechanism here, doing the job the set does in the other solutions; `found_pairs` never sees a repeated key.
- The self-pair works naturally: `(6, 6)` is found when the two pointers sit on two distinct positions holding equal values, and the guard `left_position < right_position` keeps one element from pairing with itself.

### One-Pass Hash Set

#### Derivation

Sorting was one way to answer "have I seen the partner gain?"; a hash set answers it without any ordering. Fix a gain: its partner is fully determined as `target - gain`, so one membership test against the gains seen so far decides whether a pair completes here. The completing pair goes into `found_pairs` under its normalized key, which absorbs repeats; the current gain joins `seen_values` after the test, so a gain can never pair with itself at a single position, while two positions holding equal values still find each other:

1. Start with `seen_values` and `found_pairs` as empty sets.
2. For each `gain` in `stocksProfit`: compute
   `needed_gain = target - gain`.
3. When `needed_gain in seen_values`, add
   `(min(gain, needed_gain), max(gain, needed_gain))` to `found_pairs`.
4. Add `gain` to `seen_values`.
5. Return `len(found_pairs)`.

#### Walkthrough

Trace the pass on Example 1: `stocksProfit = [5, 7, 9, 13, 11, 6, 6, 3, 3]`, `target = 12`:

```text
gain 5:  needed 7   not in seen                  seen = {5}
gain 7:  needed 5   in seen  -> add (5, 7)       seen = {5, 7}
gain 9:  needed 3   not in seen                  seen = {5, 7, 9}
gain 13: needed -1  not in seen                  seen = {5, 7, 9, 13}
gain 11: needed 1   not in seen                  seen = {5, 7, 9, 13, 11}
gain 6:  needed 6   not in seen (first 6)        seen = {5, 7, 9, 13, 11, 6}
gain 6:  needed 6   in seen  -> add (6, 6)       seen unchanged
gain 3:  needed 9   in seen  -> add (3, 9)       seen = {..., 3}
gain 3:  needed 9   in seen  -> key (3, 9) already in found_pairs, absorbed
```

The set `found_pairs` ends as `{(5, 7), (6, 6), (3, 9)}` and the function returns `3`, matching the expected Output for Example 1. The two rows for gain `3` replay the statement's duplicate story: both positions complete a pair with `9`, and only the first changes `found_pairs`.

#### Solution

The code is the single pass with the membership test and the normalized key.

```python
from typing import List


class Solution:
    def getDistinctPairs(self, stocksProfit: List[int], target: int) -> int:
        seen_values = set()
        found_pairs = set()

        for gain in stocksProfit:
            needed_gain = target - gain
            if needed_gain in seen_values:
                found_pairs.add(
                    (min(gain, needed_gain), max(gain, needed_gain))
                )
            seen_values.add(gain)

        return len(found_pairs)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass over the gains; each iteration does an average `O(1)` set membership test, one insertion, and constant-time key arithmetic.

##### Space Complexity: `O(n)`

`seen_values` holds every distinct gain and `found_pairs` every distinct value pair, both bounded by the number of distinct values.

#### Key Insights

- The complement question from Two Sum carries over unchanged; only the bookkeeping differs, because the answer is a count of distinct value pairs rather than one pair of positions.
- Testing membership before inserting the current gain is what lets `(6, 6)` count on two positions but never on one: the first `6` finds nothing, the second finds the first.
- The normalized key is the uniqueness guarantee, and it costs two constant-time calls per hit; without it the set would treat `(3, 9)` and `(9, 3)` as different pairs and overcount.

## Comparison of Solutions

### Time Complexity

- **Brute Force with a Seen-Pair Set**: `O(n^2)` - every position pair is inspected once.
- **Sort and Two Pointers**: `O(n log n)` - one sort, then a linear converging sweep.
- **One-Pass Hash Set**: `O(n)` - a single pass with average constant-time set operations.

### Space Complexity

- **Brute Force with a Seen-Pair Set**: `O(n)` - the `found_pairs` set.
- **Sort and Two Pointers**: `O(n)` - the sorted copy of the gains plus `found_pairs`.
- **One-Pass Hash Set**: `O(n)` - `seen_values` plus `found_pairs`.

### Trade-offs

- The brute force defines the answer by enumeration and needs no insight about duplicates beyond the normalized key, at a quadratic price that disqualifies it for the stated constraints.
- Sort and Two Pointers avoids hashing entirely and keeps memory to the sorted copy, but the duplicate-skip bookkeeping on each hit is the fiddly part and the classic place to slip.
- The one-pass hash set is the shortest of the three and touches each gain once, at the cost of hash memory and average-case (not worst-case) constant lookups.

### When to Use Each

- **Brute Force with a Seen-Pair Set**: for tiny inputs, as the oracle the fast versions are checked against.
- **Sort and Two Pointers**: when memory is tight or the input is already sorted, or when the interviewer asks to solve it without extra hash structures.
- **One-Pass Hash Set** (Recommended): the interview and OA default: linear time, two sets, and the uniqueness argument is one sentence about the normalized key.

### Optimization Notes

- The insertion order in the hash-set pass matters: adding `gain` to `seen_values` after the membership test is what prevents a single element from pairing with itself; moving the insertion above the test breaks `(6, 6)` handling on inputs with one `6`.
- Gains run up to `10^9` and the target up to `5 * 10^9`, so a count-array bucketing of values is not viable; sets keep memory proportional to the distinct values actually seen.
- All three versions return the same count on every input; a disagreement is a bug, most often a missing normalization (`(3, 9)` versus `(9, 3)`) or a self-pair counted from one position.
