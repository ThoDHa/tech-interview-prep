# [Available Recipes from Initial Supplies](https://www.fastprep.io/problems/amazon-available-recipes-from-supplies)

**Medium** | **NN minutes** | **Graph, Topological Sort, Hash Table**

You are given distinct recipe names in recipes. Row ingredients[i] lists everything needed to make recipes[i]. An ingredient can be an initial supply, another recipe, or a name that is unavailable.

Every initial supplies item is available in unlimited quantity. Whenever every ingredient of a recipe is available, that recipe also becomes available in unlimited quantity and can be used by other recipes. A recipe with no ingredients is available immediately. Recipe-to-recipe dependencies form a directed acyclic graph.

Return every recipe that can eventually become available, in the original order of recipes. Ingredients are never consumed. Initial supplies have distinct names and do not include recipe names.

## Examples

### Example 1

**Input:** `recipes = ["bread","sandwich"]`, `ingredients = [["flour","water"],["bread","ham"]]`, `supplies = ["flour","water","ham"]`

**Output:** `["bread","sandwich"]`

**Explanation:** Bread becomes available first, so it can then enable sandwich.

### Example 2

**Input:** `recipes = ["cake","icing","tea"]`, `ingredients = [["flour","icing"],["sugar"],["water"]]`, `supplies = ["sugar","water"]`

**Output:** `["icing","tea"]`

**Explanation:** Icing and tea are available, but missing flour keeps cake unavailable.

### Example 3

**Input:** `recipes = ["meal","base"]`, `ingredients = [["base"],[]]`, `supplies = []`

**Output:** `["meal","base"]`

**Explanation:** The empty base recipe is immediately available. Return the completed recipes in input order, even though base is enabled first.

## Constraints

- `0 <= recipes.length <= 200 and ingredients.length == recipes.length.`
- `0 <= supplies.length <= 1000.`
- `Names contain from 1 through 20 lowercase ASCII letters.`
- `Every ingredient row contains distinct names; the total number of ingredient references is at most 10000.`
- `Recipe names and supply names are distinct within each array and no recipe name is an initial supply.`
- `The graph formed by references from one recipe to another is acyclic.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
