# [Get Minimum Amount](https://www.fastprep.io/problems/amazon-get-min-amount)

**unknown difficulty** | **NN minutes** | **unknown categories**

Special thanks: A special thank you to a lovely, amazing fren who shared that this question appeared again on September 21, 2026! 💜

The manager of the Amazon warehouse has decided to make changes to the inventory. Currently, the inventory has n products, where the quality of the ith product after quality checks is represented by the array element quality[i].

The manager wants to create an optimal inventory, where the array of products quality follows the following property:

All occurrences of each quality value must be contiguous.In order to convert the inventory into an optimal inventory, the manager can do the following operation any number of times:

Choose two quality values x and y.Replace every product with quality x to have quality y instead.This operation costs num_replacements units of money, where num_replacements is the number of products whose quality was changed.Given n products and an array quality, find the minimum amount of money the manager has to spend to convert the inventory into an optimal inventory.

Note: The quality of a product can be negative indicating that the product is of poor quality.

## Examples

### Example 1

**Input:** `quality = [7, 7, 5, 7, 3, 5, 3]`

**Output:** `4`

**Explanation:** Given n = 7, quality = [7, 7, 5, 7, 3, 5, 3].

One of the optimal ways to convert is explained below:

Hence, the total amount spent is 4.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-get-min-amount; fill them in. -->

## Solutions

### Brute Force over Value Partitions

#### Derivation

The operation renames *every* product of one value, so two products with equal quality can never diverge: they share one fate forever. That observation collapses the problem from products to value classes. Compress the array into blocks of equal adjacent values; which classes survive the conversion, and at what price? If a set of values ends up as one final value, every one of its blocks must sit contiguously in the block sequence (renaming never reorders products). So a conversion plan is a partition of the distinct values into classes, each class contiguous on its own, and the price of a class is the products that must change: everything except the class's most frequent value, which survives untouched. Enumerate all set partitions of the values, keep the contiguous ones, and take the cheapest:

1. Compress `quality` into `block_letters` and `block_sizes`.
2. Count products per value into `value_count` and list the values in order of
   first appearance.
3. Recursively enumerate every set partition of the values (`partitions_values`
   assigns each value either to an existing class or to a new one).
4. A partition is valid when every class is contiguous in `block_letters`; a
   valid partition costs the sum over classes of (class size - largest value count).
5. Return the minimum cost over valid partitions.

#### Walkthrough

Example 1, `quality = [7, 7, 5, 7, 3, 5, 3]`, compresses into six blocks with letters `7, 5, 7, 3, 5, 3` and sizes `2, 1, 1, 1, 1, 1`; value 7 owns 3 products, values 5 and 3 own 2 each. The five set partitions of `{7, 5, 3}`:

| Partition | Class blocks | Valid? | Cost |
| --- | --- | --- | --- |
| `{7,5,3}` | blocks `0..5`, one run | yes | `7 - 3 = 4` |
| `{7,5}` / `{3}` | class `{7,5}` at blocks `0,1,2,4` | gap at block 3 | - |
| `{7,3}` / `{5}` | class `{7,3}` at blocks `0,2,3,5` | gap at block 1 | - |
| `{5,3}` / `{7}` | class `{5,3}` at blocks `1,3,4,5` | gap at block 2 | - |
| `{7}` / `{5}` / `{3}` | value 7 at blocks `0,2` | gap | - |

Value 7 appears in three scattered blocks, so every partition that keeps 7 apart from some other value breaks contiguity. Only the single all-merging class survives, costing `7 - 3 = 4`: rename the two 5-products and the two 3-products to 7, and the array is one uniform run. That matches the expected Output.

#### Solution

```python
from typing import Dict, List, Set


class Solution:
    def getMinAmount(self, quality: List[int]) -> int:
        block_letters: List[str] = []
        block_sizes: List[int] = []
        for value in quality:
            if block_letters and block_letters[-1] == str(value):
                block_sizes[-1] += 1
            else:
                block_letters.append(str(value))
                block_sizes.append(1)

        value_count: Dict[str, int] = {}
        for letter, block_size in zip(block_letters, block_sizes):
            value_count[letter] = value_count.get(letter, 0) + block_size
        values = list(value_count)

        def class_is_contiguous(class_letters: Set[str]) -> bool:
            seen_class_block = False
            seen_other_block = False
            for letter in block_letters:
                if letter in class_letters:
                    if seen_other_block:
                        return False
                    seen_class_block = True
                elif seen_class_block:
                    seen_other_block = True
            return True

        best_cost = sum(quality)

        def search_partitions(value_index: int, classes: List[Set[str]]) -> None:
            nonlocal best_cost
            if value_index == len(values):
                if all(class_is_contiguous(class_letters) for class_letters in classes):
                    partition_cost = sum(
                        sum(value_count[letter] for letter in class_letters)
                        - max(value_count[letter] for letter in class_letters)
                        for class_letters in classes
                    )
                    best_cost = min(best_cost, partition_cost)
                return
            for class_letters in classes:
                class_letters.add(values[value_index])
                search_partitions(value_index + 1, classes)
                class_letters.remove(values[value_index])
            classes.append({values[value_index]})
            search_partitions(value_index + 1, classes)
            classes.pop()

        search_partitions(0, [])
        return best_cost
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(Bell(m) × m × n)`

Where `m` is the number of distinct values and `Bell(m)` the number of set partitions: each partition checks up to `m` classes for contiguity over the `n`-block sequence. Exponential in `m`, so it serves small inputs and as a correctness oracle.

##### Space Complexity: `O(m + n)`

The block list plus the recursion over partitions holding up to `m` classes.

#### Key Insights

- Equal values are inseparable: the operation renames all of them at once, so planning happens on value classes, never on individual products.
- Renaming never reorders anything, so a surviving class must already occupy a contiguous run of blocks.
- A class converts for the price of its minority products: its most frequent value stays put, the rest rename into it.
- The baseline `best_cost` seed is the everything-into-one-value plan, which is always contiguous and costs `n - (largest value count)`.

### Block Letters with Partition Labels Cuts

#### Derivation

The brute force wastes work on partitions the block sequence already rules out. A valid class is a contiguous run of blocks, and classes never interleave (each block belongs to exactly one class), so the classes carve the block sequence into consecutive segments cut only between blocks. A cut is legal exactly when no value has blocks on both sides: value `v`'s blocks span from its first block to its last, so the boundary after block `i` is open whenever some value seen so far reappears later. Tracking each value's last block turns that into a running maximum, the classic partition labels sweep. And cutting is never harmful: splitting a segment at a legal cut moves each value wholly into one side, so the merged segment's largest count equals one side's largest, and

```text
merged cost - split cost = (size - largest) - (size_left - largest_left)
                                         - (size_right - largest_right)
                         = largest_right - (largest - largest_left) <= 0
```

because `largest` is one of `largest_left`, `largest_right`. Finer is never worse, so cutting at every closed boundary is optimal:

1. Compress `quality` into `block_letters` and `block_sizes`.
2. Record `last_block[value]`, the last block index holding each value.
3. Sweep the blocks keeping `segment_end` (the furthest last-block among values
   seen in the open segment), `segment_size`, and `segment_max_count`.
4. When the sweep reaches block `i == segment_end`, the segment closes: add
   `segment_size - segment_max_count` to `total_cost` and reset the trackers.

#### Walkthrough

Example 1 again: blocks with letters `7, 5, 7, 3, 5, 3` and sizes `2, 1, 1, 1, 1, 1`, giving `last_block[7] = 2`, `last_block[5] = 4`, `last_block[3] = 5`:

```text
block 0 (7, size 2)   segment_end = 2
block 1 (5, size 1)   segment_end = max(2, 4) = 4
block 2 (7, size 1)   segment_end = 4        (block 0 was open here)
block 3 (3, size 1)   segment_end = max(4, 5) = 5
block 4 (5, size 1)   segment_end = 5
block 5 (3, size 1)   i == segment_end -> close: size 7, max 2, cost 7 - 2 = 5?
```

The last line shows why the tracker must accumulate counts per value, not just carry the largest single block: value 7 owns blocks 0 and 2, so the segment's largest *value count* is `2 + 1 = 3`. With `segment_max_count = 3` the closing segment costs `7 - 3 = 4`, the expected Output. No boundary ever closed earlier (`segment_end` stayed ahead of `i` until block 5), so the whole array forms one segment: with 7 scattered across three blocks, nothing cheaper is legally reachable, exactly as the brute force concluded.

#### Solution

The code is the sweep from the walkthrough; `segment_counts` accumulates products per value inside the open segment so the closing cost uses value totals.

```python
from typing import Dict, List


class Solution:
    def getMinAmount(self, quality: List[int]) -> int:
        block_letters: List[str] = []
        block_sizes: List[int] = []
        for value in quality:
            if block_letters and block_letters[-1] == str(value):
                block_sizes[-1] += 1
            else:
                block_letters.append(str(value))
                block_sizes.append(1)

        block_count = len(block_letters)
        last_block: Dict[str, int] = {}
        for block_index, letter in enumerate(block_letters):
            last_block[letter] = block_index

        total_cost = 0
        segment_end = 0
        segment_size = 0
        segment_counts: Dict[str, int] = {}
        for block_index, letter in enumerate(block_letters):
            segment_end = max(segment_end, last_block[letter])
            segment_size += block_sizes[block_index]
            segment_counts[letter] = segment_counts.get(letter, 0) + block_sizes[block_index]
            if block_index == segment_end:
                total_cost += segment_size - max(segment_counts.values())
                segment_end = 0
                segment_size = 0
                segment_counts = {}
        return total_cost
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass to compress the array and one pass over the blocks; each block does constant dictionary work.

##### Space Complexity: `O(n)`

The block lists; the per-segment dictionaries hold at most the distinct values.

#### Key Insights

- Compressing to blocks first makes the geometry visible: contiguity of values is a property of the block sequence, and legal cuts sit only where no value spans the boundary.
- The running `segment_end` maximum is the partition-labels device: a segment closes at the first block reaching the horizon of every value seen inside it.
- Splitting at a legal cut never raises the cost, so the finest legal partition - a cut at every closed boundary - is optimal without any search.
- The closing charge is `segment_size - largest value count`: the segment's most frequent value stays, everything else renames into it.

## Comparison of Solutions

### Time Complexity

- **Brute Force over Value Partitions**: `O(Bell(m) × m × n)` - every set partition of the `m` distinct values is scored against the block sequence.
- **Block Letters with Partition Labels Cuts**: `O(n)` - two linear passes, compression plus sweep.

### Space Complexity

- **Brute Force over Value Partitions**: `O(m + n)` - block bookkeeping plus the partition recursion.
- **Block Letters with Partition Labels Cuts**: `O(n)` - the block lists dominate.

### Trade-offs

- **Brute Force over Value Partitions**: small, direct, and obviously faithful to the statement, but exponential in the distinct-value count, which large OA tests would blow past.
- **Block Letters with Partition Labels Cuts**: linear and simple once the cut-monotonicity argument is in hand, but it leans on the block compression and the finer-is-never-worse reasoning being exactly right.

### When to Use Each

- **Brute Force over Value Partitions**: an interview where the distinct values are few, or as the reference oracle when validating the linear sweep on random small inputs.
- **Block Letters with Partition Labels Cuts (Recommended)**: the real OA constraints: one pass, no search, and a cost provably matching the best valid partition.

### Optimization Notes

- Compression is what makes the sweep cheap: consecutive equal values collapse into one block, so the sweep's length is the block count, not `n`.
- `last_block` is built in one pre-pass; building it inline would force a lookahead the sweep cannot afford.
- Tracking counts per value (`segment_counts`) instead of the largest block size matters when one value contributes several blocks to a segment, as value 7 does in Example 1.
