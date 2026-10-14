# [Get Max Information Gain](https://www.fastprep.io/problems/amazon-get-max-information-gain)

**Easy** | **NN minutes** | **String, Hash Table, Sorting**

Data analysts at Amazon are analyzing a data set of n strings in the array 
dataSet[], each consisting of lowercase English letters. Each character in a 
string corresponds to a particular feature.



The information gain obtained by training a model with two strings, dataSet[i] 
and dataSet[j], is the difference between the lengths of the strings i.e., 
|len(dataSet[i]) - len(dataSet[j])|. To avoid too many overlapping features, two 
strings can be selected only if the number of common features between them does not exceed a 
given threshold, max_common_features. The number of common features here is equal 
to the number of common characters between the two strings. For example, "abc" and "bcd" have 
2 common features 'b' and 'c'. While "aa" and "aaa" have two common features, the "a" two 
'a' characters.



Given dataSet and max_common_features, determine the maximum 
information gain possible.

## Examples

### Example 1

**Input:** `dataSet = ["abofh", "ab", "mo"]`, `max_common_features = 1`

**Output:** `3`

**Explanation:** It is optimal to choose the strings "abofh" and "mo". Their number of common features is 1 ('o') and the information gain is |5 - 2| = 3.

### Example 2

**Input:** `dataSet = ["a", "bcdef"]`, `max_common_features = 1`

**Output:** `4`

**Explanation:** The two strings can be chosen. They do not share any common features and their difference in length is 4.

## Constraints

- `2 ≤ n ≤ 1000`
- `1 ≤ len(dataSet[i]) ≤ 1000`
- `1 ≤ max_common_features ≤ 1000`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
