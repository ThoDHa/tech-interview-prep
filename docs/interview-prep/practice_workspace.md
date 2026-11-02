# The Practice Workspace

The site explains every solution; the practice workspace is where you write them. The `practice/` directory is a `pytest` workspace with a folder for every problem in the catalog: a stub `solution.py` for your attempt, case files that mirror LeetCode's Run and Submit buttons, and the tests that check your work. This page takes you from a fresh fork to your first green test.

## Fork and clone the repository

The published site is read-only, so the first move is your own copy of the code.

1. Fork [ThoDHa/tech-interview-prep](https://github.com/ThoDHa/tech-interview-prep) on GitHub: click **Fork** at the top right of the repository page; the dialog's defaults are fine. You now have a copy at `https://github.com/<your-username>/tech-interview-prep`.
2. Clone your fork and enter it:

   ```bash
   git clone https://github.com/<your-username>/tech-interview-prep.git
   cd tech-interview-prep
   ```

## Two branches: main and your practice

The whole practice model rests on a two-branch split:

- `main` is the guide: the problem write-ups, pattern guides, foundations, and planning pages, plus the practice workspace with its unsolved stubs. It is also the branch the published site is built from.
- `practice` is yours: a branch you create from `main`, where your attempts live, so you can commit half-finished solutions to `practice/` without ever touching the guide.

Create your branch right after cloning:

```bash
git switch -c practice main
```

This creates a local `practice` branch at `main`'s tip and switches to it. The upstream repository itself also carries a `practice` branch, holding the maintainer's own worked attempts; leave it alone and build on `main`.

The intended rhythm: attempt each problem on `practice`, and when you are stuck or finished, read the write-up on the site to compare answers. Your attempts and the guide stay out of each other's way.

## One-time setup

The workspace is a [uv](https://docs.astral.sh/uv/) project, and uv also provisions the Python interpreter it needs. Install uv, then run:

```bash
cd practice
uv sync
```

This creates a virtual environment in `practice/.venv` and installs `pytest`. Every command from here on runs inside `practice/`.

## What is in the workspace

```text
practice/
├── harness.py            # shared helpers: case loader, list/tree/graph builders
├── progress.py           # progress tracker (scan, rate, status, due)
├── pyproject.toml        # uv project definition
├── pytest.ini            # pytest configuration: markers and import path
├── test_progress.py      # the tracker's own unit tests
├── leetcode/             # Grind 75 + NeetCode 150 problems, one folder each
│   └── two_sum/
└── amazon/               # Amazon OA bank, one folder each
    └── amazon-aggressive-cows/
```

The common shape is the same four files in each `leetcode/<slug>/` folder (Amazon folders usually ship the same set minus `cases_full.json`; see [Run versus Submit](#run-versus-submit)):

```text
leetcode/two_sum/
├── solution.py       # YOUR attempt: the only file you edit
├── cases.json        # the example cases ("Run")
├── cases_full.json   # examples plus a corner-case gauntlet ("Submit")
└── test_two_sum.py   # runs your solution against both case sets
```

`solution.py` is always an unsolved stub: it raises `NotSolved` until you implement it, and the worked write-up lives on the site, linked from the top of every `solution.py`. About a hundred folders additionally carry a `reference.py`, the write-up's own solution kept next to the harness so its authored case files stay checkable (91 of the 168 LeetCode folders, 47 of the 410 Amazon ones, as of October 2026); treat it as the answer key and stay out of it until after your own attempt. Some of those folders also add a `test_reference_<slug>.py` that checks `reference.py` itself.

## The practice loop

1. **Pick a problem** from the [Problems catalog](../leetcode/index.md) and open its folder, `practice/leetcode/two_sum/`.
2. **Read the problem** in the `solution.py` docstring or on its page, [Two Sum](../leetcode/two_sum.md).
3. **Implement the method** on the `Solution` class. The stub body raises `NotSolved`; replace it with your attempt.
4. **Debug one case.** Every `solution.py` ends with a `__main__` block: set `CASE` near the bottom to a case id from `cases.json`, then run the file directly:

   ```bash
   uv run python leetcode/two_sum/solution.py
   ```

   It prints the case's arguments, the expected output, and what your code returned; on an untouched stub it raises `NotSolved` instead, so there is nothing to debug until step 3 is done. To step through your method in a debugger, set a breakpoint inside it and run this same command under your debugger instead of in the terminal.
5. **Run the tests** when the output looks right:

   ```bash
   uv run pytest leetcode/two_sum/ -m simple   # "Run": just the examples
   uv run pytest leetcode/two_sum/ -m full     # "Submit": the full gauntlet
   uv run pytest                               # the whole workspace
   ```
6. **Compare with the write-up** on the problem page once your tests pass (or once you are stuck): the page derives every approach from brute force to optimal, so reading it after your own attempt shows you exactly what to improve.

The loop is identical for the Amazon bank, with paths like `practice/amazon/amazon-aggressive-cows/` and its single case set:

```bash
uv run python amazon/amazon-aggressive-cows/solution.py
uv run pytest amazon/amazon-aggressive-cows/
```

## Run versus Submit

The two case files mirror the two buttons on a LeetCode problem page:

| File | Marker | Role |
|------|--------|------|
| `cases.json` | `simple` | The problem's own examples where they parse, otherwise a few promoted gauntlet cases: fast feedback while you iterate. |
| `cases_full.json` | `full` | The examples plus a comprehensive corner-case gauntlet (empties, single elements, negatives, duplicates, boundary values, large inputs) built to the problem's constraints. |

The `-m simple` and `-m full` flags select between them; a plain `uv run pytest leetcode/<slug>/` runs both sets. Amazon problems use no markers: 363 of the 410 ship only `cases.json`, so a plain `uv run pytest amazon/<slug>/` is all they need, and the 47 that also carry `cases_full.json` and a reference test run their whole folder with that same plain command.

## Stubs skip until you implement them

An untouched `solution.py` raises `NotSolved`, and its tests **skip** rather than fail:

```text
SKIPPED [3] leetcode/two_sum/test_two_sum.py:32: solution.py not implemented yet
```

A fresh clone therefore shows a wall of skips, over 3,100 across the workspace; besides the tracker's own unit tests, the immediate green is just the reference tests where a folder carries `reference.py`. All of it is expected. The moment you implement a problem, its skips turn into real tests that can go red before they go green.

## Track your progress

`practice/progress.py` is a small tracker that remembers what you have solved, how confident each solve felt, and what is due for review. Its state lives in `.progress.json` next to it, which is personal and gitignored.

```bash
uv run python progress.py scan     # run the suite, record per-problem status
uv run python progress.py rate <slug> <solid|shaky|struggled>
uv run python progress.py status   # the full board in study order
uv run python progress.py due      # the spaced-repetition review queue
```

A slug is the problem's directory name, such as `two_sum` or `amazon-aggressive-cows`. The `scan` status is honest by construction: `solved` only while every test passes, `attempted` when any test fails or only some pass, `unsolved` when everything still skips. After a solve, rate it; the rating sets the review interval (`struggled` 2 days, `shaky` 7, `solid` 21, unrated 14), and `due` lists the queue most overdue first. Re-solve a due problem and rate it again to reset the clock.

## Where this fits

The [study plan](study_plan.md) paces the problems into weeks and tells you which batch to attempt next, and the [Foundations](../foundations/index.md) teach the prerequisites the problem pages assume. For the workspace's own reference sheet, see `practice/README.md` in the repository.
