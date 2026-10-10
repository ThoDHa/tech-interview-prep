# [Environment Variable Store and Substitution](https://www.fastprep.io/problems/amazon-environment-variable-substitution)

**Medium** | **NN minutes** | **String, Hash Table, Simulation**

Process a sequence of environment-variable operations:

["SET", key, value] stores or overwrites a value.["GET", key] emits the value or NULL when missing.["PARSE", text] emits text after replacing every complete %KEY% placeholder whose key exists. Missing placeholders remain unchanged.Substitution is one pass: replacement values are not expanded again during the same operation.

## Examples

### Example 1

**Input:** `operations = [["SET","NAME","Tom"],["PARSE","Hello I am %NAME%"]]`

**Output:** `["Hello I am Tom"]`

**Explanation:** The stored NAME value replaces its placeholder.

### Example 2

**Input:** `operations = [["GET","MISSING"],["PARSE","%MISSING%"]]`

**Output:** `["NULL","%MISSING%"]`

**Explanation:** Missing GET and PARSE have distinct deterministic outputs.

## Constraints

- `1 <= operations.length <= 10^5.`
- `Keys contain letters, digits, or underscores and are nonempty.`
- `Each operation row has the required fields.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and solutions land
     on the solutions branch later. See ../_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
