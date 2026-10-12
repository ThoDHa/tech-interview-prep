# [Bit at an Index After Repeated Binary Expansion](https://www.fastprep.io/problems/amazon-indexed-bit-after-binary-expansion)

**Medium** | **NN minutes** | **String, Math**

Start with a binary string bits. In one expansion round, replace every character independently:

0 becomes 00.1 becomes 10.After exactly rounds expansions, return the bit at the zero-based position index. The position is guaranteed to exist in the expanded string.

## Examples

### Example 1

**Input:** `bits = "01"`, `rounds = 1`, `index = 2`

**Output:** `1`

**Explanation:** One expansion produces 0010, whose zero-based index 2 contains 1.

### Example 2

**Input:** `bits = "1"`, `rounds = 2`, `index = 3`

**Output:** `0`

**Explanation:** The two expansions are 1 -> 10 -> 1000, and its last bit is 0.

### Example 3

**Input:** `bits = "101"`, `rounds = 0`, `index = 2`

**Output:** `1`

**Explanation:** With zero rounds, query the original string directly.

## Constraints

- `1 <= bits.length <= 10^5`
- `bits contains only 0 and 1.`
- `0 <= rounds <= 30`
- `0 <= index <= 10^9`
- `index < bits.length * 2^rounds.`

## Solutions

### Round-by-Round Simulation

#### Derivation

The most literal reading of the problem is to do exactly what the statement says: apply every expansion round to the whole string, then read off the requested position. Each character maps to its own two-bit block, `'0'` to `"00"` and `'1'` to `"10"`, and one round replaces the string with the concatenation of those blocks. The string doubles in length every round, so this is only viable while `rounds` stays tiny:

1. Hold the current string in `expanded`, starting from `bits`.
2. Repeat `rounds` times: rebuild `expanded` by replacing every `character`
   with `"00"` when it is `'0'` and `"10"` when it is `'1'`.
3. Return `int(expanded[index])`.

#### Walkthrough

Example 1, `bits = "01"`, `rounds = 1`, `index = 2`:

```text
round 0   expanded = "01"
round 1   '0' becomes "00", '1' becomes "10"   expanded = "0010"
read      expanded[2] = '1' -> 1
```

The read returns `1`, matching the expected Output. Example 2, `bits = "1"`, `rounds = 2`, `index = 3`, runs `"1"` to `"10"` to `"1000"` and reads `expanded[3] = '0'`, again matching.

#### Solution

```python
class Solution:
    def solve(self, bits: str, rounds: int, index: int) -> int:
        """Return the bit at position index after rounds expansions.

        Time:  O(bits.length * 2^rounds): every round rebuilds a string
            twice as long as the previous one.
        Space: O(bits.length * 2^rounds): the expanded string dominates.
        """
        expanded = bits
        for _ in range(rounds):
            expanded = "".join(
                "00" if character == "0" else "10" for character in expanded
            )
        return int(expanded[index])
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(bits.length × 2^rounds)`

The final round alone rebuilds a string of `bits.length × 2^rounds` characters, up to roughly `10^14` under the stated constraints.

##### Space Complexity: `O(bits.length × 2^rounds)`

The expanded string dominates; the builder expression holds the old and new copies side by side at peak.

#### Key Insights

- The simulation is correct by construction and a fine spoken baseline, but the doubling length is unusable at `rounds = 30`.
- Nothing about the query needs the whole string: only one position's ancestry matters, which the next approach exploits.

### Index Backtracking

#### Derivation

The simulation materializes every round, yet the query needs a single position. Read the expansion from the receiving end instead: a position in the expanded string sits inside the two-bit block of one source character, and every block has the shape `character + "0"`, its first bit repeating the source character and its second bit always `'0'`. So position `index` after one round decodes without the string: at an odd offset the bit is `'0'` with certainty, and at an even offset the bit equals the source character at `index // 2` one round earlier. Working upward converts `rounds` doublings into at most `rounds` constant-time decisions:

1. While `rounds > 0`:
   - when `index` is odd, the position is a block's constant second bit, so
     return `0`;
   - otherwise halve `index` and decrement `rounds`, moving the question to
     that round's source string.
2. When no rounds remain, `index` addresses the original string directly:
   return `int(bits[index])`.

#### Walkthrough

Example 1, `bits = "01"`, `rounds = 1`, `index = 2`:

```text
rounds = 1   index = 2   even -> halve to index = 1, rounds = 0
rounds = 0   no rounds left -> read bits[1] = '1' -> return 1
```

The return is `1`, matching the expected Output. Example 2, `bits = "1"`, `rounds = 2`, `index = 3`:

```text
rounds = 2   index = 3   odd -> a block's second bit is always '0'
return 0
```

which matches the statement: the expansions run `"1"` -> `"10"` -> `"1000"`, and position 3 is the constant `'0'` tail of the block descended from position 1 of `"10"`.

#### Solution

The code is the walkthrough's upward walk:

```python
class Solution:
    def solve(self, bits: str, rounds: int, index: int) -> int:
        """Return the bit at position index after rounds expansions.

        Time:  O(rounds): each iteration answers at once or strips one
            bit off index; rounds <= 30 by the constraints.
        Space: O(1): two integers change in place.
        """
        while rounds > 0:
            if index % 2 == 1:
                return 0
            index //= 2
            rounds -= 1
        return int(bits[index])
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rounds)`

Each iteration either returns immediately or removes one bit from `index` together with one round; there are at most `rounds` iterations, capped at 30 by the constraints.

##### Space Complexity: `O(1)`

Two integers change in place; nothing grows with the input.

#### Key Insights

- A position needs its ancestry, not its siblings: each round contributes one bit test, so the query collapses from exponential length to `rounds` steps.
- The odd-offset shortcut is what makes the walk end early: a block's second bit is `'0'` no matter how many further rounds would follow.
- The guarantee `index < bits.length × 2^rounds` means the final read lands inside `bits`, so no bounds check is needed.

### Divisibility Closed Form

#### Derivation

The upward walk answers `0` exactly when it meets an odd `index` at some level, and meeting an odd value at level `r` means bit `r` of the original `index` is `1`. The loop's outcome therefore depends on a single question: are the lowest `rounds` bits of `index` all zero? One modulo test decides it. When `index % 2^rounds == 0`, the walk descends cleanly through every round into the original string at `index // 2^rounds`; any other value means some level met an odd position and the answer is `0`:

1. Compute `block_size = 2 ** rounds`.
2. When `index % block_size == 0`, return `int(bits[index // block_size])`.
3. Otherwise return `0`.

#### Walkthrough

Example 2, `bits = "1"`, `rounds = 2`, `index = 3`: `block_size = 4` and `3 % 4 = 3`, so some level met an odd position and the closed form returns `0`, matching the expected Output. Example 1, `bits = "01"`, `rounds = 1`, `index = 2`: `block_size = 2` and `2 % 2 = 0`, so the answer is `bits[2 // 2] = bits[1] = '1'`, again matching. Example 3 has `rounds = 0`, so `block_size = 1`: every `index` passes the modulo test and the answer is `bits[2] = '1'`.

#### Solution

```python
class Solution:
    def solve(self, bits: str, rounds: int, index: int) -> int:
        """Return the bit at position index after rounds expansions.

        Time:  O(rounds): one exponentiation and one modulo over numbers
            bounded by 2^30.
        Space: O(1): one integer beside the inputs.
        """
        block_size = 2 ** rounds
        if index % block_size == 0:
            return int(bits[index // block_size])
        return 0
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rounds)`

One exponentiation and one modulo over numbers bounded by `2^30`; the same bit levels as the walk, without the loop.

##### Space Complexity: `O(1)`

One integer beside the inputs.

#### Key Insights

- The closed form is the walk rewritten over binary representations: "the lowest `rounds` bits are all zero" is the divisibility test.
- It reads as one sentence in an interview and is the version to write once the ancestry argument is on the table.
- The `rounds = 0` case falls out for free: `block_size = 1` makes every index divisible and queries the original string.

## Comparison of Solutions

### Time Complexity

- **Round-by-Round Simulation**: `O(bits.length × 2^rounds)` - every round rebuilds a doubly long string.
- **Index Backtracking**: `O(rounds)` - at most one halving step per round, capped at 30.
- **Divisibility Closed Form**: `O(rounds)` - one exponentiation and one modulo over bounded numbers.

### Space Complexity

- **Round-by-Round Simulation**: `O(bits.length × 2^rounds)` - the expanded string dominates.
- **Index Backtracking**: `O(1)` - two integers change in place.
- **Divisibility Closed Form**: `O(1)` - one integer beside the inputs.

### Trade-offs

- **Round-by-Round Simulation**: zero insight required and trivially correct, but exponential in `rounds` and unusable at the stated bounds.
- **Index Backtracking**: linear in the round count with constant space, and its derivation explains where the answer comes from.
- **Divisibility Closed Form**: the shortest expression of the same idea, but the reason it is correct lives in the backtracking argument above it.

### When to Use Each

- **Index Backtracking (Recommended)**: the interview answer: derive the block structure aloud, then write the six-line walk.
- **Divisibility Closed Form**: once the ancestry argument has been explained and brevity matters.
- **Round-by-Round Simulation**: as the spoken baseline before improving it, or when `rounds` is genuinely 1 or 2.

### Optimization Notes

- The insight to state before coding: every block in every round has the shape `character + "0"`, so a block's second bit is always `'0'` and its first bit is inherited from one level up.
- `rounds <= 30` keeps `2^rounds` inside a machine word, which is why the closed form's exponentiation costs nothing in practice.
- The guarantee `index < bits.length × 2^rounds` removes bounds checking in every approach; mention it when justifying the final `bits[index]` read.
