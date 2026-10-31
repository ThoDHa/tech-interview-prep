# Practice Workspace

A `pytest` workspace for practicing the problems in this repository yourself: the Grind 75 and NeetCode 150 LeetCode lists and the Amazon OA bank. Each problem gets a directory you solve in, debug through, and test. Every `solution.py` is an unsolved stub: it raises `NotSolved` until you implement it, and it links to the matching write-up, at `../docs/leetcode/<slug>.md` for the LeetCode track and `../docs/amazon/<slug>.md` for the Amazon bank, whose page links back, so you can go back and forth. About half the LeetCode folders and a small subset of the Amazon ones additionally carry a `reference.py`, the write-up's own solution kept next to the harness so its authored case files stay checkable; treat it as the answer key and stay out of it until after your own attempt, with some folders adding a `test_reference_<slug>.py` that checks it.

## Get a copy

Your attempts live on your own `practice` branch, created from the study guide's `main` branch, so they never touch the guide. Fork [ThoDHa/tech-interview-prep](https://github.com/ThoDHa/tech-interview-prep) on GitHub, clone your fork, and create the branch from `main`:

```bash
git clone https://github.com/<your-username>/tech-interview-prep.git
cd tech-interview-prep
git switch -c practice main
```

This creates a local `practice` branch at `main`'s tip and switches to it. The repository also carries a `practice` branch holding the maintainer's own worked attempts; leave it alone and build on `main`.

## Layout

```text
practice/
├── harness.py                 # shared helpers (ListNode/TreeNode/graph builders, case loader, pick_case)
├── progress.py                # progress tracker (scan, rate, status, due)
├── pyproject.toml             # uv project (pytest dependency)
├── pytest.ini                 # markers, import path, and other pytest settings
├── leetcode/                  # Grind 75 + NeetCode 150 problems
│   └── <slug>/                # the four files below; some folders add reference.py + test_reference_<slug>.py
│       ├── solution.py        # YOUR attempt: solve here; run it directly to debug a case
│       ├── cases.json         # simple cases: the LeetCode examples ("Run")
│       ├── cases_full.json    # full cases: the corner-case gauntlet ("Submit")
│       └── test_<slug>.py     # runs your solution against both case sets
└── amazon/                    # Amazon OA bank
    └── <slug>/                # solution.py + cases.json + test_<slug>.py; a few folders add cases_full.json + reference.py + a reference test
```

## Setup (uv)

```bash
cd practice
uv sync           # creates .venv and installs pytest
```

## The practice loop

1. Open `leetcode/<slug>/solution.py`. The header links to the write-up at `../../docs/leetcode/<slug>.md`: read the problem there.
2. Implement the method.
3. **Debug it inside the file.** Each `solution.py` has a `__main__` block that runs one case and prints input / expected / actual. Set a breakpoint in your method, pick the case (edit the `CASE` id near the bottom), and run/debug the file directly:

   ```bash
   uv run python leetcode/two_sum/solution.py
   ```

   On an untouched stub the `__main__` block raises `NotSolved`: there is nothing to debug until the method exists.

4. **Test it.** Two case sets, mirroring LeetCode's two buttons:

   ```bash
   uv run pytest leetcode/two_sum/             # both sets
   uv run pytest leetcode/two_sum/ -m simple   # "Run": just the examples
   uv run pytest leetcode/two_sum/ -m full     # "Submit": the full gauntlet
   uv run pytest                               # everything
   ```

   An unsolved `solution.py` raises `NotSolved`, so its tests **skip** rather than fail. Once you implement it, they run for real (red → green).

5. To study the approaches, open `../docs/leetcode/<slug>.md` (linked from the top of `solution.py`).

Amazon problems follow the same loop with paths like `amazon/amazon-aggressive-cows/` and its single case set:

```bash
uv run python amazon/amazon-aggressive-cows/solution.py
uv run pytest amazon/amazon-aggressive-cows/
```

## Case sets: Run vs Submit

| File | Marker | Role |
|------|--------|------|
| `cases.json` | `simple` | The problem's own examples where they parse, otherwise a few promoted gauntlet cases. Fast feedback while you iterate. |
| `cases_full.json` | `full` | Examples **plus** a comprehensive corner-case gauntlet (empties, single elements, negatives, duplicates, boundary values, large inputs). |

`cases_full.json` is a thorough corner-case suite built to each problem's constraints. LeetCode's literal hidden tests are not public, but this set targets the same failure modes. Amazon problems use no markers: most ship only `cases.json`, so a plain `uv run pytest amazon/<slug>/` is all they need, and the few that also carry `cases_full.json` and a reference test run their whole folder with that same plain command.

## Tracking your progress

`progress.py` is a small stdlib-only tracker that remembers which problems you have solved, how confident each solve felt, and which ones are due for a spaced-repetition review. Its state lives in `.progress.json` next to it (personal, gitignored, and never read by the tests).

```bash
uv run python progress.py scan             # run the suite, record per-problem status
uv run python progress.py rate <slug> <solid|shaky|struggled>
uv run python progress.py status           # full board in canonical study order
uv run python progress.py due              # just the review queue
```

**Status model.** `scan` runs the full test suite and reports it honestly: a problem is `solved` only while every test passes, `attempted` when any test fails (or only some pass), and `unsolved` when everything skips. The date of the first successful solve is recorded automatically. If a solved problem later reverts to the stub, its status drops back to `unsolved`, but the solve date and rating history are kept.

**Confidence and review.** After solving, rate how it felt with `rate <slug> <level>`. The rating sets the spaced-repetition interval:

| Confidence | Review after |
|------------|--------------|
| `struggled` | 2 days |
| `shaky` | 7 days |
| `solid` | 21 days |
| solved but unrated | 14 days |

A problem is due once that many days have passed since you last practiced it (the later of the solve date and the rating date). `due` lists the queue, most overdue first: re-solve it, rate it again, and the clock resets.

## Case format

Both `cases.json` and `cases_full.json` are lists of cases. For most problems a case is `{"id": ..., "args": [...], "expected": ...}` where `args` is the positional argument list and `expected` the return value. Problems with linked lists, trees, graphs, or design-operation sequences store plain JSON in the case files and the test module marshals it via the `harness` helpers.
