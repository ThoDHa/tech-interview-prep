# [Cleanup Dataset](https://www.fastprep.io/problems/amazon-cleanup-dataset)

**Medium** | **NN minutes** | **Greedy, Hash Table**

Data Scientists at Amazon are working on cleansing a machine learning dataset. The dataset is represented as a string dataset consisting of an even number of lowercase English letters. The goal is to clean the dataset efficiently by performing specific operations.



Here's how the operations work:



In each operation, two characters from the dataset are selected and removed.
Each operation has an associated cost:

x: the cost of removing two identical characters.
y: the cost of removing two different characters.



The task is to determine the optimal strategy that minimizes the total cost to completely clean up the dataset. In other words, find the minimum cost required to remove all characters and make the dataset empty.

## Examples

### Example 1

**Input:** `dataset = "aaabca"`, `x = 3`, `y = 2`

**Output:** `7`

**Explanation:** In the first operation, the first and second characters are deleted from the dataset, resulting in dataset = "abca". The cost of this operation is x = 3 because both removed characters are equal (also 'a').



In the next operation, the first and third characters are deleted, making dataset = "ba". The cost of this operation is y = 2 because the removed characters are not equal. In the final operation, the remaining two characters are deleted, making the dataset an empty string. The cost of this operation is y = 2 because the removed characters are not equal.



Hence, the total cost is 3 + 2 + 2 = 7.

### Example 2

**Input:** `dataset = "ouio"`, `x = 2`, `y = 4`

**Output:** `6`

**Explanation:** Operation 1 -
Action: removed the first and last characters of the dataset, resulting in the string dataset = "ui".
Cost: x = 2 (since both removals, 'o' and 'o' are the same)

Operation 2 -
Action: delete the remaining characters of "ui", making dataset an empty string.
Cost: y = 4 (since the removed characters, 'u' and 'i' are diff)

Total cost --> x + y = 2 + 4 = 6

## Constraints

- `2 ≤ |dataset| ≤ 105`
- `|dataset| is even`
- `1 ≤ x, y ≤ 104`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
