# [About Mortgage](https://www.fastprep.io/problems/amazon-maximum-number-of-days-to-survive)

**Medium** | **NN minutes** | **Greedy, Sorting**

A lender lent money to a borrower, each day a different lender lent the money to the borrower.
The borrower borrowed money on the jth day should payback on the (j+1)th day to maintain good credit and avoid defaulting.
The borrower can payback the jth day loan from the (j+1)th day's borrowed money and can use the leftover money on that day.
Find the maximum number of days the borrower can survive before defaulting.



lender[i] represents the ith lending amount, and payback[i] represents the ith payback amount.

## Examples

### Example 1

**Input:** `lender = [4, 6, 1, 8]`, `payback = [7, 10, 3, 9]`

**Output:** `3`

**Explanation:** Choose lender -> 1, so payback is 3.Choose lender -> 4, repay previous payback 3, hence remaining 4-3 = 1 (borrower spends it), the current Payback is 7.Choose lender -> 8, repay previous payback 7, hence remaining 8-7 = 1 (borrower spends it), the current Payback is 9.Left with lender -> 6, cannot repay previous payback which is 9, 9 > 6 hence default.
So the borrower can survive 3 days.

### Example 2

**Input:** `lender = [2, 1, 5]`, `payback = [2, 2, 5]`

**Output:** `3`

**Explanation:** The borrower can pay back each day's loan with the next day's borrowed money without any leftover, thus surviving for all 3 days.

### Example 3

**Input:** `lender = [1, 1, 1, 2]`, `payback = [2, 2, 2, 3]`

**Output:** `2`

**Explanation:** Choose lender -> 1, so payback is 2.Choose lender -> 1, repay previous payback 2, hence no remaining (borrower spends it), the current Payback is 2.Left with lender -> 1, cannot repay previous payback which is 2, 2 > 1 hence default.
So the borrower can survive 2 days.

## Constraints

- `TO-DO`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
