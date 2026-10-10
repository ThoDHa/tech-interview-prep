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

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
