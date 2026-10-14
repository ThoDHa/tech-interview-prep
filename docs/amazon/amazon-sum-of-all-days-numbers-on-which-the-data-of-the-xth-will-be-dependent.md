# [Sum of All Days Numbers on Which the Data of the Xth Will Be Dependent](https://www.fastprep.io/problems/amazon-sum-of-all-days-numbers-on-which-the-data-of-the-xth-will-be-dependent)

**Medium** | **NN minutes** | **Math**

Data analysts at Amazon are analyzing time series data. It was concluded that the data of the nth item was dependent on the data of the some xth day if there is a positive integer k such that the floor (n/k) = x where floor(z) represents the largest integer less than or equal to z.



Given n, find the sum of all the days numbers on which the data of the xth (0 ≤ x ≤ n) will be dependent.


Function Description 
Complete the function sumOfAllDaysNumbers in the editor.



sumOfAllDaysNumbers has the following parameter:



int n: the nth item
Returns 
int: the sum of all the days numbers on which the data of the xth will be dependent

## Examples

### Example 1

**Input:** `n = 5`

**Output:** `8`

**Explanation:** For n = 5, the days on which the data of the xth will be dependent are calculated as follows:



x   k   floor(n/k)  
0   6   0  
1   5   1  
2   2   2  
3   does not exist -  
4   does not exist -  
5   1   5  



The sum of all days numbers is 0 + 1 + 2 + 5 = 8.

## Constraints

- `🐰`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
