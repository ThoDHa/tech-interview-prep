# [Multiply Strings](https://leetcode.com/problems/multiply-strings/)

**Medium** | **25 minutes** | **Math, String, Simulation**

**Pattern:** [Simulation](../patterns/simulation/intuition.md)

**Algorithm:** [Multiplication algorithm](https://en.wikipedia.org/wiki/Multiplication_algorithm) · [Positional notation](https://en.wikipedia.org/wiki/Positional_notation) · [Carry (arithmetic)](https://en.wikipedia.org/wiki/Carry_(arithmetic))

**Practice:** [`practice/multiply_strings/solution.py`](../../practice/multiply_strings/solution.py)

You are given two strings `num1` and `num2` that represent non-negative integers.

Return the product of `num1` and `num2` in the form of a string.

Assume that neither `num1` nor `num2` contain any leading zero, unless they are the number `0` itself.

**Note**: You can not use any built-in library to convert the inputs directly into integers.

## Examples

### Example 1

**Input:** `num1 = "3", num2 = "4"`

**Output:** `"12"`

### Example 2

**Input:** `num1 = "111", num2 = "222"`

**Output:** `"24642"`

## Constraints

- `1 <= num1.length, num2.length <= 200`
- `num1` and `num2` consist of digits only.

## Deriving the Solution

The product of an `m`-digit and an `n`-digit number has at most `m + n` digits, and schoolbook multiplication's grid makes that precise: multiplying digit `i` of `num1` by digit `j` of `num2` contributes to positions `i + j` and `i + j + 1` of the result. Every approach is a scheme for computing those `m * n` pairwise products and resolving the carries, differing in when the carries are settled.

1. **Start literal.** Multiply the whole first number by each single digit of
   the second, shift, and add the partial products with a hand-rolled big-add:
   see [Schoolbook Partial Products](#schoolbook-partial-products).
2. **Settle carries at the end.** Skip building intermediate numbers: drop
   each digit pair's product straight into its `i + j + 1` bucket and resolve
   every column's carry in one final sweep: see
   [Position Accumulator](#position-accumulator).
3. **Tidy with the library.** The same accumulate-then-normalize shape is one
   loop with `divmod` per bucket once the index arithmetic is understood: see
   [Accumulator with divmod Normalization](#accumulator-with-divmod-normalization).

## Solutions

### Schoolbook Partial Products

#### Derivation

The way multiplication is taught on paper: `num1` times the ones digit of `num2`, written shifted one left below `num1` times the tens digit, and so on, then everything summed. The note barring `int(num1)` conversion leaves all of that to be built by hand, so the approach needs one helper, a string big-add, plus per-digit multiplies with carries:

1. Write `add(a, b)`: add two digit strings right to left with a carry,
   returning the sum string.
2. Write `mul_digit(num, d)`: multiply a digit string by a one-digit number,
   carrying left to right, producing the partial product string.
3. For `j` from the last index of `num2` down to `0`: compute
   `mul_digit(num1, num2[j])` and append `num2`-position zeros so the partial
   product sits at the right shift.
4. Accumulate the partials with `add`; strip a leading zero if the result is
   longer than one digit.

The mechanism is honest but the bookkeeping dominates: each partial is a fresh string, and each `add` re-walks the whole result.

#### Walkthrough

Multiply Example 2: `num1 = "111"`, `num2 = "222"`. Three partial products, each shifted one position further, then two big-adds:

```text
partial 0   111 * 2 (ones)  = 222      shift 0 -> "222"
partial 1   111 * 2 (tens)  = 222      shift 1 -> "2220"
partial 2   111 * 2 (hundreds) = 222   shift 2 -> "22200"
add 0+1     222 + 2220  = 2442
add +2      2442 + 22200 = 24642
```

The running sum lands on `"24642"`, matching the expected Output for Example 2. Each partial is the full product of `num1` with one digit of `num2`, and the shifts place them exactly where the schoolbook grid says.

#### Solution

The code is the two helpers and the shifted accumulation loop.

```python
class Solution:
    def add(self, a: str, b: str) -> str:
        i, j = len(a) - 1, len(b) - 1
        carry = 0
        out = []
        while i >= 0 or j >= 0 or carry:
            total = carry
            if i >= 0:
                total += ord(a[i]) - ord("0")
                i -= 1
            if j >= 0:
                total += ord(b[j]) - ord("0")
                j -= 1
            carry, digit = divmod(total, 10)
            out.append(digit)
        return "".join(chr(d + ord("0")) for d in reversed(out))

    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"
        result = "0"
        for j in range(len(num2) - 1, -1, -1):
            d = ord(num2[j]) - ord("0")
            carry = 0
            partial = []
            for i in range(len(num1) - 1, -1, -1):
                product = (ord(num1[i]) - ord("0")) * d + carry
                carry, digit = divmod(product, 10)
                partial.append(digit)
            if carry:
                partial.append(carry)
            shifted = "".join(chr(p + ord("0")) for p in reversed(partial)) + "0" * (len(num2) - 1 - j)
            result = self.add(result, shifted)
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

Each of the `n` digits of `num2` drives an `O(m)` partial-product pass, and each `add` is `O(m + n)`, giving `O(n * (m + m + n))`, quadratic overall.

##### Space Complexity: `O(m + n)`

The running sum and each partial product are at most `m + n` digits long.

#### Key Insights

- Multiplication decomposes into operations on one digit at a time; the difficulty is entirely in bookkeeping the shifts and carries by hand.
- `ord(ch) - ord("0")` is the digit read and `chr(d + ord("0"))` the digit write, the conversion primitives that stand in for the barred `int()` calls.
- The strings-as-vectors style does reallocation per partial product, which is the waste the next approach removes by writing straight into one array.

### Position Accumulator

#### Derivation

The grid observation turns the whole computation into `m * n` writes into a fixed array: the product of `num1[i]` and `num2[j]` lands in result positions `i + j` (tens) and `i + j + 1` (units). If every pairwise product is added into its bucket first and carries are resolved in one right-to-left sweep afterwards, no intermediate strings exist at all:

1. Handle the zero shortcut: either input `"0"` returns `"0"`.
2. Allocate `pos`, an `m + n` array of buckets, all zero.
3. For `i` from `m - 1` down to `0`, for `j` from `n - 1` down to `0`:
   add `d1 * d2` into `pos[i + j + 1]`, and add that bucket's overflow into
   `pos[i + j]` immediately.
4. Sweep `pos` right to left normalizing each bucket with `divmod` (buckets
   can hold values above `9` mid-pass), then skip leading zeros and join.

#### Walkthrough

Accumulate Example 2: `num1 = "111"`, `num2 = "222"`, so `m = n = 3`, `pos` has six buckets indexed `0..5`, and every pair contributes `d1 * d2 = 1 * 2 = 2` into bucket `i + j + 1`. Since `i + j + 1` ranges over `1..5`, bucket `0` stays empty (pure carry space):

```text
bucket 5 gets (2,2):               2     -> units:        2
bucket 4 gets (2,1),(1,2):       2+2 = 4  -> tens:         4
bucket 3 gets (2,0),(1,1),(0,2): 2+2+2=6  -> hundreds:     6
bucket 2 gets (1,0),(0,1):       2+2 = 4  -> thousands:    4
bucket 1 gets (0,0):               2     -> ten-thousands:2
bucket 0 gets nothing:             0     -> carry space

pos after the 9 adds = [0, 2, 4, 6, 4, 2]
carry sweep: every bucket < 10, nothing to propagate
join from the first nonzero bucket (index 1): "24642"
```

The tally cross-checks against positional arithmetic: `111 * 222 = 24642` has digits `2,4,6,4,2` in the ten-thousands through units positions, exactly the buckets `1..5` in order. Joining from bucket `1` reads `"24642"`, matching the expected Output for Example 2.

#### Solution

The code is the double loop writing `i + j + 1` and `i + j`, then the carry sweep and the leading-zero skip.

```python
class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"
        m, n = len(num1), len(num2)
        pos = [0] * (m + n)
        for i in range(m - 1, -1, -1):
            d1 = ord(num1[i]) - ord("0")
            for j in range(n - 1, -1, -1):
                d2 = ord(num2[j]) - ord("0")
                total = pos[i + j + 1] + d1 * d2
                pos[i + j + 1] = total % 10
                pos[i + j] += total // 10
        start = 0
        while start < len(pos) - 1 and pos[start] == 0:
            start += 1
        return "".join(chr(p + ord("0")) for p in pos[start:])
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

The double loop performs `m * n` constant-time bucket updates, and the final sweep is `O(m + n)`.

##### Space Complexity: `O(m + n)`

One bucket array, exactly the size of the largest possible product.

#### Key Insights

- The index law, digit `i` times digit `j` shifts by `i + j`, is the entire algorithm: positions `i + j` and `i + j + 1` hold the two digits of each pairwise product.
- Settling carries as you go (`total % 10` down, `total // 10` left) keeps every bucket a single digit without a separate normalization pass.
- Bucket `0` of the `m + n` array is pure carry space: the units product `i + j + 1` can never land there, which is why the result is at most `m + n` digits.

### Accumulator with divmod Normalization

#### Derivation

The Position Accumulator interleaves two jobs, accumulating products and keeping buckets single-digit, which the inner loop does with a two-line modulo-plus-floor-division dance. Letting the buckets grow freely during the double loop and normalizing once at the end with `divmod` reads cleaner and moves the branchless adds into the tight loop:

1. Allocate `acc` with `m + n` buckets, all zero.
2. For each pair `(i, j)`: `acc[i + j + 1] += d1 * d2` and nothing else;
   buckets may hold values far above `9` mid-loop.
3. Normalize right to left: `acc[k], carry = divmod(acc[k], 10)`, then
   `acc[k - 1] += carry`, propagating the final carry by shifting.
4. Skip leading zeros and join as before.

#### Walkthrough

Run accumulate-then-normalize on Example 2: `num1 = "111"`, `num2 = "222"`. The nine adds drop `2` (each pair contributes `d1 * d2 = 1 * 2`) into the same buckets the Position Accumulator walkthrough tallied, so `acc` starts as the doubled counts and one sweep finishes:

```text
after the 9 adds   acc = [0, 2, 4, 6, 4, 2]
k = 5              divmod(2 + 0, 10)  -> carry 0, keep 2
k = 4              divmod(4 + 0, 10)  -> carry 0, keep 4
k = 3              divmod(6 + 0, 10)  -> carry 0, keep 6
k = 2              divmod(4 + 0, 10)  -> carry 0, keep 4
k = 1              divmod(2 + 0, 10)  -> carry 0, keep 2
k = 0              divmod(0 + 0, 10)  -> carry 0, keep 0
join from index 1: "24642"
```

No bucket exceeded `9`, so the sweep is a pass-through and the string `"24642"` matches the expected Output for Example 2. A bigger case, `"999" * "999" = 998001`, is where the deferred carries earn their keep: buckets reach `243` before the sweep.

#### Solution

The code is the free-accumulating double loop, one `divmod` sweep, and the shared leading-zero join.

```python
class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"
        m, n = len(num1), len(num2)
        acc = [0] * (m + n)
        for i in range(m - 1, -1, -1):
            d1 = ord(num1[i]) - ord("0")
            for j in range(n - 1, -1, -1):
                acc[i + j + 1] += d1 * (ord(num2[j]) - ord("0"))
        carry = 0
        for k in range(m + n - 1, -1, -1):
            carry, acc[k] = divmod(acc[k] + carry, 10)
        start = 0
        while start < len(acc) - 1 and acc[start] == 0:
            start += 1
        return "".join(chr(p + ord("0")) for p in acc[start:])
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m * n)`

The accumulation loop is `m * n` additions and the normalization sweep is `O(m + n)` `divmod`s, quadratic overall.

##### Space Complexity: `O(m + n)`

The bucket array; buckets temporarily hold values up to `81` plus carries, which changes no asymptotics.

#### Key Insights

- Deferring all carry work to one sweep is the classic trade of batch normalization over incremental maintenance: fewer moving parts per iteration, one clean pass at the end.
- The final carry can only be a single digit here (the product of an `m`-digit and `n`-digit number fits in `m + n` digits), which is why the fixed-size array never overflows.
- `divmod(total, 10)` names both halves of the carry split in one call, replacing the `%`/`//` pair of the incremental version.

## Comparison of Solutions

The practice harness's `practice/multiply_strings/reference.py` implements the **Position Accumulator** solution.

### Time Complexity

- **Schoolbook Partial Products**: `O(m * n)` - `n` partial products of length `m` plus `n` big-adds.
- **Position Accumulator**: `O(m * n)` - one constant-time bucket update per digit pair.
- **Accumulator with divmod Normalization**: `O(m * n)` - the same pair loop plus one linear sweep.

### Space Complexity

- **Schoolbook Partial Products**: `O(m + n)` - running sum plus one partial product at a time.
- **Position Accumulator**: `O(m + n)` - the bucket array, single digits throughout.
- **Accumulator with divmod Normalization**: `O(m + n)` - the bucket array, briefly holding two-digit buckets.

### Trade-offs

- **Schoolbook Partial Products**: Closest to the pencil-and-paper mental model, but string churn and repeated adds make it the longest and slowest in practice.
- **Position Accumulator**: One array, no intermediate representations, carries folded into the inner loop at the cost of a two-line bucket update.
- **Accumulator with divmod Normalization**: The tidiest inner loop, paying with temporarily multi-digit buckets and a second pass.

### When to Use Each

- **Schoolbook Partial Products**: When explaining multiplication from first principles, or when the big-add helper is separately required.
- **Position Accumulator** (recommended): The default; the grid index law is the only idea needed and no bucket ever holds a non-digit.
- **Accumulator with divmod Normalization**: When the `%`/`//` split in the hot loop reads noisier than a deferred `divmod` sweep.

### Optimization Notes

- For inputs at the constraint cap (`200` digits each), all three quadratic versions do at most `40000` bucket updates, far below any limit; Karatsuba's `O(n^1.58)` recursion only pays off far beyond this size.
- Precomputing `ord("0")` saves two constant lookups per pair, a measurable constant-factor win in Python's interpreted inner loop but invisible in complexity terms.
- Building the output with `"".join` over a generator of `chr` calls beats string concatenation, which would be quadratic in the output length.

