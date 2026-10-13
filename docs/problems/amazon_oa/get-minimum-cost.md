# [Get Minimum Costs](https://www.fastprep.io/problems/get-minimum-cost)

**Medium** | **NN minutes** | **Heap, Greedy**

In Amazon Go Store, there are nitems, each associated with two positive
values a[i] and b[i]. There are infinitely many items of each 
type numbered from 1 to infinity and the item numbered j of type 
i costs a[i] + (j - 1) * b[i] units.



Determine the minimum possible cost to purchase exactly m items.


Function Description 
Complete the function getMinimumCost in the editor.



getMinimumCost has the following parameters:



1. int a[n]: an array of integers
2. int b[n]: an array of integers
3. m: the number of items to purchase
Returns 
long integer: the minimum cost

## Examples

### Example 1

**Input:** `a = [2, 1, 1]`, `b = [1, 2, 3]`, `m = 4`

**Output:** `7`

**Explanation:** The optimal types to buy are-    

1. Choose i = 1. This is the first purchase of this type of item, so j = 1. The first item costs a[1] + (1 - 1) * b[i] = 1 + (1 - 1) * 2 = 1.

2. Choose i = 2. Again, it is the first purchase of this type so j = 1. The second item costs 1 + (1 - 1) * 3 = 1.

3. Choose i = 0 which costs 2 + (1 - 1) * 1 = 2.

4. When a second unit of any type is purchased, j = 2 for that transaction. The costs of a second units of each item are:
a. a[0] costs a[0] + (2 - 1) * b[0] = 2 + 1*1 = 3
b. a[1] costs 1 + 1*2 = 3
c. a[2] costs 1 + 1*3 = 4
d. Choose either a[0] or a[1] since they cost less.

The total cost to purchase is 1 + 1 + 2 + 3 = 7.

## Constraints

- `1 <= n <= 10^5`
- `1 <= a[i], b[i] <= 10^5`
- `1 <= m <= 10^5`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
