# [Find Hash](https://www.fastprep.io/problems/amazon-find-hash)

**Medium** | **NN minutes** | **Array, Math**

The developers at AWS IAM are designing a new checksum logic for an authentication module. The checksum is calculated as an array hash where hash[i] = secretKey[i] % param[i]. There are n parameters for the checksum, where the ith parameter is represented by param[i]. The secret key consists of n values, with the ith value denoted as secretKey[i].



A good secret key is one that results in more distinct values in the hash array.



Given the array param of size n, determine the maximum number of possible distinct values in the hash array by selecting an appropriate secretKey.

## Examples

### Example 1

**Input:** `param = [1, 2, 4]`

**Output:** `3`

**Explanation:** You can choose secretKey = [1, 3, 2], resulting in the hash array [0, 1, 2], which consists of 3 distinct elements.

### Example 2

**Input:** `param = [1, 1, 1]`

**Output:** `1`

**Explanation:** If we set secretKey = [1, 2, 3], we get hash = [0, 0, 0], resulting in only one unique value, which is 0. Therefore, the answer is 1.

## Constraints

- `1 ≤ n ≤ 2 * 10^5`
- `1 ≤ param[i] ≤ 10^9`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
