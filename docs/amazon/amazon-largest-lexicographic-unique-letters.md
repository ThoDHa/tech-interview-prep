# [Remove Duplicate Letters for the Largest Result](https://www.fastprep.io/problems/amazon-largest-lexicographic-unique-letters)

**Hard** | **NN minutes** | **String, Stack, Greedy**

Given a lowercase string s, remove characters so that every distinct letter appears exactly once. The remaining characters must preserve their original relative order.

Return the lexicographically largest possible result.

## Examples

### Example 1

**Input:** `s = "bcabc"`

**Output:** `"cab"`

**Explanation:** The subsequence cab contains each distinct letter once and is lexicographically largest.

### Example 2

**Input:** `s = "cbacdcbc"`

**Output:** `"cbad"`

**Explanation:** Keeping the early c and b allows the largest valid prefix.

### Example 3

**Input:** `s = "bbcaac"`

**Output:** `"bca"`

**Explanation:** The best unique-letter subsequence is bca.

## Constraints

- `1 ≤ s.length ≤ 100000.`
- `s contains only lowercase English letters.`

## Solutions

### Brute Force

#### Derivation

The most literal reading of "remove characters so every distinct letter appears exactly once" enumerates the survivors directly: the result must contain each distinct letter exactly once, so it has exactly as many characters as `s` has distinct letters, and it must be some subsequence of `s` of that length. Enumerating every subsequence of that length, keeping those whose letter multiset is exactly the distinct set, and tracking the lexicographic maximum answers the question:

1. Count the distinct letters of `s` as `distinct_count`.
2. Enumerate every `itertools.combinations` of positions of `s` of length
   `distinct_count`; each combination spells one candidate string.
3. Accept a candidate only when `len(set(candidate)) == distinct_count`, which
   rejects any candidate that drops a letter or repeats one beyond its budget.
4. Track the largest accepted candidate in `best`; return `best`.

The scan order of `combinations` does not matter because every candidate is compared.

#### Walkthrough

Example 1: `s = "bcabc"`. The distinct letters are `{a, b, c}`, so every candidate has three characters:

```text
"bca" (positions 0,1,2)  all distinct -> best = "bca"
"bcb" (positions 0,1,3)  b repeats -> rejected
"bcc" (positions 0,1,4)  c repeats -> rejected
"bac" (positions 0,2,3)  all distinct -> "bac" < "bca", best unchanged
"bbc" (positions 0,2,4)  b repeats -> rejected
"bcb" (positions 0,3,4)  b repeats -> rejected
"cab" (positions 1,2,3)  all distinct -> "cab" > "bca", best = "cab"
"cac" (positions 1,2,4)  c repeats -> rejected
"cbb" (positions 1,3,4)  b repeats -> rejected
"abc" (positions 2,3,4)  all distinct -> "abc" < "cab", best unchanged
```

The maximum accepted candidate is `"cab"`, matching the expected Output for Example 1. Example 2 (`"cbacdcbc"`) has distinct letters `{a, b, c, d}` and its maximum is `"cbad"`; Example 3 (`"bbcaac"`) has `{a, b, c}` and its maximum is `"bca"`.

#### Solution

The code is the candidate loop from the walkthrough with the multiset filter and the running maximum.

```python
from itertools import combinations


class Solution:
    def solve(self, s: str) -> str:
        distinct_count = len(set(s))
        best = ""
        for positions in combinations(range(len(s)), distinct_count):
            candidate = "".join(s[position] for position in positions)
            if len(set(candidate)) == distinct_count and candidate > best:
                best = candidate
        return best
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(C(n, d) × d)`

Where `d` is the number of distinct letters: the loop visits `C(n, d)` position combinations and builds and filters each candidate in `d` work. With `n` at the stated `100000` bound this is astronomically beyond any budget, even though `d` never exceeds `26`.

##### Space Complexity: `O(d)`

The candidate string of `d` characters and the best-so-far copy.

#### Key Insights

- Transcribes the requirement literally: the result length is forced to the distinct-letter count, which collapses the search to one combination size.
- The filter `len(set(candidate)) == distinct_count` carries the entire constraint: a candidate passes exactly when every distinct letter appears, exactly once each.
- Correct but combinatorial: it validates the two faster approaches on small inputs, and cannot run at the stated constraint.

### Positional Greedy

#### Derivation

The brute force wastes its budget deciding whole strings at once, most of them invalid or dominated. The greedy observation decides one letter at a time, from the largest letter down: the largest letter that can still start the answer must be used first, and "can still start" means a copy of it exists at or after the current position AND everything still needed fits in the suffix behind that copy. Fixing the first letter shrinks the problem to the suffix after it, where the same rule repeats:

1. Hold `remaining`, the set of letters not yet placed, and `start`, the scan
   position just after the last chosen letter.
2. While `remaining` is non-empty, try its letters in descending order.
3. For each candidate letter, find its first position at or after `start`;
   the letter is pickable when that position exists and
   `set(s[position:])` still covers `remaining` (every unplaced letter,
   including itself, appears later).
4. Pick the largest pickable letter: append it, move `start` past its
   position, and remove it from `remaining`.
5. Return the chosen letters joined.

#### Walkthrough

Example 2: `s = "cbacdcbc"`, `remaining = {a, b, c, d}`. Each round tries letters largest first; each candidate position is the letter's first occurrence at or after `start`:

```text
round 1:  d: no occurrence at or after 0 -> skip
          c: position 0, suffix "cbacdcbc" still holds a, b, d
             -> choose c   chosen = [c]    start = 1   remaining = {a, b, d}
round 2:  d: no occurrence at or after 1 -> skip
          b: position 1, suffix "bacdcbc" still holds a, d
             -> choose b   chosen = [cb]   start = 2   remaining = {a, d}
round 3:  d: position 3, suffix "cdcbc" lacks a -> not pickable
          a: position 2, suffix "acdcbc" still holds d
             -> choose a   chosen = [cba]  start = 3   remaining = {d}
round 4:  d: position 3, suffix "cdcbc" holds d
             -> choose d   chosen = [cbad]             remaining = {}
return "cbad"
```

Round 3 is the decisive beat: `d` is the largest remaining letter, but its only occurrence sits after a suffix that has already lost its `a`, so choosing `d` first would make the answer impossible; the greedy falls to `a`. The result is `"cbad"`, matching the expected Output for Example 2.

#### Solution

The code is the descending-letter rounds from the walkthrough, with the suffix-coverage test guarding each pick.

```python
class Solution:
    def solve(self, s: str) -> str:
        remaining = set(s)
        chosen_letters = []
        start = 0
        while remaining:
            for candidate_letter in sorted(remaining, reverse=True):
                candidate_position = s.find(candidate_letter, start)
                if candidate_position != -1 and set(s[candidate_position:]) >= remaining:
                    chosen_letters.append(candidate_letter)
                    start = candidate_position + 1
                    remaining.remove(candidate_letter)
                    break
        return "".join(chosen_letters)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(26² × n)`

Every round rescans up to `26` candidate letters, and each attempt builds a suffix set over up to `n` characters; there are at most `26` rounds, so the bound is linear in `n` with a large constant.

##### Space Complexity: `O(n)`

The suffix slice `s[candidate_position:]` and its character set, rebuilt per attempt.

#### Key Insights

- Greedy choice in descending letter order is safe: a larger first letter beats any longer-or-shorter alternative that starts smaller, and the coverage test is what separates "largest" from merely "possible".
- The coverage test `set(s[position:]) >= remaining` is the feasibility oracle; skipping it would let the greedy strand a letter with no occurrence left.
- The same suffix is re-set-checked once per candidate letter, which is the inefficiency the monotonic stack below removes.

### Monotonic Stack with Last Occurrence

#### Derivation

The positional greedy re-derives suffix feasibility from scratch for every candidate letter. The stack formulation instead answers, for each incoming character, a single local question: could any letter already kept be improved by dropping it now and re-taking it later? A kept letter is worth dropping exactly when it is smaller than the incoming character and a copy of it appears later; otherwise it is locked. One pass with a [monotonic stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) and a last-occurrence table decides every drop in constant time:

1. Build `last_occurrence`, mapping each letter to the last position where it
   appears in `s`.
2. Sweep `position` over `s`. Skip a letter that is already kept (the one-copy
   rule); it can never improve its position later.
3. While the kept stack's top `kept[-1]` is smaller than the incoming letter
   AND `last_occurrence[kept[-1]]` is beyond `position`, pop it: dropping it
   now is safe because it can be re-taken later, ahead of the smaller
   context it currently sits in.
4. Push the incoming letter.
5. Return the stack joined bottom to top.

#### Walkthrough

Example 1: `s = "bcabc"`, with `last_occurrence = {b: 3, c: 4, a: 2}`:

```text
position 0 'b'  not kept yet; kept empty -> keep
                kept = [b]
position 1 'c'  top 'b' < 'c' and last['b'] = 3 > 1 -> pop b
                kept empty -> keep
                kept = [c]
position 2 'a'  top 'c' < 'a' is false -> no pops, keep
                kept = [ca]
position 3 'b'  top 'a' < 'b', but last['a'] = 2 < 3 -> a stays, keep
                kept = [cab]
position 4 'c'  already kept -> skip
return "cab"
```

The pop at position 1 is the mechanism: the early `b` is smaller than the incoming `c` and reappears at position 3, so trading it away is safe, and it re-enters later in front of nothing better. On Example 2 (`"cbacdcbc"`) no pop ever fires: the incoming `a` at position 2 is smaller than both kept letters, and the later `d` wants to pop `a` but `last['a'] = 2` has already passed. The stack accumulates `c, b, a, d` and the function returns `"cbad"`, matching the expected Output for Example 2; Example 3 (`"bbcaac"`) keeps its first `b`, drops nothing, and returns `"bca"`.

#### Solution

The code is the single sweep from the walkthrough: skip kept letters, pop improvable tops, push the incoming letter.

```python
class Solution:
    def solve(self, s: str) -> str:
        last_occurrence = {letter: position for position, letter in enumerate(s)}
        kept = []
        in_stack = set()
        for position, letter in enumerate(s):
            if letter in in_stack:
                continue
            while kept and kept[-1] < letter and last_occurrence[kept[-1]] > position:
                in_stack.remove(kept.pop())
            kept.append(letter)
            in_stack.add(letter)
        return "".join(kept)
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each character is pushed at most once and popped at most once, so the total stack work is bounded by `2n`; the last-occurrence table is built in one pass.

##### Space Complexity: `O(1)`

The stack and the membership set hold at most `26` letters, and `last_occurrence` has at most `26` entries, all bounded by the alphabet rather than by `n`.

#### Key Insights

- The pop rule encodes the whole greedy: a kept letter is only surrendered when it is strictly smaller than the incoming letter AND provably re-takeable (`last_occurrence` beyond the current position); otherwise it is locked in place.
- The skip rule (`letter in in_stack`) is the one-copy constraint; a second occurrence of a kept letter can never beat the earlier position it already occupies, because the earlier copy dominates lexicographically.
- Reversing the pop comparison (`kept[-1] > letter`) turns the same algorithm into the lexicographically smallest variant, which is the form most references teach; the direction of the inequality is the only difference.
- `last_occurrence` collapses the greedy's per-letter suffix rescans into one table lookup, which is what buys the single linear pass.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(C(n, d) × d)` - every position combination of the distinct-letter count is built and filtered.
- **Positional Greedy**: `O(26² × n)` - up to `26` rounds, each rescanning up to `26` candidate letters with an `O(n)` suffix check.
- **Monotonic Stack with Last Occurrence**: `O(n)` - one pass; each character is pushed and popped at most once.

### Space Complexity

- **Brute Force**: `O(d)` - the candidate and best strings of `d` characters.
- **Positional Greedy**: `O(n)` - the suffix slice and its character set per attempt.
- **Monotonic Stack with Last Occurrence**: `O(1)` - alphabet-bounded stack, membership set, and last-occurrence table.

### Trade-offs

- **Brute Force**: impossible to get wrong and a natural oracle, but combinatorial time rules it out beyond toy inputs.
- **Positional Greedy**: the most explainable decision procedure (largest pickable letter first), but its repeated suffix rescans carry a `26²` constant and linear scratch space.
- **Monotonic Stack with Last Occurrence**: single pass, constant auxiliary space, and no suffix re-derivation, at the cost of the least obvious correctness argument (why a popped letter is always recoverable and why a skipped duplicate is never a loss).

### When to Use Each

- **Brute Force**: as the reference oracle while testing the other two; fine only for strings of a dozen or so characters.
- **Positional Greedy (Recommended for explanation)**: when the interviewer wants the decision rule narrated; it derives naturally from "take the largest letter you can still afford".
- **Monotonic Stack with Last Occurrence**: the implementation answer: linear time, constant space, and the form that scales to the stated `100000`-character constraint.

### Optimization Notes

- The brute force compares whole candidate strings; restricting `combinations` to positions in descending-letter order would find a maximum sooner, but the asymptotics remain combinatorial, so the simpler full scan is kept.
- The positional greedy's `set(s[candidate_position:]) >= remaining` rebuilds a suffix set per attempt; precomputing, for each position and letter, the next occurrence table turns the coverage test into lookups, which is exactly the information the monotonic stack stores as `last_occurrence`.
- In the stack version, the `in_stack` set is what makes the skip rule constant time; without it, a duplicate letter would push twice and violate the one-copy rule.
- The stated constraint guarantees at least one character, so every approach returns a non-empty string; no empty-input case exists.
