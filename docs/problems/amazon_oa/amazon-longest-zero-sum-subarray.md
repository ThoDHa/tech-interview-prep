# [Longest Zero Sum Subarray](https://www.fastprep.io/problems/amazon-longest-zero-sum-subarray)

**unknown difficulty** | **NN minutes** | **unknown categories**

You are given an integer array nums containing positive and negative integers.

Return the length of the longest contiguous subarray whose sum is equal to 0. If no such subarray exists, return 0.

## Examples

### Example 1

**Input:** `nums = [15, -2, 2, -8, 1, 7, 10, 23]`

**Output:** `5`

**Explanation:** The subarray [-2, 2, -8, 1, 7] has sum 0 and length 5.

### Example 2

**Input:** `nums = [1, 2, 3]`

**Output:** `0`

**Explanation:** No non-empty contiguous subarray has sum 0.

## Constraints

- `1 <= nums.length`
- `nums[i] may be positive, negative, or zero.`

## Solutions

### Brute Force

#### Derivation

The most literal reading enumerates the object the problem names: every contiguous subarray. Each of the `n` starting positions grows one `end` at a time, and a running `total` accumulated during the growth keeps the sum of the current window without re-adding it from scratch. Whenever `total` hits `0`, the window from `start` through `end` is a zero-sum candidate, and its length `end - start + 1` challenges the longest seen so far:

1. Initialize `longest = 0`.
2. Loop `start` over every position of `nums`.
3. For each `start`, reset `total = 0` and loop `end` from `start` to the last
   position, adding `nums[end]` on every step.
4. When `total == 0`, update `longest = max(longest, end - start + 1)`.
5. Return `longest`, which stays `0` when no window ever sums to zero.

#### Walkthrough

Example 1: `nums = [15, -2, 2, -8, 1, 7, 10, 23]`. The scan tries every `start`; the interesting row is `start = 1`, whose running `total` crosses zero twice:

```text
start = 1   window grows right, total after each end:
            end 1   total = -2
            end 2   total =  0    longest = 2   (window [-2, 2])
            end 3   total = -8
            end 4   total = -7
            end 5   total =  0    longest = 5   (window [-2, 2, -8, 1, 7])
            end 6   total = 10
            end 7   total = 33
            end 8   total = 40
```

No other starting position produces a longer zero-sum window (most totals never touch zero at all), so the double loop finishes with `longest = 5`, the expected Output.

#### Solution

The code is the walkthrough's row scan: an outer loop over `start`, an inner loop accumulating `total`.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        longest = 0
        for start in range(len(nums)):
            total = 0
            for end in range(start, len(nums)):
                total += nums[end]
                if total == 0:
                    longest = max(longest, end - start + 1)
        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

Every `(start, end)` pair is visited once, and the running `total` makes each visit constant work; the naive re-summing variant would be `O(n³)`.

##### Space Complexity: `O(1)`

Only `longest` and the running `total` are stored.

#### Key Insights

- A running sum along the inner loop is what keeps this at `O(n²)` rather than `O(n³)`; re-summing each window from scratch is the classic first-draft mistake.
- The approach never looks at anything but the current window, so it needs no extra memory, but it also never learns anything from one window that helps with the next.

### Prefix Sum with Hash Map

#### Derivation

The brute force re-sums overlapping windows without reusing their work. Define the prefix sum `total` as the sum of the first elements of `nums`; the sum of the window from position `start` (exclusive, counting consumed elements) to position `position` (exclusive) is then `total_at_position - total_at_start`. That difference is zero exactly when the two prefix sums are equal, so "longest zero-sum subarray" becomes "longest gap between two positions holding the same prefix sum". One left-to-right pass with a hash map `first_seen` mapping each prefix sum to its earliest position answers every gap question in constant time:

1. Seed `first_seen = {0: -1}`: the empty prefix (zero elements consumed)
   already has sum `0` at position `-1`, which lets a zero-sum window starting
   at the array's first element be measured too.
2. Sweep `position` from left to right, maintaining the running `total` by
   adding `nums[position]`'s value on each step.
3. When `total` is already a key in `first_seen`, the window between that
   earliest position and the current one sums to zero, so update
   `longest = max(longest, position - first_seen[total])`.
4. Otherwise record `first_seen[total] = position`: only the first occurrence
   matters, because the earliest partner gives the longest window.
5. Return `longest`.

#### Walkthrough

Example 1: `nums = [15, -2, 2, -8, 1, 7, 10, 23]`. Each line shows the running `total` after consuming `nums[position]`, and what the `first_seen` lookup decides:

```text
seed          first_seen = {0: -1}, longest = 0
position 0    total = 15   new key, first_seen = {0: -1, 15: 0}
position 1    total = 13   new key, first_seen = {0: -1, 15: 0, 13: 1}
position 2    total = 15   seen at 0   longest = 2 - 0 = 2   ([-2, 2])
position 3    total =  7   new key, first_seen[7] = 3
position 4    total =  8   new key, first_seen[8] = 4
position 5    total = 15   seen at 0   longest = 5 - 0 = 5   ([-2, 2, -8, 1, 7])
position 6    total = 25   new key, first_seen[25] = 6
position 7    total = 48   new key, first_seen[48] = 7
```

The decisive beat is position 2: `15` repeats, but `first_seen[15]` still holds the earliest position `0`, because the repeat at position 2 never overwrote it. That earliest pairing is what makes the position-5 repeat worth a full window of length 5, the expected Output. (Example 2, `nums = [1, 2, 3]`, produces totals `1, 3, 6`: no key ever repeats, so `longest` stays at its initial `0`.)

#### Solution

The code is the sweep from the walkthrough: update `total`, then either measure the gap to the first occurrence or record one.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        first_seen = {0: -1}
        total = 0
        longest = 0
        for position, value in enumerate(nums):
            total += value
            if total in first_seen:
                longest = max(longest, position - first_seen[total])
            else:
                first_seen[total] = position
        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass over `nums` with a constant-time hash map lookup or insert at every position.

##### Space Complexity: `O(n)`

The `first_seen` map can hold one entry per distinct prefix sum, which is one more than the number of positions.

#### Key Insights

- Equal prefix sums bracket a zero-sum window: `sum(window) = total_now - total_then`, so the subtraction argument converts an `O(n²)` enumeration into an `O(n)` lookup.
- The `{0: -1}` seed is the standard trick for windows that begin at the array's first element; without it, a prefix summing to zero would be missed.
- Store only the first occurrence of each prefix sum: a later occurrence can only shorten the window, so overwriting is both wasted work and a correctness hazard.

### Prefix Sum with setdefault

#### Derivation

The hash map solution carries one branch purely for bookkeeping: seen sums read the map, unseen sums write it. The dict method `setdefault` performs both in one call, returning the stored earliest position when the key exists and inserting (and returning) the current position when it does not. The algorithm is unchanged; the branch collapses, and the miss case needs no special handling at all, because a just-inserted position measures a window of length zero:

1. Sweep as before, updating the running `total`.
2. `earliest = first_seen.setdefault(total, position)` returns the first
   occurrence, inserting the current position first when none exists.
3. `longest = max(longest, position - earliest)` is safe in both cases: a fresh
   insertion yields `position - position = 0`, which never beats an existing
   `longest`.

#### Walkthrough

Example 1 again, `nums = [15, -2, 2, -8, 1, 7, 10, 23]`, with each line now showing the `earliest` that `setdefault` hands back:

```text
seed          first_seen = {0: -1}, longest = 0
position 0    total = 15   earliest = 0 (inserted)   gap 0, longest stays 0
position 1    total = 13   earliest = 1 (inserted)   gap 0, longest stays 0
position 2    total = 15   earliest = 0 (stored)     gap 2, longest = 2
position 3    total =  7   earliest = 3 (inserted)   gap 0, longest stays 2
position 4    total =  8   earliest = 4 (inserted)   gap 0, longest stays 2
position 5    total = 15   earliest = 0 (stored)     gap 5, longest = 5
position 6    total = 25   earliest = 6 (inserted)   gap 0, longest stays 5
position 7    total = 48   earliest = 7 (inserted)   gap 0, longest stays 5
```

Stored keys measure real windows and inserted keys measure nothing, so the merged branch lands on the same `longest = 5` with two lines of loop body instead of four.

#### Solution

The code is the hash map sweep with the seen-or-insert decision handed to `setdefault`:

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> int:
        first_seen = {0: -1}
        total = 0
        longest = 0
        for position, value in enumerate(nums):
            total += value
            earliest = first_seen.setdefault(total, position)
            longest = max(longest, position - earliest)
        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Same single sweep; `setdefault` is one hash operation per position, exactly replacing the old lookup-or-insert pair.

##### Space Complexity: `O(n)`

The same `first_seen` map of distinct prefix sums.

#### Key Insights

- `setdefault` shines when the "already present" and "insert now" cases converge: here both return a position, and a fresh insertion simply measures a zero-length window.
- The gain over the explicit branch is small but real: one hash operation instead of two on the miss path, and no duplicated `first_seen` access to mistype.
- Readability is the trade: a reader must see why inserting the current position is harmless, where the two-branch version spells it out.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n²)` - every `(start, end)` pair is visited once with constant work per pair.
- **Prefix Sum with Hash Map**: `O(n)` - one sweep with constant-time map operations per position.
- **Prefix Sum with setdefault**: `O(n)` - the identical sweep with the branch collapsed into one call.

### Space Complexity

- **Brute Force**: `O(1)` - only the running total and the best length.
- **Prefix Sum with Hash Map**: `O(n)` - up to one map entry per distinct prefix sum.
- **Prefix Sum with setdefault**: `O(n)` - the same map, one entry per distinct prefix sum.

### Trade-offs

- **Brute Force**: zero auxiliary memory and impossible to mistrust, but the quadratic cost dominates any realistic input size.
- **Prefix Sum with Hash Map**: linear time for linear extra memory, and the subtraction argument it rests on is the transferable idea of the page.
- **Prefix Sum with setdefault**: the same asymptotics with terser bookkeeping, at a small cost in self-explanation.

### When to Use Each

- **Brute Force**: tiny inputs or a reference implementation to diff against while testing.
- **Prefix Sum with Hash Map (Recommended)**: the interview answer: it is linear, and the prefix-sum-equality insight generalizes to every "subarray sum equals k" variant.
- **Prefix Sum with setdefault**: production code once the team is fluent with `setdefault`'s insert-and-return contract.

### Optimization Notes

- The `{0: -1}` seed is the part most likely to be forgotten under pressure; rehearse the zero-prefix example `nums = [1, -1]`, which returns `2` only because of it.
- Never overwrite an existing map entry: keeping the earliest position is both the correctness and the longest-window condition.
- For the "subarray sum equals k" generalization, the same map stores counts of occurrences instead of first positions, because every matching pair contributes a window.
