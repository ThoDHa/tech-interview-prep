# [Sort Error Codes by Frequency](https://www.fastprep.io/problems/amazon-sort-error-codes-by-frequency)

**Easy** | **NN minutes** | **Sorting, Hash Table**

You are given an integer array codes representing error codes.

Sort the entire array using these priority rules:

Error codes with lower frequency come first.If two error codes have the same frequency, the smaller numeric value comes first.Return the sorted array, keeping duplicate values in the result.

Function Description Complete the function sortErrorCodesByFrequency in the editor below.

sortErrorCodesByFrequency has the following parameter:

int[] codes: the input error codesReturns int[]: the reordered array.

## Examples

### Example 1

**Input:** `codes = [4, 5, 6, 5, 4, 3]`

**Output:** `[3, 6, 4, 4, 5, 5]`

**Explanation:** 3 and 6 appear once, so they come first in numeric order. Then 4 and 5 each appear twice, so 4 comes before 5.

### Example 2

**Input:** `codes = [2, 2, 1, 1, 1, 3]`

**Output:** `[3, 2, 2, 1, 1, 1]`

**Explanation:** 3 has frequency 1, 2 has frequency 2, and 1 has frequency 3.

## Constraints

- `The output must contain the same multiset of values as the input.`
- `Order by increasing frequency, then by increasing numeric value.`

## Solutions

### Tally Then Sort by Two Keys

#### Derivation

The output rule is a pure function of the frequencies: group values by frequency (ascending), and inside equal frequency order by value (ascending). The baseline follows that recipe literally:

1. Count every code with a hash map.
2. Build the result by walking `(frequency, value)` pairs in sorted order, emitting each value `frequency` times.

A two-pass structure makes it linear-plus-sort: one pass to count, one sort over distinct values, one emission pass. A more naive variant (re-scanning the array per output block) is possible but adds nothing.

#### Walkthrough

Example 1, `codes = [4, 5, 6, 5, 4, 3]`: counts are `3: 1, 6: 1, 4: 2, 5: 2`. Sorting by `(frequency, value)` gives `(1, 3)`, `(1, 6)`, `(2, 4)`, `(2, 5)`, emitting `[3, 6, 4, 4, 5, 5]`, the expected output. Example 2, `[2, 2, 1, 1, 1, 3]`: counts `3: 1, 2: 2, 1: 3`; emission `[3, 2, 2, 1, 1, 1]`.

#### Solution

```python
from collections import Counter
from typing import List


class Solution:
    def solve(self, codes: List[int]) -> List[int]:
        """Return the codes ordered by frequency then value.

        Time:  O(n log n): the distinct-value sort dominates.
        Space: O(n) for counts and output.
        """
        counts = Counter(codes)
        ordered = sorted(counts.items(), key=lambda item: (item[1], item[0]))
        result: List[int] = []
        for value, frequency in ordered:
            result.extend([value] * frequency)
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

The count pass is linear; the sort covers distinct values; emission is linear.

##### Space Complexity: `O(n)`

Counts bounded by distinct values, plus the output.

#### Key Insights

- Sorting the distinct `(frequency, value)` pairs by the tuple's natural order encodes both tie-break rules at once.
- Duplicates reappear exactly `frequency` times, so the multiset is preserved by construction.

### Bucket by Frequency

#### Derivation

Frequencies lie between 1 and `n`, which makes them bucket-sortable: after counting, group the distinct values into buckets indexed by frequency, then walk the buckets in ascending frequency order, sorting inside each bucket only. When every bucket holds few values the inner sorts are near-linear; in the worst case (all values distinct, one giant bucket) it degenerates to the comparison rung. The win is practical, not asymptotic-guaranteed:

1. Count codes into a map.
2. Scatter values into `buckets[frequency]`.
3. Walk frequencies ascending; sort each bucket's values ascending; emit each value `frequency` times.

#### Walkthrough

Example 1 again: buckets hold `1 -> [3, 6]` and `2 -> [4, 5]`; the walk emits `[3, 6]` then `[4, 4, 5, 5]`, matching. Example 2: buckets `1 -> [3]`, `2 -> [2]`, `3 -> [1]` emit `[3, 2, 2, 1, 1, 1]`.

#### Solution

```python
from collections import Counter
from typing import List


class Solution:
    def solve(self, codes: List[int]) -> List[int]:
        """Return the codes ordered by frequency then value.

        Time:  O(n + f * d log d) summed over buckets: linear counting
            plus per-bucket value sorts (f the max frequency, d the
            bucket sizes).
        Space: O(n).
        """
        counts = Counter(codes)
        buckets: List[List[int]] = [[] for _ in range(len(codes) + 1)]
        for value, frequency in counts.items():
            buckets[frequency].append(value)
        result: List[int] = []
        for frequency in range(1, len(buckets)):
            if buckets[frequency]:
                for value in sorted(buckets[frequency]):
                    result.extend([value] * frequency)
        return result
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + sum of d log d over buckets)`

Linear counting and bucketing; the per-bucket sorts shrink as frequencies spread.

##### Space Complexity: `O(n)`

Buckets and output.

#### Key Insights

- Frequencies are bounded by `n`, which is exactly the condition that makes bucket indexing possible.
- The comparison rung is the ceiling case of this rung with one bucket holding everything.

## Comparison of Solutions

### Time Complexity

- **Tally Then Sort by Two Keys**: `O(n log n)` always.
- **Bucket by Frequency**: `O(n + sum of per-bucket sorts)`, near-linear when frequencies spread.

### Space Complexity

- Both `O(n)`.

### Trade-offs

- The comparison rung is three lines and immune to input shape.
- The bucket rung exploits the bounded frequency domain for a practical speedup.

### When to Use Each

- **Tally Then Sort by Two Keys**: the default answer.
- **Bucket by Frequency**: hot paths with many distinct frequencies.

### Optimization Notes

- Values themselves are often bounded too (error codes), which would make the inner sorts count-sorts and the whole pipeline linear.
- Python's stable sort with key `lambda value: (counts[value], value)` collapses the bucket walk into one statement at the same `O(n log n)`.
