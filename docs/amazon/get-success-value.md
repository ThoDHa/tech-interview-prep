# [Get Success Value](https://www.fastprep.io/problems/get-success-value)

**Easy** | **NN minutes** | **Sorting, Prefix Sum**

Amazon Prime Video has recently released an exclusive series on its platform. They collected the number of viewers from n
different regions across the world and stored the data in the array num_viewers.



The success value of the release is defined as the sum of viewership in the top k regions, those with the highest viewers.
For example, if num_viewers = [3, 2, 1, 4, 5] and k = 3, then the success value of the release is 
3 + 4 + 5 = 12 as [3, 4, 5] are the top 3 values.



Given a number of k values, calculate the success value for each query.


Complete the function findSuccessValue in the editor.

findSuccessValue has the following parameters:

int num_viewers[n]: viewership from n different regionsint queries[q]: an array of k valueslong[q]: the maximum possible success values for each query

## Examples

### Example 1

**Input:** `num_viewers = [2, 5, 6, 3, 5]`, `queries = [2, 3, 5]`

**Output:** `[11, 16, 21]`

**Explanation:** The viewership in 5 regions is num_viewers = [2, 5, 6, 3, 5], and we want to find the success value for 3 queries that are queries = [2, 3, 5].

For the first query, k = 2, the viewership of the top 2 regions is [6, 5]. The success value is 6 + 5 = 11.

For the second query, k = 3, the viewership of the top 3 regions is [6, 5, 5] and 6 + 5 + 5 = 16.

For the third query, k = 5, all the 5 regions are used for the success value and 6 + 5 + 5 + 3 + 2 = 21.

Return [11, 16, 21].

### Example 2

**Input:** `num_viewers = [7, 3, 5, 2]`, `queries = [1, 4]`

**Output:** `[7, 17]`

**Explanation:** For the first query, k = 1, only the top region is used for the success value.

For the second query, k = 4, all 4 regions are used.


Return [7, 17].

### Example 3

**Input:** `num_viewers = [7, 5, 6]`, `queries = [1, 2, 3]`

**Output:** `[7, 13, 18]`

**Explanation:** For the first query, k = 1, only the top region is used for the success value.

For the second query, k = 2, only the top 2 regions are used.

For the third query, k = 3, all 3 regions are used.


Return [7, 13, 18].

## Constraints

- `1 <= n <= 10^5`
- `1 <= q <= 10^5`
- `1 <= num_viewers[i] <= 10^9`
- `1 <= queries[i] <= n`
- `Each success value is at most 10^14 and requires a 64-bit integer.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
