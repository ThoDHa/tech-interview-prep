# [Grouped-Query Attention with a KV Cache](https://www.fastprep.io/problems/amazon-grouped-query-attention-with-kv-cache)

**Hard** | **NN minutes** | **Matrix, Simulation, Math**

Compute one projection-free grouped-query scaled dot-product attention pass using an existing key-value cache plus newly generated key and value rows.

query has width queryHeads * headDim. Every cached or new key and value row has width kvHeads * headDim. Append the new rows after the cached rows for the attention calculation. queryHeads is divisible by kvHeads; each consecutive group of queryHeads / kvHeads query heads shares one key-value head.

For each query row and query head, compute scaled dot products against all cached and new key rows, divide by sqrt(headDim), apply maximum-subtracted softmax, and combine the corresponding value-head slices. Concatenate the query-head outputs and return each row as comma-separated values formatted to exactly six decimal places.

## Examples

### Example 1

**Input:** `query = [[1]]`, `cachedKey = []`, `cachedValue = []`, `newKey = [[0],[1]]`, `newValue = [[10],[20]]`, `queryHeads = 1`, `kvHeads = 1`

**Output:** `["17.310586"]`

**Explanation:** With one head and no cache, this is ordinary scaled dot-product attention.

### Example 2

**Input:** `query = [[1,0]]`, `cachedKey = [[1]]`, `cachedValue = [[4]]`, `newKey = [[0]]`, `newValue = [[8]]`, `queryHeads = 2`, `kvHeads = 1`

**Output:** `["5.075766,6.000000"]`

**Explanation:** Two query heads share one key-value head and attend over one cached and one new token.

### Example 3

**Input:** `query = [[1,0],[0,1]]`, `cachedKey = [[1,0]]`, `cachedValue = [[10,20]]`, `newKey = [[0,1]]`, `newValue = [[30,40]]`, `queryHeads = 2`, `kvHeads = 2`

**Output:** `["15.378828,30.000000","20.000000,34.621172"]`

**Explanation:** Equal query and key-value head counts recover ordinary multi-head attention while still using the cache.

## Constraints

- `1 <= query rows, cached rows + new rows <= 40`
- `1 <= kvHeads <= queryHeads <= 16 and queryHeads is divisible by kvHeads.`
- `1 <= headDim <= 16; all matrices are rectangular with the stated widths and cached/new key-value row counts match.`
- `newKey and newValue are nonempty; cached matrices may be empty.`
- `Every entry is an integer from -100 through 100.`

## Solutions

### Slice Inside the Head Loop

#### Derivation

The statement fixes every step; the baseline follows it literally. Each query row has width `queryHeads * headDim`, and each key or value row has width `kvHeads * headDim`. Concatenating the cached rows and the new rows gives the full token sequence. For each query row and each query head, the head's slice of the row (positions `q_head * headDim` through the next `headDim` entries) scores against the matching key-head slice of every token: dot product, divided by `sqrt(headDim)`. A maximum-subtracted softmax turns the scores into weights, and the weighted sum of the same key-value head's value slices is that head's output. The group structure only decides the mapping: query head `q_head` uses key-value head `q_head // group_size`, where `group_size = queryHeads // kvHeads`:

1. Build `key_rows = cachedKey + newKey` and `value_rows = cachedValue + newValue`.
2. For every query row and query head, slice, score against every token's key slice, softmax with the row maximum subtracted, and combine the value slices.
3. Concatenate the per-head outputs and format each number to exactly six decimal places.

#### Walkthrough

Example 2, `query = [[1,0]]`, `cachedKey = [[1]]`, `newKey = [[0]]`, `queryHeads = 2`, `kvHeads = 1`, so `headDim = 1` and `group_size = 2`; both query heads share key-value head 0, whose token keys are `[1]` and `[0]` with values `[4]` and `[8]`. Query head 0 slices `[1]`: scores `[1, 0]`, softmax with maximum `1` subtracted gives weights `[1, e^-1]` normalized to `[0.731059, 0.268941]`; the output is `4 * 0.731059 + 8 * 0.268941 = 5.075766`. Query head 1 slices `[0]`: scores `[0, 0]`, uniform weights `[0.5, 0.5]`, output `(4 + 8) / 2 = 6.000000`. The concatenated row matches the expected `["5.075766,6.000000"]`.

#### Solution

```python
from math import exp, sqrt
from typing import List


class Solution:
    def solve(
        self,
        query: List[List[int]],
        cachedKey: List[List[int]],
        cachedValue: List[List[int]],
        newKey: List[List[int]],
        newValue: List[List[int]],
        queryHeads: int,
        kvHeads: int,
    ) -> List[str]:
        """Return formatted grouped-query attention outputs per query row.

        Time:  O(rows * queryHeads * tokens * headDim): every query-head
            slice rescans every token's key slice.
        Space: O(tokens + headDim): token scores and one output accumulator.
        """
        head_dim = len(query[0]) // queryHeads
        key_rows = cachedKey + newKey
        value_rows = cachedValue + newValue
        group_size = queryHeads // kvHeads
        outputs: List[str] = []
        for row in query:
            row_parts: List[str] = []
            for q_head in range(queryHeads):
                kv_head = q_head // group_size
                q_start = q_head * head_dim
                q_slice = row[q_start : q_start + head_dim]
                scores: List[float] = []
                for token in range(len(key_rows)):
                    k_start = kv_head * head_dim
                    k_slice = key_rows[token][k_start : k_start + head_dim]
                    dot = sum(q * k for q, k in zip(q_slice, k_slice))
                    scores.append(dot / sqrt(head_dim))
                top = max(scores)
                weights = [exp(score - top) for score in scores]
                denominator = sum(weights)
                combined = [0.0] * head_dim
                for token, weight in enumerate(weights):
                    v_start = kv_head * head_dim
                    v_slice = value_rows[token][v_start : v_start + head_dim]
                    for dimension, value in enumerate(v_slice):
                        combined[dimension] += weight / denominator * value
                row_parts.extend(f"{value:.6f}" for value in combined)
            outputs.append(",".join(row_parts))
        return outputs
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows * queryHeads * tokens * headDim)`

Each of the `rows * queryHeads` slices rescans all `tokens` key slices, `headDim` entries each; the softmax and the value combination add one more linear token pass.

##### Space Complexity: `O(tokens + headDim)`

The score and weight lists hold one entry per token; the accumulator holds `headDim` entries.

#### Key Insights

- The cache and the new rows differ only in provenance: appending them into one sequence is the whole cache mechanism.
- Maximum subtraction is numerics, not math: softmax outputs are unchanged, and the largest exponent stays bounded.
- The group mapping is integer division: consecutive query-head blocks of size `queryHeads // kvHeads` share one key-value head.

### Precompute Key-Value Blocks per Head

#### Derivation

The baseline re-slices every token's key and value for every query head, although the slices depend only on the key-value head, and there are `kvHeads` of those, not `queryHeads`. Hoisting the slicing out of the query-head loop removes that repetition: once per call, build `key_blocks[kv_head]` and `value_blocks[kv_head]`, each holding every token's slice for that head. The scoring loop then reads prebuilt blocks, and the per-token slice bounds vanish from the inner loop. The arithmetic count is unchanged; the constant improves by the reuse factor `group_size` on slicing and bounds computation, and the code states the head alignment once instead of recomputing index arithmetic per access:

1. Precompute, for each key-value head, the list of key slices and value slices across all tokens.
2. Run the same per-row, per-head scoring and softmax over the prebuilt blocks.
3. Format and concatenate exactly as before.

#### Walkthrough

Example 3, `queryHeads = kvHeads = 2`, `headDim = 1`, cached plus new tokens give keys `[[1,0],[0,1]]` and values `[[10,20],[30,40]]`. The prebuilt blocks are `key_blocks[0] = [1, 0]`, `key_blocks[1] = [0, 1]`, `value_blocks[0] = [10, 30]`, `value_blocks[1] = [20, 40]`. Row `[1,0]`: query head 0 scores against `key_blocks[0]` as `[1, 0]`, weights `[0.731059, 0.268941]`, output `10 * 0.731059 + 30 * 0.268941 = 15.378828`; query head 1 slices `[0]` and scores against `key_blocks[1]` as `[0, 0]`, uniform weights, output `(20 + 40) / 2 = 30.000000`. The row reads `"15.378828,30.000000"`, matching. Row `[0,1]` symmetrically yields `"20.000000,34.621172"`.

#### Solution

```python
from math import exp, sqrt
from typing import List


class Solution:
    def solve(
        self,
        query: List[List[int]],
        cachedKey: List[List[int]],
        cachedValue: List[List[int]],
        newKey: List[List[int]],
        newValue: List[List[int]],
        queryHeads: int,
        kvHeads: int,
    ) -> List[str]:
        """Return formatted grouped-query attention outputs per query row.

        Time:  O(rows * queryHeads * tokens * headDim + total_key_width):
            the same arithmetic as the baseline, with per-head token
            slices prebuilt once.
        Space: O(tokens * kvHeads * headDim): the prebuilt blocks, which
            equals the size of the concatenated key and value rows.
        """
        head_dim = len(query[0]) // queryHeads
        key_rows = cachedKey + newKey
        value_rows = cachedValue + newValue
        group_size = queryHeads // kvHeads
        key_blocks: List[List[List[int]]] = [[] for _ in range(kvHeads)]
        value_blocks: List[List[List[int]]] = [[] for _ in range(kvHeads)]
        for token in range(len(key_rows)):
            for kv_head in range(kvHeads):
                start = kv_head * head_dim
                key_blocks[kv_head].append(key_rows[token][start : start + head_dim])
                value_blocks[kv_head].append(value_rows[token][start : start + head_dim])
        outputs: List[str] = []
        for row in query:
            row_parts: List[str] = []
            for q_head in range(queryHeads):
                kv_head = q_head // group_size
                q_start = q_head * head_dim
                q_slice = row[q_start : q_start + head_dim]
                scores = [
                    sum(q * k for q, k in zip(q_slice, key)) / sqrt(head_dim)
                    for key in key_blocks[kv_head]
                ]
                top = max(scores)
                weights = [exp(score - top) for score in scores]
                denominator = sum(weights)
                combined = [0.0] * head_dim
                for token, weight in enumerate(weights):
                    for dimension, value in enumerate(value_blocks[kv_head][token]):
                        combined[dimension] += weight / denominator * value
                row_parts.extend(f"{value:.6f}" for value in combined)
            outputs.append(",".join(row_parts))
        return outputs
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows * queryHeads * tokens * headDim + total_key_width)`

The scoring arithmetic matches the baseline; the added term is the one-time block construction, linear in the concatenated key and value widths, and the slicing inside the hot loop disappears.

##### Space Complexity: `O(tokens * kvHeads * headDim)`

The blocks together hold exactly the entries of the concatenated key and value rows, reorganized per head.

#### Key Insights

- Slicing depends on the key-value head only, so hoisting it amortizes across the `group_size` query heads that share each block.
- The memory trade is real but bounded: the blocks are a permutation of data already in memory, not a copy per query head.
- With `kvHeads` equal to `queryHeads` (multi-head attention, no grouping), the blocks degenerate to the plain layout and both rungs coincide.

## Comparison of Solutions

### Time Complexity

- **Slice Inside the Head Loop**: `O(rows * queryHeads * tokens * headDim)` with a per-access slicing constant.
- **Precompute Key-Value Blocks per Head**: the same asymptotics plus a one-time `O(total_key_width)` pass, with a smaller constant in the hot loop.

### Space Complexity

- **Slice Inside the Head Loop**: `O(tokens + headDim)`.
- **Precompute Key-Value Blocks per Head**: `O(tokens * kvHeads * headDim)`, equal to the concatenated key and value data.

### Trade-offs

- The baseline touches no extra memory and is the honest transcription of the statement.
- The blocked rung trades a full copy of the key-value data for slicing reuse; at these constraint sizes either fits easily.

### When to Use Each

- **Slice Inside the Head Loop**: one-shot small inputs, or when the key-value data must not be copied.
- **Precompute Key-Value Blocks per Head**: whenever `group_size` exceeds one and the attention pass runs repeatedly, as a real KV cache does.

### Optimization Notes

- A real implementation batches rows through matrix products per key-value head; the per-row loop here keeps the arithmetic inspectable.
- Formatting to six decimals belongs at the boundary only; carrying floats internally avoids accumulated rounding in the join.
