# [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/)

**Medium** | **25 minutes** | **Array, Dynamic Programming**

**Pattern:** [DP 1D Linear](../patterns/dp_1d_linear/intuition.md)

**Algorithm:** [Kadane's algorithm](https://en.wikipedia.org/wiki/Maximum_subarray_problem) · [Dynamic programming](https://en.wikipedia.org/wiki/Dynamic_programming) · [Recurrence relation](https://en.wikipedia.org/wiki/Recurrence_relation)

**Practice:** [`practice/maximum_product_subarray/solution.py`](../../practice/maximum_product_subarray/solution.py)

Given an integer array `nums`, find a **subarray** that has the largest product, and return the product.

A **subarray** is a contiguous non-empty sequence of elements within an array.

You can assume the output will fit into a **32-bit** integer.

**Note** that the product of an array with a single element is the value of that element.

## Examples

### Example 1

**Input:** `nums = [2,4,-3,5]`

**Output:** `8`

**Explanation:** `[2,4]` has the largest product `8`.

### Example 2

**Input:** `nums = [-3,0,-2]`

**Output:** `0`

**Explanation:** The result cannot be `6`, because `[-3,-2]` is not a subarray.

## Constraints

- `1 <= nums.length <= 20,000`
- `-10 <= nums[i] <= 10`
- The product of any subarray of `nums` is **guaranteed** to fit in a **32-bit** integer.

## Deriving the Solution

A subarray is fixed by its two endpoints, so the literal search enumerates pairs of endpoints and is quadratic. Every faster solution replaces one endpoint with a quantity carried through a single left-to-right scan, and products add one twist sums never have: multiplying by a negative number flips the ordering, so the scan must carry both ends of the value range.

1. **Start literal.** Fix each start index and sweep the ends, carrying a
   running product so each extension costs one multiplication. Correct, but the
   sweep restarts for every start, costing `O(n^2)`: see [Brute Force](#brute-force).
2. **Spot the waste.** Ask the narrower question Kadane's algorithm asks for
   sums: what is the largest product of a subarray that ends exactly at index
   `i`? That answer extends in constant time, but with products the extension
   hides a trap: multiplying by a negative turns the largest ending product
   into the smallest and the smallest into the largest, so a single running
   maximum is not enough state to extend.
3. **Carry both extremes.** Keep the smallest ending product alongside the
   largest; every index then picks the best of three candidates and the fill is
   one `O(n)` pass: see [Bottom-Up DP](#bottom-up-dp).
4. **Shrink the state.** Each entry reads only the previous pair, so the two
   tables collapse into two rolling scalars and the space drops to `O(1)`: see
   [Kadane's Algorithm with Min-Max Tracking](#kadanes-algorithm-with-min-max-tracking).

## Solutions

### Brute Force

#### Derivation

The most direct reading enumerates every contiguous span, multiplies it out, and keeps the largest product. A span is fixed by its start and end indices, and a running product makes each extension constant work:

1. Initialize `best` to `nums[0]` so the answer is valid even when every
   number is negative.
2. For each start index, reset `current` to `1`, the empty product.
3. Sweep `end` from `start` to the array's end, multiplying `nums[end]` into
   `current` so it always holds the product of `nums[start..end]`.
4. Update `best` with `max(best, current)` at every pair.
5. Return `best` after all pairs are examined.

Carrying the running product across the inner loop keeps the work quadratic rather than cubic: each span costs one multiplication instead of a re-multiplication of the whole span.

#### Walkthrough

Let us run the pair scan by hand on Example 1: `nums = [2, 4, -3, 5]`. The outer loop fixes `start` and resets `current = 1`; the inner sweep multiplies each `nums[end]` in and updates `best`. Each row below is one `(start, end)` pair: the element just multiplied in, the running `current` product, and `best` after the update.

| `start` | `end` | `nums[end]` | `current` (product of `nums[start..end]`) | `best` |
| ------- | ----- | ----------- | ----------------------------------------- | ------ |
| 0 | 0 | `2`  | `2`    | `2`  |
| 0 | 1 | `4`  | `8`    | `8`  |
| 0 | 2 | `-3` | `-24`  | `8`  |
| 0 | 3 | `5`  | `-120` | `8`  |
| 1 | 1 | `4`  | `4`    | `8`  |
| 1 | 2 | `-3` | `-12`  | `8`  |
| 1 | 3 | `5`  | `-60`  | `8`  |
| 2 | 2 | `-3` | `-3`   | `8`  |
| 2 | 3 | `5`  | `-15`  | `8`  |
| 3 | 3 | `5`  | `5`    | `8`  |

The first row sets `best = 2`, the second lifts it to `8`, the product of `[2, 4]`. Every span that reaches the `-3` at index `2` turns negative, and no later start recovers a larger positive product, so `best` stays `8` through the last pair. The scan returns `8`, which matches the expected Output for Example 1.

#### Solution

The code is the walkthrough's double loop: fix `start`, grow `end`, carry `current`.

```python
from typing import List


class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        n = len(nums)
        best = nums[0]

        for start in range(n):
            current = 1
            for end in range(start, n):
                current *= nums[end]
                best = max(best, current)

        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The outer loop fixes each of the `n` start indices and the inner sweep runs to the array's end, so the number of `(start, end)` pairs is about `n^2 / 2`, each handled with one multiplication and one comparison.

##### Space Complexity: `O(1)`

Only the `best` and `current` scalars are tracked, regardless of input size.

#### Key Insights

- Seeding `best` with `nums[0]` rather than `0` or `1` is what makes single-element and all-negative arrays correct: the answer may be negative, and the answer may be the lone element itself.
- The running product buys the drop from `O(n^3)` to `O(n^2)`; nothing is remembered between starts, which is exactly the waste the later solutions remove.
- Too slow near the `20,000` constraint cap, where the pair count reaches into the hundreds of millions, which motivates the linear approaches.

### Bottom-Up DP

#### Derivation

The brute force relearns every suffix from scratch, but the narrower question extends: the largest product of a subarray ending at `i` is either `nums[i]` alone or `nums[i]` times some product that ends at `i - 1`. The trap from the derivation arc decides what "some product" must include: a negative `nums[i]` flips signs, so the least ending product can become the greatest. Keep both extremes per index:

1. Let `best[i]` be the largest product of a subarray ending at `i`, and
   `worst[i]` the smallest.
2. Seed `best[0] = worst[0] = nums[0]`: over one element, the two coincide.
3. At each later index form the three candidates `nums[i]`,
   `nums[i] * best[i - 1]`, and `nums[i] * worst[i - 1]`; `best[i]` takes their
   max and `worst[i]` their min.
4. Track `answer` as the running max of every `best[i]` and return it after the
   fill.

#### Recurrence

Let `best[i]` be the largest product of a subarray that ends exactly at index `i`, and `worst[i]` the smallest. Such a subarray is either the single element `nums[i]` or `nums[i]` glued onto a subarray ending at `i - 1`, and gluing multiplies the whole earlier product by `nums[i]`:

$$ best[i] = \begin{cases} \text{nums}[0], & i = 0 \\[4pt] \max\bigl(\text{nums}[i],\ \text{nums}[i] \cdot best[i-1],\ \text{nums}[i] \cdot worst[i-1]\bigr), & i \ge 1 \end{cases} $$

$$ worst[i] = \begin{cases} \text{nums}[0], & i = 0 \\[4pt] \min\bigl(\text{nums}[i],\ \text{nums}[i] \cdot best[i-1],\ \text{nums}[i] \cdot worst[i-1]\bigr), & i \ge 1 \end{cases} $$

```text
best[0]  = worst[0] = nums[0]
best[i]  = max(nums[i], nums[i] * best[i - 1], nums[i] * worst[i - 1])   for i >= 1
worst[i] = min(nums[i], nums[i] * best[i - 1], nums[i] * worst[i - 1])   for i >= 1
```

The answer maximizes over every endpoint:

$$ \text{answer} = \max_{0 \le i < n}\ best[i] $$

```text
answer = max(best[i]) over 0 <= i < n
```

The third candidate is the whole point. When `nums[i]` is negative, multiplying flips signs, so the previous smallest product `worst[i - 1]` can turn into the current largest and the previous largest into the current smallest. The single element `nums[i]` covers starting fresh, which is what rescues the scan at a zero or at the lone positive that beats every run around it.

#### Walkthrough

Example 2 exercises zeros, but no official example makes the stored minimum win, so this walkthrough uses the tailored array `nums = [-2, 3, -4]`, whose product is maximized by taking the whole array. `best[0]` and `worst[0]` seed at `-2`, and each row shows the three candidates the recurrence forms:

```text
start    best = [-2, 0, 0]    worst = [-2, 0, 0]     answer = -2
i = 1    candidates (3, 3 * -2, 3 * -2) = (3, -6, -6)
         best[1] = 3          worst[1] = -6          answer = 3
i = 2    candidates (-4, -4 * 3, -4 * -6) = (-4, -12, 24)
         best[2] = 24         worst[2] = -12         answer = 24
```

The flip happens at `i = 2`: the stored minimum `-6` is multiplied by the negative `-4` and produces `24`, which beats both the single element and the extension of the previous maximum. The method returns `answer = 24`, the product of the whole array. Example 2's `[-3, 0, -2]` shows the same machinery handling a zero: the candidates at `i = 1` are all `0`, both extremes collapse to `0`, and `answer` stays `0` through the end.

#### Solution

The code is the table fill from the walkthrough: seed both extremes, then loop the recurrence upward while raising `answer`.

```python
from typing import List


class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        n = len(nums)
        # best[i] / worst[i]: largest / smallest product of a subarray ending at i
        best = [0] * n
        worst = [0] * n
        best[0] = worst[0] = nums[0]
        answer = nums[0]

        for i in range(1, n):
            # A negative nums[i] can turn the smallest ending product into
            # the largest candidate, so worst[i - 1] joins the max
            candidates = (nums[i], nums[i] * best[i - 1], nums[i] * worst[i - 1])
            best[i] = max(candidates)
            worst[i] = min(candidates)
            answer = max(answer, best[i])

        return answer
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass seeds the base case and one pass applies the recurrence: three candidates, one max, one min, and one comparison per index.

##### Space Complexity: `O(n)`

The `best` and `worst` tables store one entry per index each.

#### Key Insights

- The third candidate `nums[i] * worst[i - 1]` is the entire trick: it is the product of a real subarray, and it wins exactly when a negative `nums[i]` completes a favorable run of signs.
- Dropping `worst` and keeping only the largest ending product reduces the method to plain Kadane's, which answers `3` instead of `24` on the walkthrough input.
- The answer is a running max over `best[i]`, not `best[n - 1]`: the winning subarray may end early, and in Example 1 the `8` sits at index `1` and no later entry beats it.

### Kadane's Algorithm with Min-Max Tracking

#### Derivation

The table fill reads only one step back: `best[i]` and `worst[i]` are computed from `best[i - 1]` and `worst[i - 1]`, and everything older is dead weight. Collapse the two tables into two rolling scalars, `best_ending` and `worst_ending`, and keep a running `answer` alongside them:

1. Seed `best_ending = worst_ending = answer = nums[0]`: before the first
   index there is exactly the one-element subarray, and the answer must contain
   at least one element.
2. For each later element, form the same three candidates `nums[i]`,
   `nums[i] * best_ending`, and `nums[i] * worst_ending`.
3. Overwrite `best_ending` with their max and `worst_ending` with their min.
4. Raise `answer` to `max(answer, best_ending)` and return it after the pass.

Seeding at `nums[0]` instead of `0` or `1` matters as much as the candidate list: a `0` seed answers `0` on every all-negative array, and a `1` seed reports `1` for `[-5]`.

#### Walkthrough

Let us roll the scalars through Example 1: `nums = [2, 4, -3, 5]`. Both scalars seed at `2`, and each row shows the candidate triple and the overwrites:

```text
i=0  nums[0]= 2   seeded                      best_ending = 2   worst_ending = 2     answer = 2
i=1  nums[1]= 4   candidates (4, 8, 8)        best_ending = 8   worst_ending = 4     answer = 8
i=2  nums[2]=-3   candidates (-3, -24, -12)   best_ending = -3  worst_ending = -24   answer = 8
i=3  nums[3]= 5   candidates (5, -15, -120)   best_ending = 5   worst_ending = -120  answer = 8
```

At `i = 2` the negative `-3` turns the stored maximum `8` into a liability: `-24` becomes the new minimum while `best_ending` falls to `-3`. The positive `5` at `i = 3` rewards neither liability, because `-15` and `-120` both lose to the lone element, so `answer` stays `8` from index `1` on, matching the expected Output for Example 1. On Example 2 the zero at `nums[1]` drives every candidate to `0`, both scalars collapse to `0`, and `answer` ends at `0`.

#### Solution

The code is the walkthrough's rolling update: one candidate triple, two overwrites, one `answer` raise per element.

```python
from typing import List


class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        best_ending = nums[0]
        worst_ending = nums[0]
        answer = nums[0]

        for i in range(1, len(nums)):
            # All three candidates are products of real subarrays ending at
            # i; the minimum must be carried because a negative nums[i]
            # flips which extreme can become the largest
            candidates = (nums[i], nums[i] * best_ending, nums[i] * worst_ending)
            best_ending = max(candidates)
            worst_ending = min(candidates)
            answer = max(answer, best_ending)

        return answer
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The array is traversed exactly once, with constant work per element: three candidate products, one max, one min, and one comparison.

##### Space Complexity: `O(1)`

Three scalars, `best_ending`, `worst_ending`, and `answer`, regardless of input size.

#### Key Insights

- One pass at constant space: the same loop as the table fill with each array replaced by its two live entries.
- The `candidates` tuple is not just shorter code: it freezes the previous step's snapshot, so both overwrites read the old pair and the read-after-write ordering bug the two-scalar update invites cannot happen.
- Every candidate is the product of a real subarray, so the problem's 32-bit guarantee covers all intermediate values; fixed-width languages need no wider accumulator.

## Comparison of Solutions

The practice harness's `practice/maximum_product_subarray/reference.py` implements the **Kadane's Algorithm with Min-Max Tracking** solution.

### Time Complexity

- **Brute Force**: `O(n^2)` - every start extends its own sweep, so the pair count is about `n^2 / 2`.
- **Bottom-Up DP**: `O(n)` - one pass fills both tables with constant work per index.
- **Kadane's Algorithm with Min-Max Tracking**: `O(n)` - the same pass with the tables collapsed to two scalars.

### Space Complexity

- **Brute Force**: `O(1)` - only `best` and the running `current` product.
- **Bottom-Up DP**: `O(n)` - the `best` and `worst` tables, one entry per index.
- **Kadane's Algorithm with Min-Max Tracking**: `O(1)` - `best_ending`, `worst_ending`, and `answer`.

### Trade-offs

- The Brute Force is the easiest to derive and trust, but its quadratic pair count is hopeless at the `20,000` constraint cap.
- The Bottom-Up DP pays one entry per index for each extreme, keeping every "best subarray ending here" answer in view, which only pays off when those per-index answers are queried again by a variant.
- Kadane's Algorithm with Min-Max Tracking keeps exactly the two live entries and a running answer, reaching the linear-time constant-space optimum with no new risk.

### When to Use Each

- **Brute Force**: as the derivational baseline and a correctness oracle for checking the faster versions on small arrays.
- **Bottom-Up DP**: when a variant needs the per-index extremes (for example, reporting where the winning subarray ends) or when a table is easier to explain.
- **Kadane's Algorithm with Min-Max Tracking** (recommended): the default answer; one pass, constant space, and the sign-flip reasoning is the insight the problem exists to teach.

### Optimization Notes

- Both linear approaches form every candidate as the product of a real subarray, so the 32-bit guarantee covers all intermediates; no wider integer type is needed even in fixed-width languages.
- Seeding at `nums[0]`, never `0` or `1`, is what keeps single-element and all-negative arrays honest: a `0` seed answers `0` on `[-2, -3]`, and a `1` seed answers `1` on `[-5]`.
- The tuple-of-candidates idiom does more than shorten the code: it forces both overwrites to read the previous step's snapshot, removing the read-after-write ordering bug that hand-rolling the two scalar updates invites.
- For the `20,000`-element cap the linear scans are the interview bar; the Brute Force would need roughly `2 * 10^8` multiplications.
