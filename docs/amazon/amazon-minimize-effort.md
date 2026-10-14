# [Minimize Effort](https://www.fastprep.io/problems/amazon-minimize-effort)

**Medium** | **NN minutes** | **Array, Math, Greedy**

Source note: 2026-07-17 — The EffiBin era is over. Long live Minimum Total Batch Expense. The problem has returned to the Circle of Source Fidelity, with its terminology, function signature, example, and visible requirements fully aligned with the latest official source.


With Amazon's new innovative OptiBatch Kit users can effortlessly optimize the arrangement of their processing batches. This kit is designed to minimize the overall expense needed for efficient processing.



The process starts with an array of batches, and the objective is to reduce the total expense required. The expense is the sum of expenses needed for each batch.



Formally, given an array expense of size p, utilizing the OptiBatch Kit, users can perform operations on the array. In each operation, the user chooses two positions a and b, such that the expense of the batch at position a (expense[a]) is divisible by the expense of the batch at position b (expense[b]). When this condition is satisfied, the expense of batch a can be updated to equal the expense of batch b. This operation can be repeated as many times as possible, on different batches or positions.



An integer a is divisible by another integer b if a can be divided by b exactly, with nothing left over; for example, 6 is divisible by 3, while 7 is not.



Find the minimum total expense after applying some (possibly zero) number of operations.



Complete the function determineMinimalExpense in the editor below.


determineMinimalExpense has the following parameter:


int expense[p]: the expense array, where expense[a] is the expense needed for each batch

long: the minimum total expense after applying some (possibly zero) number of operations

## Examples

### Example 1

**Input:** `expense = [3, 6, 2, 5, 25]`

**Output:** `17`

**Explanation:** $24

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-minimize-effort; fill them in. -->

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
