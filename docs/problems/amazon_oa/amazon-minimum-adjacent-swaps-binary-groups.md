# [Minimum Adjacent Swaps to Group Binary Values](https://www.fastprep.io/problems/amazon-minimum-adjacent-swaps-binary-groups)

**Medium** | **NN minutes** | **Array, Greedy**

You are given a binary array bits. Using adjacent swaps, rearrange it so that equal values form two contiguous groups.

Either order is valid: all 0s before all 1s, or all 1s before all 0s. Return the minimum number of adjacent swaps over both orders.

## Examples

### Example 1

**Input:** `bits = [0,1,0,1]`

**Output:** `1`

**Explanation:** Swap the middle 1 and 0 to obtain [0,0,1,1].

### Example 2

**Input:** `bits = [1,1,0,0]`

**Output:** `0`

**Explanation:** The array already has all ones before all zeroes.

## Constraints

- `1 <= bits.length <= 100000`
- `Every value in bits is either 0 or 1.`

## Solutions

### Inversion Pair Enumeration

#### Derivation

The most literal reading counts crossings straight from their definition. Fix one target order: all 0s before all 1s. Take any pair of positions `left < right` where `bits[left] == 1` and `bits[right] == 0`. Those two values sit in the wrong relative order for the target, and the relative order of two values changes only when they are swapped with each other, so every such pair demands at least one adjacent swap. Conversely, each adjacent swap of neighboring 1 and 0 settles exactly one crossed pair, which is what a bubble-style regrouping achieves, so the minimum swap count for the target equals the number of crossed pairs. The other order, all 1s first, counts the mirrored pairs. Enumerating every pair yields both totals:

1. For every pair of positions `left < right`, add one to
   `swaps_zeros_first` when `bits[left] == 1` and `bits[right] == 0`.
2. Add one to `swaps_ones_first` when `bits[left] == 0` and
   `bits[right] == 1`.
3. Return `min(swaps_zeros_first, swaps_ones_first)`, since either order is
   accepted.

#### Walkthrough

Example 1, `bits = [0,1,0,1]`, has four positions and six pairs:

```text
pair (0,1)   0,1   crossed for ones-first
pair (0,2)   0,0   equal values, never crossed
pair (0,3)   0,1   crossed for ones-first
pair (1,2)   1,0   crossed for zeros-first
pair (1,3)   1,1   equal values, never crossed
pair (2,3)   0,1   crossed for ones-first
```

The zeros-first target counts one crossed pair, the ones-first target counts three, and the function returns `min(1, 3) = 1`. That single crossing is the swap the explanation performs: swapping the middle 1 and 0 yields [0,0,1,1], matching the expected Output.

#### Solution

```python
from typing import List


class Solution:
    def minimumAdjacentSwaps(self, bits: List[int]) -> int:
        length = len(bits)
        swaps_zeros_first = 0
        swaps_ones_first = 0

        for left in range(length):
            for right in range(left + 1, length):
                if bits[left] == 1 and bits[right] == 0:
                    swaps_zeros_first += 1
                elif bits[left] == 0 and bits[right] == 1:
                    swaps_ones_first += 1

        return min(swaps_zeros_first, swaps_ones_first)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Every one of the `n × (n - 1) / 2` position pairs is inspected once, for `n` the length of `bits`.

##### Space Complexity: `O(1)`

Two running totals, independent of the input size.

#### Key Insights

- Reframing "which swaps?" into "which pairs must cross?" turns a search for a move sequence into a count.
- The relative order of two values changes only when they swap with each other, so the crossed-pair count is simultaneously a lower bound and achievable by bubbling the groups into place.
- Both orders must be scored because neither dominates: Example 1 is cheaper zeros-first, while Example 2 is already grouped ones-first.

### Single-Pass Prefix Count

#### Derivation

The double loop re-answers one question for every element: how many 1s appear before this 0 (or how many 0s appear before this 1, for the mirrored order)? A left-to-right scan carries that answer for free in a running tally, because the count for the current element depends only on what came before. For the zeros-first target, maintain `ones_before`, the number of 1s seen so far: when the scan reads a 0, that 0 crosses every 1 already seen, so add `ones_before` to `swaps_zeros_first`; when it reads a 1, increment `ones_before`. The mirrored counters `zeros_before` and `swaps_ones_first` advance in the same pass:

1. Initialize `swaps_zeros_first`, `swaps_ones_first`, `ones_before`, and
   `zeros_before` to 0.
2. Scan `bits` once. On a 0: increment `zeros_before` and add `ones_before` to
   `swaps_zeros_first`. On a 1: increment `ones_before` and add `zeros_before`
   to `swaps_ones_first`.
3. Return `min(swaps_zeros_first, swaps_ones_first)`.

#### Walkthrough

The same Example 1, `bits = [0,1,0,1]`, one row per scanned element:

```text
position   bit   ones_before   zeros_first_swaps   zeros_before   ones_first_swaps
0          0     0             +0 = 0              0 -> 1         0
1          1     0 -> 1        0                   1              +1 = 1
2          0     1             +1 = 1              1 -> 2         1
3          1     1 -> 2        1                   2              +2 = 3
```

The totals finish at `swaps_zeros_first = 1` and `swaps_ones_first = 3`, so the function returns `1`, matching the expected Output. The same scan on Example 2, `bits = [1,1,0,0]`, totals `4` and `0` and returns `0`, matching its expected Output.

#### Solution

The code is the walkthrough's two tallies and two totals written down.

```python
from typing import List


class Solution:
    def minimumAdjacentSwaps(self, bits: List[int]) -> int:
        swaps_zeros_first = 0
        swaps_ones_first = 0
        ones_before = 0
        zeros_before = 0

        for bit in bits:
            if bit == 0:
                zeros_before += 1
                swaps_zeros_first += ones_before
            else:
                ones_before += 1
                swaps_ones_first += zeros_before

        return min(swaps_zeros_first, swaps_ones_first)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass over `bits` with constant work per element.

##### Space Complexity: `O(1)`

Four integer counters regardless of input length.

#### Key Insights

- Each element's crossed-pair count reduces to "how many of the other value appeared before me", which a running prefix tally answers in constant time.
- Scoring both orders in one pass halves the work; a second scan for the mirrored order would still be linear.
- An array with a single distinct value returns 0 because no pair ever crosses.

## Comparison of Solutions

### Time Complexity

- **Inversion Pair Enumeration**: `O(n^2)` - every position pair is checked once.
- **Single-Pass Prefix Count**: `O(n)` - one scan with constant work per element.

### Space Complexity

- **Inversion Pair Enumeration**: `O(1)` - two running totals.
- **Single-Pass Prefix Count**: `O(1)` - four integer counters.

### Trade-offs

- **Inversion Pair Enumeration**: trivially faithful to the definition of crossing pairs, which makes it a good correctness reference, but the quadratic pair loop cannot process the constraint limit of `10^5` elements.
- **Single-Pass Prefix Count**: the same answer in linear time, at the cost of trusting the prefix-tally identity rather than checking pairs directly.

### When to Use Each

- **Inversion Pair Enumeration**: as a brute-force oracle when testing, or on tiny inputs where the quadratic loop is irrelevant.
- **Single-Pass Prefix Count (Recommended)**: the interview answer, and the only variant that fits the stated constraints.

### Optimization Notes

- The single pass already computes both orders; splitting it into two scans stays linear but doubles the constant.
- The crossed-pair identity generalizes: minimum adjacent swaps to force any two-valued grouping equals the inversions against that grouping, so the same tally works when the required order is fixed by the caller rather than chosen by a `min`.
