# [Min Energy Cost](https://www.fastprep.io/problems/amazon-minimum-energy-cost)

**Medium** | **NN minutes** | **Dynamic Programming, Array**

Janet has N bags in a row. Each bag has a weight (Wi). Janet can collect bags from either the leftmost or rightmost position, but there are energy costs:


The cost of collecting a bag is the bag's weight (Wi) multiplied by X (if collecting from the left) or Y (if collecting from the right).If you are collecting a bag consecutively from the same side twice in a row, then there is an additional cost of El (if collected from the left side consecutively) or Er (if collected from the right side consecutively).
Find the strategy that minimizes the total energy cost Janet spends to collect all the bags and display the minimum cost Bob has to pay.



Input Format



The first line of input contains five space-separated integers: N (number of bags), X, Y, El, Er (energy costs)



The second line of input contains N space-separated integers representing the weight of each bag (Wi).



Output Format



Display the minimum energy cost expenditure for Bob.

## Examples

### Example 1

**Input:** `weights = [42, 3, 99]`, `X = 4`, `Y = 4`, `El = 19`, `Er = 1`

**Output:** `576`

**Explanation:** 🐡 🦚 🦤 🐌 🦦

## Constraints

- `:O`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
