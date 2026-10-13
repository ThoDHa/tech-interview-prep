# [Get Max Charge](https://www.fastprep.io/problems/amazon-get-max-charge)

**Hard** | **NN minutes** | **Dynamic Programming, Stack**

A team of engineers at Amazon, using advanced simulation tools, are analyzing a series of interconnected systems, where each system has a charge value represented by charge[i] (which can be positive, negative, or zero).



The engineers have a specialized tool that allows them to perform the following operation: Select a system and remove it, causing the neighboring systems to automatically merge and combine their charge values. If the removed system has neighboring systems with charges x and y directly to its left and right, they will combine to form a new system with charge x + y. No combination will take place if the system is the leftmost or rightmost in the array.



Since this process is computationally expensive, the engineers will simulate the operation using Amazon's advanced tools.



For example, if the system charges are [-3, 1, 4, -1, 5, -9], using the tool on the 4th system (index 3) will result in the new sequence [-3, 1, 9, -9], as the charges from the 3rd and 5th systems also combine to 4 + 5 = 9. If they then use the tool on the 1st system in this new sequence, it will become [1, 9, -9].

## Examples

### Example 1

**Input:** `charge = [-2, 4, 3, -2, 1]`

**Output:** `4`

**Explanation:** Therefore, the maximum possible charge that can be obtained is 4.

### Example 2

**Input:** `charge = [-2, 4, 9, 1, -1]`

**Output:** `9`

**Explanation:** Therefore, the maximum possible charge that can be obtained is 9.

### Example 3

**Input:** `charge = [-1, 3, 2]`

**Output:** `3`

**Explanation:** Therefore, the maximum possible charge that can be obtained is 3.

## Constraints

- `1 <= n <= 2 * 10^5`
- `-10^9 <= charge[i] <= 10^9`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
