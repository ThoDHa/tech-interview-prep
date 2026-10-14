# [Get The Most Out Of The Data](https://www.fastprep.io/problems/amazon-get-most-out-of-the-data)

**Medium** | **NN minutes** | **Array, Greedy, Sorting**

DAs at TomTom Global are deeply engaged in the analysis of the info gained when the company's re-inforcement learning AI model named Supa Helo is trained with different arrangements of exact the same dataset.



This time, the process involves exploring how the order of data points tends to affect the model's overall performance.



That being said, for an arr of n integers, denoted as data, the analysts all agree that the arrangement is represented using a permutation of the integers from 1 to n.



DAs at TomTom Global soon observed that the information gained for a given specific permutation p of the n integers in the arr data can be quantified using a special formula.



Detaily speaking, the info gained == sum of i * data[p[i]] for all indices i from 0 to n :)



You are required to complete the func pre-defined in the editor on the right side of this page 👉👉



This func has int[] data, which is an arr of integers, as its parameter.



If doing right, your implementation should return an int[] that represents the lexicographically smallest permutation p with the maximum info gain.



Memo: A permutation p is considered lexicographically smaller than another permutation pp if, at the first index i where p[i] and pp[i] differ, p[i] is less than pp[i]. This concept is crucial when determining the smallest permutation among multiple valid options.

## Examples

### Example 1

**Input:** `data = [2, 1, 2]`

**Output:** `[2, 1, 3]`

**Explanation:** Permutation   | Information Gain
[1, 2, 3] | 1 * 2 + 2 * 1 + 3 * 2 = 10
[2, 1, 3] | 1 * 1 + 2 * 2 + 3 * 2 = 11
[1, 3, 2] | 1 * 2 + 2 * 2 + 3 * 1 = 9
[3, 1, 2] | 1 * 2 + 2 * 2 + 3 * 1 = 9
[2, 3, 1] | 1 * 1 + 2 * 2 + 3 * 2 = 11
[3, 2, 1] | 1 * 2 + 2 * 1 + 3 * 2 = 10



The maximum information is gained for permutations [2, 1, 3] and [2, 3, 1], but [2, 1, 3] is the lexicographically smallest permutation.




More than happy to modify the explanation if found to be incorrect or misleading. Thanks for the feedback :)

## Constraints

- `:)`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
