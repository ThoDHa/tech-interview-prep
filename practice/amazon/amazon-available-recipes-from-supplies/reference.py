"""Available Recipes from Initial Supplies — https://www.fastprep.io/problems/amazon-available-recipes-from-supplies

Write-up & approaches: ../../../docs/amazon/amazon-available-recipes-from-supplies.md

Reference implementation of the write-up's recommended Topological
Release Queue solution. Your own attempt lives in solution.py.

  uv run python amazon/amazon-available-recipes-from-supplies/reference.py  # debug one case (see below)
  uv run pytest amazon/amazon-available-recipes-from-supplies/              # run the test sets
"""

from collections import deque
from typing import DefaultDict, List

from harness import pick_case


class Solution:
    def findAvailableRecipes(self, recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:
        """Return every recipe that can eventually become available, in input order.

        A recipe becomes available the moment its last outstanding
        ingredient does, and making it available can release its
        dependents, so the computation is a topological release: each
        recipe counts the ingredients that are not already supplies,
        fully available recipes enter a queue, and completing a recipe
        decrements the outstanding count of every dependent that
        referenced it by name. Ingredient names that are neither
        supplies nor recipes sit in the outstanding counts forever and
        hold their recipes back. The queue order is deliberately
        discarded: the answer is reported in the input order of
        `recipes`, exactly as the statement requires.

        Args:
            recipes: Distinct recipe names.
            ingredients: ingredients[i] lists the distinct names
                recipes[i] needs; a name may be a supply, another
                recipe, or permanently unavailable.
            supplies: Distinct available names, none of them recipe
                names.

        Returns:
            The completable recipes in the original order of `recipes`.

        Time:  O(recipes + supplies + references): every name is set-
            probed once and every reference is decremented at most once.
        Space: O(recipes + references): the outstanding counts, the
            reverse adjacency over recipe-named references, and the
            availability flags.
        """
        available = set(supplies)
        recipe_names = set(recipes)

        outstanding: List[int] = []
        dependents: DefaultDict[str, List[int]] = DefaultDict(list)
        for index, (name, needed) in enumerate(zip(recipes, ingredients)):
            count = 0
            for ingredient in needed:
                if ingredient in available:
                    continue
                count += 1
                if ingredient in recipe_names:
                    dependents[ingredient].append(index)
            outstanding.append(count)

        ready = deque(index for index, count in enumerate(outstanding) if count == 0)
        completed = [False] * len(recipes)
        while ready:
            index = ready.popleft()
            completed[index] = True
            for dependent in dependents[recipes[index]]:
                outstanding[dependent] -= 1
                if outstanding[dependent] == 0:
                    ready.append(dependent)

        return [name for index, name in enumerate(recipes) if completed[index]]


if __name__ == "__main__":
    # Debug playground: set a breakpoint in findAvailableRecipes above, then run this file.
    case = pick_case(__file__, "example_1")
    result = Solution().findAvailableRecipes(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")
