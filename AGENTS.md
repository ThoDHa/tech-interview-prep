# AGENTS.md

Standards for agent-authored work in this repository. Agent tooling loads this
file automatically; the rules below are the bar the repo's audits and sweeps
enforce, not a restatement of global agent standards.

## Naming

- Descriptive identifiers; opaque abbreviations are rejected in review
  (`nxt`, `cur`, `curr`, `prev`, `cnt`, `tmp`, `idx`, `ans`, `res`, `temp`).
  Established domain terms are fine (`dfs`, `bfs`, `bst`, `lru`).
- Single-letter names (`i`, `j`, `n`, `k`) only as loop counters or established
  algorithm variables in tight scopes.
- Compound identifiers carrying an abbreviation morpheme follow the bank's
  established convention (`current_idx`, `pivot_idx`, `open_idx`).
- Diagram fences (flowcharts, trace tables) may use short trace notation
  (`ans`, `R`, `L`) when a legend declares it.
- Adjacency-successor iteration names the element: typed `next_<noun>`
  (`next_course`, `next_letter`), or `neighbor` when the page's own prose
  says neighbor.
- Functions name the operation as a verb phrase; booleans read as predicates.

## Code blocks

Applies to write-up fences and reference implementations alike.

- Runnable in isolation: every import a block uses is present and correct.
- Every fence carries a language tag matching its content (`python`, `text`,
  `java`, among others); untagged fences are audit findings.
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
| `docs/leetcode/<slug>.md` | `two_sum.md` |
| `docs/amazon/<slug>.md` | `../leetcode/two_sum.md` |
| `docs/patterns/<pattern>/intuition.md` | `../../leetcode/two_sum.md` |
| `docs/foundations/*.md`, `docs/interview-prep/*.md` | `../leetcode/two_sum.md` |
| `README.md` (repo root) | `docs/leetcode/two_sum.md` |

The `practice/` tree sits outside the mkdocs docs tree: refer to practice paths
in docs prose as inline code, never as hyperlinks (the built site cannot reach
them). The generated `**Practice:**` line on problem pages is the one
exception; `scripts/mkdocs-hooks/strip_practice.py` removes it at build time.

## Generator ownership

Generated files are never hand-edited; change the owning generator or its data
sources instead. Each generator has a read-only, offline `--check` mode; run
all three after touching a generator, its data sources, or generated output.

- `scripts/generate_neetcode150_scaffolds.py` emits `docs/leetcode/<dirSlug>.md`
  and `practice/leetcode/<dirSlug>/` (`solution.py`, `cases.json`, `test_<dirSlug>.py`)
  whole-file, for delta problems only: a problem with both a write-up and a
  practice folder is never touched, and a half-state (exactly one of the two)
  aborts the run. `cases_full.json` is never generated.
- `scripts/generate_amazon_oa_scaffolds.py` emits the Amazon scaffolds under
  `docs/amazon/` and `practice/amazon/`, and owns
  `docs/amazon/index.md` whole-file. Sync is fetch-new-only: the
  committed manifest is the hold list, an online run builds its entries
  from the bank rows (discovery plus the row refresh: title, url,
  companies, updated), and FastPrep pages are fetched, parsed, and emitted
  only for slugs the manifest does not hold. A held slug's committed
  write-up, practice folder, and classification are authoritative once
  fetched: no held-slug path reaches the fetcher, an upstream page death
  or bank-row date change never touches its files, and the four
  `page-unparseable` entries are no-ops on every future sync by
  construction. A new slug whose page is dead scaffolds placeholders and
  freezes once held until hand-authored. The death and guard machinery
  stays as code off the hot path: the `page-unparseable` write-ups are
  death-preserved archives whose committed sections emission keeps and
  whose generator-owned `## Solutions` block alone is pinned; a committed
  section carrying content whose heading the fresh render lacks is
  carried and re-appended after the template sections in committed order,
  named under `death merge union` in the run log, and a marker hole (a
  section holding only placeholder comments) is dropped, not carried. A
  committed `parsed-with-cases` slug whose live parse yields no problem
  and no cases keeps its practice files and classification untouched and
  is named under `transient parse guard` for a manual decision. An
  authored write-up (placeholder marker gone) is preserved untouched
  wherever emission reaches it; the generator pins its
  `# [Title](url)` header line byte-exact, and the body is
  hand-editable. An authored-cases folder (a non-empty `cases.json` under
  a committed status other than `parsed-with-cases`) is hand-owned:
  emission leaves its stub, `cases.json`, and test module untouched, and
  `--check` pins only that those three files exist; a refresh whose live
  parse meets such a folder anyway still overwrites it, and the run log
  names the slug under `practice cases conflicted`. The provenance seed
  still lands before emission: held entries carry their committed
  classification into the written manifest, and brand-new slugs stay
  unclassified until the live parse classifies them. For every folder
  emission renders, the generator pins the `# [Title](url)` header line
  byte-exact on the write-up and fragment-pins the leading docstring
  lines of `solution.py` and `test_<slug>.py` under
  `practice/amazon/<slug>/`. When the bank pages are absent, every slug
  is held and emission is a no-op; `--no-fetch` keeps the safety net for
  new slugs only, rendering from the disk cache or skipping untouched,
  and repairing a held slug's scaffolds means removing its manifest
  entry by hand so the next run treats it as new.
- `scripts/generate_index_tables.py` owns the marker-bounded sections of
  `docs/leetcode/index.md` (`unified-leetcode`, `sources`) and the `Leetcode`
  and `Amazon` nav sections in `mkdocs.yml`.
- Hand-editable: solved problem write-ups, pattern guides, foundations,
  interview prep, system design, `cases_full.json` files, and the committed
  data sources (`scripts/neetcode150_manifest.json`,
  `scripts/amazon_oa_manifest.json`, `scripts/grind75_table.json`,
  `scripts/amazon_lc_overlap_aliases.json`,
  `scripts/amazon_difficulty_overrides.json`,
  `scripts/amazon_constraints_overrides.json`).

## Verification

From the repository root:

```bash
cd practice && uv run pytest ../scripts/                # generator tests
cd practice && uv run pytest                            # problem suites
python3 scripts/generate_neetcode150_scaffolds.py --check
python3 scripts/generate_amazon_oa_scaffolds.py --check
python3 scripts/generate_index_tables.py --check        # index tables + nav
mkdocs build --strict                                   # docs build, zero warnings
```

Skips are expected in both suites: offline cache fixtures in the generator
tests; in the problem suites, unsolved `NotSolved` stubs plus a few committed
module-level skips (non-assertable outputs, unparsed cases). Failures are not.
