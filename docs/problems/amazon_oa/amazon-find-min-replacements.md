# [Find Replacement](https://www.fastprep.io/problems/amazon-find-min-replacements)

**Hard** | **NN minutes** | **Array, Greedy**

In Amazon's distribution network, there are several drones with varying capacities, ranging from 1 to 10^9. Each j-th drone has a carrying capacity of j. The company needs to dispatch n packages, where the weight of the i-th package is given by pack[i].

During peak delivery times, only two drones are available to transport the packages, and they must alternate in their duties. This means that if Drone 1 handles the i-th package, Drone 2 must handle the (i + 1)-th package, and so on.

However, there may be challenges if the drones cannot handle certain package weights (i.e., some packages may be too heavy for a drone). To address this, Amazon can replace certain packages with others of a different weight to ensure that all packages are successfully delivered.

Given the ability to choose any two drones, your task is to determine the minimum number of replacements needed to ensure that all packages can be successfully delivered.

Complete the function findMinReplacements in the editor.

findMinReplacements has the following parameter:

int pack[n]: an array representing the weights of packages.int: the minimum number of replacements needed.

## Examples

### Example 1

**Input:** `parcels = [3, 1, 3, 2]`

**Output:** `1`

**Explanation:** With the provided package weights [3, 1, 3, 2], the two drones won't be able to alternate in handling the packages. To resolve this, the fourth package, which weighs 2, can be replaced with a package of weight 1. This results in the adjusted weights pack = [3, 1, 3, 1]. Now, two drones with carrying capacities of 3 and 1 can handle the packages alternately. Therefore, only one replacement is needed. Thus, the answer is 1.

### Example 2

**Input:** `parcels = [1, 1, 1, 1]`

**Output:** `2`

## Constraints

- `Each chosen drone has a carrying capacity in the range 1 to 10^9.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
