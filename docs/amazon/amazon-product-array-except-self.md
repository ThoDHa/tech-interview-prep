# [Product of Array Except Self](https://www.fastprep.io/problems/amazon-product-array-except-self)

**Medium** | **NN minutes** | **Array, Prefix Sum**

Given an integer array nums, return an array answer where answer[i] equals the product of every element of nums except nums[i].

Solve the problem without division in O(n) time. The output array does not count as extra space.

## Examples

### Example 1

**Input:** `nums = [1,2,3,4]`

**Output:** `[24,12,8,6]`

**Explanation:** For index 0, the product is 2 * 3 * 4 = 24; apply the same rule at every index.

### Example 2

**Input:** `nums = [-1,1,0,-3,3]`

**Output:** `[0,0,9,0,0]`

**Explanation:** Only the position containing zero has a nonzero result, equal to (-1) * 1 * (-3) * 3 = 9.

### Example 3

**Input:** `nums = [2,3]`

**Output:** `[3,2]`

**Explanation:** With two values, each output is the other value.

## Constraints

- `2 <= nums.length <= 10^5.`
- `-30 <= nums[i] <= 30.`
- `Every prefix product and suffix product fits in a signed 32-bit integer.`

## Solutions

### Brute Force

#### Derivation

The statement asks for one product per position, so the literal reading computes each product from scratch: for each index `i`, multiply every element of `nums` except `nums[i]`. Nothing needs to be observed or reformulated, and the no-division rule is trivially respected because no division is even tempting:

1. For each index `i`, start a running `product` at `1`.
2. Walk the whole array with `j`, multiplying in every `nums[j]` where `j != i`.
3. Append the finished `product` to `result` and move to the next index.

Each pass recomputes products the previous pass already knew, which is where the quadratic cost comes from.

#### Walkthrough

Let us watch the Brute Force run on Example 1: `nums = [1,2,3,4]`. The outer loop fixes one index `i`, then the inner loop multiplies in every `nums[j]` where `j != i`, building a fresh `product` from `1`:

| `i` | element skipped | inner-loop products (`product` after each `j != i`) | appended | `result` so far |
| --- | --- | --- | --- | --- |
| `0` | `nums[0] = 1` | `1*2=2`, then `2*3=6`, then `6*4=24` | `24` | `[24]` |
| `1` | `nums[1] = 2` | `1*1=1`, then `1*3=3`, then `3*4=12` | `12` | `[24, 12]` |
| `2` | `nums[2] = 3` | `1*1=1`, then `1*2=2`, then `2*4=8` | `8` | `[24, 12, 8]` |
| `3` | `nums[3] = 4` | `1*1=1`, then `1*2=2`, then `2*3=6` | `6` | `[24, 12, 8, 6]` |

Reading one row to see the mechanism: at `i = 1` the inner loop skips `nums[1] = 2`, so it multiplies `1` by `nums[0]=1`, then `nums[2]=3`, then `nums[3]=4`, giving `1*3*4 = 12`. After all four indices, `result = [24, 12, 8, 6]`, which matches the expected Output for Example 1.

#### Solution

The code is the nested loop pair from the walkthrough: fix `i`, multiply over every `j != i`.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> List[int]:
        count = len(nums)
        result: List[int] = []

        for i in range(count):
            product = 1
            for j in range(count):
                if j != i:
                    product *= nums[j]
            result.append(product)

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

For each of the `n` positions, the inner loop multiplies through all `n` elements.

##### Space Complexity: `O(1)`

Only the running `product` scalar is extra; the output array is not counted as extra space.

#### Key Insights

- The approach mirrors the problem statement literally, which makes it the natural first attempt and a correctness reference for the faster versions.
- The repeated inner pass is the waste: the product of "everything before `i`" and "everything after `i`" is rebuilt from scratch at every position.

### Prefix and Suffix Arrays

#### Derivation

The brute force's inner loop is the flaw: consecutive positions need products that overlap almost entirely, yet each is rebuilt from zero. Split the target product at the excluded index instead. Everything except `nums[i]` is (everything before `i`) times (everything after `i`), and each of those families grows by one factor per step, so both can be tabulated in one linear pass apiece: the multiplicative analogue of a [prefix sum](https://en.wikipedia.org/wiki/Prefix_sum):

1. `prefix[i]` holds the product of all elements before index `i`. Seed `prefix[0] = 1` and roll forward with `prefix[i] = prefix[i - 1] * nums[i - 1]`.
2. `suffix[i]` holds the product of all elements after index `i`. Seed `suffix[count - 1] = 1` and roll backward with `suffix[i] = suffix[i + 1] * nums[i + 1]`.
3. Combine: `result[i] = prefix[i] * suffix[i]`.

Seeding the boundaries with `1`, the multiplicative identity, makes the first and last positions fall out correctly without special cases. The excluded index never appears as a factor on either side, so zeros need no handling at all.

#### Formula

The target is a product that skips one index:

$$ \text{result}[i] = \prod_{\substack{0 \le j < n \\ j \ne i}} \text{nums}[j] $$

```text
result[i] = product of nums[j] over 0 <= j < count with j != i
```

Splitting that product at `i` factors it into a left half and a right half, each a one-step recurrence:

$$ \text{prefix}[i] = \text{prefix}[i-1] \cdot \text{nums}[i-1], \qquad \text{suffix}[i] = \text{suffix}[i+1] \cdot \text{nums}[i+1], \qquad \text{result}[i] = \text{prefix}[i] \cdot \text{suffix}[i] $$

```text
prefix[0] = 1,  suffix[count - 1] = 1       (the empty product)
prefix[i] = prefix[i - 1] * nums[i - 1]     for i >= 1
suffix[i] = suffix[i + 1] * nums[i + 1]     for i <= count - 2
result[i] = prefix[i] * suffix[i]
```

An empty product is `1`, which is why the boundaries are seeded there: `prefix[0]` sees no elements before index `0`, and `suffix[count - 1]` sees none after the last index. Reading the formula back, `result[i]` multiplies every element left of `i` by every element right of `i`, so `nums[i]` itself never enters.

#### Walkthrough

Let us fill the three passes by hand on Example 1: `nums = [1,2,3,4]`, `count = 4`.

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
    def solve(self, nums: List[int]) -> List[int]:
        count = len(nums)

        prefix: List[int] = [1] * count
        for i in range(1, count):
            prefix[i] = prefix[i - 1] * nums[i - 1]

        suffix: List[int] = [1] * count
        for i in range(count - 2, -1, -1):
            suffix[i] = suffix[i + 1] * nums[i + 1]

        result: List[int] = []
        for i in range(count):
            result.append(prefix[i] * suffix[i])

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Three separate linear passes: build the prefix array, build the suffix array, and combine them.

##### Space Complexity: `O(n)`

Two auxiliary arrays of size `n` hold the prefix and suffix products, in addition to the output array.

#### Key Insights

- The decomposition `result[i] = (product of the left) * (product of the right)` is the heart of the problem and avoids division entirely.
- Seeding both boundary products to `1` handles the first and last positions cleanly, with no special cases.
- Zeros need no branch: the excluded index never becomes a factor, so Example 2's `0` entries and its lone `9` fall out of the same three passes.

### Constant-Space Prefix and Suffix

#### Derivation

The two auxiliary arrays are more memory than the idea needs, and the statement's follow-up asks exactly for their removal. Two observations eliminate them. First, the output array has to be filled anyway, so the forward pass can write the [prefix products](https://en.wikipedia.org/wiki/Prefix_sum) straight into `result`. Second, the backward pass only ever reads one suffix value at a time, so a single running scalar `suffix_product` replaces the whole suffix array:

1. Seed `result` with ones, then store the prefix products directly in it: after pass one, `result[i]` is the product of everything before `i`.
2. Sweep right to left with `suffix_product = 1`. At each `i`, multiply `result[i] *= suffix_product` first, then fold the current element in with `suffix_product *= nums[i]`.

The output array doubles as the prefix store, and the suffix side never needs more than the one scalar folded in on the reverse sweep.

#### Walkthrough

Let us run both passes on Example 1: `nums = [1,2,3,4]`. Pass 1 is the prefix fill from the previous walkthrough, now landing in `result` itself:

```text
result = [1, 1, 1, 1]                        seeded with 1s
i = 1   result[1] = result[0]*nums[0] = 1    result = [1, 1, 1, 1]
i = 2   result[2] = result[1]*nums[1] = 2    result = [1, 1, 2, 1]
i = 3   result[3] = result[2]*nums[2] = 6    result = [1, 1, 2, 6]
```

Pass 2 sweeps right to left. Entering each `i`, `suffix_product` holds the product of everything after `i`; multiply it in first, then fold `nums[i]` into it:

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
    def solve(self, nums: List[int]) -> List[int]:
        count = len(nums)
        result: List[int] = [1] * count

        for i in range(1, count):
            result[i] = result[i - 1] * nums[i - 1]

        suffix_product = 1
        for i in range(count - 1, -1, -1):
            result[i] *= suffix_product
            suffix_product *= nums[i]

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Two linear passes through the array.

##### Space Complexity: `O(1)`

Only the scalar `suffix_product` is extra; the output array does not count as extra space, as the statement itself allows.

#### Key Insights

- Reusing the output array to hold prefix products is the trick that collapses `O(n)` auxiliary space to `O(1)`.
- A suffix only ever needs to be remembered as one accumulating scalar, never as a full array.
- This meets every stated requirement: `O(n)` time, no division, and `O(1)` extra space.

### Division Method

#### Derivation

There is a tempting shortcut the constraints exist to block: the product of everything except `nums[i]` is the total product divided by `nums[i]`. If division were allowed, one pass would compute the total and a second would divide it out per position. The complication is zeros, which make division undefined, so they force a case split:

1. Compute the product of all non-zero elements into `total_product` while counting zeros in `zero_count` and remembering `zero_index`.
2. **Two or more zeros**: every position's product includes a zero, so return all zeros.
3. **Exactly one zero**: only the zero position has a non-zero result, equal to the product of the others; every other position is `0`.
4. **No zeros**: each position receives `total_product // num`.

The statement bans division outright, so this approach is included for contrast rather than as a submission.

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

This matches the expected Output for Example 2. Had a second zero appeared, the counting pass would have returned all zeros immediately; with no zeros at all, each position would receive `total_product // num` instead.

#### Solution

The code is the count-then-dispatch structure from the walkthrough, one branch per zero count.

```python
from typing import List


class Solution:
    def solve(self, nums: List[int]) -> List[int]:
        count = len(nums)

        total_product = 1
        zero_count = 0
        zero_index = -1

        for i, num in enumerate(nums):
            if num == 0:
                zero_count += 1
                zero_index = i
                if zero_count > 1:
                    return [0] * count
            else:
                total_product *= num

        result: List[int] = []
        if zero_count == 1:
            for i in range(count):
                result.append(total_product if i == zero_index else 0)
        else:
            for num in nums:
                result.append(total_product // num)

        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass to accumulate the product and count zeros, then one pass to build the result.

##### Space Complexity: `O(1)`

Only a few scalars for the product, the zero count, and the zero index; the output array is not counted.

#### Key Insights

- Division reduces the problem to one total product, but the zero corner cases are fragile and easy to get wrong.
- The problem forbids division precisely to push toward the prefix and suffix technique, which generalizes to non-invertible operations where division has no analogue.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - for each of the `n` positions, a fresh inner pass multiplies through all `n` elements.
- **Prefix and Suffix Arrays**: `O(n)` - three linear passes to build prefix, build suffix, and combine.
- **Constant-Space Prefix and Suffix**: `O(n)` - two linear passes through the array.
- **Division Method**: `O(n)` - one pass for the total product and zero count, one pass to build the result.

### Space Complexity

- **Brute Force**: `O(1)` - a single running-product variable, not counting the output array.
- **Prefix and Suffix Arrays**: `O(n)` - two auxiliary arrays of size `n` for the prefix and suffix products.
- **Constant-Space Prefix and Suffix**: `O(1)` - only the `suffix_product` scalar; the output array does not count.
- **Division Method**: `O(1)` - a few scalars for the product, zero count, and zero index.

### Trade-offs

- **Brute Force**: simplest to write and obviously correct, but quadratic time makes it impractical for large arrays.
- **Prefix and Suffix Arrays**: clear and easy to reason about, at the cost of `O(n)` auxiliary space.
- **Constant-Space Prefix and Suffix**: optimal space while staying linear, at the cost of the less obvious reuse of the output array and the ordered multiply-then-fold step.
- **Division Method**: intuitive when division is allowed, but it breaks the problem constraint and needs careful zero handling.

### When to Use Each

- **Constant-Space Prefix and Suffix (Recommended)**: the interview answer: it satisfies every stated constraint, `O(n)` time, no division, and `O(1)` extra space.
- **Prefix and Suffix Arrays**: a good stepping stone when the constant-space version feels opaque; the two-array form makes the decomposition visible first.
- **Brute Force**: only for tiny arrays or as a reference implementation to test the faster versions against.
- **Division Method**: only if the no-division constraint is explicitly lifted, and zeros are still handled by the case split.

### Optimization Notes

- The recommended answer is Constant-Space Prefix and Suffix: prefix products land in the output array on the first pass, then a single running suffix scalar folds in on the reverse sweep.
- The multiply-then-fold order inside the reverse pass is load-bearing: scaling `result[i]` by the suffix before `nums[i]` joins it is what keeps the excluded element out of its own answer.
- Seed boundary products to `1`, the multiplicative identity, so the first and last positions multiply out correctly; a common pitfall is initializing with the wrong identity.
- The Division Method is disqualified by the explicit no-division rule and introduces fragile zero-handling logic; avoid it unless the constraint is lifted.
