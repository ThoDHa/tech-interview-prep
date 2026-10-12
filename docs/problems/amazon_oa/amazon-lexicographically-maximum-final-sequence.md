# [Lexicographically Maximum Final Sequence](https://www.fastprep.io/problems/amazon-lexicographically-maximum-final-sequence)

**unknown difficulty** | **NN minutes** | **unknown categories**

You are given a binary string shipmentData consisting only of '0' and '1'.

A final string is built from a chosen ordering of shipmentData as follows:

Start with an empty string finalSequence.For each character c in the chosen ordering from left to right, append c to finalSequence, then reverse finalSequence.You may rearrange the characters of shipmentData arbitrarily before applying the operation. Return the rearranged shipmentData string that should be fed into the operation to produce the lexicographically maximum possible finalSequence.

Do not return finalSequence itself. The answer must be a rearrangement of the original shipmentData.

## Examples

### Example 1

**Input:** `shipmentData = "0011"`

**Output:** `"0101"`

**Explanation:** The returned rearranged string is "0101". If this string is fed into the operation, the resulting final sequence is "1100", which is lexicographically maximum among all rearrangements.

### Example 2

**Input:** `shipmentData = "10100"`

**Output:** `"00101"`

**Explanation:** The final sequence reads positions 5,3,1,2,4 from the rearranged string. Placing the two '1' characters at positions 5 and 3 produces final sequence "11000".

## Constraints

- `shipmentData.length >= 1`
- `shipmentData contains only '0' and '1'.`

## Solutions

### Brute Force over Rearrangements

#### Derivation

The problem hands over a tiny alphabet and a mechanical operation, so the literal answer is enumeration: build every distinct rearrangement of `shipment_data`, run the append-then-reverse operation on each, and keep the rearrangement whose final string is largest. [Brute force](https://en.wikipedia.org/wiki/Brute-force_search) is correct because the rearrangement set is finite, and it doubles as the oracle the fast solution is checked against:

1. Generate every distinct permutation of the characters of `shipment_data`.
2. For each candidate, simulate the operation: append the character, then
   reverse the growing list.
3. Track the candidate whose simulated final string is lexicographically
   largest.
4. Return that candidate.

#### Walkthrough

Example 1, `shipment_data = "0011"`, has six distinct rearrangements. Each line pairs a rearrangement with the final string its operation produces:

```text
0011 -> 1001      0101 -> 1100      0110 -> 0101
1001 -> 1010      1010 -> 0011      1100 -> 0110
```

The largest final string is `1100`, produced by the rearrangement `0101`, which is the expected Output.

#### Solution

The code is the enumeration and the append-reverse simulation:

```python
from itertools import permutations
from typing import List


class Solution:
    def solve(self, shipment_data: str) -> str:
        def simulate(ordering: List[str]) -> str:
            final: List[str] = []
            for character in ordering:
                final.append(character)
                final.reverse()
            return "".join(final)

        best_arrangement = shipment_data
        best_final = simulate(list(shipment_data))
        for candidate in set(permutations(shipment_data)):
            arrangement = "".join(candidate)
            candidate_final = simulate(candidate)
            if candidate_final > best_final:
                best_final = candidate_final
                best_arrangement = arrangement
        return best_arrangement
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(L! x L)`

Where `L` is the string length: up to `L!` distinct rearrangements, each simulated in `O(L)` list reversals.

##### Space Complexity: `O(L)`

The growing `final` list; the permutation iterator does not materialize all candidates.

#### Key Insights

- Simulating the operation is cheap (`O(L)` reversals per candidate); the factorial candidate count is what makes the approach unusable beyond toy lengths.
- Comparing final strings, not arrangements, is the easy trap: the answer must be a rearrangement of the input, so the winner is recorded by its arrangement.
- The simulation exposes the structure the fast solution needs: every input character ends up in the final string exactly once, only the reading order varies.

### Reading-Order Slot Placement

#### Derivation

The simulation never reorders anything except by reversal, so each output position reads exactly one input position, and the mapping from output position to input position is fixed by the length alone: the character appended at operation step `step` is the input character at index `step`, and after all `L` reversals it lands at one fixed output position. Tracing where each appended character lands gives the reading order `reading_order[t]`, the input position whose character becomes `final[t]`. For any length the order reads the same: odd indices from the far end inward, then even indices from the innermost outward.

That mapping turns selection into placement. The lexicographically largest final string over all rearrangements is the ceiling `"1" x ones + "0" x rest` with `ones = shipment_data.count('1')`: any final string that puts a `'0'` in a slot where a `'1'` could sit is beaten at that slot, and the ceiling is achievable by placing each `'1'` into one of the first `ones` reading slots. The arrangement returned is the one whose `'1'` positions are exactly those first `ones` reading slots:

1. Count `ones = shipment_data.count('1')` and set
   `reading_order = list(range(length - 1, -1, -2))` extended with
   `list(range(length % 2, length, 2))`.
2. Fill `arrangement` with `'0'`.
3. Set `arrangement[position] = '1'` for the first `ones` entries of
   `reading_order`.
4. Return the joined `arrangement`.

#### Walkthrough

Example 1, `shipment_data = "0011"`: `length = 4` gives the reading order `[3, 1, 0, 2]` (odd indices `3, 1` from the far end, then even indices `0, 2` outward). With `ones = 2`, the first two reading slots win the `'1'`s:

```text
reading_order   [3, 1, 0, 2]
first 2 slots   positions 3 and 1 -> arrangement "0101"
slot values     final[0] = arrangement[3] = '1'
                final[1] = arrangement[1] = '1'
                final[2] = arrangement[0] = '0'
                final[3] = arrangement[2] = '0'
final string    "1100"   (the ceiling "1" x 2 + "0" x 2)
```

The placed arrangement `0101` is the expected Output, and its operation produces `1100`, the lexicographic ceiling, exactly as the brute-force table in the first walkthrough confirms.

#### Solution

The code is the count, the reading order, and the placement:

```python
from typing import List


class Solution:
    def solve(self, shipment_data: str) -> str:
        length = len(shipment_data)
        ones = shipment_data.count('1')

        reading_order = list(range(length - 1, -1, -2))
        reading_order.extend(range(length % 2, length, 2))

        arrangement = ['0'] * length
        for position in reading_order[:ones]:
            arrangement[position] = '1'
        return "".join(arrangement)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(L)`

One pass counts the `'1'`s, the reading order is built in one pass, and the placement writes each `'1'` once.

##### Space Complexity: `O(L)`

The `reading_order` list and the `arrangement` character list.

#### Key Insights

- The append-reverse operation is a fixed permutation of input positions for a given length: deriving the reading order once replaces simulating every candidate.
- The lexicographic ceiling `"1" x ones + "0" x rest` is a valid final string, which makes it optimal outright: no final string can beat it at any slot.
- `length % 2` is the innermost even index: for odd lengths the odd chain ends at index `0` and the even chain starts at `1`; for even lengths the odd chain ends at `1` and the even chain starts at `0`. One expression covers both parities.
- A rearrangement of the input is returned, never the final string; the check the problem warns about is exactly the bug of returning the ceiling itself.

## Comparison of Solutions

### Time Complexity

- **Brute Force over Rearrangements**: `O(L! x L)` - factorial candidates, linear simulation each.
- **Reading-Order Slot Placement**: `O(L)` - one count pass, one order build, one placement pass.

### Space Complexity

- **Brute Force over Rearrangements**: `O(L)` - the simulation list per candidate.
- **Reading-Order Slot Placement**: `O(L)` - the reading order and the arrangement.

### Trade-offs

- **Brute Force over Rearrangements**: impossible to misimplement and self-evidently correct, but factorial time confines it to strings of length ten or so.
- **Reading-Order Slot Placement**: linear time on any length, at the cost of trusting a derived reading order that should be verified against the operation on a small example before use.

### When to Use Each

- **Brute Force over Rearrangements**: validating the placement formula on short strings, or when the operation's mechanics are still unclear.
- **Reading-Order Slot Placement (Recommended)**: the interview answer: the ceiling argument plus the reading order solves any length in one pass.

### Optimization Notes

- The placement formula never simulates the operation; its correctness rests on the ceiling being achievable, which the reading order guarantees by construction.
- The reading order depends only on the length, so an implementation that handles many queries could precompute it once per length.
- A frequent wrong answer is returning the ceiling `"1" x ones + "0" x rest` itself; it is the final string, not a rearrangement of the input, and the problem explicitly rejects it.
