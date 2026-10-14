# [Maximize Similarity](https://www.fastprep.io/problems/amazon-maximize-similarity)

**Easy** | **NN minutes** | **Array, Greedy, Math**

In the world of Amazon's vast inventory management, you face a challenge of optimizing two inventories, inv1 and inv2, each containing n elements.



Your goal is to maximize the similarity between these inventories. The similarity is measured by the number of indices i (0 ≤ i < n) where inv1[i] equals inv2[i].



Amazon provides a unique tool, the "Inventory Optimizer". This tool allows you to perform the following operation:


Select two distinct indices i and j (where 0 ≤ i, j < n and i ≠ j), provided that the jth element of inv1 is positive.Apply the operation: add 1 to inv1[i] and subtract 1 from inv1[j].
Using the Inventory Optimizer, you can perform this operation any number of times (including zero) to maximize the similarity between inv1 and inv2.



🧡 Thanks A LOT! spike!! 🧡

## Examples

### Example 1

**Input:** `inv1 = [2, 4, 1]`, `inv2 = [1, 2, 3]`

**Output:** `2`

**Explanation:** Apply the operation on indices i = 2 and j = 0, which makes inv1 = [1, 4, 2].
Next, apply the operation on indices i = 2 and j = 1, which updates inv1 = [1, 3, 3].



Now, there are two indices, i = 0 and i = 2, for which inv1[i] = inv2[i]. Since it's impossible to make the elements at all indices of the two arrays equal, the answer is 2.

## Constraints

- `1 <= n <= 10^5`
- `1 <= inv1[i], inv2[i] <= 10^4`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
