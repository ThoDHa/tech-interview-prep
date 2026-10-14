# [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/)

**Medium** | **30 minutes** | **Array, Prefix Sum**

**Pattern:** [Prefix Sum](../patterns/prefix_sum/intuition.md)

**Algorithm:** [Prefix sum](https://en.wikipedia.org/wiki/Prefix_sum)

**Practice:** [`practice/product_of_array_except_self/solution.py`](../../practice/product_of_array_except_self/solution.py)

Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`.

The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in `O(n)` time and without using the division operation.

## Examples

### Example 1

**Input:** `nums = [1,2,3,4]`

**Output:** `[24,12,8,6]`

**Explanation:** `answer[0] = 2*3*4 = 24`, `answer[1] = 1*3*4 = 12`, `answer[2] = 1*2*4 = 8`, and `answer[3] = 1*2*3 = 6`.

### Example 2

**Input:** `nums = [-1,1,0,-3,3]`

**Output:** `[0,0,9,0,0]`

**Explanation:** Every position except index `2` includes the zero in its product, so it becomes `0`. Index `2` is the product of the remaining elements, `(-1)*1*(-3)*3 = 9`.

## Constraints

- `2 <= nums.length <= 10^5`
- `-30 <= nums[i] <= 30`
- The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.

## Follow-up

Can you solve the problem in `O(1)` extra space complexity? (The output array does not count as extra space for space complexity analysis.)

## Deriving the Solution

The product of everything except `nums[i]` splits at `i` into two independent halves: everything to its left times everything to its right. Every solution below computes those two halves; they differ in how much work and memory the halves cost.

1. **Start literal.** For each index, multiply every other element in a fresh
   inner pass. Correct, but each pass recomputes products the previous pass already knew, costing `O(n^2)`: see [Brute Force](#brute-force).
2. **Name the waste.** The inner pass rebuilds "product of the left part" and
   "product of the right part" from scratch for every `i`, yet each of those extends its neighbor by a single factor. Precompute them: a `prefix` array rolled forward and a `suffix` array rolled backward give `result[i] = prefix[i] * suffix[i]` in `O(n)` time and `O(n)` extra space: see [Prefix and Suffix Arrays](#prefix-and-suffix-arrays).
3. **Answer the follow-up.** The prefix array can live inside the output array,
   and the suffix side never needs more than one running scalar folded in on a reverse sweep, reaching `O(1)` extra space: see [Constant-Space Prefix and Suffix](#constant-space-prefix-and-suffix).
4. **The forbidden shortcut.** Dividing the total product by `nums[i]` looks
   simpler, but the problem bans division, and zeros break it anyway; it is included for contrast: see [Division Method](#division-method).

## Solutions

### Brute Force

#### Derivation

The brute force asks the problem's question verbatim: for each index `i`, what is the product of every element other than `nums[i]`? Nothing needs to be observed or reformulated; simply compute that product afresh for each position:

1. For each index `i`, start a running `product` of `1`.
2. Walk the whole array with `j`, multiplying in every `nums[j]` where
   `j != i`.
3. Append that `product` to `result`.

It is correct and easy to read, but it recomputes overlapping products for every position, which makes it too slow for large arrays.

#### Walkthrough

Let us watch the Brute Force run on Example 1: `nums = [1,2,3,4]`. The outer loop fixes one index `i`, then the inner loop multiplies in every `nums[j]` where `j != i`, building up a fresh `product` that starts at `1`.

Here is the outer loop, one row per value of `i`. Each row shows how `product` grows as the inner loop visits the other indices, then the value appended to `result`:

| `i` | element skipped | inner-loop products (`product` after each `j != i`) | appended | `result` so far |
| --- | --- | --- | --- | --- |
| `0` | `nums[0] = 1` | `1*2=2`, then `2*3=6`, then `6*4=24` | `24` | `[24]` |
| `1` | `nums[1] = 2` | `1*1=1`, then `1*3=3`, then `3*4=12` | `12` | `[24, 12]` |
| `2` | `nums[2] = 3` | `1*1=1`, then `1*2=2`, then `2*4=8` | `8` | `[24, 12, 8]` |
| `3` | `nums[3] = 4` | `1*1=1`, then `1*2=2`, then `2*3=6` | `6` | `[24, 12, 8, 6]` |

Reading one row to see the mechanism: at `i = 1` the inner loop skips `nums[1] = 2`, so it multiplies `1` (start) by `nums[0]=1`, then `nums[2]=3`, then `nums[3]=4`, giving `1*3*4 = 12`.

After the outer loop finishes all four indices, the function returns `result = [24, 12, 8, 6]`, which matches the example's expected Output `[24,12,8,6]`.

#### Solution

The code is the nested loop pair from the walkthrough: fix `i`, multiply over every `j != i`.

```python
from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = []

        # For each position, multiply every other element
        for i in range(n):
            product = 1
            for j in range(n):
                if j != i:
                    product *= nums[j]
            result.append(product)

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

For each of the `n` elements, we iterate through all `n` elements to compute the product.

##### Space Complexity: `O(1)`

Only a single running-product variable is used, not counting the output array.

#### Key Insights

- It mirrors the problem statement literally, which makes it the natural first attempt.
- The repeated inner pass wastes work: the product of "everything before `i`" and "everything after `i`" is recomputed from scratch each time.

### Prefix and Suffix Arrays

#### Derivation

The brute force's inner loop is the flaw: the products it computes overlap almost entirely between consecutive positions, yet each is rebuilt from scratch. Split the target product at the excluded index instead. Everything except `nums[i]` is (everything before `i`) times (everything after `i`), and each of those families grows by one factor per step, so both can be tabulated in a single linear pass apiece: the multiplicative analogue of a [prefix sum](https://en.wikipedia.org/wiki/Prefix_sum). Build the two pieces explicitly:

1. **Prefix array**: `prefix[i]` holds the product of all elements before
   index `i`. Seed `prefix[0] = 1` and roll forward with `prefix[i] = prefix[i - 1] * nums[i - 1]`.
2. **Suffix array**: `suffix[i]` holds the product of all elements after index
   `i`. Seed `suffix[n - 1] = 1` and roll backward with `suffix[i] = suffix[i + 1] * nums[i + 1]`.
3. **Combine**: `result[i] = prefix[i] * suffix[i]`.

Seeding the boundaries with `1` (the multiplicative identity) makes the first and last positions fall out correctly without special cases.

#### Formula

The target is a product that skips one index:

$$ \text{result}[i] = \prod_{\substack{0 \le j < n \\ j \ne i}} \text{nums}[j] $$

```text
result[i] = product of nums[j] over 0 <= j < n with j != i
```

Splitting that product at `i` factors it into a left half and a right half. This is the multiplicative analogue of a [prefix sum](https://en.wikipedia.org/wiki/Prefix_sum), with \(\prod\) in place of \(\sum\) and `1` in place of `0` as the identity:

$$ \text{result}[i] = \underbrace{\prod_{j<i} \text{nums}[j]}_{\text{prefix}[i]} \ \cdot \ \underbrace{\prod_{j>i} \text{nums}[j]}_{\text{suffix}[i]} $$

```text
prefix[i] = product of nums[j] over j < i
suffix[i] = product of nums[j] over j > i
result[i] = prefix[i] * suffix[i]
```

Each side is a one-step recurrence, so both tables fill in linear time:

$$ \text{prefix}[i] = \text{prefix}[i-1] \cdot \text{nums}[i-1], \qquad \text{suffix}[i] = \text{suffix}[i+1] \cdot \text{nums}[i+1] $$

```text
prefix[0] = 1,  suffix[n - 1] = 1         (the empty product)
prefix[i] = prefix[i - 1] * nums[i - 1]   for i >= 1
suffix[i] = suffix[i + 1] * nums[i + 1]   for i <= n - 2
```

An empty product is `1`, which is why `prefix[0]` and `suffix[n-1]` are seeded there. Because the index `i` is never a factor on either side, this stays correct when `nums[i]` is zero: the reason it beats the division approach further down, which needs a special case for zeros.

#### Walkthrough

Let us fill the three passes by hand on Example 1: `nums = [1,2,3,4]`, `n = 4`.

The forward pass seeds `prefix[0] = 1` and rolls each new entry from the last:

```text
prefix = [1, 1, 1, 1]                              seed: empty product before 0
i = 1   prefix[1] = prefix[0]*nums[0] = 1*1 = 1    prefix = [1, 1, 1, 1]
i = 2   prefix[2] = prefix[1]*nums[1] = 1*2 = 2    prefix = [1, 1, 2, 1]
i = 3   prefix[3] = prefix[2]*nums[2] = 2*3 = 6    prefix = [1, 1, 2, 6]
```

The backward pass mirrors it from the right, seeding `suffix[3] = 1`:

```text
suffix = [1, 1, 1, 1]                              seed: empty product after 3
i = 2   suffix[2] = suffix[3]*nums[3] = 1*4 = 4    suffix = [1, 1, 4, 1]
i = 1   suffix[1] = suffix[2]*nums[2] = 4*3 = 12   suffix = [1, 12, 4, 1]
i = 0   suffix[0] = suffix[1]*nums[1] = 12*2 = 24  suffix = [24, 12, 4, 1]
```

The combine pass multiplies the halves position by position:

```text
result[0] = prefix[0]*suffix[0] = 1*24 = 24
result[1] = prefix[1]*suffix[1] = 1*12 = 12
result[2] = prefix[2]*suffix[2] = 2*4  = 8
result[3] = prefix[3]*suffix[3] = 6*1  = 6
```

`result = [24, 12, 8, 6]` matches the expected Output for Example 1: each entry is the product of everything left of `i` times everything right of `i`, with `nums[i]` itself never multiplied in.

#### Solution

The code is the three passes from the walkthrough, one loop each.

```python
from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)

        # prefix[i] = product of all elements before index i
        prefix = [1] * n
        for i in range(1, n):
            prefix[i] = prefix[i - 1] * nums[i - 1]

        # suffix[i] = product of all elements after index i
        suffix = [1] * n
        for i in range(n - 2, -1, -1):
            suffix[i] = suffix[i + 1] * nums[i + 1]

        # result[i] = prefix[i] * suffix[i]
        result = []
        for i in range(n):
            result.append(prefix[i] * suffix[i])

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Three separate linear passes: build the prefix array, build the suffix array, and combine them.

##### Space Complexity: `O(n)`

Two auxiliary arrays of size `n` hold the prefix and suffix products, in addition to the output array.

#### Key Insights

- The decomposition `answer[i] = (product of the left) * (product of the right)` is the heart of the problem and avoids division entirely.
- Initializing both arrays to `1` handles the empty-prefix and empty-suffix edge positions cleanly.

### Constant-Space Prefix and Suffix

#### Derivation

The two auxiliary arrays are more memory than the idea needs, and the follow-up asks for their removal. Two observations eliminate them. First, the output array has to be filled anyway, so the forward pass can write the [prefix products](https://en.wikipedia.org/wiki/Prefix_sum) straight into `result`. Second, the backward pass only ever reads one suffix value at a time, so a single running scalar `suffix_product` replaces the whole suffix array:

1. **Pass 1**: store the prefix products directly in the output array, so
   `result[i]` becomes the product of everything before `i`.
2. **Pass 2**: sweep right to left with `suffix_product = 1`; at each `i`,
   multiply `result[i] *= suffix_product` first, then fold the current element in with `suffix_product *= nums[i]`.

The output array doubles as the prefix store, and the suffix only ever needs a single scalar, so no extra arrays are required.

#### Walkthrough

Let us run both passes on Example 1: `nums = [1,2,3,4]`. Pass 1 is the prefix fill from the previous walkthrough, now landing in `result` itself:

```text
result = [1, 1, 1, 1]                        seeded with 1s
i = 1   result[1] = result[0]*nums[0] = 1    result = [1, 1, 1, 1]
i = 2   result[2] = result[1]*nums[1] = 2    result = [1, 1, 2, 1]
i = 3   result[3] = result[2]*nums[2] = 6    result = [1, 1, 2, 6]
```

Pass 2 sweeps right to left. Entering each `i`, `suffix_product` holds the product of everything after `i`: multiply it in first, then fold `nums[i]` into it:

```text
suffix_product = 1
i = 3   result[3] *= 1  -> 6    suffix_product *= 4 -> 4    result = [1, 1, 2, 6]
i = 2   result[2] *= 4  -> 8    suffix_product *= 3 -> 12   result = [1, 1, 8, 6]
i = 1   result[1] *= 12 -> 12   suffix_product *= 2 -> 24   result = [1, 12, 8, 6]
i = 0   result[0] *= 24 -> 24   suffix_product *= 1 -> 24   result = [24, 12, 8, 6]
```

The ordering inside each step is the crux: `result[i]` must be scaled by the suffix *before* `nums[i]` joins it, or the excluded element would leak into its own answer. The final `result = [24, 12, 8, 6]` matches the expected Output for Example 1, now with no auxiliary arrays.

#### Solution

The code is the two passes from the walkthrough: prefix products into `result`, suffix as a single scalar.

```python
from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [1] * n

        # Pass 1: store prefix products directly in the result array
        # result[i] becomes the product of all elements before index i
        for i in range(1, n):
            result[i] = result[i - 1] * nums[i - 1]

        # Pass 2: fold in suffix products using a single running variable
        suffix_product = 1
        for i in range(n - 1, -1, -1):
            result[i] *= suffix_product
            suffix_product *= nums[i]

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Two linear passes through the array.

##### Space Complexity: `O(1)`

Only the scalar `suffix_product` is extra; the output array does not count toward space complexity.

#### Key Insights

- Reusing the output array to hold prefix products is the key trick that collapses `O(n)` auxiliary space to `O(1)`.
- A suffix only needs to be remembered as a single accumulating scalar, never as a full array.
- This meets every stated constraint: `O(n)` time, no division, and `O(1)` extra space.

### Division Method

#### Derivation

There is a tempting shortcut the constraints exist to block: the product of everything except `nums[i]` is simply the total product divided by `nums[i]`. If division were allowed, one pass would compute `total_product` and a second would divide it out per position. The complication is zeros, which make division undefined, so they are handled by cases:

1. Compute the product of all non-zero elements in `total_product` while
   counting zeros in `zero_count` and remembering `zero_index`.
2. **Two or more zeros**: every position's product includes a zero, so return
   all zeros.
3. **Exactly one zero**: only the zero position is non-zero (the product of
   the others); every other position is `0`.
4. **No zeros**: divide `total_product` by each element.

This approach violates the problem's explicit "no division" rule, so it is included for contrast rather than as a submission.

#### Walkthrough

Example 2, `nums = [-1,1,0,-3,3]`, exercises the delicate branch: exactly one zero. The counting pass multiplies the non-zero elements and tracks the zero:

```text
i = 0   num = -1   total_product = -1
i = 1   num = 1    total_product = -1
i = 2   num = 0    zero_count = 1, zero_index = 2   (total_product untouched)
i = 3   num = -3   total_product = 3
i = 4   num = 3    total_product = 9
```

`zero_count` is exactly `1`, so the build pass hands `total_product` to the zero's position and `0` to every other position, since every other product includes the zero at index `2`:

```text
result = [0, 0, 9, 0, 0]
```

This matches the expected Output for Example 2. Had a second zero appeared, the counting pass would have returned `[0] * n` immediately; with no zeros at all, each position would receive `total_product // num` instead.

#### Solution

The code is the count-then-dispatch structure from the walkthrough, one branch per zero count.

```python
from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)

        # Total product of all non-zero elements, plus zero bookkeeping
        total_product = 1
        zero_count = 0
        zero_index = -1

        for i, num in enumerate(nums):
            if num == 0:
                zero_count += 1
                zero_index = i
                if zero_count > 1:
                    # Two or more zeros: every product is 0
                    return [0] * n
            else:
                total_product *= num

        result = []
        if zero_count == 1:
            # Only the zero position gets the product of the others
            for i in range(n):
                result.append(total_product if i == zero_index else 0)
        else:
            # No zeros: divide the total product by each element
            for num in nums:
                result.append(total_product // num)

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass to accumulate the product and count zeros, then one pass to build the result.

##### Space Complexity: `O(1)`

Only a few scalars for the product, the zero count, and the zero index.

#### Key Insights

- Division reduces the problem to one total product, but the zero corner cases are fragile and easy to get wrong.
- The problem forbids division precisely to push toward the prefix/suffix technique, which generalizes to non-invertible operations.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - for each of the `n` elements, iterate through all `n` elements to compute the product.
- **Prefix and Suffix Arrays**: `O(n)` - three linear passes to build prefix, build suffix, and combine.
- **Constant-Space Prefix and Suffix**: `O(n)` - two linear passes through the array.
- **Division Method**: `O(n)` - one pass for the total product and zero count, one pass to build the result.

### Space Complexity

- **Brute Force**: `O(1)` - a single running-product variable, not counting the output array.
- **Prefix and Suffix Arrays**: `O(n)` - two extra arrays of size `n` for the prefix and suffix products.
- **Constant-Space Prefix and Suffix**: `O(1)` - only a single `suffix_product` scalar; the output array does not count.
- **Division Method**: `O(1)` - a few scalars for the product, zero count, and zero index.

### Trade-offs

- **Brute Force**: simplest to write, but quadratic time makes it impractical for large inputs.
- **Prefix and Suffix Arrays**: clear and easy to reason about, at the cost of `O(n)` auxiliary space.
- **Constant-Space Prefix and Suffix**: optimal space while staying linear, at the cost of being slightly less obvious.
- **Division Method**: intuitive when division is allowed, but it breaks the problem constraint and needs careful zero handling.

### When to Use Each

- **Brute Force**: only for understanding the problem or for very small arrays.
- **Prefix and Suffix Arrays**: a good stepping stone for learning the technique before optimizing space.
- **Constant-Space Prefix and Suffix** (recommended): best for interviews; it satisfies every constraint with optimal complexity.
- **Division Method**: only if the no-division constraint is explicitly lifted and zeros are handled carefully.

### Optimization Notes

- The recommended answer is Constant-Space Prefix and Suffix: it meets the `O(n)` time and no-division constraints while reaching `O(1)` extra space by reusing the output array.
- The core technique is storing prefix products in the output array on the first pass, then folding in a single running suffix product on the reverse pass.
- Seed prefix and suffix values to `1` (the multiplicative identity) so boundary positions multiply out correctly; a common pitfall is initializing with the wrong identity.
- The Division Method is disqualified by the explicit no-division rule and introduces fragile zero-handling logic; avoid it unless the constraint is lifted.
