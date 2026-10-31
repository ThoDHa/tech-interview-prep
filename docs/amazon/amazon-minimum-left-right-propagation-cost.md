# [Minimum Cost of Left and Right Propagation](https://www.fastprep.io/problems/amazon-minimum-left-right-propagation-cost)

**Medium** | **NN minutes** | **Array, Greedy**

You are given a positive integer array values. You may perform either propagation operation any number of times and in any order:

Choose index i and propagate left: replace every element before i with values[i]. This costs i * values[i].Choose index i and propagate right: replace every element after i with values[i]. This costs (n - 1 - i) * values[i].Return the minimum total cost needed to make every array element equal. You may perform zero operations when the array is already uniform.

## Examples

### Example 1

**Input:** `values = [5,2,4]`

**Output:** `4`

**Explanation:** Keep the middle value 2, propagate it left for cost 2, and propagate it right for another cost 2.

### Example 2

**Input:** `values = [1,1,2,1]`

**Output:** `2`

**Explanation:** Keep the first run of two 1s and propagate right from index 1 for cost 2.

### Example 3

**Input:** `values = [5,1,1,2,1,1]`

**Output:** `4`

**Explanation:** Keep the run of two 1s at indices 1 and 2. Propagate left from index 1 for cost 1, then right from index 2 for cost 3. The total is 4; no original equal-value run gives a lower cost.

## Constraints

- `1 <= values.length <= 100000`
- `1 <= values[i] <= 10^9`
- `The answer fits in a signed 64-bit integer.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
