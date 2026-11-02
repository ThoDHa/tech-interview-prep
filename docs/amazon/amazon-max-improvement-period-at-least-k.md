# [Best Improvement Period of at Least K Intervals](https://www.fastprep.io/problems/amazon-max-improvement-period-at-least-k)

**Medium** | **NN minutes** | **Array, Prefix Sum, Dynamic Programming**

A machine learning team tracks how a recommendation model changes over n consecutive time intervals. You are given an integer array changes of length n, where changes[i] is the change in recommendation quality during interval i compared with the interval before it. A positive value is an improvement and a negative value is a decline. You are also given an integer k.

Choose a non-empty period of consecutive intervals [i, j], where 0 <= i <= j < n. The period must contain at least k intervals, so j - i + 1 >= k. Its cumulative improvement is:

## Examples

### Example 1

**Input:** `changes = [3,-2,5,-1,4]`, `k = 2`

**Output:** `10`

**Explanation:** Choose the period [1, 4], which has 4 intervals. Its first change -2 is subtracted, so the score is -(-2) + 5 + (-1) + 4 = 10.

Starting on a decline helps here, because subtracting a negative change adds to the score. The full period [0, 4] scores only -3 + (-2) + 5 + (-1) + 4 = 3, and no other period of at least 2 intervals scores more than 10.

## Constraints

- `N/A (FastPrep lists no constraints)`

## Deriving the Solution

The scoring rule, pinned from the worked example's explanation (the scaffold's formula line did not survive the parse, and both scores the explanation computes confirm it): a period's score adds every change in `[i, j]` except that the first interval's change is subtracted instead of added, so `score(i, j) = -changes[i] + changes[i+1] + ... + changes[j]`. The constraints block is likewise empty in the scaffold, so the gauntlet's corner sizes below are chosen, not statement-derived. One consequence drives the whole ladder: because the subtraction follows the period's start, no static transform of `changes` (negating every element, say) turns the problem into an ordinary maximum-sum window; the flipped element moves with `i`. The ladder keeps `i` explicit:

1. **Start literal.** Walk every qualifying period, summing each one's intervals: see [Every Qualifying Period](#every-qualifying-period).
2. **Prefix sums.** Score any period in constant time from a prefix array, dropping the per-period sum: see [Prefix Sums over Every Start](#prefix-sums-over-every-start).
3. **Cheapest start so far.** The admissible starts for each end form a set that only grows, so one running minimum of start costs replaces the per-end rescan: see [Cheapest Start So Far](#cheapest-start-so-far).

## Solutions

### Every Qualifying Period

#### Derivation

The definition is a direct specification: try every start `i`, extend the end `j` until the period holds at least `k` intervals, keep a running sum of the period's changes, and score by subtracting the first interval's change once instead of adding it:

1. For each start `i`: begin the running sum at `-changes[i]`.
2. For each end `j` from `i + k - 1` to the last index: add `changes[i+1..j]` into the running sum as `j` grows.
3. Track the maximum score over all periods.

#### Walkthrough

Example 1 (`changes = [3,-2,5,-1,4]`, `k = 2`), the strongest contender per start:

```text
start 0: best period [0, 4]: -3 + (-2) + 5 + (-1) + 4 = 3
start 1: best period [1, 4]:  2 +  5 + (-1) + 4    = 10
start 2: best period [2, 4]: -5 + (-1) + 4         = -2
start 3: best period [3, 4]:  1 + 4                = 5
```

The maximum over starts is `10`, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, changes: List[int], k: int) -> int:
        periods = len(changes)
        best = None
        for i in range(periods):
            score = -changes[i]
            for j in range(i, periods):
                if j > i:
                    score += changes[j]
                if j - i + 1 >= k and (best is None or score > best):
                    best = score
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Every period is visited once and extended by one interval per step; the per-period work is shared with the next period through the running sum.

##### Space Complexity: `O(1)`

One running sum and one best-so-far.

#### Key Insights

- The first change must flip sign exactly once per period, at emission time: forgetting the flip scores plain window sums and answers `9` here instead of `10`.
- The running sum makes the inner loop `O(1)` per end; without it the definition costs `O(n^3)`.
- This approach is the oracle: it reads the rule verbatim, so any transformation-based rewrite is checked against it.

### Prefix Sums over Every Start

#### Derivation

A period's score rearranges into two prefix sums plus the flipped first change. With `P[t]` the sum of the first `t` changes, `score(i, j) = -changes[i] + (P[j+1] - P[i+1])`: the flipped first change stays attached to `i`, exactly as the rule requires. Precomputing `P` makes any single period's score constant time, so every qualifying period is one nested pass:

1. Build `P` of length `n + 1`, `P[0] = 0`.
2. For every `i` and every `j >= i + k - 1`: score `P[j+1] - P[i+1] - changes[i]`.
3. Track the maximum.

#### Walkthrough

Example 1's prefix sums are `P = [0, 3, 1, 6, 5, 9]`. The best period per end:

```text
end j = 1: i = 0:  P[2] - P[1] - 3 =  1 - 3 - 3 = -5
end j = 2: i = 1:  P[3] - P[2] + 2 =  6 - 1 + 2 =  7
end j = 3: i = 1:  P[4] - P[2] + 2 =  5 - 1 + 2 =  6
end j = 4: i = 1:  P[5] - P[2] + 2 =  9 - 1 + 2 = 10
```

The best score seen is `10`, matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, changes: List[int], k: int) -> int:
        periods = len(changes)
        prefix = [0] * (periods + 1)
        for t in range(periods):
            prefix[t + 1] = prefix[t] + changes[t]
        best = None
        for i in range(periods):
            for j in range(i + k - 1, periods):
                score = prefix[j + 1] - prefix[i + 1] - changes[i]
                if best is None or score > best:
                    best = score
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Every qualifying period is scored in constant time; there are `O(n^2)` of them.

##### Space Complexity: `O(n)`

The prefix array of `n + 1` entries.

#### Key Insights

- The rearrangement separates the period into a start term and an end term; the flipped first change belongs entirely to the start term.
- The start term `-changes[i] - P[i+1]` depends only on `i`, and the end term `P[j+1]` only on `j`; that separation is what the next rung exploits.
- Nothing here assumes the periods are contiguous windows of a transformed array; the flip rides on `i`.

### Cheapest Start So Far

#### Derivation

Group the nested loops by end. A period ending at `j` must start at some `i <= j - k + 1`, and its score is `P[j+1] - (P[i+1] + changes[i])`: the end term minus a start cost that depends only on `i` (equivalently, the plain window sum `P[j+1] - P[i]` minus twice the first change, which is what flipping it costs). As `j` advances one step, exactly one new start `i = j - k + 1` becomes admissible and no start ever leaves, so the cheapest admissible start cost is a running minimum, updated once per step:

1. Build the prefix array `P`.
2. Walk ends `j` from `k - 1` to `n - 1`; before scoring end `j`, admit the new start `i = j - k + 1` into the running minimum of `P[i+1] + changes[i]`.
3. The candidate for end `j` is `P[j+1] - cheapest`; track the maximum.

#### Walkthrough

Example 1 again, with the start costs `g(i) = P[i+1] + changes[i]`:

```text
g(0) = 3 + 3  =  6    g(1) = 1 + (-2) = -1    g(2) = 6 + 5 = 11    g(3) = 5 + (-1) = 4

end j = 1: admit g(0) =  6; cheapest  6; P[2] -  6 =  1 -  6 = -5
end j = 2: admit g(1) = -1; cheapest -1; P[3] + 1 =  6 + 1 =  7
end j = 3: admit g(2) = 11; cheapest -1; P[4] + 1 =  5 + 1 =  6
end j = 4: admit g(3) =  4; cheapest -1; P[5] + 1 =  9 + 1 = 10
```

The maximum candidate is `10`, matching the expected Output; the cheapest start is start 1, the decline the example's explanation starts on.

#### Solution

```python
from typing import List


class Solution:
    def solve(self, changes: List[int], k: int) -> int:
        periods = len(changes)
        prefix = [0] * (periods + 1)
        for t in range(periods):
            prefix[t + 1] = prefix[t] + changes[t]
        best = None
        cheapest = None
        for end in range(k - 1, periods):
            start = end - k + 1
            start_cost = prefix[start + 1] + changes[start]
            if cheapest is None or start_cost < cheapest:
                cheapest = start_cost
            candidate = prefix[end + 1] - cheapest
            if best is None or candidate > best:
                best = candidate
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass builds the prefix array; one pass over the ends admits each start and scores each end exactly once.

##### Space Complexity: `O(n)`

The prefix array; the running minimum and maximum are two scalars.

#### Key Insights

- The admissible-start set grows by one and never shrinks, which is why a running minimum needs no sliding-window deque: there is nothing to evict.
- The start cost `P[i+1] + changes[i]` is the prefix through `i` plus a second payment of `changes[i]`: everything before the window is given up, and the first change is given up twice (dropped from the sum, then subtracted). Start 1 wins here because its negative change makes that double payment a double bonus.
- The `k = 1` edge needs no special case: the first end is `0` and single-interval periods score `-changes[i]`, all through the same formula.

## Comparison of Solutions

### Time Complexity

- **Every Qualifying Period**: `O(n^2)` - each period extended once per end.
- **Prefix Sums over Every Start**: `O(n^2)` - constant-time scores, all pairs visited.
- **Cheapest Start So Far**: `O(n)` - one pass over the ends.

### Space Complexity

- **Every Qualifying Period**: `O(1)` - a running sum.
- **Prefix Sums over Every Start**: `O(n)` - the prefix array.
- **Cheapest Start So Far**: `O(n)` - the prefix array plus two scalars.

### Trade-offs

- **Every Qualifying Period**: the rule verbatim and the natural oracle; quadratic even though every score it needs is derivable in constant time.
- **Prefix Sums over Every Start**: constant-time scoring exposes the start/end separation the fast rung needs; still visits every pair.
- **Cheapest Start So Far (Recommended)**: linear time, one pass, and the only subtlety is admitting each start exactly when it becomes admissible.

### When to Use Each

- **Every Qualifying Period**: first on the whiteboard to pin the rule, and always as the independent checker for the faster rungs.
- **Prefix Sums over Every Start**: when the interviewer asks for a first speedup; the separation it exposes is the derivation of the linear rung.
- **Cheapest Start So Far (Recommended)**: the answer to give: linear, constant extra state beyond the prefix array, and a one-line explanation of why the running minimum is enough.

### Optimization Notes

- The running minimum never needs a monotonic deque on this statement, because the admissible start window's left edge never moves; a variant that capped period length would need one.
- The same start-cost decomposition solves the length-constrained maximum-average variant: maximize `P[j+1] - P[i+1]` over `j - i + 1 >= k` is the special case where no first change is flipped.
- The scaffold carries no parsed constraints, so no bound-specific claim is made here; the linear scan and the prefix array fit any plausible bound for this problem class, and the constructed scale corners in the gauntlet run six-figure period counts.
