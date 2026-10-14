# [Ordered Confirguration](https://www.fastprep.io/problems/amazon-orda-layout)

**Medium** | **NN minutes** | **String, Sorting, Parsing**

Note - Feel free to checkout the source image for the original statement :) 🐳



A barcode scanner's settings are stored in a backend system as a single string of configurations, each encoded with a four-digit ordinal index followed by a configuration value, all separated by '|'. To set up the scanner correctly, the client needs to request this string and present the configurations in the proper sequence. Your task is to ensure the validity of this configuration string and return the configurations in the right order. The validation criteria include ensuring that configurations are separated by '|', indices are sequential and unique without any gaps, configuration values are alphanumeric and unique, and there are no duplicate ordinal indices. If the string fails these checks, the function should return ["Invalid configuration"].

## Examples

### Example 1

**Input:** `layout = "0001LAJ5KBX9H8|0003UKURNK403F|0002MO6K1Z9WFA|0004OWRXZFMS2C"`

**Output:** `["LAJ5KBX9H8", "MO6K1Z9WFA", "UKURNK403F", "OWRXZFMS2C"]`

**Explanation:** The configuration string contains several values, each prefixed with a four-digit order number. For instance, "LAJ5KBX9H8" with the prefix "0001" is listed first, while "MO6K1Z9WFA" is marked with "0002" and therefore comes second. Even though "UKURNK403F" appears second in the string, its prefix "0003" places it third in the final sequence. Lastly, "OWRXZFMS2C" has the prefix "0004" and is listed fourth.

### Example 2

**Input:** `layout = "000533B8XLD2EZ|0001DJ2M2JBZZR|0002Y9YK0A7MYO|0004IKDJCAPG5Q|0003IBHMH59SBO"`

**Output:** `["DJ2M2JBZZR", "Y9YK0A7MYO", "IBHMH59SBO", "IKDJCAPG5Q", "33B8XLD2EZ"]`

**Explanation:** No explanation for now

### Example 3

**Input:** `layout = "0002f7c22e7904|000176a3a4d214|000305d29f4a4b"`

**Output:** `["76a3a4d214", "f7c22e7904", "05d29f4a4b"]`

**Explanation:** No explanation for now :)

### Example 4

**Input:** `layout = "0002f7c22e7904|000176a3a4d214|000205d29f4a4b"`

**Output:** `["Invalid configuration"]`

**Explanation:** ..

## Constraints

- `1 ≤ orders ≤ 9999`
- `1 ≤ orders(configuration) ≤ 9999`
- `Order values may not be unique or complete`
- `Configuration values are not always unique, the same configuration may appear in multiple configuration steps`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
