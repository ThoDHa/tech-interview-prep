# [Count Promotional Periods](https://www.fastprep.io/problems/amazon-count-promotional-periods)

**unknown difficulty** | **NN minutes** | **unknown categories**

Data analysts at Amazon are studying product order patterns. They classify a period of at least three consecutive days as a promotional period when the order counts on the first and last days are both greater than every order count on the days between them.

More formally, for an array orders, a subarray from index i to index j is a promotional period if j - i + 1 >= 3 and min(orders[i], orders[j]) > max(orders[i + 1], orders[i + 2], ..., orders[j - 1]).

Given the order statistics for n consecutive days, return the number of promotional periods.

Function Description Complete the function countPromotionalPeriods.

countPromotionalPeriods has the following parameter:

int orders[n]: the order statistics for each dayReturns long: the number of promotional periods.

## Examples

### Example 1

**Input:** `orders = [3, 2, 8, 6]`

**Output:** `1`

**Explanation:** Using 1-based indexing, the candidate periods of length at least 3 are [1, 3], [1, 4], and [2, 4]. Period [1, 3] is valid because min(3, 8) = 3 and the only middle value is 2. The other two periods are invalid because their middle maximum is 8. Therefore, the answer is 1.

### Example 2

**Input:** `orders = [5, 1, 4, 2, 6]`

**Output:** `3`

**Explanation:** The promotional periods are [5, 1, 4], [4, 2, 6], and [5, 1, 4, 2, 6].

## Constraints

- `3 <= n <= 2 x 10^5`
- `1 <= orders[i] <= 10^9`
- `All integers in orders are distinct.`

## Solutions

### Brute Force Over All Periods

#### Derivation

The most literal reading applies the definition directly: take every start and every end at least two apart, compute the maximum of the days between them, and compare it against the smaller endpoint. Nothing is assumed about the array's shape, so this is also the ground truth the faster solutions are checked against:

1. Loop `start` from `0` to `length - 1` and `end` from `start + 2` to
   `length - 1`, so every period has at least three days.
2. Compute `middle_max = max(orders[start + 1:end])`.
3. Count the period when `min(orders[start], orders[end]) > middle_max`.
4. Return the count.

#### Walkthrough

Example 1, `orders = [3, 2, 8, 6]`, has three candidates of length 3 or more:

```text
period [3, 2, 8]    min(3, 8) = 3  >  middle max 2   counts, total = 1
period [3, 2, 8, 6] min(3, 6) = 3  >  middle max 8   no
period [2, 8, 6]    min(2, 6) = 2  >  middle max 8   no
return 1
```

Only the first period survives, matching the expected Output of `1`. On Example 2 the same scan finds `[5, 1, 4]`, `[4, 2, 6]`, and `[5, 1, 4, 2, 6]`, returning `3`.

#### Solution

```python
from typing import List


class Solution:
    def countPromotionalPeriods(self, orders: List[int]) -> int:
        length = len(orders)
        total = 0
        for start in range(length):
            for end in range(start + 2, length):
                middle_max = max(orders[start + 1:end])
                if min(orders[start], orders[end]) > middle_max:
                    total += 1
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^3)`

There are `O(n^2)` periods and each middle maximum takes `O(n)` to compute.

##### Space Complexity: `O(1)`

Only loop counters and a running maximum.

#### Key Insights

- Transcribing the formal condition is enough for correctness: `j - i + 1 >= 3` becomes the inner loop starting at `start + 2`.
- The slice `orders[start + 1:end]` is empty for no candidate here, because `end >= start + 2` guarantees at least one middle day.
- Correct on any input, but with `n` up to `2 × 10^5` a cubic scan is far too slow, which motivates the structure-based approaches.

### Shrinking Window with Running Maximum

#### Derivation

The brute force recomputes each middle maximum from nothing, but fix the left end and extend the right end one day at a time: the middle span grows by exactly one element per step, so its maximum can be maintained incrementally. The extension also buys an early exit: once the running maximum reaches the left endpoint, `orders[start] > middle_max` can never hold again on this row, because the maximum only grows as the window widens. The right endpoint check `orders[end] > middle_max` then completes the condition:

1. For each `start`, initialize `middle_max` to `orders[start + 1]`, the sole
   middle day of the shortest candidate period.
2. Sweep `end` from `start + 2` rightward. Stop when
   `middle_max >= orders[start]`: the period can never be valid again.
3. Otherwise count the period when `orders[end] > middle_max` (the endpoint
   test `min(orders[start], orders[end]) > middle_max` with the left half
   already verified by the exit condition).
4. Fold `orders[end]` into `middle_max` before the next step.
5. Return the count.

Every period is still examined exactly once per `start`, but the exit cuts each row short at the first element that pins the maximum, which for many inputs makes the scan far shorter than its `O(n^2)` bound.

#### Walkthrough

Example 2, `orders = [5, 1, 4, 2, 6]`, one row per start:

```text
start 0 (value 5)   middle_max = 1
   end 2 (4):  middle_max 1 < 5 and 4 > 1   counts, total = 1   middle_max -> 4
   end 3 (2):  middle_max 4 < 5 but 2 <= 4  no                  middle_max -> 4
   end 4 (6):  middle_max 4 < 5 and 6 > 4   counts, total = 2   middle_max -> 6
start 1 (value 1)   middle_max = 4
   end 3 (2):  middle_max 4 >= 1            row exits immediately
start 2 (value 4)   middle_max = 2
   end 4 (6):  middle_max 2 < 4 and 6 > 2   counts, total = 3   middle_max -> 6
return 3
```

The three counted periods are `[5, 1, 4]`, `[5, 1, 4, 2, 6]`, and `[4, 2, 6]`, the expected Output, and the row for `start 1` died at its first candidate. On Example 1 the only counted period is `[3, 2, 8]`, again matching the expected `1`.

#### Solution

```python
from typing import List


class Solution:
    def countPromotionalPeriods(self, orders: List[int]) -> int:
        length = len(orders)
        total = 0
        for start in range(length - 1):
            middle_max = orders[start + 1]
            for end in range(start + 2, length):
                if middle_max >= orders[start]:
                    break
                if orders[end] > middle_max:
                    total += 1
                    middle_max = orders[end]
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each `(start, end)` pair is visited at most once, with constant work per pair; the break only shortens rows, never lengthens them.

##### Space Complexity: `O(1)`

One running maximum per row.

#### Key Insights

- A window whose middle span grows by one element per step needs only a running maximum; the `O(n)` slice `max` was pure recomputation.
- The left endpoint condition doubles as an exit condition: once `middle_max >= orders[start]`, the running maximum has pinned and no later `end` can revive the row.
- Worst-case quadratic (a decreasing array keeps every row alive to the end), so the worst case still cannot survive `n = 2 × 10^5`; the stack approach removes the row structure entirely.

### Monotonic Stack Pop Counting

#### Derivation

Both previous approaches still enumerate period starts. The faster question is the reverse: as the right end `end` sweeps once across the array, which left ends pair with it validly, and can those pairings be counted in bulk?

For `end` fixed, a period `[start, end]` is valid when every middle value is below both endpoints. A [monotonic stack](https://en.wikipedia.org/wiki/Monotonic_stack) of indices with strictly decreasing values turns that test into a bookkeeping count. While `orders[stack[-1]] < orders[end]`, pop the top `popped_start` and look at `start`, the index now directly beneath it on the stack (when one exists). Then every day strictly between `start` and `end` is smaller than both endpoint values. Split the span at `popped_start`. For the days between `popped_start` and `end`: the largest among them must still pop during this while loop (had it popped earlier, the day that popped it would be a larger day in the same range), so the loop condition bounds it by `orders[end]`, and the element directly beneath it at that pop is `popped_start`, so the strictly decreasing stack bounds the whole range by `orders[popped_start]`. For the days between `start` and `popped_start`: the same chase at the moment `popped_start` arrived bounds them by `orders[start]` and `orders[popped_start]`. So `min(orders[start], orders[end])` exceeds every middle value, and `[start, end]` is a valid promotional period.

The correspondence is also exhaustive. A valid period's left endpoint is still on the stack when its right end arrives: an index popped before `end` has a strictly larger day after it, which the span would have to exceed but cannot. And it is counted at the moment the stack entry directly above that left endpoint pops, which happens exactly at the period's right end. Each valid period therefore maps to exactly one pop. The only pop that certifies nothing is one that empties the stack: it has no index beneath it, so it has no left endpoint to pair with, and the count withdraws one per stack-emptying pop. Because each index is pushed and popped at most once, one sweep suffices.

#### Walkthrough

Example 2, `orders = [5, 1, 4, 2, 6]`. The stack holds indices; each line shows the pops for one `end`:

```text
end 0 (5)   stack empty, push 0                 stack = [0]           total = 0
end 1 (1)   5 !< 1, no pop; push 1              stack = [0, 1]        total = 0
end 2 (4)   pop 1 (orders 1 < 4)  stack after = [0], non-empty -> total = 1
            5 !< 4, stop; push 2                stack = [0, 2]        total = 1
end 3 (2)   4 !< 2, no pop; push 3              stack = [0, 2, 3]     total = 1
end 4 (6)   pop 3 (orders 2 < 6)  stack after = [0, 2] -> total = 2
            pop 2 (orders 4 < 6)  stack after = [0]    -> total = 3
            5 !< 6, stop; push 4                stack = [0, 4]        total = 3
return 3
```

Each pop certifies the period from the index beneath it to `end`: popping index 1 at `end 2` certifies `[0, 2]`, the period `[5, 1, 4]`; popping index 3 at `end 4` certifies `[2, 4]`, the period `[4, 2, 6]`; popping index 2 right after certifies `[0, 4]`, the whole array. No pop emptied the stack, so nothing was withdrawn, and the total is `3`, the expected Output.

Example 1, `orders = [3, 2, 8, 6]`, exercises the withdrawal: the pop of index 1 at `end 2` certifies `[0, 2]`, the period `[3, 2, 8]`, and raises the total to `1`. At `end 3` nothing pops at all, because `orders[2] = 8` is not below `6`: index 2 never comes off the stack, so the candidate `[2, 8, 6]` is never certified, which is correct since its left endpoint 2 is smaller than the middle maximum 8. The total stays `1`, again the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def countPromotionalPeriods(self, orders: List[int]) -> int:
        length = len(orders)
        stack: List[int] = []
        total = 0
        for end in range(length):
            popped_count = 0
            while stack and orders[stack[-1]] < orders[end]:
                stack.pop()
                popped_count += 1
            if popped_count:
                total += popped_count if stack else popped_count - 1
            stack.append(end)
        return total
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each index is pushed exactly once and popped at most once, so the total work across all `end` steps is linear.

##### Space Complexity: `O(n)`

The stack holds every index of a strictly decreasing prefix in the worst case (for example, a fully decreasing array pushes everything and never pops).

#### Key Insights

- Each monotonic-stack pop certifies one period: from the index directly beneath the popped one to the current end, with the stack's decreasing shape guaranteeing every day in between is smaller than both endpoints.
- A pop that empties the stack has no index beneath it and certifies nothing; subtracting one per stack-emptying pop is the entire correction the count needs.
- The earlier `O(n^2)` approach already contains the linear idea in embryo: its rows die exactly when the running maximum pins, and the stack makes those deaths bulk and shared across rows instead of recomputed per row.

## Comparison of Solutions

### Time Complexity

- **Brute Force Over All Periods**: `O(n^3)` - `O(n^2)` periods, each scanned in `O(n)` for the middle maximum.
- **Shrinking Window with Running Maximum**: `O(n^2)` - one pass per start with constant work per end; the early break only shortens rows.
- **Monotonic Stack Pop Counting**: `O(n)` - one sweep, each index pushed and popped at most once.

### Space Complexity

- **Brute Force Over All Periods**: `O(1)` - loop counters and a transient maximum.
- **Shrinking Window with Running Maximum**: `O(1)` - one running maximum per row.
- **Monotonic Stack Pop Counting**: `O(n)` - the index stack on a decreasing input.

### Trade-offs

- **Brute Force Over All Periods**: the definition transcribed, trivially correct, and the natural oracle for testing, but hopeless at the stated scale.
- **Shrinking Window with Running Maximum**: a modest change (maintain one maximum, exit pinned rows) that buys a factor of `n`, yet its worst case stays quadratic on decreasing inputs.
- **Monotonic Stack Pop Counting**: linear and short, but its counting rule (a pop certifies the period from the index beneath it, except the pop that empties the stack) is subtle enough that it demands the brute-force cross-check.

### When to Use Each

- **Brute Force Over All Periods**: small inputs and correctness reference; also the fastest way to explore the condition's edge cases by hand.
- **Shrinking Window with Running Maximum**: a strong interview middle step when the linear invariant does not surface in time; it is easy to argue and easy to test.
- **Monotonic Stack Pop Counting (Recommended)**: the answer for the stated `n <= 2 × 10^5`, and the pattern to name when a counting problem asks "for each right endpoint, how many valid left endpoints?"

### Optimization Notes

- The stack version leans on the distinctness constraint; if duplicate orders were allowed, the pop comparison and both corrections would need rederivation, and `O(n^2)` worst cases (flat plateaus) reappear.
- The `popped_count if stack else popped_count - 1` line applies the correction in one expression: only the final pop of a batch can empty the stack, and that one pop is the only one with no index beneath it.
- The running-maximum version's break condition (`middle_max >= orders[start]`) is what the stack generalizes; recognizing rows that die early is the bridge between the quadratic and linear solutions.
