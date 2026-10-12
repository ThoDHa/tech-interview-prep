# [Max Consecutive Ones III](https://www.fastprep.io/problems/amazon-max-consecutive-ones-iii)

**Medium** | **NN minutes** | **Array, Sliding Window, Two Pointers**

Given a binary array nums and an integer k, return the maximum number of consecutive ones obtainable by flipping at most k zeros to ones.

## Examples

### Example 1

**Input:** `nums = [1,1,1,0,0,0,1,1,1,1,0]`, `k = 2`

**Output:** `6`

**Explanation:** Flipping two zeros creates a six-element run.

### Example 2

**Input:** `nums = [0,0,1,1,1,0,0]`, `k = 0`

**Output:** `3`

**Explanation:** Without flips, the central run has length three.

### Example 3

**Input:** `nums = [0,0,0]`, `k = 3`

**Output:** `3`

**Explanation:** All three zeros can be flipped.

## Constraints

- `0 ≤ nums.length ≤ 100000.`
- `Every value in nums is 0 or 1.`
- `0 ≤ k ≤ nums.length.`

## Solutions

### Brute Force

#### Derivation

The most literal reading checks every stretch of the array: a valid window is one holding at most `k` zeros, and the answer is the longest such window. So anchor a `start`, grow an `end` rightward counting the zeros seen, and stop the moment the count exceeds `k` (extending further only adds zeros). The best width over all starts is the answer:

1. Sweep every `start` from `0` through `len(nums) - 1`, resetting `zero_count` to `0`.
2. For each `end` from `start` onward, add `1` to `zero_count` when `nums[end]` is `0`.
3. When `zero_count > k`, break: no window starting at `start` can pass this `end`.
4. Otherwise the window `[start, end]` is valid; record its width in `longest`.
5. Return `longest`.

#### Walkthrough

Example 2: `nums = [0,0,1,1,1,0,0]`, `k = 0`. With no flips allowed, each start dies at its first zero:

```text
start=0  end=0 (0) zero_count=1 > 0 break                longest 0
start=1  end=1 (0) zero_count=1 > 0 break                longest 0
start=2  end=2 (1), end=3 (1), end=4 (1)  width 3
         end=5 (0) zero_count=1 > 0 break                longest 3
start=3  end=3, end=4  width 2; end=5 (0) break          longest 3
start=4  end=4 width 1; end=5 (0) break                  longest 3
start=5  end=5 (0) break                                 longest 3
start=6  end=6 (0) break                                 longest 3
return 3
```

The longest flip-free run of ones is the central `[1,1,1]` of width `3`, matching the expected Output for Example 2.

#### Solution

The code is the anchored expansion from the walkthrough: reset `zero_count`, grow `end`, break on the first excess zero.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int], k: int) -> int:
        longest = 0
        for start in range(len(nums)):
            zero_count = 0
            for end in range(start, len(nums)):
                if nums[end] == 0:
                    zero_count += 1
                if zero_count > k:
                    break
                longest = max(longest, end - start + 1)
        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

Every `start` can scan forward to the end of the array, so one run may perform `n + (n - 1) + ... + 1` element visits.

##### Space Complexity: `O(1)`

Only `zero_count`, `start`, `end`, and `longest` are kept.

#### Key Insights

- The early `break` is valid because a window's zero count only grows as it extends; the first excess zero retires that `start` for good.
- The final width comparison `end - start + 1` runs only on valid windows, so `longest` never sees an invalid candidate.
- Correct on every input including the empty array, but quadratic: each start re-counts the zeros the previous starts already walked.

### Sliding Window

#### Derivation

The brute force re-counts the same zeros once per start. Both mistakes come from the same habit: throwing the window away. Keep one window `[left, right]` and a running `zero_count`; growing costs one visit, and repair is local. When the count exceeds `k`, advance `left`, decrementing the count whenever the seat leaving the window was a `0`, until the window is valid again. Because `left` only ever moves forward, every element enters and leaves the window once:

1. Sweep `right` over the array; add `1` to `zero_count` when `nums[right] == 0`.
2. While `zero_count > k`, drop `nums[left]`: decrement `zero_count` when it is
   `0`, then advance `left`.
3. After the repair, the window `[left, right]` is valid; record
   `right - left + 1` in `longest`.
4. Return `longest`.

#### Walkthrough

Example 1: `nums = [1,1,1,0,0,0,1,1,1,1,0]`, `k = 2`. Each line is one `right` step; the shrink runs only when `zero_count` exceeds `2`:

```text
right=0  nums 1  zero_count=0  window [0,0]   width 1   longest 1
right=1  nums 1  zero_count=0  window [0,1]   width 2   longest 2
right=2  nums 1  zero_count=0  window [0,2]   width 3   longest 3
right=3  nums 0  zero_count=1  window [0,3]   width 4   longest 4
right=4  nums 0  zero_count=2  window [0,4]   width 5   longest 5
right=5  nums 0  zero_count=3 > 2  shrink: left 0,1,2 hold 1;
         nums[3]=0 leaves, zero_count=2, left=4
                        window [4,5]   width 2   longest 5
right=6  nums 1  zero_count=2  window [4,6]   width 3   longest 5
right=7  nums 1  zero_count=2  window [4,7]   width 4   longest 5
right=8  nums 1  zero_count=2  window [4,8]   width 5   longest 5
right=9  nums 1  zero_count=2  window [4,9]   width 6   longest 6
right=10 nums 0  zero_count=3 > 2  nums[4]=0 leaves, zero_count=2, left=5
                        window [5,10]  width 6   longest 6
return 6
```

The widest valid window holds six seats: `[4,9]` (flipping the zeros at `4` and `5`) and `[5,10]` (flipping `5` and `10`) both qualify. The final `longest` is `6`, matching the expected Output for Example 1.

#### Solution

The code is the walkthrough's grow-then-repair loop: one `right` visit per iteration, a `while` for the shrink, one width sample per iteration.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int], k: int) -> int:
        longest = 0
        left = 0
        zero_count = 0
        for right in range(len(nums)):
            if nums[right] == 0:
                zero_count += 1
            while zero_count > k:
                if nums[left] == 0:
                    zero_count -= 1
                left += 1
            longest = max(longest, right - left + 1)
        return longest
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

`right` advances `n` times and `left` advances at most `n` times in total across all shrinks, so the loop body runs at most `2n` element visits.

##### Space Complexity: `O(1)`

Three scalar trackers: `left`, `zero_count`, and `longest`.

#### Key Insights

- The amortized argument is the whole design: two pointers that each only move forward give linear work even though the loop is nested.
- `zero_count` is maintained incrementally; no window is ever re-counted from scratch.
- Sampling the width after the repair guarantees the recorded window is valid, so `longest` is always achievable.
- The empty array falls out of the loop untouched and returns `0`, matching the constraint `0 <= nums.length`.

### Non-Shrinking Sliding Window

#### Derivation

The classic window's `while` loop and per-step width sample exist to keep the window valid at every instant. But the answer never needs the window itself, only its best width, and a window that briefly holds too many zeros still fits that purpose: sliding `left` forward once per step keeps the window's width from ever decreasing, and the window becomes valid again on its own as zeros leave. Dropping the `while` (use `if`), dropping the width sample, and returning the final width directly:

1. Sweep `right`; add `1` to `zero_count` when `nums[right] == 0`.
2. When `zero_count > k`, drop `nums[left]` (decrement on `0`) and advance
   `left` exactly once.
3. Never sample the width and never shrink below the current size.
4. Return `len(nums) - left`, the final window's width.

#### Invariant

After each iteration, `right` covers the prefix `nums[0..right]`, and the window width equals the largest valid width achievable inside that prefix:

```text
width(right) = right - left + 1 = max valid window width inside nums[0..right]
answer       = len(nums) - left   at loop exit (right = len(nums) - 1)
```

Each step preserves it. Say the window before the step is `[left, right - 1]` at width `w`, the prefix maximum by the previous step. Growth (`zero_count <= k` after `nums[right]` enters): the grown window `[left, right]` is valid at width `w + 1`, and every valid window ending before `right` has width at most `w`, so the prefix maximum rises to `w + 1`. Slide (`zero_count` exceeded `k`): the width stays `w`, and no wider valid window can exist, because a valid window ending at `right` that started at or before `left` would contain `[left, right]` as a sub-window, and a sub-window of a valid window is valid while `[left, right]` holds more than `k` zeros by the branch condition; the previous width-`w` valid window remains a witness inside the grown prefix. At loop exit the prefix is the whole array, and `len(nums) - left` reads the maximum width off the final window.

#### Walkthrough

Example 1 again, `nums = [1,1,1,0,0,0,1,1,1,1,0]`, `k = 2`, so the never-shrinking ride can be compared with the classic window step by step. The window goes invalid at `right=5` and simply stops growing, sliding forward at the same width until zeros drain out:

```text
right=0..4   zero_count reaches 2      window [0,4]   width 5
right=5   nums 0  zero_count=3  slide: nums[0]=1 leaves, left=1
                                 window [1,5]   width 5   (still invalid)
right=6   nums 1  zero_count=3  slide: nums[1]=1 leaves, left=2
                                 window [2,6]   width 5   (still invalid)
right=7   nums 1  zero_count=3  slide: nums[2]=1 leaves, left=3
                                 window [3,7]   width 5   (still invalid)
right=8   nums 1  zero_count=3  slide: nums[3]=0 leaves, zero_count=2, left=4
                                 window [4,8]   width 5   (valid again)
right=9   nums 1  zero_count=2  window [4,9]   width 6
right=10  nums 0  zero_count=3  slide: nums[4]=0 leaves, zero_count=2, left=5
                                 window [5,10]  width 6
return len(nums) - left = 11 - 5 = 6
```

The width never decreases: it grows to `5`, holds through the invalid stretch, then reaches `6`. The final width `11 - 5 = 6` matches the expected Output for Example 1.

#### Solution

The code is the walkthrough's coast-along loop: grow, slide at most once per step, return the final width.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int], k: int) -> int:
        left = 0
        zero_count = 0
        for right in range(len(nums)):
            if nums[right] == 0:
                zero_count += 1
            if zero_count > k:
                if nums[left] == 0:
                    zero_count -= 1
                left += 1
        return len(nums) - left
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each iteration performs constant work: `right` advances every step and `left` advances at most once per step.

##### Space Complexity: `O(1)`

Two scalar trackers: `left` and `zero_count`.

#### Key Insights

- Removing the width sample is safe because the width is monotone: it never decreases, so the final width is the maximum width ever held.
- The window may run invalid mid-sweep, holding more than `k` zeros while it coasts forward; that is harmless, because the slide fires once per step while any excess zero is aboard, so the width cannot grow past an unearned size.
- `len(nums) - left` reads the answer from the final window and handles the empty array with no guard: the loop never runs and the expression returns `0`.
- The form generalizes to any window rule where a window of width `w + 1` is valid whenever some window of width `w` is; the trade is a subtler correctness argument for slightly leaner code.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n²)` - every start scans forward until its first excess zero.
- **Sliding Window**: `O(n)` - `right` visits every element once and `left` advances at most `n` times total.
- **Non-Shrinking Sliding Window**: `O(n)` - both pointers advance at most once per element.

### Space Complexity

- **Brute Force**: `O(1)` - a counter and the loop scalars.
- **Sliding Window**: `O(1)` - `left`, `zero_count`, and `longest`.
- **Non-Shrinking Sliding Window**: `O(1)` - `left` and `zero_count`.

### Trade-offs

- **Brute Force**: the definition written as code, with no invariants to defend, but the quadratic cost rules it out at the `100000`-element constraint scale.
- **Sliding Window**: the standard linear answer whose window is valid at every step, at the cost of a nested `while` and a per-step width sample.
- **Non-Shrinking Sliding Window**: the same linear cost with the leanest loop, paid for with a monotonicity invariant that takes a moment to trust.

### When to Use Each

- **Brute Force**: to pin down the definition and as the oracle when testing the fast versions on small inputs.
- **Sliding Window (Recommended)**: the interview default: the amortized argument is well known, and the always-valid window makes the width sample self-evidently correct.
- **Non-Shrinking Sliding Window**: once the sliding window is on the board and the interviewer asks for something leaner, or in languages where the branch-free inner step matters.

### Optimization Notes

- Maintain `zero_count` incrementally in both fast versions; re-counting a window per step is the single most common way to lose the linear bound.
- In the classic window, `while` is load-bearing: replacing it with `if` silently turns it into the non-shrinking variant, whose width sample (`right - left + 1`) would then overreport during invalid stretches.
- The non-shrinking form reads its answer from `len(nums) - left` instead of a sampled maximum, which is where its empty-array and no-guard behavior comes from.
- The same three-step shape (grow, repair, sample) solves the whole family of "longest window with at most k rule violations" problems; only the repair condition changes.
