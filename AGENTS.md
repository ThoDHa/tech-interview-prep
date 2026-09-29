# AGENTS.md

Standards for agent-authored work in this repository. Agent tooling loads this
file automatically; the rules below are the bar the repo's audits and sweeps
enforce, not a restatement of global agent standards.

## Naming

- Descriptive identifiers; opaque abbreviations are rejected in review.
  Established domain terms are fine (`dfs`, `bfs`, `bst`, `lru`).
- Single-letter names (`i`, `j`, `n`, `k`) only as loop counters or established
  algorithm variables in tight scopes.
- Functions name the operation as a verb phrase; booleans read as predicates.

## Code blocks

Applies to write-up fences and reference implementations alike.

- Runnable in isolation: every import a block uses is present and correct.
- Every fence carries a language tag (`python`, `text`); untagged fences are
  audit findings.
- Signatures carry type annotations on parameters and returns.
- Complexity claims next to code match what the code actually does; where a
  page has a `reference.py`, the write-up's approach and complexity match it.

## Comments

- Absent by default. Add a comment only when the code cannot express the intent
  itself, and say why, not what. No filler markers, no bug-fix history: commit
  messages carry that.

## Internal links

Match the per-directory prefix exactly:

| Page location | Link to a problem page as |
| --- | --- |
| `docs/problems/<slug>.md` | `two_sum.md` |
| `docs/problems/amazon_oa/<slug>.md` | `../two_sum.md` |
| `docs/patterns/<pattern>/intuition.md` | `../../problems/two_sum.md` |
| `docs/foundations/*.md`, `docs/interview_prep/*.md` | `../problems/two_sum.md` |
| `README.md` (repo root) | `docs/problems/two_sum.md` |

The `practice/` tree sits outside the mkdocs docs tree: refer to practice paths
in docs prose as inline code, never as hyperlinks (the built site cannot reach
them). The generated `**Practice:**` line on problem pages is the one
exception; `hooks/strip_practice.py` removes it at build time.

## Generator ownership

Generated files are never hand-edited; change the owning generator or its data
sources instead. Each generator has a read-only, offline `--check` mode; run
all three after touching a generator, its data sources, or generated output.

- `scripts/generate_neetcode150_scaffolds.py` emits `docs/problems/<dirSlug>.md`
  and `practice/<dirSlug>/` (`solution.py`, `cases.json`, `test_<dirSlug>.py`)
  whole-file, for delta problems only: a problem with both a write-up and a
  practice folder is never touched, and a half-state (exactly one of the two)
  aborts the run. `cases_full.json` is never generated.
- `scripts/generate_amazon_oa_scaffolds.py` emits the Amazon scaffolds under
  `docs/problems/amazon_oa/` and `practice/amazon_oa/`, and owns
  `docs/problems/amazon_oa/index.md` whole-file. Three write-ups rendered from
  the manifest alone are byte-compared, never hand-edited:
  `amazon-find-minimum-possible-variance.md`, `amazon-get-min-cost-book.md`,
  `amazon-find-minimum-number-of-operations.md`. Every other Amazon write-up
  owns its `# [Title](url)` header line byte-exact; the body is hand-editable.
- `scripts/generate_index_tables.py` owns the marker-bounded sections of
  `docs/problems/index.md` (`unified-leetcode`, `amazon-oa`, `sources`) and the
  `Problems` nav in `mkdocs.yml`.
- Hand-editable: solved problem write-ups, pattern guides, foundations,
  interview prep, system design, `cases_full.json` files, and the committed
  data sources (`scripts/neetcode150_manifest.json`,
  `scripts/amazon_oa_manifest.json`, `scripts/grind75_table.json`).

## Verification

From the repository root:

```bash
cd practice && uv run pytest ../scripts/                # generator tests
python3 scripts/generate_neetcode150_scaffolds.py --check
python3 scripts/generate_amazon_oa_scaffolds.py --check
python3 scripts/generate_index_tables.py --check        # index tables + nav
mkdocs build --strict                                   # docs build, zero warnings
```

Skips are expected in both suites: offline cache fixtures in the generator
tests, unsolved `NotSolved` practice stubs in the problem suites. Failures
are not.
