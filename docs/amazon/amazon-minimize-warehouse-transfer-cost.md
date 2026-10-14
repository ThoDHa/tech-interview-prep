# [Minimize Warehouse Transfer Cost](https://www.fastprep.io/problems/amazon-minimize-warehouse-transfer-cost)

**Hard** | **NN minutes** | **Array, Prefix Sum, Greedy**

Source note: Confirmed on 2026-06-23 as a duplicate of Find Minimum Cost. The linked version is more complete and is the recommended practice version.

Special thanks: A solution contributor helped identify the duplicate.


Basically, Amazon has its warehouses lined up in a circle, you can start from any warehouse move in either clockwise or anti-clockwise direction, the direction must remain the same throughout the remaining moves.



Each warehouse stores some items. The goal is to collect excess items from some warehouses and deliver them to others need them, so that each warehouse stores the same number of items in the end (guaranteed).



The distance between 2 adjacent warehouses is 1, and the cost of each product transfer is the distance the product is moved.



Complete the function minimizeWarehouseTransferCost in the editor.



minimizeWarehouseTransferCost has the following parameter:



int[] warehouses: an array of integers representing the number of items in each warehouse

long integer: the minimum cost to make all warehouses store the same number of items

## Examples

### Example 1

**Input:** `warehouses = [6, 6, 6, 3, 4]`

**Output:** `7`

**Explanation:** The source compares two possible routes with costs 7 and 8. Since the problem asks for the minimum cost, the example output is 7.


We can optimally start from the first warehouse and collect 1 item, repeat the same for the following 2 warehouses and deliver 2 to the 4th warehouse and 1 to the 5th warehouse. In the end, each warehouse has 5 items and the total cost is 1 + 2 + 3 + 1 = 7. This is just a possible clockwise move, the optimal cost should consider the anti-clockwise direction as well and return the minimum cost.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-minimize-warehouse-transfer-cost; fill them in. -->

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
