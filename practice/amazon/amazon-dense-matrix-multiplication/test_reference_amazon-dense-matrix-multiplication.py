"""Reference-parametrized gauntlet for Dense Matrix Multiplication.

The generator-emitted test module replays solution.py against cases.json
and stays untouched; this module replays the write-up's recommended
Row-Wise Loop Reorder reference against cases_full.json. Per the F8
ruling for literal-procedure statements, the oracle is an independently
coded implementation of the same procedure: right is transposed and
every output cell is a zip dot product of a left row with a right
column, which shares no loop mechanism with the reference's in-place
accumulator walks. Expectations were frozen from that oracle and the
scratch script deleted; the product is a deterministic matrix, so the
comparison is plain `==` with no canonicalization.

The gauntlet covers the statement's named corners at eye-auditable
sizes: the page's three examples, a single-cell product, the identity
matrix on the left and on the right, an all-zero product, a zero row in
left, a zero column in right, negatives multiplying negatives, mixed
signs, the +-100 element extremes dotting to the largest magnitude the
int32 guarantee covers and cancelling to zero, row and column vectors
against a square, a wide rectangular mixed-sign product, the k = 1
outer-product column, and a zero buried in the inner dimension. Scale
corners live here as constructed cases per the Testing Strategy rule
that length corners are constructible or synthesized, never serialized
bulk; three derive their expected outcome from the construction (an
identity product, and both k = 1 or m = n = 1 shapes at the 64 bounds
whose constant-value products are arithmetic), and the fourth, the
64 by 64 extremes square, re-derives its expectation through the same
transpose-dot mechanism as the frozen oracle, re-typed below, never
through the reference:

- test_constructed_sixty_four_square_extremes: two 64 by 64 matrices
  at the +-100 element bound with checkerboard and modulo patterns,
  cross-checked against the in-module transpose-dot oracle.
- test_constructed_row_times_column_at_bounds: 1 by 64 times 64 by 1
  at the bounds, 64 copies of 100 * -100 = -640000, the statement's
  stated worst partial sum.
- test_constructed_column_times_row_at_bounds: 64 by 1 times 1 by 64,
  the k = 1 outer product at the bounds, every cell -100 * 100.
- test_constructed_identity_sixty_four: the 64 by 64 identity times an
  alternating-sign matrix must return that matrix unchanged.

Discrimination record, naming the mutant classes the serialized cases
catch, each claim verified by running the mutant against every case:
swapping the operand roles (computing right * left) is caught by
example_1, example_2, example_3, zero_row_in_left, zero_column_in_right,
negative_times_negative, mixed_signs, element_extremes_dot,
element_extremes_cancel, row_vector_times_square,
square_times_row_vector, wide_rect_mixed, inner_dim_one_column,
zero_inner_middle, constructed_row_times_column_at_bounds, and
constructed_column_times_row_at_bounds (the identity and all-zero cases
cannot catch it because A * I = I * A and 0 * M = M * 0); reading
right[j][t] instead of right[t][j] is caught by example_1, example_2,
example_3, identity_left, zero_row_in_left, zero_column_in_right,
negative_times_negative, mixed_signs, element_extremes_dot,
element_extremes_cancel, row_vector_times_square,
square_times_row_vector, wide_rect_mixed, zero_inner_middle,
constructed_row_times_column_at_bounds, and
constructed_column_times_row_at_bounds; assigning
left_value * right_row[j] instead of accumulating it (keeping only the
last inner index's product) is caught by example_1, example_3,
identity_left, identity_right, zero_row_in_left, zero_column_in_right,
negative_times_negative, mixed_signs, element_extremes_dot,
element_extremes_cancel, row_vector_times_square,
square_times_row_vector, wide_rect_mixed, zero_inner_middle,
constructed_sixty_four_square_extremes,
constructed_row_times_column_at_bounds, and
constructed_identity_sixty_four (the k = 1 cases cannot catch it
because one product needs no accumulation); skipping inner index t = 0
is caught by every case except all_zeros, whose product stays zero
under any inner-index subset (the k = 1 cases lose their only product,
the rest lose a real summand); aliasing the
result rows ([[0] * columns] * rows, every row write sharing one list)
is caught by example_1, example_2, identity_left, identity_right,
zero_row_in_left, zero_column_in_right, negative_times_negative,
mixed_signs, square_times_row_vector, wide_rect_mixed,
inner_dim_one_column, zero_inner_middle,
constructed_column_times_row_at_bounds, and
constructed_identity_sixty_four (single-row products cannot catch it
because one row aliases nothing); and reading left[i][j] inside the
innermost loop instead of the hoisted scalar left[i][t] is caught by
example_1, example_2, example_3, identity_left, zero_row_in_left,
zero_column_in_right, negative_times_negative, mixed_signs,
element_extremes_dot, element_extremes_cancel, row_vector_times_square,
square_times_row_vector, wide_rect_mixed, zero_inner_middle,
constructed_sixty_four_square_extremes,
constructed_column_times_row_at_bounds, and
constructed_identity_sixty_four.
"""

import pytest

from harness import load_cases, load_solution

FULL = load_cases(__file__, "cases_full.json")

reference = load_solution(__file__, "reference.py")

SIDE_BOUND = 64
ELEMENT_BOUND = 100


class TransposeDotOracle:
    """The frozen oracle's mechanism: transpose right, zip dot products."""

    @staticmethod
    def multiply(left, right):
        right_columns = list(zip(*right))
        return [[sum(a * b for a, b in zip(left_row, right_column)) for right_column in right_columns]
                for left_row in left]


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", FULL, ids=_ids(FULL))
def test_reference_cases(case):
    _check(reference.Solution().multiplyMatrices, case)


def test_constructed_sixty_four_square_extremes():
    left = [[ELEMENT_BOUND if (i + j) % 2 == 0 else -ELEMENT_BOUND for j in range(SIDE_BOUND)] for i in range(SIDE_BOUND)]
    right = [[-ELEMENT_BOUND if (i * j) % 3 == 0 else ELEMENT_BOUND for j in range(SIDE_BOUND)] for i in range(SIDE_BOUND)]
    assert reference.Solution().multiplyMatrices(left, right) == TransposeDotOracle.multiply(left, right)


def test_constructed_row_times_column_at_bounds():
    left = [[ELEMENT_BOUND] * SIDE_BOUND]
    right = [[-ELEMENT_BOUND]] * SIDE_BOUND
    assert reference.Solution().multiplyMatrices(left, right) == [[-SIDE_BOUND * ELEMENT_BOUND * ELEMENT_BOUND]]


def test_constructed_column_times_row_at_bounds():
    left = [[-ELEMENT_BOUND]] * SIDE_BOUND
    right = [[ELEMENT_BOUND] * SIDE_BOUND]
    assert reference.Solution().multiplyMatrices(left, right) == [[-ELEMENT_BOUND * ELEMENT_BOUND] * SIDE_BOUND] * SIDE_BOUND


def test_constructed_identity_sixty_four():
    identity = [[1 if i == j else 0 for j in range(SIDE_BOUND)] for i in range(SIDE_BOUND)]
    alternating = [[ELEMENT_BOUND if (i + j) % 2 == 0 else -ELEMENT_BOUND for j in range(SIDE_BOUND)] for i in range(SIDE_BOUND)]
    assert reference.Solution().multiplyMatrices(identity, alternating) == alternating
