# [Longest Content Window with Bounded Labels](https://www.fastprep.io/problems/amazon-streaming-content-label-window)

**Hard** | **NN minutes** | **Array, Hash Table, Sliding Window**

A content stream arrives in order. Each item carries a non-empty set of labels. Given contentLabels and a limit k, find the longest contiguous window of items whose combined label set contains at most k distinct labels.

Return the inclusive zero-based endpoints [start, end]. If several windows have the same maximum length, return the one with the smallest start. Return [-1, -1] when the stream is empty. Labels within one item are unique.

This finite batch represents the same ordered add(contentLabels) stream followed by a longest() query.

## Examples

### Example 1

**Input:** `contentLabels = [["toxic","ok"],["toxic","ok","spam"]]`, `k = 2`

**Output:** `[0,0]`

**Explanation:** The first item uses exactly two labels. Including the second item introduces spam, exceeding the limit.

### Example 2

**Input:** `contentLabels = [["toxic","ok"],["toxic","ok","spam"]]`, `k = 3`

**Output:** `[0,1]`

**Explanation:** All two items together use the three permitted labels.

### Example 3

**Input:** `contentLabels = [["a"],["b","c"],["a","b"],["d"]]`, `k = 3`

**Output:** `[0,2]`

**Explanation:** The first three items use a, b, c. Adding the final item introduces a fourth label.

## Constraints

- `0 <= contentLabels.length <= 200000.`
- `1 <= k <= 200000.`
- `Each item has between 1 and 20 unique non-empty labels.`
- `The total number of label occurrences does not exceed 400000.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
