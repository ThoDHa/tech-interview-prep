# Tech Interview Prep

This repository is a structured study guide for algorithmic problem solving built on three curated problem banks: the [Grind 75](https://www.techinterviewhandbook.org/grind75) list of LeetCode questions from the [Tech Interview Handbook](https://www.techinterviewhandbook.org/) team, the [NeetCode 150](https://neetcode.io/practice/practice/neetcode150) track from the [NeetCode](https://neetcode.io/) team, and an [Amazon OA](docs/amazon/index.md) bank collected from the [Tech-OA-Interview-Questions](https://github.com/perixtar/Tech-OA-Interview-Questions) repository. All credit for the curated problem lists goes to them for their excellent work in creating these focused interview preparation resources.

**Read it as a website:** the full guide, including worked solution write-ups for every Grind 75 and NeetCode 150 problem and a growing share of the Amazon OA bank, is published at [thodha.github.io/tech-interview-prep](https://thodha.github.io/tech-interview-prep/).

## The three problem banks

- **Grind 75** is the core track: the canonical 75 problems in study order, plus two bonus problems ([Binary Tree Maximum Path Sum](docs/leetcode/binary_tree_maximum_path_sum.md) and [Maximum Frequency Stack](docs/leetcode/maximum_frequency_stack.md)).
- **NeetCode 150** extends the LeetCode track to 150 problems in NeetCode's section order; 59 of them overlap with Grind 75 and share their pages and write-ups.
- **Amazon OA** is a growing bank of Amazon-tagged online-assessment questions (383 problems as of October 2026, tracked against its upstream sources), with its own [bank index](docs/amazon/index.md), most recently updated first, and practice stubs under `practice/amazon/`.

All three banks are presented through one generated catalog, the [Problems page](docs/leetcode/index.md): the Grind 75 and NeetCode 150 tracks merge into a single unified table of 168 unique problems (each problem appears once, credited to every track it belongs to), and the Amazon OA bank gets its own table on the same page.

Every problem, regardless of track, has the same core page structure (statement and examples, with constraints where available) and a matching practice folder under `practice/` with stubs and tests; the Grind 75 and NeetCode 150 pages (not the Amazon OA pages) also link the **Pattern** guide behind the technique.

## How this repository is organized

- The `main` branch carries the complete study guide: problem statements with full multi-approach write-ups for every Grind 75 and NeetCode 150 problem (Amazon OA write-ups land in waves, 183 of 383 as of October 2026), the pattern guides, foundations, interview prep planning, system design material, and the `practice/` workspace with stubs and tests. The published site is built from this branch.
- The `practice` branch stacks your own problem attempts on top of `main`: it is where your commits in the `practice/` workspace live, without touching the underlying material. Attempt a problem there first; read the write-up when you are ready to compare answers.
- The `scripts/` directory holds the generators that maintain the generated tracks: `generate_neetcode150_scaffolds.py` emits problem pages and practice stubs for new NeetCode-only problems from `scripts/neetcode150_manifest.json`, `generate_amazon_oa_scaffolds.py` does the same for the Amazon OA bank (and owns its bank index) from `scripts/amazon_oa_manifest.json`, and `generate_index_tables.py` assembles the tables on the Problems catalog page and the site navigation from those data sources. All three are manifest-driven: a generator scaffolds a problem once and never touches it again once the write-up and practice folder have landed, so write-up bodies are hand-maintained after landing, and changes are validated with `cd practice && uv run pytest ../scripts/` and the generators' `--check` modes.

## First time here?

New to algorithms or interview prep? Start with the [Foundations](docs/foundations/index.md) section before the problems. It teaches the prerequisites the problem pages assume, all from zero:

1. [Big-O Notation](docs/foundations/big_o.md): what `O(n)` and `O(log n)` mean and when each is too slow.
2. [Recursion and the Call Stack](docs/foundations/recursion.md): how a function that calls itself actually works.
3. [Data Structures in Pictures](docs/foundations/data_structures.md): arrays, hash maps, stacks, queues, trees, graphs, and heaps.
4. [How to Approach a Problem](docs/foundations/how_to_approach.md): a repeatable method from problem statement to working solution.
5. [Glossary](docs/foundations/glossary.md): the jargon the guides lean on, defined in plain language.

Then work the problems in the [Problems catalog](docs/leetcode/index.md)'s unified study order, reading each one's linked **Pattern** guide for the *why* behind the technique. The [8-week schedule](docs/interview-prep/study_plan.md#the-8-week-schedule) paces that order into eight weeks, easier to harder with related problem types grouped together. For the plan around the problems, how to budget your time, and what the non-coding rounds require, see the [Interview Prep](docs/interview-prep/index.md) section. To record what you have solved as you go, use the practice progress tracker (`practice/progress.py`, described under [Practice Workspace](#practice-workspace)).

## Pattern Intuition

Beyond the individual problems, the guide includes [algorithm pattern intuition guides](docs/patterns/index.md) covering the recurring patterns these problems share (sliding window, two pointers, binary search, backtracking, dynamic programming, graph traversal, and more). Each guide explains *why* the pattern works, when it applies, and the invariant that makes it correct, then maps the pattern to the Grind 75 problems that use it. Most of the guides are adapted from the [NeetCode practice framework](https://lufftw.github.io/neetcode/); the Fundamentals guides (Hashing & Frequency Counting, Stack, Simulation, Data-Structure Design, String) and Grid DP are original to this project, and the corner-case checklists are adapted from the [Tech Interview Handbook](https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/) algorithm cheatsheets.

## System Design

Coding rounds are only half the interview loop. The [System Design section](docs/system-design/index.md) is a growing scaffold for the other half: a repeatable [interview method](docs/system-design/method.md) with a 45-minute time budget, [back-of-envelope estimation](docs/system-design/estimation.md) skills, a [building-blocks vocabulary](docs/system-design/building_blocks.md) from load balancers to consistency models, and [guided case studies](docs/system-design/case_studies/index.md) (URL shortener, rate limiter, news feed, chat, web crawler) that walk the method with collapsible answers and extension checklists.

## Practice Workspace

The [`practice/`](practice/) directory is a `pytest` workspace for solving the problems yourself rather than just reading them. Each problem has its own folder with a `solution.py` to implement, two test sets that mirror LeetCode's Run (the examples) and Submit (a full corner-case gauntlet), and a `__main__` block for stepping through a single case in a debugger. An unsolved `solution.py` raises `NotSolved` so its tests skip until you fill it in. A progress tracker (`practice/progress.py`) derives solved status from the test suite, records your confidence per problem, and maintains a spaced-repetition review queue. See [`practice/README.md`](practice/README.md) for setup and the full workflow.

## Creating a PDF of All Problems with Pandoc

You can compile every problem page in the repository into a single PDF with the included configuration. `configs/all-problems.yaml` lists all 551 problem pages (as of October 2026): the 168 LeetCode track pages in study order, then the 383 Amazon OA bank pages newest-first, with a divider introducing each collection.

### Prerequisites

1. Install [Pandoc](https://pandoc.org/installing.html) - universal document converter
   - On Debian/Ubuntu: `sudo apt-get install pandoc`
   - On macOS: `brew install pandoc`
2. Install a [LaTeX](https://www.latex-project.org/get/) distribution with the XeLaTeX engine (like TeX Live, MiKTeX, or MacTeX)
   - On Debian/Ubuntu: `sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-plain-generic`
   - On macOS: `brew install --cask mactex`
3. Install the [DejaVu Sans Mono](https://www.dejavu-fonts.org/) font, which the configuration uses for code blocks
   - On Debian/Ubuntu: `sudo apt-get install fonts-dejavu`
   - On macOS: `brew install --cask font-dejavu-mono`

### Generating the PDF

Run the following command from the terminal in the repository root (the `leetcode/` and `amazon/` page paths in the configuration resolve relative to `docs/`):

```bash
cd docs && pandoc --defaults ../configs/all-problems.yaml
```

This will:

- Read configuration from `configs/all-problems.yaml`
- Combine all 551 problem pages (`two_sum.md`, `amazon-concatenated-words-variant.md`, etc.)
- Create a table of contents
- Generate `docs/all-problems.pdf` using the XeLaTeX engine (the PDF is gitignored)

To customize the output, do not edit `configs/all-problems.yaml`: the file is generated whole by `scripts/generate_index_tables.py` from the committed manifests, and hand edits are lost on the next regeneration. Adjust the generator or the manifests it reads (`scripts/neetcode150_manifest.json`, `scripts/amazon_oa_manifest.json`, `scripts/grind75_table.json`) and regenerate with `python3 scripts/generate_index_tables.py`.
