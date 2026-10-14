# [Maximum Equal Parts for Prefixes](https://www.fastprep.io/problems/amazon-maximum-equal-parts-for-prefixes)

**Medium** | **NN minutes** | **String, Array, Hash Table, Math**

A team at Amazon is working to ensure all packages are correctly sorted for delivery. Each package has a label represented by an uppercase English letter. The full list of labels is given as the string packages, where the i^th character is the label of the i^th package.

To optimize the sorting process, the team wants to analyze each prefix of the string packages (from length 1 to n) and determine the maximum number of equal parts it can be divided into. Each part must satisfy the following conditions:

Each part must have the same frequency of every character as every other part in that divisionGiven a string packages, calculate for each prefix t (from length 1 to n), the maximum number of equal parts into which the prefix can be divided, such that each part has the same number of occurrences of each character.

## Examples

### Example 1

**Input:** `packages = "ABAB"`

**Output:** `[1, 1, 1, 2]`

**Explanation:** Given, packages = "ABAB".

In the given example t represents prefix string and length represents the length of the prefix string.

Return [1, 1, 1, 2] as the answer.

## Constraints

- `packages consists only of uppercase English letters ('A' to 'Z').`
- `The answer is computed for every prefix of packages of length 1 to n, where n is the length of packages.`
- `For each prefix, the maximum number of equal parts is at least 1, since a prefix can always be treated as a single undivided part.`

## Solutions

### Per-Prefix Recount with Full Split Scan

#### Derivation

The most literal reading handles one prefix at a time and asks, for each candidate split count `candidate_split`, whether the prefix divides evenly. The key reformulation is that "every part has the same frequency of every character" is a divisibility statement: if `candidate_split` parts share each character evenly, every character's total count in the prefix is a multiple of `candidate_split`; conversely, when `candidate_split` divides every count, the prefix's characters deal out into `candidate_split` identical groups, one per part. So a prefix's answer is the largest `candidate_split` dividing all 26 counts, and the scarcest character caps the search: no split can exceed the smallest nonzero count, since every part needs at least one of it:

1. For each prefix length from `1` to `n`, recount the prefix into
   `char_counts`, a 26-slot array indexed by `letter_slot = ord(letter) - ord('A')`.
2. Read `smallest_count`, the minimum nonzero slot value.
3. Scan `candidate_split` from `smallest_count` down to `2`; the first value
   where every slot satisfies `count % candidate_split == 0` is the prefix's
   answer.
4. When no candidate above 1 passes, the answer is 1, and the collected
   `split_counts` list is the result.

#### Walkthrough

Example 1 is `packages = "ABAB"`, short enough to recount in full at every step:

```text
prefix "A"     char_counts A=1        smallest 1, scan range empty      split 1
prefix "AB"    char_counts A=1, B=1   smallest 1, scan range empty      split 1
prefix "ABA"   char_counts A=2, B=1   smallest 1, scan range empty      split 1
prefix "ABAB"  char_counts A=2, B=2   smallest 2
                 candidate_split 2: 2 % 2 == 0 and 2 % 2 == 0          split 2
```

The first three prefixes each hold a character an odd number of times or hold a lone character, so nothing above 1 can divide them evenly. The full prefix `"ABAB"` has both counts at 2, the candidate `2` divides both, and `split_counts` ends as `[1, 1, 1, 2]`, matching the expected Output.

#### Solution

The code is the per-prefix loop from the walkthrough: recount, cap, scan downward.

```python
from typing import List


class Solution:
    def maximumEqualParts(self, packages: str) -> List[int]:
        total_letters = len(packages)
        split_counts: List[int] = []
        for prefix_length in range(1, total_letters + 1):
            char_counts = [0] * 26
            for position in range(prefix_length):
                letter_slot = ord(packages[position]) - ord('A')
                char_counts[letter_slot] += 1

            smallest_count = min(
                count for count in char_counts if count > 0
            )
            best_split = 1
            for candidate_split in range(smallest_count, 1, -1):
                if all(count % candidate_split == 0 for count in char_counts):
                    best_split = candidate_split
                    break
            split_counts.append(best_split)
        return split_counts
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

Each of the `n` prefixes recounts its `prefix_length` characters and then scans up to `smallest_count` candidates with a 26-slot check, giving quadratic total work; the alphabet size 26 is a constant factor.

##### Space Complexity: `O(1)`

One 26-slot counter array is reused per prefix, beyond the output list.

#### Key Insights

- "Equal parts" reduces to divisibility: `candidate_split` works exactly when it divides every character's count, which removes all geometry of where a cut falls.
- The smallest nonzero count is both the search cap and a candidate, because every part must contain at least one of the scarcest character.
- `candidate_split = 1` always passes, so the fallback needs no special case; the scan simply finds nothing better.
- The recomputation of `char_counts` from scratch at every prefix is the waste the next approach removes.

### Running Counts with Divisor Scan

#### Derivation

The baseline pays twice for work it already did: it recounts the whole prefix though only one counter changes per letter, and it tries every `candidate_split` though only divisors of `smallest_count` can pass the divisibility test. Two repairs fix this. Keep the counts incremental, updating one slot per input letter. And enumerate only divisor candidates: divisors of `smallest_count` come in pairs `(divisor, smallest_count // divisor)` discovered by trial division up to its square root, so roughly `2 × √smallest_count` candidates replace the full scan, and each surviving candidate must still divide the other 25 counts:

1. Maintain `char_counts` across letters, incrementing one slot per letter.
2. Compute `smallest_count` over the nonzero slots.
3. For each `divisor` with `divisor * divisor <= smallest_count` that divides
   `smallest_count`, form the candidate pair
   `(smallest_count // divisor, divisor)`; the sweep tests every candidate
   and keeps the largest one that divides all 26 counts.
4. A candidate above `best_split` that divides all 26 counts replaces it; the
   final `best_split` per prefix (1 as the floor) is appended to `split_counts`.

#### Walkthrough

The same `packages = "ABAB"`, now with the counts carried forward. Only the last prefix has a `smallest_count` above 1, so it is the only one that exercises the divisor scan:

```text
letter A: A=1           smallest 1, divisor 1: pair (1, 1), none > 1    split 1
letter B: A=1, B=1      smallest 1, divisor 1: pair (1, 1)              split 1
letter A: A=2, B=1      smallest 1, divisor 1: pair (1, 1)              split 1
letter B: A=2, B=2      smallest 2
          divisor 1: pair (2, 1): candidate 2 divides both counts      best 2
          divisor 2: 2 * 2 > 2, loop ends                              split 2
```

At the final letter the divisor pair `(2, 1)` offers candidate 2, the all-count check passes, and `best_split` is 2; `split_counts` again ends `[1, 1, 1, 2]`, matching the expected Output.

#### Solution

The code keeps the counts alive across letters and swaps the full scan for the divisor-pair enumeration.

```python
from typing import List


class Solution:
    def maximumEqualParts(self, packages: str) -> List[int]:
        char_counts = [0] * 26
        split_counts: List[int] = []
        for letter in packages:
            char_counts[ord(letter) - ord('A')] += 1

            smallest_count = min(
                count for count in char_counts if count > 0
            )
            best_split = 1
            divisor = 1
            while divisor * divisor <= smallest_count:
                if smallest_count % divisor == 0:
                    for candidate_split in (
                        smallest_count // divisor,
                        divisor,
                    ):
                        if candidate_split > best_split and all(
                            count % candidate_split == 0
                            for count in char_counts
                        ):
                            best_split = candidate_split
                divisor += 1
            split_counts.append(best_split)
        return split_counts
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n × √n)`

Each prefix runs one constant counter update, then trial division up to `√smallest_count ≤ √n` with a constant-size (26-slot) validation per candidate; the increments amortize to one per letter.

##### Space Complexity: `O(1)`

The counter array persists across prefixes at a fixed 26 slots, beyond the output list.

#### Key Insights

- Only divisors of the smallest count deserve testing: a candidate that fails to divide the scarcest character can never divide the rest.
- Divisor pairs let one pass of trial division surface two candidates at once, and the sweep still tests every candidate, because a small divisor can pass the all-count check where its large partner fails.
- Incremental counting turns the per-prefix `O(prefix_length)` recount into a single counter bump, which is what drops the quadratic term.
- The residual cost is still the candidate validation loop; the next approach removes candidate enumeration entirely.

### Incremental GCD of Counts

#### Derivation

The divisor scan still asks, candidate by candidate, "does this split divide every count?" One arithmetic object answers for all candidates at once: a split count is admissible exactly when it divides every count, and the largest integer dividing a set of numbers is their [greatest common divisor](https://en.wikipedia.org/wiki/Euclidean_algorithm). So the maximum number of equal parts for a prefix is the gcd of its 26 counters, and the gcd folds left to right with Euclid's algorithm; slots still at zero are neutral because `gcd(x, 0) = x`, so the fold needs no filtering of unseen letters:

1. Keep `char_counts` incremental as before.
2. After each letter, fold `counts_gcd` over the 26 slots:
   `counts_gcd = gcd_of(counts_gcd, count)` with `counts_gcd` starting at 0.
3. Append `counts_gcd` per prefix; the fold runs the whole array without
   materializing any candidate list.

#### Walkthrough

The gcd fold over `"ABAB"`, showing the running `counts_gcd` after each letter (zero slots are neutral, `gcd(x, 0) = x`):

```text
letter A: A=1        fold: gcd(0, 1) = 1, zeros keep it 1              split 1
letter B: A=1, B=1   fold: gcd(1, 1) = 1                               split 1
letter A: A=2, B=1   fold: gcd(1, 2) = 1                               split 1
letter B: A=2, B=2   fold: gcd(0, 2) = 2 at slot A, gcd(2, 2) = 2
                     at slot B, zeros keep it 2                        split 2
```

The last line deserves a second look: each prefix restarts the fold at 0, so at the fourth letter slot `A` lifts `counts_gcd` from 0 to 2 and slot `B` holds it there. Every count is a multiple of 2, so 2 equal parts exist, and `split_counts` ends `[1, 1, 1, 2]`, matching the expected Output. At the third letter the fold found `gcd(1, 2) = 1`, correctly reporting that no split above 1 divides both a count of 2 and a count of 1.

#### Solution

The code is the fold from the walkthrough, with `gcd_of` as Euclid's algorithm on two counters.

```python
from typing import List


class Solution:
    def maximumEqualParts(self, packages: str) -> List[int]:
        def gcd_of(first: int, second: int) -> int:
            while second:
                first, second = second, first % second
            return first

        char_counts = [0] * 26
        split_counts: List[int] = []
        for letter in packages:
            char_counts[ord(letter) - ord('A')] += 1

            counts_gcd = 0
            for count in char_counts:
                counts_gcd = gcd_of(counts_gcd, count)
            split_counts.append(counts_gcd)
        return split_counts
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Each prefix folds 26 slots, each Euclid step halving the smaller argument, so per prefix the cost is constant times `log` of the largest count; summed over `n` prefixes this is `O(n log n)`.

##### Space Complexity: `O(1)`

The counter array persists at a fixed 26 slots, beyond the output list.

#### Key Insights

- "Largest split dividing every count" is the definition of the gcd, so the whole candidate search collapses into one fold.
- `gcd(0, x) = x` makes unseen letters neutral, which is why the fold can run over all 26 slots without filtering.
- When a letter's count stops being compatible with the current gcd (the `A=2, B=1` prefix), the fold drops to 1 and only another exact common factor restores it.
- The per-letter recomputation of the fold is deliberate: a gcd cannot be maintained incrementally when one element grows, because gcd removal is not computable in place.

## Comparison of Solutions

### Time Complexity

- **Per-Prefix Recount with Full Split Scan**: `O(n²)` - each prefix recounts its characters and scans up to its smallest count of candidates.
- **Running Counts with Divisor Scan**: `O(n × √n)` - incremental counts plus at most `2 × √smallest_count` divisor candidates per prefix.
- **Incremental GCD of Counts**: `O(n log n)` - a 26-slot Euclid fold per prefix, logarithmic in the largest count.

### Space Complexity

- **Per-Prefix Recount with Full Split Scan**: `O(1)` - a reused 26-slot counter, beyond the output list.
- **Running Counts with Divisor Scan**: `O(1)` - a persistent 26-slot counter, beyond the output list.
- **Incremental GCD of Counts**: `O(1)` - a persistent 26-slot counter, beyond the output list.

### Trade-offs

- **Per-Prefix Recount with Full Split Scan**: the most direct transcription of the divisibility idea and easy to verify, but the from-scratch recount and the exhaustive split scan make it quadratic.
- **Running Counts with Divisor Scan**: keeps every byte of work incremental and prunes candidates to divisors, but still materializes and validates a candidate list per prefix.
- **Incremental GCD of Counts**: replaces candidate enumeration with one arithmetic fold and is the simplest code once the gcd observation is in hand, at the cost of trusting that the fold recomputes rather than maintains the gcd.

### When to Use Each

- **Per-Prefix Recount with Full Split Scan**: as a first working version or a reference to test the faster versions against on small inputs.
- **Running Counts with Divisor Scan**: when the divisor structure is easier to explain than the gcd reduction, or in languages where a fold over 26 slots per letter feels heavy.
- **Incremental GCD of Counts (Recommended)**: as the submission: strictly less work per prefix and the shortest correct code on the page.

### Optimization Notes

- `math.gcd` expresses the fold directly (`counts_gcd = gcd(counts_gcd, count)` imported from `math`) and matches the hand-rolled Euclid loop in complexity; the hand-rolled version shows the algorithm the fold relies on.
- A prefix cannot improve its split count unless the incoming letter raises the smallest count or introduces a factor common to every count, but detecting that cheaply is harder than the fold itself, so the fold is the practical endpoint.
- The divisor-pair trick from the second approach generalizes to per-query divisor listing; here it is only a stepping stone, since the gcd makes it unnecessary.
- Counting into `ord(letter) - ord('A')` slots keeps every operation on fixed arrays; a dict keyed by letter works too but adds hashing per letter for no benefit on a 26-letter alphabet.
