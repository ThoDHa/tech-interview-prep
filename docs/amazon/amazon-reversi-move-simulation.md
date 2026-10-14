# [Apply a Reversi Move](https://www.fastprep.io/problems/amazon-reversi-move-simulation)

**Medium** | **NN minutes** | **Array, Matrix, Simulation**

Given a Reversi board board, a zero-based target cell row, col, and a player player equal to B or W, apply exactly one move.

A direction captures pieces when one or more consecutive opponent pieces start next to the target and are followed, in that same direction, by one of the current player's pieces. A legal move places the player's piece and flips every captured line in all eight directions.

If the target is occupied or no direction captures an opponent piece, return the original board unchanged. Do not modify the input strings.

## Examples

### Example 1

**Input:** `board = ["....",".WB.","...."]`, `row = 1`, `col = 3`, `player = "W"`

**Output:** `["....",".WWW","...."]`

**Explanation:** The new white piece at column 3 brackets the black piece with the existing white piece at column 1.

### Example 2

**Input:** `board = ["..B..","..W..","BW.WB","..W..","..B.."]`, `row = 2`, `col = 2`, `player = "B"`

**Output:** `["..B..","..B..","BBBBB","..B..","..B.."]`

**Explanation:** The move captures one white piece in each cardinal direction.

### Example 3

**Input:** `board = ["...","...","..."]`, `row = 1`, `col = 1`, `player = "B"`

**Output:** `["...","...","..."]`

**Explanation:** No opponent line is bracketed, so the move is invalid and the board remains unchanged.

## Constraints

- `1 <= board.length, board[i].length <= 50.`
- `Every row has the same length and contains only ., B, or W.`
- `0 <= row < board.length and 0 <= col < board[0].length.`
- `player is B or W.`

## Solutions

### Optimistic Flip with Undo

#### Derivation

The most direct reading of the move is the one a Reversi app would actually perform: place the piece immediately, then walk outward in each of the eight directions flipping opponent pieces as they pass, and deal with legality afterwards. A direction is a capture when the run of opponent pieces stops on one of the current player's pieces; when it stops on anything else (an empty cell, the board edge), the flips made in that direction were premature and must be taken back:

1. Reject the move up front when the target cell `board[row][col]` is already
   occupied, returning the original `board` unchanged.
2. Copy every row of `board` into `flipped`, lists of single characters, and
   set `flipped[row][col]` to `player`.
3. For each `(row_step, col_step)` direction, walk from the target counting
   consecutive `opponent` pieces and flipping each to `player` in `flipped`.
4. Inspect the first cell after the run: when it holds `player` (and exists),
   the direction captured and the flips stand; otherwise undo the run by
   walking it again and restoring `opponent`.
5. Return the original `board` when no direction captured; otherwise join
   every row of `flipped` back into strings.

#### Walkthrough

Let us play Example 1, `board = ["....",".WB.","...."]`, `row = 1`, `col = 3`, `player = "W"` (`opponent = "B"`), direction by direction. The target `(1, 3)` is empty, so the piece is placed first:

```text
place W at (1,3):   .WWW   <- the placed W plus the pre-existing W at (1,1)
```

Now each of the eight directions walks from `(1, 3)`:

```text
up (-1,0)    first cell (0,3) is "."   no opponent run, nothing flipped
down (1,0)   first cell (2,3) is "."   nothing flipped
left (0,-1)  (1,2) is "B": flip to W, run_length 1; next (1,1) is "W"
                                       -> bracketed, the flip stands
right (0,1)  (1,4) off the board      nothing flipped
(-1,-1)      (0,2) is "."             nothing flipped
(-1,1)       (0,4) off the board      nothing flipped
(1,-1)       (2,2) is "."             nothing flipped
(1,1)        (2,4) off the board      nothing flipped
```

Exactly one direction captured: the left run flipped the `B` at `(1, 2)`, bracketed by the `W` at `(1, 1)`. Every other direction either starts on a non-opponent cell or walks off the board, so no undo is ever needed. Joining the rows gives `["....", ".WWW", "...."]`, matching the expected Output for Example 1.

The undo path is what a single example cannot show. On the tailored row `"WB.B."` with `player = "W"` at `col = 2`, the left direction flips the `B` at column 1 and finds the bracketing `W` at column 0, but the right direction flips the `B` at column 3 and then hits the `"."` at column 4: that flip is undone, leaving `"WWWB."` rather than the illegal `"WWWW."`.

#### Solution

The code is the walkthrough: place first, flip runs outward, and restore the runs whose far end fails to bracket.

```python
from typing import List


class Solution:
    def applyReversiMove(self, board: List[str], row: int, col: int,
                         player: str) -> List[str]:
        if board[row][col] != '.':
            return board
        rows, cols = len(board), len(board[0])
        opponent = 'W' if player == 'B' else 'B'
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]

        flipped = [list(line) for line in board]
        flipped[row][col] = player
        captured_any = False
        for row_step, col_step in directions:
            walk_row, walk_col = row + row_step, col + col_step
            run_length = 0
            while (0 <= walk_row < rows and 0 <= walk_col < cols
                   and flipped[walk_row][walk_col] == opponent):
                flipped[walk_row][walk_col] = player
                run_length += 1
                walk_row += row_step
                walk_col += col_step
            bracketed = (run_length > 0 and 0 <= walk_row < rows
                         and 0 <= walk_col < cols
                         and flipped[walk_row][walk_col] == player)
            if bracketed:
                captured_any = True
                continue
            undo_row, undo_col = row + row_step, col + col_step
            for _ in range(run_length):
                flipped[undo_row][undo_col] = opponent
                undo_row += row_step
                undo_col += col_step

        if not captured_any:
            return board
        return ["".join(line) for line in flipped]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows × cols)`

Each of the 8 direction walks visits at most `max(rows, cols)` cells, and building or joining the board copy touches every cell once, so the total stays linear in the board size.

##### Space Complexity: `O(rows × cols)`

The `flipped` copy of the board dominates; the direction list and walk positions are constant.

#### Key Insights

- The board is at most 50 by 50, so every approach that respects the rules is fast; the game here is correctness, not speed.
- Placing the piece before checking capture legality is what forces the undo machinery; the bracket test must then look at the `flipped` copy, where the just-placed piece already sits.
- The bracket test needs three conditions together: a non-empty opponent run, a cell that exists after the run, and that cell holding `player`. Dropping the in-bounds test either raises an IndexError past the far edge or, through Python's negative indexing on the copied rows, silently reads the opposite edge of the board.
- Two hidden edge cases live in the statement's last sentence: an occupied target returns the board unchanged (the naive path would overwrite the occupant), and an illegal move must return the original list object, not a rebuilt copy of it.

### Validate-First Direction Scan

#### Derivation

The undo pass exists only because the first approach mutates the board before it knows the move is legal. Splitting the move into its two natural phases removes that hazard: scan all eight directions against the untouched `board` and record only the directions that truly bracket, then flip exactly those runs on a fresh copy. Nothing is ever written that might need reverting:

1. Reject an occupied `board[row][col]` immediately, returning `board`.
2. For each direction, count `opponent_count`, the consecutive opponent pieces
   next to the target, by walking on the read-only `board`.
3. When the run ends on an in-bounds `player` cell, record
   `(row_step, col_step, opponent_count)` in `capturing_directions`.
4. Return `board` unchanged when `capturing_directions` is empty.
5. Otherwise copy `board` into `flipped`, place the piece at `(row, col)`, and
   replay each recorded direction, flipping its `opponent_count` cells.

#### Walkthrough

Let us run the fully surrounded move of Example 2, `board = ["..B..","..W..","BW.WB","..W..","..B.."]`, `row = 2`, `col = 2`, `player = "B"`. The validation pass records one entry per direction, each with its opponent run length:

```text
up (-1,0)     (1,2)=W count 1  then (0,2)=B  -> capture
down (1,0)    (3,2)=W count 1  then (4,2)=B  -> capture
left (0,-1)   (2,1)=W count 1  then (2,0)=B  -> capture
right (0,1)   (2,3)=W count 1  then (2,4)=B  -> capture
diagonals     (1,1),(1,3),(3,1),(3,3) are all "."  -> no run
capturing_directions = [up 1, down 1, left 1, right 1]
```

The target `(2, 2)` holds `"W"`, not `"."`, so the occupied-target guard fires first and the function returns the original board unchanged, matching the expected Output for Example 2. The recorded table shows what would have happened on an empty center: four legal captures of one piece each, producing the all-`B` cross and arms shown in the expected output.

A quick confirmation on Example 1, where the target is empty: the validation pass records only `left 1` (the run `(1,2)=B` ending on `(1,1)=W`), so the replay phase places the `W` at `(1, 3)` and flips that single cell, giving `["....", ".WWW", "...."]`.

#### Solution

The code is the two phases: a read-only scan that collects bracketing directions, then a single replay that flips exactly those runs.

```python
from typing import List


class Solution:
    def applyReversiMove(self, board: List[str], row: int, col: int,
                         player: str) -> List[str]:
        if board[row][col] != '.':
            return board
        rows, cols = len(board), len(board[0])
        opponent = 'W' if player == 'B' else 'B'
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]

        capturing_directions = []
        for row_step, col_step in directions:
            walk_row, walk_col = row + row_step, col + col_step
            opponent_count = 0
            while (0 <= walk_row < rows and 0 <= walk_col < cols
                   and board[walk_row][walk_col] == opponent):
                opponent_count += 1
                walk_row += row_step
                walk_col += col_step
            if (opponent_count > 0 and 0 <= walk_row < rows
                    and 0 <= walk_col < cols
                    and board[walk_row][walk_col] == player):
                capturing_directions.append(
                    (row_step, col_step, opponent_count))

        if not capturing_directions:
            return board

        flipped = [list(line) for line in board]
        flipped[row][col] = player
        for row_step, col_step, opponent_count in capturing_directions:
            flip_row, flip_col = row + row_step, col + col_step
            for _ in range(opponent_count):
                flipped[flip_row][flip_col] = player
                flip_row += row_step
                flip_col += col_step
        return ["".join(line) for line in flipped]
```

#### Time and Space Complexity Analysis

##### Time Complexity: `O(rows × cols)`

The validation scan walks at most `max(rows, cols)` cells per direction and the replay flips only cells already counted, so the work remains linear in the board size; the same copy-and-join cost as before dominates the constant.

##### Space Complexity: `O(rows × cols)`

The `flipped` copy is allocated once, and `capturing_directions` holds at most 8 entries.

#### Key Insights

- Reading before writing splits the problem at its natural joint: legality is fully decidable from the immutable input, so mutation can wait until it is certain.
- Recording `(row_step, col_step, opponent_count)` lets the replay skip re-walking and re-testing; the count is the only state the validation needs to carry forward.
- The board is only read during validation, so no undo can ever be needed; this is the structural fix for the hazard the optimistic version patches at runtime.
- Like the first approach, this one returns the original `board` object for illegal moves and occupied targets, exactly as the statement's "return the original board unchanged" demands.

## Comparison of Solutions

### Time Complexity

- **Optimistic Flip with Undo**: `O(rows × cols)` - eight direction walks plus one board copy and join.
- **Validate-First Direction Scan**: `O(rows × cols)` - a read-only direction scan plus a single copy and replay.

### Space Complexity

- **Optimistic Flip with Undo**: `O(rows × cols)` - the `flipped` board copy.
- **Validate-First Direction Scan**: `O(rows × cols)` - the same copy, plus at most 8 recorded directions.

### Trade-offs

- The optimistic version commits the placement up front, which reads naturally but pays for it with the undo loop and a bracket test that must run against the mutated copy.
- The validate-first version scans the untouched board and mutates only after legality is certain, trading one extra bookkeeping list for the disappearance of the entire undo path.

### When to Use Each

- **Optimistic Flip with Undo**: when reasoning about the move as "place then resolve" feels most natural, or as the springboard to spotting why undoing is necessary at all.
- **Validate-First Direction Scan (Recommended)**: the interview answer: the same linear cost, no revert logic, and a legality phase that is trivial to argue correct because it only reads the input.

### Optimization Notes

- Both versions keep the direction deltas in a flat list of 8 `(row_step, col_step)` pairs rather than two nested range loops, which keeps the diagonal bookkeeping honest.
- The occupied-target guard must come before anything else: the statement returns the unchanged board for an occupied cell, and both capture mechanisms would otherwise flip that cell's owner.
- Returning `board` itself (not a copy of it) for illegal moves matches the statement's wording and avoids a needless allocation.
- If the function were extended to full-game play, the recorded `capturing_directions` of the validate-first scan is exactly the data a per-move flip-count heuristic would consume, which is why the two-phase shape generalizes better than place-then-undo.
