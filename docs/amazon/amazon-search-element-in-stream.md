# [Search for an Element in a Stream](https://www.fastprep.io/problems/amazon-search-element-in-stream)

**Medium** | **NN minutes** | **Hash Table, Tree, Design**

Values arrive one at a time in a stream. At any moment, you may be asked whether a given value has already arrived.

You are given two arrays of the same length, operations and values. Process them from left to right. At index i:

If operations[i] is "add", the value values[i] arrives in the stream.
If operations[i] is "search", check whether values[i] arrived at an earlier index.

Return a boolean array with one entry for each "search", in the order the searches appear. An entry is true if that value arrived before the search, and false otherwise. A value may arrive more than once; a repeat arrival changes nothing. If there are no searches, return an empty array.

## Examples

### Example 1

**Input:** `operations = ["add","add","search","search","add","search"]`, `values = [5,3,3,7,7,7]`

**Output:** `[true,false,true]`

**Explanation:** The values 5 and 3 arrive first, so the search for 3 returns true. The value 7 has not arrived yet, so the next search returns false. After 7 arrives, searching for it again returns true.

## Constraints

<!-- Constraints not parseable from FastPrep for amazon-search-element-in-stream; fill them in. -->

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
