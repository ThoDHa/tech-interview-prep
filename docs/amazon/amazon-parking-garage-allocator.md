# [Parking Garage Allocator](https://www.fastprep.io/problems/amazon-parking-garage-allocator)

**Medium** | **NN minutes** | **Array, Simulation, String**

Manage spaceCount parking spaces. Each operation is "PARK size" or "LEAVE start size". A park request occupies the leftmost available run of the requested size and contributes its starting index, or -1 when no run fits. A leave operation frees the stated valid occupied range and contributes no output.

Sizes are 1, 2, or 3.

## Examples

### Example 1

**Input:** `spaceCount = 6`, `operations = ["PARK 2","PARK 3","LEAVE 0 2","PARK 1"]`

**Output:** `[0,2,0]`

**Explanation:** The final request reuses the leftmost freed space.

### Example 2

**Input:** `spaceCount = 2`, `operations = ["PARK 3","PARK 2"]`

**Output:** `[-1,0]`

**Explanation:** The oversized request fails without changing state.

## Constraints

- `1 <= spaceCount, operations.length <= 100000.`
- `Every leave operation refers to a currently occupied range.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
