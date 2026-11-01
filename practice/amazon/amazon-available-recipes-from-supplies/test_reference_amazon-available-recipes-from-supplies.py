"""Reference-parametrized gauntlet for Available Recipes from Supplies.

The statement fixes the output order (the original order of
`recipes`), so the comparison is plain `==` with no canonicalization;
the gauntlet pins that order with cases whose enablement order differs
from their input order. Every expectation in cases_full.json is
oracle-derived, never hand-computed and never recorded from this
reference: the oracle is a repeated availability sweep straight from
the statement's definition (any recipe whose ingredients are all
available joins the supply set; sweep until a full pass changes
nothing, then report the available recipes in input order), which
shares no mechanism with the reference's topological release queue.
The band covers the statement's named corners: the empty recipe list
(the `0 <= recipes.length` bound), the empty-ingredient recipe
(immediately available, with and without supplies), every-ingredient-a-
supply recipes, permanently unavailable names holding recipes back,
blocked recipes blocking their dependents, input order differing from
enablement order, reused supplies across rows, and a seeded random
band of acyclic reference graphs. The statement's scale corners (200
recipes, 10000 total references) stay out of the JSON and are
constructed here, where the expectations follow from the construction:

- test_constructed_release_chain_of_200_recipes_at_the_reference_cap:
  recipes r000..r199 where r000 needs 49 supply fillers and each later
  recipe needs its predecessor plus 49 supply fillers, 200 x 49 + 199
  = 9999 references, just under the statement's 10000 cap. Every
  recipe's needs complete in chain order, so all 200 come back in
  input order.
- test_constructed_ghost_break_holds_the_chain_suffix: the same chain
  with recipe r013 also referencing the unavailable name "ghost",
  lifting the total to exactly 10000 references. r013 never completes,
  every later recipe waits on its predecessor forever, so exactly
  r000..r012 come back, in input order.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")

CHAIN_RECIPE_COUNT = 200
FILLERS_PER_RECIPE = 49
GHOST_BREAK_INDEX = 13


def _ids(cases):
    return [case["id"] for case in cases]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().findAvailableRecipes, case)


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


def _chain_ingredients(ghost_index=None):
    fillers = [f"f{filler:03d}" for filler in range(FILLERS_PER_RECIPE)]
    ingredients = []
    for index in range(CHAIN_RECIPE_COUNT):
        row = list(fillers)
        if index > 0:
            row.append(f"r{index - 1:03d}")
        if ghost_index is not None and index == ghost_index:
            row.append("ghost")
        ingredients.append(row)
    return ingredients


def test_constructed_release_chain_of_200_recipes_at_the_reference_cap():
    recipes = [f"r{index:03d}" for index in range(CHAIN_RECIPE_COUNT)]
    ingredients = _chain_ingredients()
    supplies = [f"f{filler:03d}" for filler in range(FILLERS_PER_RECIPE)]
    assert sum(len(row) for row in ingredients) == CHAIN_RECIPE_COUNT * FILLERS_PER_RECIPE + CHAIN_RECIPE_COUNT - 1
    assert reference.Solution().findAvailableRecipes(recipes, ingredients, supplies) == recipes


def test_constructed_ghost_break_holds_the_chain_suffix():
    recipes = [f"r{index:03d}" for index in range(CHAIN_RECIPE_COUNT)]
    ingredients = _chain_ingredients(ghost_index=GHOST_BREAK_INDEX)
    supplies = [f"f{filler:03d}" for filler in range(FILLERS_PER_RECIPE)]
    expected = [f"r{index:03d}" for index in range(GHOST_BREAK_INDEX)]
    assert reference.Solution().findAvailableRecipes(recipes, ingredients, supplies) == expected
