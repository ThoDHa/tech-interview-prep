# [Evaluate Division](https://www.fastprep.io/problems/amazon-evaluate-division)

**Medium** | **NN minutes** | **Graph, Depth First Search, Breadth First Search**

You are given variable pairs equations and positive real numbers values. For every index i, equations[i] = [a, b] and values[i] mean a / b = values[i].

For each pair in queries, return the requested quotient. Return -1.0 when it cannot be determined. The equations are valid and mutually consistent, and a variable absent from all equations is undefined even when queried against itself.

The query stream can be very large and can repeat the same ordered pairs. Reuse previously resolved relationships or preprocess component weights so repeated calls do not traverse the full graph again.

## Examples

### Example 1

**Input:** `equations = [["a","b"],["b","c"]]`, `values = [2.0,3.0]`, `queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]`

**Output:** `[6.0,0.5,-1.0,1.0,-1.0]`

**Explanation:** Compose or reverse known ratios; undefined variables produce -1.0.

### Example 2

**Input:** `equations = [["a","b"],["b","c"],["bc","cd"]]`, `values = [1.5,2.5,5.0]`, `queries = [["a","c"],["c","b"],["bc","cd"],["cd","bc"]]`

**Output:** `[3.75,0.4,5.0,0.2]`

**Explanation:** Products along graph paths evaluate indirect ratios.

### Example 3

**Input:** `equations = [["a","b"]]`, `values = [0.5]`, `queries = [["a","b"],["b","a"],["a","c"],["x","y"]]`

**Output:** `[0.5,2.0,-1.0,-1.0]`

**Explanation:** The reverse edge uses the reciprocal; unknown variables have no path.

## Constraints

- `1 <= equations.length <= 200000`
- `values.length == equations.length`
- `0.0 < values[i] <= 10^9`
- `1 <= queries.length <= 200000`
- `Variable names contain one to five lowercase letters or digits.`
- `The equations contain no contradictions and no division by zero.`
- `Every quotient implied between two connected variables is between 10^-100 and 10^100, inclusive, so all component weights and requested results are finite.`
- `Results within 10^-5 of the expected value are accepted.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
