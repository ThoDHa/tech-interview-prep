# [Minimum S3 Storage Cost](https://www.fastprep.io/problems/amazon-minimum-s3-storage-cost)

**unknown difficulty** | **NN minutes** | **unknown categories**

A batch contains files numbered from 1 to 2^n. Some files are sensitive and require encryption; their indices are given in sensitiveFiles.

For any contiguous batch of M files:

If it contains X > 0 sensitive files, storing the whole batch costs M * X * encCost.If it contains no sensitive files, storing the whole batch costs flatCost.If the batch size is even, you may either store the whole batch or split it into two equal contiguous batches and pay the sum of their optimal costs. Return the minimum possible storage cost modulo 1_000_000_007.

## Examples

### Example 1

**Input:** `n = 2`, `encCost = 2`, `flatCost = 1`, `sensitiveFiles = [1,3]`

**Output:** `6`

**Explanation:** Splitting all the way to single files costs 2 + 1 + 2 + 1 = 6, which is better than keeping the full batch or only splitting once.

### Example 2

**Input:** `n = 3`, `encCost = 2`, `flatCost = 1`, `sensitiveFiles = [1,2,3,4,5,6,7,8]`

**Output:** `16`

**Explanation:** Every file is sensitive. Splitting into single files gives eight batches, each costing 2.

### Example 3

**Input:** `n = 3`, `encCost = 2`, `flatCost = 1`, `sensitiveFiles = [7,1]`

**Output:** `8`

**Explanation:** One optimal split is [1], [2], [3,4], [5,6], [7], and [8], for total cost 8.

## Constraints

- `1 <= n <= 3 * 10^5`
- `1 <= encCost, flatCost <= 10^5`
- `1 <= sensitiveFiles.length <= 2^n`
- `Each sensitive file index is between 1 and 2^n.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
