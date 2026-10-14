# [Replace Values and Return Sums](https://www.fastprep.io/problems/amazon-replace-values-and-return-sums)

**unknown difficulty** | **NN minutes** | **unknown categories**

You are given an integer array entries and a 2D integer array transactions. Each transaction is a pair [oldValue, newValue].

For each transaction, replace every occurrence of oldValue in entries with newValue. After applying the transaction, record the sum of all values in entries.

Return an array containing the recorded sums after each transaction.

The sums may exceed the range of a 32-bit integer.

## Examples

### Example 1

**Input:** `entries = [1, 2, 1, 3]`, `transactions = [[1, 4], [2, 1], [4, 2]]`

**Output:** `[13, 12, 8]`

**Explanation:** After replacing 1 with 4, the array is [4,2,4,3] with sum 13. After replacing 2 with 1, the sum is 12. After replacing 4 with 2, the sum is 8.

### Example 2

**Input:** `entries = [5, 5]`, `transactions = [[1, 2], [5, 1]]`

**Output:** `[10, 2]`

**Explanation:** The first transaction has no matching value, so the sum stays 10. The second transaction changes both values to 1, so the sum becomes 2.

## Constraints

- `transactions[i].length == 2`
- `The returned sums may require 64-bit integers.`

## Solutions

### Rescan per Transaction

#### Derivation

The problem is a procedure, so the first solution performs the procedure: keep a working copy of `entries`, apply each transaction as a literal find-and-replace pass, and record `sum` of the copy after the pass. No state is carried between transactions beyond the mutated copy, which makes the simulation impossible to misread:

1. Copy `entries` into `values` so the input stays intact.
2. For each `[old_value, new_value]` in `transactions`, walk `values` and
   rewrite every matching position.
3. Append `sum(values)` to `sums`.
4. Return `sums`.

#### Walkthrough

Example 1, `entries = [1, 2, 1, 3]`, `transactions = [[1, 4], [2, 1], [4, 2]]`. Each line is one transaction with the rewritten copy:

```text
start         [1, 2, 1, 3]
replace 1->4  [4, 2, 4, 3]   sum 13
replace 2->1  [4, 1, 4, 3]   sum 12
replace 4->2  [2, 1, 2, 3]   sum 8
```

The recorded sums `13, 12, 8` match the expected Output. Note the last transaction rewrites the positions the first one changed: replacements persist across transactions.

#### Solution

The code is the per-transaction rewrite and resum:

```python
from typing import List


class Solution:
    def solve(self, entries: List[int],
              transactions: List[List[int]]) -> List[int]:
        values = list(entries)
        sums = []
        for old_value, new_value in transactions:
            for position, value in enumerate(values):
                if value == old_value:
                    values[position] = new_value
            sums.append(sum(values))
        return sums
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(T x n)`

Each of the `T` transactions pays one `O(n)` rewrite pass and one `O(n)` summation.

##### Space Complexity: `O(n)`

The working copy `values`.

#### Key Insights

- Replacements persist: a transaction sees every earlier transaction's writes, so the copy must never be reset between transactions.
- `old_value == new_value` is a harmless no-op here; the scan finds the values, rewrites them to themselves, and the sum is unchanged.
- The rescan repeats all of its work every transaction although only the occurrences of one value move the total, which is exactly the waste the counting approach removes.

### Count Bookkeeping with a Running Sum

#### Derivation

The rescan recomputes the whole picture to learn a number only two counts can move. Every transaction changes the total by `occurrences x (new_value - old_value)`, where `occurrences` is how many positions currently hold `old_value`, and it moves that entire population from `old_value`'s bucket to `new_value`'s bucket. A count map plus a running sum therefore serves every transaction in constant time, turning the `O(T x n)` loop into one `O(n)` preprocessing pass and `O(1)` per transaction:

1. Build `value_counts` over `entries` and `running_sum` in one pass.
2. For each `[old_value, new_value]`: read
   `occurrences = value_counts.get(old_value, 0)`.
3. Add `occurrences * (new_value - old_value)` to `running_sum`.
4. When occurrences exist, zero the `old_value` bucket and merge the
   population into the `new_value` bucket.
5. Append `running_sum`.

#### Walkthrough

Example 1, `entries = [1, 2, 1, 3]`, `transactions = [[1, 4], [2, 1], [4, 2]]`. The pass builds `value_counts = {1: 2, 2: 1, 3: 1}` and `running_sum = 7`. Each line is one transaction:

```text
replace 1->4   occurrences 2   sum 7 + 2 x (4 - 1) = 13
               counts {1: 0, 2: 1, 3: 1, 4: 2}
replace 2->1   occurrences 1   sum 13 + 1 x (1 - 2) = 12
               counts {1: 1, 2: 0, 3: 1, 4: 2}
replace 4->2   occurrences 2   sum 12 + 2 x (2 - 4) = 8
               counts {2: 2, 3: 1, 4: 0}
```

The recorded sums `13, 12, 8` match the expected Output, and the third line shows the merge at work: the two values that started as `1` now sit in the `2` bucket. (Example 2's first transaction finds `occurrences 0`, so the sum stays `10` and no bucket moves.)

#### Solution

The code is the count pass and the per-transaction delta:

```python
from typing import Dict, List


class Solution:
    def solve(self, entries: List[int],
              transactions: List[List[int]]) -> List[int]:
        value_counts: Dict[int, int] = {}
        running_sum = 0
        for entry in entries:
            value_counts[entry] = value_counts.get(entry, 0) + 1
            running_sum += entry

        sums = []
        for old_value, new_value in transactions:
            occurrences = value_counts.get(old_value, 0)
            running_sum += occurrences * (new_value - old_value)
            if occurrences:
                value_counts[old_value] = 0
                value_counts[new_value] = (value_counts.get(new_value, 0)
                                           + occurrences)
            sums.append(running_sum)
        return sums
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + T)`

One preprocessing pass over the `n` entries and constant work per transaction.

##### Space Complexity: `O(n)`

The count map holds one bucket per distinct value.

#### Key Insights

- A global replacement moves a whole bucket, so its effect on the total is a single multiplication; no per-position work is ever needed.
- The merge step is what keeps chained transactions honest: after `1 -> 4`, the `4` bucket must include those arrivals before any later `4 -> 2` can price them.
- Python integers are arbitrary precision, so the 64-bit warning in the constraints costs nothing; in a fixed-width language the running sum would need a wide type.
- The `if occurrences` guard does double duty: it skips the bucket surgery for absent values and keeps `old_value == new_value` a clean no-op (zero, then restore).

## Comparison of Solutions

### Time Complexity

- **Rescan per Transaction**: `O(T x n)` - a full rewrite pass plus a full summation per transaction.
- **Count Bookkeeping with a Running Sum**: `O(n + T)` - one counting pass and constant work per transaction.

### Space Complexity

- **Rescan per Transaction**: `O(n)` - the working copy of the values.
- **Count Bookkeeping with a Running Sum**: `O(n)` - one count bucket per distinct value.

### Trade-offs

- **Rescan per Transaction**: mirrors the problem statement line for line, but its cost grows with the product of transaction count and array length.
- **Count Bookkeeping with a Running Sum**: flat per-transaction cost regardless of array length, at the price of maintaining bucket merges that must never lose an arrival.

### When to Use Each

- **Rescan per Transaction**: one-shot scripts or as the oracle that validates the counting logic.
- **Count Bookkeeping with a Running Sum (Recommended)**: the interview answer: the delta formula is one line and the bucket merge is three.

### Optimization Notes

- The merge must add the migrating occurrences to whatever the `new_value` bucket already holds; overwriting instead of merging silently drops values and corrupts every later transaction.
- When `new_value` has never been seen, `value_counts.get(new_value, 0)` seeds its bucket; the `defaultdict` alternative reads the same intent with less ceremony.
- The running sum absorbs the 64-bit concern: it is maintained incrementally, so no summation ever re-touches the array.
