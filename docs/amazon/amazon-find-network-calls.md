# [Find Networking Calls](https://www.fastprep.io/problems/amazon-find-network-calls)

**Medium** | **NN minutes** | **Array, Sorting, Prefix Sum**

Source note: Example 2 was added on 2025-03-31; its relevant source image is included in Problem Source.


A digital commerce platform is conducting an experiment on the number of customer feedback entries associated with each item in its catalog.



You are provided with an array feedback of size n, where feedback[i] denotes the current number of feedback entries for the i-th item. The platform offers API endpoints that allow modifying these counts by either increasing or decreasing them by one per call.



Given an integer array targetCounts of size q, your task is to determine the number of API calls required to adjust the feedback count of every item in feedback so that all items match each value in targetCounts.



The objective is to return an array of size q, where the i-th element represents the total number of API calls necessary to align all feedback counts with targetCounts[i].



Complete the function findNetworkCalls in the editor below.



findNetworkCalls has the following parameters:



int feedback[n]: the initial count of reviews of each product
int targetCounts[q]: the equal count of reviews

long[]: an array where each element denotes the total API calls needed to align all feedback counts to the corresponding value in targetCounts

## Examples

### Example 1

**Input:** `feedback = [4, 6, 5, 2, 1]`, `targetCounts = [3]`

**Output:** `[10, 20]`

**Explanation:** Answer Version 1 - 



Therefore, the total API calls made to change the number of reviews for all products to 3 is: 1 + 3 + 2 + 1 + 2 = 9.


Hence, return the array [9].

Answer Version 2 (newly found on 03-31-2025) -

The source indicates that the expected output for this test case is expected to be [10, 20].

As we can see, the table is not complete in the source found this time. I will update once find more complete source.




As the screenshots were taken on the platform, our expected output will go with [10, 20].

### Example 2

**Input:** `feedback = [3, 6, 6]`, `targetCounts = [5, 6]`

**Output:** `[4, 3]`

**Explanation:** For counts value 5 -

The total number of API calls to be made is 2 + 1 + 1 = 4.

For counts value 6 -

The total number of API calls to be made is 3 + 0 + 0 = 3.

So, we return [4, 3].

## Constraints

- `1 ≤ n ≤ 10^5`
- `1 ≤ feedback[i] ≤ 10^6`
- `1 ≤ q ≤ 10^5`
- `1 ≤ targetCounts[i] ≤ 10^6`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
