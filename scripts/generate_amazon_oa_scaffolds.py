"""Generate the Amazon OA coding problem bank for grind75.

Pipeline:
  1. Parse the cached Tech-OA bank pages, keep Amazon-tagged coding rows,
      dedup by FastPrep slug, and sort most-recently-updated first.
  2. Write scripts/amazon_oa_manifest.json; each entry carries the
      write-up header's difficulty and categories (None where the header
      carries the unknown markers).
  3. For each manifest entry absent from the committed manifest or left
      unclassified (parse_status None) by it, fetch the
      FastPrep problem page (disk cache, polite delay), parse the
      statement/examples/constraints, and emit:
        - docs/amazon/<slug>.md                  (statement write-up scaffold)
        - practice/amazon/<slug>/solution.py     (NotSolved stub)
        - practice/amazon/<slug>/cases.json      (parseable examples, else [])
        - practice/amazon/<slug>/test_<slug>.py  (harness-driven tests)
        - docs/amazon/index.md   (bank table: Problem, Difficulty, Category,
          Time, Companies, Updated)

Fetch-new-only contract: a slug the committed manifest genuinely
classifies (parse_status set) is held; its committed write-up, practice
folder, and classification are authoritative once fetched, and no sync
path fetches, parses, or re-emits it. An entry whose parse_status is None
is not held: written unclassified by a --manifest-only bootstrap, a
--limit overshoot, or a --no-fetch skip, it stays fetchable and the next
bank-available run classifies it. The bank pages drive discovery and the
manifest row refresh (title, url, companies, updated); FastPrep is
fetched only for slugs the manifest does not hold or has not classified.
A new slug whose page is dead scaffolds placeholders, is
classified `page-unparseable`, and freezes once held until hand-authored.

Cases contract: a case is emitted only when every example value parses to a
JSON-representable literal assertable with `==` against the method's return
value. Trees, linked lists, graphs, design-operation sequences, and free-text
outputs produce an empty cases.json and a test module that skips with a reason
naming the slug. Empty is never a silent pass.

Authored protection: when the committed manifest does not mark a slug
`parsed-with-cases` but its committed cases.json is a non-empty list
(cases authored by hand after the scaffold), emission leaves the folder's
practice files untouched, and --check exempts them from the generator-owned
fragment pins. A `parsed-with-cases` entry's non-empty cases.json is the
generator's own last render and stays generator-owned.

Offline contract: the committed scripts/amazon_oa_manifest.json (with its
per-slug parse_status) is the source of truth. When the bank pages under /tmp
are absent (any fresh clone), every mode falls back to the committed manifest,
where every slug is held and emission is a no-op, and --check compares the
tree against manifest-driven expectations, never against a re-render from the
unversioned fastprep cache. --no-fetch keeps a narrower safety net for
unheld slugs: such a slug renders from the disk cache when one
exists and is skipped untouched when it does not; repairing a held slug's
scaffolds means removing its manifest entry by hand so the next run treats
it as new. The bank index's
Difficulty/Time columns reuse generate_index_tables.py's conventions: the
committed amazon_difficulty_overrides.json corrects externally sourced
difficulties at render time, and Time carries the shared difficulty-based
estimates (Easy 15 / Medium 25 / Hard 40 minutes, a dash where unknown).
The committed amazon_constraints_overrides.json supplies Constraints bullets
for slugs whose FastPrep page lists none, so their generator-owned write-ups
render a filled section on every refresh.

Usage (from the repository root):
  cd practice && uv run pytest ../scripts/          # run the generator tests
  python3 scripts/generate_amazon_oa_scaffolds.py \
      [--bank-page PATH]... [--manifest-only | --limit N | --check] [--no-fetch]
"""

from __future__ import annotations

import argparse
import ast
import datetime
import html
import json
import keyword
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Collection, Dict, List, Mapping, NamedTuple, Optional, Sequence, Tuple

import generate_index_tables as index_tables

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "scripts" / "amazon_oa_manifest.json"
CONSTRAINTS_OVERRIDES_PATH = REPO_ROOT / "scripts" / "amazon_constraints_overrides.json"
DOCS_DIR = REPO_ROOT / "docs" / "amazon"
PRACTICE_DIR = REPO_ROOT / "practice" / "amazon"
TEMPLATE_PATH = REPO_ROOT / "docs" / "leetcode" / "_TEMPLATE.md"
MKTABS_PATH = REPO_ROOT / "mkdocs.yml"

DEFAULT_BANK_PAGES = (
    Path("/tmp/opencode/tech-oa/coding.md"),
    Path("/tmp/opencode/tech-oa/coding-page-2.md"),
    Path("/tmp/opencode/tech-oa/coding-page-3.md"),
)
# Bank rows whose FastPrep problem pages are dead (HTTP 404): the write-ups
# behind them were deliberately dropped, and keeping the rows out of the
# manifest stops every regeneration from re-emitting placeholder-only
# scaffolds for problems FastPrep no longer serves.
EXCLUDED_SLUGS = {
    "amazon-find-minimum-number-of-operations",
    "amazon-find-minimum-possible-variance",
    "amazon-get-min-cost-book",
}
FASTPREP_CACHE_DIR = Path("/tmp/opencode/fastprep-cache")
FASTPREP_URL_TEMPLATE = "https://www.fastprep.io/problems/{slug}"
FETCH_DELAY_SECONDS = 0.5
FETCH_FAILED_MARKER_TEMPLATE = "<!-- fetch failed: HTTP {error_code} for {slug} -->"
AMAZON_TAG = "Amazon"
WRITEUP_LINK_TEMPLATE = "../../../docs/amazon/{slug}.md"
WRITEUP_PLACEHOLDER_MARKER = "<!-- Scaffold placeholder:"
# Header placeholders for what FastPrep does not publish; the bank index
# renders those rows with the dash filler instead.
WRITEUP_UNKNOWN_DIFFICULTY_MARKER = "unknown difficulty"
WRITEUP_UNKNOWN_CATEGORIES_MARKER = "unknown categories"
# The write-up's line-3 metadata line (`**<Difficulty>** | **NN minutes** |
# **<Topics>**`) is the parseable source of the manifest's difficulty and
# categories; generate_index_tables.py pins the same layout for its own
# header parse.
WRITEUP_DIFFICULTY_LINE = 3
WRITEUP_HEADER_PATTERN = re.compile(
    r"^\*\*(?P<difficulty>.+?)\*\* \| \*\*(?P<minutes>.+?)\*\*"
    r" \| \*\*(?P<categories>.+?)\*\*$"
)
# Site-relative links cannot reach the practice/ tree outside the mkdocs
# docs_dir, and the AGENTS.md internal-links rule bars hyperlinks to
# practice paths in docs prose; the index names the path as inline code.

BANK_ROW_PATTERN = re.compile(
    r"^\|\*\*(?P<companies>[^*]+)\*\*\*?"
    r"\|\[(?P<title>[^]]+)\]\((?P<url>https://www\.fastprep\.io/problems/(?P<slug>[^)]+))\)"
)
DATE_SUFFIX_PATTERN = re.compile(
    r"(?P<month>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+"
    r"(?P<day>\d{1,2}),\s+(?P<year>\d{4})[\s|]*$"
)
CONSTRAINT_LIST_ITEM_PATTERN = re.compile(r"<li>(.*?)</li>", re.S)
STATEMENT_CONTENT_MARKER = '<div class="fp-statement-content">'
STATEMENT_SECTION_END = "</section>"
# Flight-data statements below this many rendered characters are shredded
# (katex markup consumed the prose, e.g. the literal "$23"); the statement is
# then recovered from the server-rendered page instead.
MIN_PLAUSIBLE_STATEMENT_LENGTH = 40
# FastPrep prepends contributor-credit lines ("Special thanks: Nick
# contributed this problem.") to the statement; they are chrome, not problem
# content, so extraction drops them and regenerations never re-introduce the
# residue hand cleanups remove.
CONTRIBUTOR_CHROME_PATTERN = re.compile(r"^Special thanks:.*(?:\n|$)", re.M)
WRITEUP_SECTION_HEADING_PATTERN = re.compile(r"(?m)^## .*$")
HTML_COMMENT_PATTERN = re.compile(r"<!--.*?-->", re.S)
# A `<` that opens no plausible tag (`</?letter`, no angle brackets, then
# `>`) is prose: recovered FastPrep statements carry raw comparisons like
# `0 ≤ i < n`. Escape it before the tag strips run, because the generic
# strip would otherwise swallow from the raw `<` through the next real
# tag's `>`, deleting whole clauses; `html.unescape` restores it at the
# end.
PROSE_LESS_THAN_PATTERN = re.compile(r"<(?!/?[a-zA-Z][^<>]*>)")
NEXT_FLIGHT_CHUNK_PATTERN = re.compile(
    r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)'
)
PROBLEM_RECORD_KEY = '{"problem":'

SCALAR_TYPES = {
    "int",
    "integer",
    "long",
    "float",
    "double",
    "string",
    "str",
    "char",
    "bool",
    "boolean",
    "any",
}
DESIGN_INPUT_NAMES = {"operations", "actions", "commands", "methods"}


@dataclass
class CasesResult:
    """Outcome of converting FastPrep examples into harness cases.

    Attributes:
        function_name: The method name solutions implement (e.g. `solve`).
        cases: JSON-representable cases `[{"id", "args", "expected"}]`.
        skip_reason: Why no cases exist, naming the slug; None when cases exist.
    """

    function_name: str
    cases: List[dict]
    skip_reason: Optional[str]


# ---------------------------------------------------------------------------
# Bank page extraction
# ---------------------------------------------------------------------------


def parse_bank_rows(page_text: str) -> List[dict]:
    """Extract every problem row from a Tech-OA bank page.

    Args:
        page_text: Raw markdown of a bank page (coding.md / coding-page-2.md /
            coding-page-3.md).

    Returns:
        A list of row dicts with `companies` (list of names), `title`, `url`,
        `slug`, and `updated` (ISO date string), in page order.
    """
    rows: List[dict] = []
    for line in page_text.splitlines():
        match = BANK_ROW_PATTERN.match(line)
        if match is None:
            continue
        updated_match = DATE_SUFFIX_PATTERN.search(line)
        rows.append(
            {
                "companies": [
                    name.strip() for name in match.group("companies").split(",")
                ],
                "title": match.group("title"),
                "url": match.group("url"),
                "slug": match.group("slug"),
                "updated": format_updated_date(updated_match.group(0)) if updated_match else "",
            }
        )
    return rows


def format_updated_date(raw_date: str) -> str:
    """Normalize a bank-page date like `🔥 Sep 19, 2026` to ISO `2026-09-19`."""
    cleaned = re.sub(r"[^A-Za-z0-9, ]", "", raw_date).strip()
    parsed = datetime.datetime.strptime(cleaned, "%b %d, %Y")
    return parsed.date().isoformat()


def build_manifest(page_texts: Sequence[str]) -> List[dict]:
    """Build the Amazon-tagged manifest: filter, dedup, sort most-recent first.

    Rows tagged Amazon are kept, minus the dead FastPrep pages listed in
    EXCLUDED_SLUGS. A slug never scaffolded before (no write-up and no
    practice folder) bootstraps with difficulty and categories None, so a
    bank-growth run builds the manifest before any scaffold exists; a
    missing write-up whose practice scaffolds DO exist is bank corruption
    and still aborts.

    Args:
        page_texts: Raw markdown of each bank page, in any order.

    Returns:
        Manifest entries (`slug`, `title`, `url`, `companies`, `updated`,
        `difficulty`, `categories`) sorted by `updated` descending with
        slug-ascending tie-break. When a slug appears on several pages the
        most recently updated row wins.
    """
    by_slug: Dict[str, dict] = {}
    for page_text in page_texts:
        for row in parse_bank_rows(page_text):
            if AMAZON_TAG not in row["companies"]:
                continue
            if row["slug"] in EXCLUDED_SLUGS:
                continue
            existing = by_slug.get(row["slug"])
            if existing is None or row["updated"] > existing["updated"]:
                by_slug[row["slug"]] = row
    entries = sorted(by_slug.values(), key=lambda row: row["slug"])
    entries.sort(key=lambda row: row["updated"], reverse=True)
    enriched: List[dict] = []
    for row in entries:
        writeup_path = DOCS_DIR / f"{row['slug']}.md"
        never_scaffolded = not writeup_path.exists() and not (PRACTICE_DIR / row["slug"]).exists()
        writeup_metadata = (
            {"difficulty": None, "categories": None}
            if never_scaffolded
            else parse_difficulty_line(writeup_path)
        )
        enriched.append({**row, **writeup_metadata})
    return enriched


COMMITTED_ENTRY_REQUIRED_KEYS = ("slug", "title", "url", "parse_status")


def load_committed_manifest(path: Path = MANIFEST_PATH) -> List[dict]:
    """Load the committed manifest, the offline source of truth.

    The bank pages under /tmp are recon scratch, absent on any fresh clone;
    every generation mode must be able to run from the committed manifest
    alone. Every entry must carry the identity and classification keys
    the emission, check, and seed paths read directly: an entry missing
    `parse_status` would silently flip the authored-protection predicates.

    Args:
        path: Path to the manifest JSON (default: scripts/amazon_oa_manifest.json).

    Returns:
        The manifest entries in committed order, each carrying its
        `parse_status`.

    Raises:
        SystemExit: When the manifest file is missing, is not valid JSON,
            is not a JSON list, or an entry is not a JSON object or lacks
            one of slug, title, url, or parse_status.
    """
    try:
        entries = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, UnicodeDecodeError) as error:
        raise SystemExit(f"committed manifest unusable: {error}; run the generator once with the bank pages present")
    except json.JSONDecodeError as error:
        raise SystemExit(f"committed manifest {path} is not valid JSON: {error}")
    if not isinstance(entries, list):
        raise SystemExit(f"committed manifest {path} must be a JSON list")
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise SystemExit(f"committed manifest {path} entry #{index} must be a JSON object")
        missing_keys = [key for key in COMMITTED_ENTRY_REQUIRED_KEYS if key not in entry]
        if missing_keys:
            named = f"'{entry['slug']}'" if "slug" in entry else f"#{index}"
            raise SystemExit(
                f"committed manifest {path} entry {named} is missing {', '.join(missing_keys)};"
                " the manifest is hand-editable data: add the key(s) by hand"
                " (title and url from the write-up's pinned header line,"
                " parse_status from the practice folder's cases.json or a full"
                " generation run)"
            )
    return entries


# ---------------------------------------------------------------------------
# Write-up header metadata (difficulty, categories)
# ---------------------------------------------------------------------------


def parse_difficulty_line(writeup_path: Path) -> dict:
    """Extract one write-up's difficulty and categories from its header line.

    The scaffold layout pins the metadata line at line 3:
    ``**<Difficulty>** | **NN minutes** | **<Topics>**``. The minutes are a
    literal placeholder and carry no data; the unknown markers map to None
    so the bank index can dash those cells.

    Args:
        writeup_path: Path to the committed write-up markdown.

    Returns:
        `{"difficulty": ...}` where the value is the canonical difficulty
        name, or None under the unknown-difficulty marker, and likewise
        `{"categories": ...}` with the raw comma-separated string or None.

    Raises:
        SystemExit: When the write-up is missing or its header line does
            not match the scaffold layout.
    """
    if not writeup_path.exists():
        raise SystemExit(
            f"write-up not found: {writeup_path}; restore it from git or"
            " hand-remove its manifest entry so the next run scaffolds the"
            " slug as new"
        )
    lines = writeup_path.read_text(encoding="utf-8").splitlines()
    header = (
        lines[WRITEUP_DIFFICULTY_LINE - 1]
        if len(lines) >= WRITEUP_DIFFICULTY_LINE
        else None
    )
    match = WRITEUP_HEADER_PATTERN.match(header) if header is not None else None
    if match is None:
        raise SystemExit(
            f"write-up {writeup_path} has no **difficulty** | **minutes** |"
            f" **categories** header at line {WRITEUP_DIFFICULTY_LINE}"
        )
    difficulty = match.group("difficulty")
    categories = match.group("categories")
    return {
        "difficulty": (
            None
            if difficulty == WRITEUP_UNKNOWN_DIFFICULTY_MARKER
            else difficulty
        ),
        "categories": (
            None
            if categories == WRITEUP_UNKNOWN_CATEGORIES_MARKER
            else categories
        ),
    }


# ---------------------------------------------------------------------------
# FastPrep page parsing
# ---------------------------------------------------------------------------


def extract_problem_record(page_html: str) -> Optional[dict]:
    """Pull the structured problem record out of a FastPrep page.

    FastPrep server-renders with Next.js; the page embeds `self.__next_f`
    flight payloads whose concatenated text holds a `{"problem": {...}}` JSON
    object with the statement, typed examples, constraints, and metadata.

    Args:
        page_html: Raw HTML of a FastPrep problem page.

    Returns:
        The `problem` record dict, or None when the page carries no payload.
    """
    chunks = NEXT_FLIGHT_CHUNK_PATTERN.findall(page_html)
    if not chunks:
        return None
    try:
        flight_text = "".join(json.loads(chunk) for chunk in chunks)
    except json.JSONDecodeError:
        return None
    start = flight_text.find(PROBLEM_RECORD_KEY)
    if start == -1:
        return None
    try:
        wrapper = _decode_balanced_object(flight_text, start)
    except ValueError:
        return None
    problem = wrapper.get("problem")
    return problem if isinstance(problem, dict) else None


def _decode_balanced_object(text: str, start: int) -> dict:
    """Decode the JSON object starting at `start`, tolerating sibling content."""
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : index + 1])
    raise ValueError("unbalanced JSON object in flight payload")


# ---------------------------------------------------------------------------
# Example-to-cases conversion
# ---------------------------------------------------------------------------


def unparsed_page_cases(slug: str) -> CasesResult:
    """Build the empty cases result used when a FastPrep page does not parse."""
    return CasesResult("solve", [], f"FastPrep page for {slug} did not parse")


def cases_from_record(problem: dict) -> CasesResult:
    """Convert a FastPrep problem record into harness cases.

    Every example input must parse to a JSON-representable literal for its
    declared scalar type, and the output must parse the same way; otherwise
    the problem yields an empty case list with a skip reason naming the slug.

    Args:
        problem: The parsed FastPrep problem record.

    Returns:
        A CasesResult with the function name, the cases, and a skip reason
        (None) exactly when at least one case exists.
    """
    slug = str(problem.get("id", "unknown-slug"))
    function_name = str(problem.get("functionName") or "solve")
    examples = problem.get("examples") or []
    cases: List[dict] = []
    for example in examples:
        inputs = example.get("inputText") or []
        if not inputs:
            return CasesResult(
                function_name, [], f"examples have no inputs for {slug}"
            )
        if any(
            str(item.get("inputName", "")).lower() in DESIGN_INPUT_NAMES
            for item in inputs
        ):
            return CasesResult(
                function_name,
                [],
                f"design-operation example for {slug} is not `==`-assertable",
            )
        args: List[Any] = []
        for item in inputs:
            value = parse_typed_value(item)
            if value is _UNPARSEABLE:
                return CasesResult(
                    function_name,
                    [],
                    f"example input {item.get('inputName')!r} for {slug} "
                    "is not JSON-representable",
                )
            args.append(value)
        output_type = str(example.get("outputType", "")).lower()
        if output_type.startswith("treenode"):
            return CasesResult(
                function_name,
                [],
                f"tree output for {slug} is not `==`-assertable: the method "
                "returns a TreeNode, which never equals a list",
            )
        expected = parse_scalar_literal(str(example.get("outputText", "")))
        if expected is _UNPARSEABLE:
            return CasesResult(
                function_name,
                [],
                f"example output for {slug} is not JSON-representable",
            )
        cases.append({"id": f"example_{example.get('id', len(cases) + 1)}", "args": args, "expected": expected})
    if not cases:
        return CasesResult(function_name, [], f"no examples on the page for {slug}")
    return CasesResult(function_name, cases, None)


_UNPARSEABLE = object()


def parse_typed_value(item: dict) -> Any:
    """Parse one typed example input, honoring its declared type.

    Args:
        item: An inputText entry (`inputName`, `inputValue`, `inputType`).

    Returns:
        The parsed Python value, or the _UNPARSEABLE sentinel when the type is
        structural (trees, lists, graphs) or the literal does not parse.
    """
    input_type = str(item.get("inputType", "")).lower()
    base_type = re.sub(r"[\[\] ]|list<|vector<|>", "", input_type)
    if not base_type or base_type not in SCALAR_TYPES:
        return _UNPARSEABLE
    return parse_scalar_literal(str(item.get("inputValue", "")))


def parse_scalar_literal(raw: str) -> Any:
    """Parse a literal that may be JSON or Python spelling.

    Args:
        raw: The raw literal text (e.g. `[2,3,1,5,4]`, `'abcabc'`, `10`).

    Returns:
        The parsed value, or the _UNPARSEABLE sentinel. JSON `null` anywhere
        in the literal makes it unparseable: no case may hinge on None.
    """
    text = raw.strip()
    if not text:
        return _UNPARSEABLE
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        try:
            return ast.literal_eval(text)
        except (ValueError, SyntaxError):
            return _UNPARSEABLE
    if parsed is not None and _contains_null(parsed):
        return _UNPARSEABLE
    return parsed


def _contains_null(value: Any) -> bool:
    """Report whether a parsed JSON value contains `null` anywhere."""
    if value is None:
        return True
    if isinstance(value, list):
        return any(_contains_null(item) for item in value)
    if isinstance(value, dict):
        return any(_contains_null(item) for item in value.values())
    return False


# ---------------------------------------------------------------------------
# Scaffold rendering
# ---------------------------------------------------------------------------


def extract_statement_from_page(page_html: str) -> str:
    """Extract the server-rendered statement HTML from a FastPrep page.

    Returns:
        The inner HTML of the `fp-statement-content` div, or "" when the page
        carries no such section.
    """
    start = page_html.find(STATEMENT_CONTENT_MARKER)
    if start == -1:
        return ""
    start += len(STATEMENT_CONTENT_MARKER)
    end = page_html.find(STATEMENT_SECTION_END, start)
    if end == -1:
        return ""
    return page_html[start:end].strip()


def resolve_statement(problem: Optional[dict], page_html: str) -> str:
    """Pick the best available statement HTML for a problem.

    Some flight-data records carry a shredded statement (katex markup reduced
    the prose to fragments like "$23"); when the record statement renders
    implausibly short, the statement is recovered from the server-rendered
    page instead.

    Args:
        problem: Parsed FastPrep record, or None when the page failed to parse.
        page_html: Raw HTML of the FastPrep problem page.

    Returns:
        Statement HTML; empty when nothing plausible exists (the caller then
        renders the statement placeholder).
    """
    raw = str((problem or {}).get("problemStatement") or "")
    if len(rendered_statement_text(raw)) >= MIN_PLAUSIBLE_STATEMENT_LENGTH:
        return raw
    recovered = extract_statement_from_page(page_html or "")
    return recovered or raw


def render_writeup(entry: dict, problem: Optional[dict], statement_html: Optional[str] = None) -> str:
    """Render the statement write-up scaffold for one problem.

    Args:
        entry: Manifest entry for the problem.
        problem: Parsed FastPrep record, or None when the page failed to parse.
        statement_html: Statement source chosen by resolve_statement; when
            None, the record's own problemStatement is used without recovery.

    Returns:
        Write-up markdown following the docs/leetcode/_TEMPLATE.md section
        order, with solution sections left as explicit placeholders.
    """
    if statement_html is None:
        statement_html = str((problem or {}).get("problemStatement") or "")
    statement = rendered_statement_text(statement_html)
    if len(statement) < MIN_PLAUSIBLE_STATEMENT_LENGTH:
        # Shredded flight-data statements render as meaningless fragments;
        # the explicit placeholder beats garbage.
        statement = ""
    parts: List[str] = [
        f"# [{entry['title']}]({entry['url']})",
        "",
        difficulty_line(problem),
        "",
        statement or "<!-- Statement not parseable from FastPrep; fill it in. -->",
        "",
        "## Examples",
        "",
    ]
    parts.extend(render_examples(problem, entry["slug"]))
    parts.extend(["## Constraints", ""])
    parts.extend(render_constraints(problem, entry["slug"]))
    parts.extend(
        [
            "## Solutions",
            "",
            f"{WRITEUP_PLACEHOLDER_MARKER} the worked derivation and write-up land",
            "     on main later. See ../../leetcode/_TEMPLATE.md for the",
            "     expected layout, naming, and ordering conventions. -->",
            "",
        ]
    )
    return "\n".join(parts).rstrip() + "\n"


def cases_are_authored(cases_path: Path) -> bool:
    """Report whether a committed cases.json holds hand-authored cases.

    Mirrors writeup_is_authored on the practice side: a page that parses to
    no harness cases would otherwise have its empty cases.json, stub, and
    test module rewritten on every run, wiping cases authored after the
    scaffold was born (trees, design sequences, free-text outputs). A
    non-empty JSON list is exactly the authored state; the empty scaffold
    state stays generator-owned and keeps refreshing.

    Args:
        cases_path: Path to the committed cases.json.

    Returns:
        True when the file exists and parses to a non-empty JSON list.
    """
    return bool(_json_list_file(cases_path))


def committed_cases_are_authored(entry: dict, cases_path: Path) -> bool:
    """Report whether a slug's cases.json is hand-owned, per the committed manifest.

    A `parsed-with-cases` entry's non-empty cases.json is the generator's
    own last render, never hand-authored; only a non-empty list under any
    other committed parse_status counts as authored. Emission and check
    share this predicate so the two sides cannot drift.

    Args:
        entry: Manifest entry whose committed parse_status classifies the
            folder (emission reads it before any in-pass rewrite).
        cases_path: Path to the committed cases.json.

    Returns:
        True when the committed parse_status is not `parsed-with-cases`
        and the file parses to a non-empty JSON list.
    """
    return entry.get("parse_status") != "parsed-with-cases" and cases_are_authored(
        cases_path
    )


def _split_writeup_sections(text: str) -> List[str]:
    """Split a write-up into [header, section, ...] at `## ` headings.

    Each section segment starts at its heading line and runs to the next
    heading (or end of text); the first segment holds everything before the
    first heading (title, metadata line, statement).
    """
    boundaries = list(WRITEUP_SECTION_HEADING_PATTERN.finditer(text))
    if not boundaries:
        return [text]
    segments = [text[: boundaries[0].start()]]
    for position, boundary in enumerate(boundaries):
        end = (
            boundaries[position + 1].start()
            if position + 1 < len(boundaries)
            else len(text)
        )
        segments.append(text[boundary.start() : end])
    return segments


def _section_carries_content(segment: str) -> bool:
    """Report whether a write-up section holds anything but HTML comments.

    The leading `## ` heading line is not content; a section whose every
    other non-blank line is a scaffold placeholder comment is a marker
    hole. The header segment carries no heading line and is checked whole.
    """
    if segment.startswith("## "):
        segment = segment.split("\n", 1)[1] if "\n" in segment else ""
    return bool(HTML_COMMENT_PATTERN.sub("", segment).strip())


def committed_only_sections(committed_text: str, fresh_text: str) -> List[str]:
    """Return committed sections the fresh placeholder has no heading for.

    A section qualifies when its heading line is absent from the fresh
    render and the section carries non-marker content. The death merge
    appends these after the fresh-driven loop (the union), and the
    emission loop names them in the run log so a carried archive section
    stays auditable.

    Args:
        committed_text: The committed write-up markdown.
        fresh_text: The freshly rendered placeholder write-up for the same
            entry.

    Returns:
        The qualifying committed sections, in committed order; empty when
        every committed section has a fresh counterpart or is a marker
        hole.
    """
    fresh_headings = {
        section.splitlines()[0] for section in _split_writeup_sections(fresh_text)[1:]
    }
    return [
        section
        for section in _split_writeup_sections(committed_text)[1:]
        if section.splitlines()[0] not in fresh_headings
        and _section_carries_content(section)
    ]


def preserve_writeup_on_death(committed_text: str, fresh_text: str) -> str:
    """Merge a committed write-up with a fresh placeholder after page death.

    When a FastPrep page has died (page-unparseable), a fresh render has no
    upstream content to offer, so re-rendering a committed write-up would
    destroy the repo's only copy of the archived statement, examples, and
    constraints (the F1 wipe mechanism). This merge keeps every committed
    section that carries non-marker content: the archived sections, and
    the header whose metadata line feeds the manifest rebuild. It fills
    only the marker holes (sections whose sole content is placeholder
    comments, i.e. the Solutions scaffold) exactly as a fresh placeholder
    would. Committed sections whose headings the fresh render lacks are
    unioned in after the template sections, so a hand-added archived
    section survives the page death too.

    Args:
        committed_text: The committed write-up markdown.
        fresh_text: The freshly rendered placeholder write-up for the same
            entry (from render_writeup with no parsed problem).

    Returns:
        The merged write-up. Equals `fresh_text` when the committed text is
        a pure placeholder; byte-stable across repeated runs once the
        archived sections are in place.
    """
    committed_sections = _split_writeup_sections(committed_text)
    fresh_sections = _split_writeup_sections(fresh_text)
    committed_by_heading = {
        section.splitlines()[0]: section for section in committed_sections[1:]
    }
    if _section_carries_content(committed_sections[0]):
        merged = [committed_sections[0]]
    else:
        merged = [fresh_sections[0]]
    for fresh_section in fresh_sections[1:]:
        committed_section = committed_by_heading.get(fresh_section.splitlines()[0])
        if committed_section and _section_carries_content(committed_section):
            merged.append(committed_section)
        else:
            merged.append(fresh_section)
    merged.extend(committed_only_sections(committed_text, fresh_text))
    return "".join(merged)


def writeup_is_authored(writeup_path: Path) -> bool:
    """Report whether a committed write-up has left the scaffold state.

    Placeholder write-ups carry WRITEUP_PLACEHOLDER_MARKER and stay
    generator-owned, so emission keeps refreshing them (an upstream
    statement change updates the scaffold). Any body without the marker is
    hand-authored and emission must leave it untouched.

    Args:
        writeup_path: Path to the committed write-up markdown.

    Returns:
        True when the file exists and no longer carries the placeholder
        marker; False when it is absent or still a placeholder.
    """
    if not writeup_path.exists():
        return False
    return WRITEUP_PLACEHOLDER_MARKER not in writeup_path.read_text(encoding="utf-8")


def difficulty_line(problem: Optional[dict]) -> str:
    """Render the template's metadata line from parsed data or placeholders."""
    difficulty = (problem or {}).get("difficulty")
    topics = (problem or {}).get("topics") or []
    if difficulty:
        difficulty_text = f"**{str(difficulty).capitalize()}**"
    else:
        difficulty_text = "**unknown difficulty**"
    minutes_text = "**NN minutes**"
    topics_text = ", ".join(str(topic).replace("_", " ").title() for topic in topics) if topics else "unknown categories"
    return f"{difficulty_text} | {minutes_text} | **{topics_text}**"


def render_examples(problem: Optional[dict], slug: str) -> List[str]:
    """Render the Examples section from parsed examples or a placeholder."""
    examples = (problem or {}).get("examples") or []
    if not examples:
        return [
            f"<!-- Examples not parseable from FastPrep for {slug}; fill them in. -->",
            "",
        ]
    lines: List[str] = []
    for index, example in enumerate(examples, start=1):
        lines.append(f"### Example {index}")
        lines.append("")
        inputs_text = ", ".join(
            f"`{item.get('inputName')} = {item.get('inputValue')}`"
            for item in example.get("inputText") or []
        )
        lines.append(f"**Input:** {inputs_text}")
        lines.append("")
        lines.append(f"**Output:** `{example.get('outputText')}`")
        explanation = html_to_markdown(str(example.get("explanation") or ""))
        if explanation:
            lines.append("")
            lines.append(f"**Explanation:** {explanation}")
        lines.append("")
    return lines


def load_constraints_overrides(path: Optional[Path] = None) -> dict:
    """Load the committed slug -> constraint-bullet overrides.

    FastPrep ships no constraints block on some problem pages, so their
    generator-owned write-ups would render an empty Constraints section on
    every refresh. This hand-editable file supplies those sections: each
    entry maps a manifest slug to the bullet strings rendered verbatim.
    An absent file is the empty mapping (the revert path: deleting it and
    regenerating restores the placeholders); anything present must be one
    JSON object whose values are non-empty lists of non-empty strings.

    Args:
        path: Path to amazon_constraints_overrides.json; None (the
            default) means the module constant, resolved at call time so
            tests can repoint it.

    Returns:
        The slug -> bullet-strings mapping, empty when the file is absent.

    Raises:
        SystemExit: When the file is unreadable, invalid JSON, not a JSON
            object, or an entry is not a non-empty list of non-empty
            strings.
    """
    if path is None:
        path = CONSTRAINTS_OVERRIDES_PATH
    try:
        overrides = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SystemExit(f"constraints overrides {path} is not valid JSON: {error}")
    if not isinstance(overrides, dict):
        raise SystemExit(f"constraints overrides {path} must be a JSON object")
    for slug, bullets in overrides.items():
        if (
            not isinstance(bullets, list)
            or not bullets
            or not all(isinstance(text, str) and text.strip() for text in bullets)
        ):
            raise SystemExit(
                f"constraints override for {slug!r} must be a non-empty list"
                " of non-empty constraint strings"
            )
    return overrides


def render_constraints(
    problem: Optional[dict],
    slug: str,
    constraints_overrides: Optional[Mapping[str, List[str]]] = None,
) -> List[str]:
    """Render the Constraints section from parsed constraints or a placeholder.

    A page whose parse yields no constraints falls back to the committed
    slug -> bullets override map (the committed file when the argument is
    None, mirroring render_index's difficulty_overrides); a slug the map
    does not address keeps the placeholder comment.

    Args:
        problem: Parsed FastPrep record, or None when the page failed to
            parse.
        slug: The FastPrep problem slug the section renders for.
        constraints_overrides: Slug -> bullet strings consulted on an
            empty parse; None (the default) means the committed overrides
            file.

    Returns:
        The section's markdown lines, with a trailing blank line.
    """
    raw_constraints = str((problem or {}).get("constraints") or "").strip()
    if not raw_constraints:
        overrides = (
            load_constraints_overrides()
            if constraints_overrides is None
            else constraints_overrides
        )
        bullets = overrides.get(slug)
        if bullets:
            return [f"- `{text}`" for text in bullets] + [""]
        return [
            f"<!-- Constraints not parseable from FastPrep for {slug}; fill them in. -->",
            "",
        ]
    lines = [f"- `{text}`" for text in split_constraints(raw_constraints)]
    return lines + [""]


def strip_contributor_chrome(statement: str) -> str:
    """Drop contributor-credit chrome lines from a statement.

    Args:
        statement: Statement text after HTML-to-markdown conversion.

    Returns:
        The statement with every `Special thanks:` line and its trailing
        blank line removed; a leading removal never leaves a blank first
        line.
    """
    stripped = CONTRIBUTOR_CHROME_PATTERN.sub("", statement)
    collapsed = re.sub(r"\n{3,}", "\n\n", stripped)
    return re.sub(r"^\n+", "", collapsed).strip()


def rendered_statement_text(statement_html: str) -> str:
    """Convert statement HTML to markdown without contributor-credit chrome."""
    return strip_contributor_chrome(html_to_markdown(statement_html))


def html_to_markdown(fragment: str) -> str:
    """Convert the small HTML subset FastPrep uses to plain markdown text.

    Block-level tags separate the blocks they bound: both the opening and
    closing tag emit a paragraph break, so a run-in `<h3>` heading or a
    `<ul>` of method specs never glues to the neighboring sentence. `<br>`
    and `<li>` emit single line breaks; inline tags are stripped bare. A
    `<` in prose that opens no plausible tag is kept as a literal `<`.
    """
    text = HTML_COMMENT_PATTERN.sub("", fragment)
    text = PROSE_LESS_THAN_PATTERN.sub("&lt;", text)
    text = re.sub(r"<sup>(.*?)</sup>", r"^\1", text, flags=re.S | re.I)
    text = re.sub(
        r"(?i)</?(?:p|h[1-6]|ul|ol|pre|blockquote|div|table|tr)\b[^>]*>",
        "\n\n",
        text,
    )
    text = re.sub(r"(?i)<li\b[^>]*>", "\n", text)
    text = re.sub(r"(?i)</li>", "", text)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    # Source indentation after a blank line would render as markdown code
    # blocks; statement prose always sits at the left margin.
    text = re.sub(r"(?m)^[ \t]+", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return html.unescape(text).strip()


def split_constraints(raw_constraints: str) -> List[str]:
    """Split a raw constraints payload into one string per constraint.

    FastPrep ships constraints as an HTML list (`<ul><li>...</li></ul>`);
    pages without list markup fall back to `<br>`/newline separation.
    """
    items = CONSTRAINT_LIST_ITEM_PATTERN.findall(raw_constraints)
    if not items:
        items = re.split(r"<br\s*/?>|\\n|\n", raw_constraints)
    return [text for text in (html_to_markdown(item).strip() for item in items) if text]


def _arg_holds_data(value: Any) -> bool:
    """Report whether one case argument carries data to debug against.

    Non-empty collections and non-empty strings do; zero, False, and empty
    containers leave nothing to inspect in a debug run.
    """
    if isinstance(value, (list, tuple, dict, set, str)):
        return len(value) > 0
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    return value is not None


def pick_default_case_id(cases: Sequence[dict]) -> Optional[str]:
    """Pick the CASE id a rendered stub should start from.

    Prefers the first non-degenerate case: one whose args hold data (a
    non-empty collection or a nonzero scalar), since debugging against a
    leading empty-container case inspects nothing. Falls back to the first
    id when every case is degenerate; None when no cases exist, which
    renders the stub's no-cases __main__ with the pick_case debug run
    guarded behind the guidance print.

    Args:
        cases: Harness cases (`[{"id", "args", "expected"}]`).

    Returns:
        The preferred case id, or None when `cases` is empty.
    """
    for case in cases:
        if any(_arg_holds_data(arg) for arg in case["args"]):
            return case["id"]
    return cases[0]["id"] if cases else None


def render_solution_stub(
    entry: dict,
    problem: Optional[dict],
    parsed_cases: CasesResult,
    statement_html: Optional[str] = None,
) -> str:
    """Render the NotSolved practice stub in the two_sum house style."""
    if statement_html is None:
        statement_html = str((problem or {}).get("problemStatement") or "")
    rendered_summary = rendered_statement_text(statement_html).split("\n")[0]
    summary = (
        rendered_summary[:200] if len(rendered_summary) >= MIN_PLAUSIBLE_STATEMENT_LENGTH else ""
    ) or "Amazon OA problem."
    case_id = pick_default_case_id(parsed_cases.cases)
    function_name = parsed_cases.function_name
    args_signature = _signature_args(problem)
    writeup_link = WRITEUP_LINK_TEMPLATE.format(slug=entry["slug"])
    if case_id is None:
        main_block = f'''if __name__ == "__main__":
    # Debug playground: set a breakpoint in {function_name} above, then run this file.
    CASE = None
    if CASE is None:
        print("no cases authored yet; add cases to cases.json or cases_full.json, then set CASE to an id")
    else:
        case = pick_case(__file__, CASE)
        result = Solution().{function_name}(*case["args"])
        print(f"case {{case['id']}}: args = {{case['args']}}")
        print(f"expected: {{case['expected']}}")
        print(f"got:      {{result}}")
'''
    else:
        main_block = f'''if __name__ == "__main__":
    # Debug playground: set a breakpoint in {function_name} above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "{case_id}"
    case = pick_case(__file__, CASE)
    result = Solution().{function_name}(*case["args"])
    print(f"case {{case['id']}}: args = {{case['args']}}")
    print(f"expected: {{case['expected']}}")
    print(f"got:      {{result}}")
'''
    return f'''"""{entry["title"]} — {entry["url"]}

Write-up & approaches: {writeup_link}

{summary}
{render_command_block(entry["slug"])}"""

from harness import NotSolved, pick_case


class Solution:
    def {function_name}(self{args_signature}):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


{main_block}'''


def _signature_args(problem: Optional[dict]) -> str:
    """Build the plain-argument list for the stub signature from example inputs.

    Python keywords in FastPrep input names are suffixed with `_` so the
    generated signature stays syntactically valid.
    """
    examples = (problem or {}).get("examples") or []
    inputs = (examples[0].get("inputText") or []) if examples else []
    if inputs:
        names = (str(item.get("inputName")) for item in inputs)
        return "".join(
            f", {name}_" if keyword.iskeyword(name) else f", {name}" for name in names
        )
    return ", *args"


def render_cases_file(parsed_cases: CasesResult) -> str:
    """Render the cases.json content (always present, `[]` when unparseable)."""
    return json.dumps(parsed_cases.cases, indent=2) + "\n"


def _python_literal(value: Any, indent: int = 0) -> str:
    """Render a value as a readable Python literal for embedding in test files.

    json.dumps would emit `null`/`true`, which are invalid Python; the harness
    cases are plain data (str, int, float, bool, list, dict, None), so a
    structured repr keeps generated test modules importable.
    """
    if isinstance(value, dict):
        if not value:
            return "{}"
        inner_indent = indent + 4
        pad = " " * inner_indent
        close_pad = " " * indent
        items = ",\n".join(
            f"{pad}{json.dumps(str(key))}: {_python_literal(item, inner_indent)}"
            for key, item in value.items()
        )
        return "{\n" + items + ",\n" + close_pad + "}"
    if isinstance(value, list):
        if not value:
            return "[]"
        inner_indent = indent + 4
        pad = " " * inner_indent
        close_pad = " " * indent
        items = ",\n".join(f"{pad}{_python_literal(item, inner_indent)}" for item in value)
        return "[\n" + items + ",\n" + close_pad + "]"
    return repr(value)


def render_test(entry: dict, function_name: str, cases: List[dict], skip_reason: Optional[str]) -> str:
    """Render the harness-driven test module in the merge_commits house style.

    No local pytest.ini: the root practice/pytest.ini governs nested
    directories. With an empty case list the module skips with a reason naming
    the slug so an unparseable problem never silently passes.
    """
    reason = skip_reason or "no cases parsed"
    case_list = _python_literal(cases)
    writeup_link = WRITEUP_LINK_TEMPLATE.format(slug=entry["slug"])
    return f'''"""Tests for {entry["title"]} — your attempt (solution.py) against cases.json.

The worked approaches live in {writeup_link}.
"""

import pytest

from harness import NotSolved, load_solution

CASES = {case_list}

if len(CASES) == 0:
    pytest.skip("{reason}", allow_module_level=True)

solution = load_solution(__file__)


def _ids(cases):
    return [case["id"] for case in cases]


def _check(method, case):
    assert method(*case["args"]) == case["expected"]


@pytest.mark.parametrize("case", CASES, ids=_ids(CASES))
def test_solution(case):
    try:
        _check(solution.Solution().{function_name}, case)
    except NotSolved:
        pytest.skip("solution.py not implemented yet")
'''


def render_index(
    manifest: Sequence[dict],
    difficulty_overrides: Optional[Mapping[str, str]] = None,
) -> str:
    """Render docs/amazon/index.md, most-recent first.

    Columns follow the unified catalog's conventions: `Problem`,
    `Difficulty`, `Category`, `Time`, `Companies`, with the `Updated`
    date trailing last. The Difficulty cell
    reads the manifest entry's difficulty (backfilled from the write-up
    headers), corrected by `difficulty_overrides` where one addresses the
    slug; the unknown-difficulty rows dash. `Time` reuses the shared
    difficulty-based estimates from generate_index_tables.py and dashes
    wherever the difficulty is unknown.

    Args:
        manifest: The manifest entries (or a suffix of them under --limit),
            most-recent first, each carrying `difficulty`.
        difficulty_overrides: Slug -> difficulty consulted before each
            entry's manifest difficulty; None (the default) means the
            committed overrides file.

    Returns:
        The index markdown with a trailing newline.
    """
    overrides = (
        index_tables.load_amazon_difficulty_overrides()
        if difficulty_overrides is None
        else difficulty_overrides
    )
    lines = [
        "# Amazon OA Problems",
        "",
        "Amazon-tagged coding problems from the"
        " [Tech-OA-Interview-Questions](https://github.com/perixtar/Tech-OA-Interview-Questions)"
        " bank (statement pages on fastprep.io), most recently updated first."
        " Practice stubs live under `practice/amazon/`."
        " Time carries difficulty-based estimates"
        " (Easy 15 / Medium 25 / Hard 40 minutes, a dash where the difficulty"
        " is unknown), corrected by the committed difficulty overrides where"
        " present.",
        "",
        "| Problem | Difficulty | Category | Time | Companies | Updated |",
        "|---------|-----------|----------|------|-----------|---------|",
    ]
    for entry in manifest:
        title = f"[{entry['title']}]({entry['slug']}.md)"
        companies = ", ".join(entry["companies"])
        difficulty = overrides.get(entry["slug"]) or entry.get("difficulty")
        lines.append(
            f"| {title} |"
            f" {difficulty or index_tables.UNKNOWN_TIME_CELL} |"
            f" {entry.get('categories') or index_tables.UNKNOWN_TIME_CELL} |"
            f" {index_tables.estimated_time_cell(difficulty)} | {companies} |"
            f" {entry['updated']} |"
        )
    return "\n".join(lines) + "\n"


def render_all(
    entry: dict,
    problem: Optional[dict],
    parsed_cases: CasesResult,
    statement_html: str,
) -> Dict[Path, str]:
    """Render every scaffold file for one problem, keyed by target path.

    Shared by the emission and idempotency-check paths so the two can never
    drift apart.
    """
    slug = entry["slug"]
    return {
        DOCS_DIR / f"{slug}.md": render_writeup(entry, problem, statement_html),
        PRACTICE_DIR / slug / "solution.py": render_solution_stub(
            entry, problem, parsed_cases, statement_html
        ),
        PRACTICE_DIR / slug / "cases.json": render_cases_file(parsed_cases),
        PRACTICE_DIR / slug / f"test_{slug}.py": render_test(
            entry,
            parsed_cases.function_name,
            parsed_cases.cases,
            parsed_cases.skip_reason,
        ),
    }


# ---------------------------------------------------------------------------
# Fetching
# ---------------------------------------------------------------------------


def has_cached_page(slug: str, cache_dir: Optional[Path] = None) -> bool:
    """Report whether the problem page is available in the disk cache."""
    cache_root = cache_dir if cache_dir is not None else FASTPREP_CACHE_DIR
    return (cache_root / f"{slug}.html").exists()


def fetch_problem_page(
    slug: str,
    cache_dir: Optional[Path] = None,
    delay: bool = True,
    network: bool = True,
) -> str:
    """Fetch a FastPrep problem page through a disk cache.

    Args:
        slug: The FastPrep problem slug.
        cache_dir: Directory holding cached HTML keyed by `<slug>.html`.
        delay: Sleep politely before a network fetch (cache hits never wait).
        network: When False, never hit the network: a cache miss returns a
            marker comment the parser treats as an unparseable page.

    Returns:
        The raw HTML for the problem page, or a marker comment when the site
        answers with an HTTP error (dead bank link) or fetching is disabled;
        the caller emits placeholder scaffolds and records the slug as a
        parse failure.

    Raises:
        RuntimeError: When the network fetch fails for a non-HTTP reason.
    """
    cache_root = cache_dir if cache_dir is not None else FASTPREP_CACHE_DIR
    cache_path = cache_root / f"{slug}.html"
    if cache_path.exists():
        return cache_path.read_text(encoding="utf-8")
    if not network:
        return f"<!-- fetch skipped (cache miss): {slug} -->"
    if delay:
        time.sleep(FETCH_DELAY_SECONDS)
    request = urllib.request.Request(
        FASTPREP_URL_TEMPLATE.format(slug=slug),
        headers={"User-Agent": "grind75-scaffolder/1.0 (personal practice repo)"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        # Dead bank links (HTTP 404) yield an unparseable page; the caller
        # emits placeholder scaffolds and records the slug as a parse failure.
        return FETCH_FAILED_MARKER_TEMPLATE.format(error_code=error.code, slug=slug)
    except Exception as error:
        raise RuntimeError(f"fetching {slug} failed: {error}") from error
    cache_root.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(body, encoding="utf-8")
    return body


# ---------------------------------------------------------------------------
# Emission
# ---------------------------------------------------------------------------


def emit_scaffolds(entries: Sequence[dict], fetch: bool = True,
                   held_slugs: Collection[str] = ()) -> dict:
    """Write docs and practice scaffolds for the given manifest entries.

    Args:
        entries: Manifest entries to scaffold, most-recent first.
        fetch: When False, never hit the network and never overwrite an
            existing non-placeholder scaffold for a slug whose page is not
            cached; such slugs are reported as `skipped_no_cache` instead.
        held_slugs: Slugs whose committed copies are authoritative; each
            is skipped before any cache probe or fetch, so no held-slug
            path can reach the fetcher.

    Returns:
        Stats: `generated` (n), `cases_parsed` (n), `cases_empty` (n),
        `parse_failures` (slugs whose FastPrep page did not parse),
        `skipped_no_cache` (slugs left untouched under fetch=False),
        `held_skipped` (held slugs left untouched by construction),
        `writeups_preserved` (slugs whose authored write-up was left
        untouched), `writeups_preserved_dead_page` (slugs whose committed
        write-up sections were merged into the placeholder because the
        FastPrep page is dead), `cases_preserved` (slugs whose authored
        practice cases.json, stub, and test module were left untouched),
        `cases_conflicted` (slugs whose hand-authored practice cases.json
        met a non-empty upstream parse and was overwritten; report-only),
        `transient_parse_guard` (slugs whose committed parse_status is
        `parsed-with-cases` but whose live parse yielded no problem and
        no cases; their committed practice files and classification are
        kept and only the write-up is written, so a genuinely dead page
        surfaces for a manual decision instead of wiping the folder in
        one pass), `death_merge_union` (slugs plus the committed-only
        section headings a dead-page merge carried into the archived
        write-up).
    """
    stats = {
        "generated": 0,
        "cases_parsed": 0,
        "cases_empty": 0,
        "parse_failures": [],
        "skipped_no_cache": [],
        "held_skipped": [],
        "writeups_preserved": [],
        "writeups_preserved_dead_page": [],
        "cases_preserved": [],
        "cases_conflicted": [],
        "transient_parse_guard": [],
        "death_merge_union": [],
    }
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    PRACTICE_DIR.mkdir(parents=True, exist_ok=True)
    for entry in entries:
        slug = entry["slug"]
        if slug in held_slugs:
            stats["held_skipped"].append(slug)
            continue
        cached = has_cached_page(slug)
        if not fetch and not cached:
            # The entry was not emitted; its classification state is left
            # untouched, so an unclassified slug stays fetchable on a
            # later bank-available run.
            stats["skipped_no_cache"].append(slug)
            continue
        page_html = fetch_problem_page(slug, delay=fetch, network=fetch)
        problem = extract_problem_record(page_html)
        parsed_cases = cases_from_record(problem) if problem else unparsed_page_cases(slug)
        if problem is None:
            stats["parse_failures"].append(slug)
        statement_html = resolve_statement(problem, page_html)
        (PRACTICE_DIR / slug).mkdir(parents=True, exist_ok=True)
        writeup_path = DOCS_DIR / f"{slug}.md"
        rendered = render_all(entry, problem, parsed_cases, statement_html)
        authored_cases = committed_cases_are_authored(
            entry, PRACTICE_DIR / slug / "cases.json"
        )
        transient_parse = (
            entry.get("parse_status") == "parsed-with-cases"
            and problem is None
            and not parsed_cases.cases
        )
        if transient_parse:
            # A transient 404 or empty parse must not wipe a committed
            # case-parsed folder: the practice files and parse_status stay
            # authoritative, and a genuinely dead page surfaces under the
            # stat for a manual decision instead of a silent wipe.
            stats["transient_parse_guard"].append(slug)
            rendered = {writeup_path: rendered[writeup_path]}
        elif authored_cases and not parsed_cases.cases:
            # Authored practice cases on a page that yields none: the stub,
            # cases.json, and test module are hand-owned, so only the
            # (separately guarded) write-up remains a write target.
            stats["cases_preserved"].append(slug)
            rendered = {writeup_path: rendered[writeup_path]}
        elif authored_cases:
            # Authored practice cases meeting a live non-empty parse: the
            # upstream refresh overwrites them (the default), but the wave
            # log must name the conflict so the loss is visible.
            stats["cases_conflicted"].append(slug)
        for path, content in rendered.items():
            if path == writeup_path:
                if writeup_is_authored(writeup_path):
                    stats["writeups_preserved"].append(slug)
                    continue
                if problem is None and writeup_path.exists():
                    committed_text = writeup_path.read_text(encoding="utf-8")
                    # Dead page: the committed write-up is the only copy of
                    # the archived statement; merge it over the fresh
                    # placeholder instead of re-rendering the wipe.
                    merged_text = preserve_writeup_on_death(committed_text, content)
                    if merged_text != content:
                        stats["writeups_preserved_dead_page"].append(slug)
                    carried_sections = committed_only_sections(committed_text, content)
                    if carried_sections:
                        carried_headings = ", ".join(
                            section.splitlines()[0] for section in carried_sections
                        )
                        stats["death_merge_union"].append(f"{slug}: {carried_headings}")
                    content = merged_text
            path.write_text(content, encoding="utf-8")
        if transient_parse:
            pass
        elif parsed_cases.cases:
            entry["parse_status"] = "parsed-with-cases"
            stats["cases_parsed"] += 1
        else:
            entry["parse_status"] = (
                "parsed-empty-cases" if problem else "page-unparseable"
            )
            stats["cases_empty"] += 1
        stats["generated"] += 1
    return stats


def write_manifest(manifest: Sequence[dict]) -> None:
    """Write scripts/amazon_oa_manifest.json, most-recent first.

    Every written entry carries the shape the strict manifest load
    requires, so the tool can always reload its own output: a slug the
    emission never classified (beyond --limit, a --no-fetch skip, a
    --manifest-only bootstrap) gains parse_status None and the next
    bank-available run classifies it. slug, title, and url always come
    from the bank row or the validated load, so parse_status is the only
    key a write-time entry can lack.
    """
    for entry in manifest:
        entry.setdefault("parse_status", None)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(list(manifest), indent=2) + "\n", encoding="utf-8")


def write_index(manifest: Sequence[dict]) -> None:
    """Write docs/amazon/index.md."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "index.md").write_text(render_index(manifest), encoding="utf-8")


def ensure_nav_entry() -> bool:
    """Add the Amazon nav section to mkdocs.yml when missing.

    Returns:
        True when mkdocs.yml was modified, False when the section already exists.
    """
    text = MKTABS_PATH.read_text(encoding="utf-8")
    nav_section = (
        "  - Amazon:\n"
        "    - amazon/index.md\n"
    )
    if "  - Amazon:\n" in text:
        return False
    leetcode_marker = "  - Leetcode:\n"
    if leetcode_marker not in text:
        raise SystemExit("mkdocs.yml has no Leetcode nav section to extend")
    text = text.replace(leetcode_marker, leetcode_marker + nav_section, 1)
    MKTABS_PATH.write_text(text, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Idempotency check
# ---------------------------------------------------------------------------


class ScaffoldExpectation(NamedTuple):
    """Pinned expectation for one scaffold file.

    The file must start with `prefix` and contain every fragment in
    `required`. Prefixes pin generator-owned file heads; `required`
    fragments pin generator-owned lines that sit below cache-rendered
    content, where no byte-exact prefix can reach.
    """

    prefix: str
    required: Tuple[str, ...] = ()


def render_command_block(slug: str) -> str:
    """Render the debug command lines embedded in a solution stub docstring.

    Shared by the stub renderer and the idempotency check so the pinned
    expectation can never drift from what emission writes.
    """
    return (
        "\n"
        f"  uv run python amazon/{slug}/solution.py   # debug one case (see CASE below)\n"
        f"  uv run pytest amazon/{slug}/              # run the test sets\n"
    )


def expected_scaffold_fragments(entry: dict) -> Dict[Path, ScaffoldExpectation]:
    """Manifest-driven scaffold expectations for one problem.

    A `page-unparseable` entry was rendered entirely from the manifest, so
    its four scaffolds are compared byte-for-byte (a whole-content prefix),
    unless the committed write-up carries archived sections (a dead page
    preserved by emission, or a fully authored write-up): then only the
    generator-owned part is pinned. A death-preserved write-up is pinned on
    its Solutions scaffold block (the one section emission fills); a fully
    authored one on its title line, matching the parsed-entry convention.
    Every other entry was rendered from FastPrep data that lives only in
    the unversioned /tmp cache; the fragments the generator owns end to end
    are compared exactly instead of re-rendering from the cache: the
    write-up header, the stub/test header and write-up link docstrings,
    and the stub's two `uv run` command lines (via a required fragment,
    since the cache-rendered statement summary sits between the header and
    the commands).

    Args:
        entry: Manifest entry carrying `slug`, `title`, `url`, and
            `parse_status`.

    Returns:
        Expected fragments keyed by scaffold path; a file matches when it
        starts with the expectation's prefix and contains every required
        fragment.
    """
    slug = entry["slug"]
    if entry.get("parse_status") == "page-unparseable":
        fresh = render_all(entry, None, unparsed_page_cases(slug), "")
        expectations = {
            path: ScaffoldExpectation(prefix=content) for path, content in fresh.items()
        }
        writeup_path = DOCS_DIR / f"{slug}.md"
        if writeup_path.exists():
            committed_text = writeup_path.read_text(encoding="utf-8")
            fresh_writeup = fresh[writeup_path]
            if writeup_is_authored(writeup_path):
                expectations[writeup_path] = ScaffoldExpectation(
                    prefix=f"# [{entry['title']}]({entry['url']})\n"
                )
            elif (
                preserve_writeup_on_death(committed_text, fresh_writeup)
                != fresh_writeup
            ):
                expectations[writeup_path] = ScaffoldExpectation(
                    prefix="",
                    required=(fresh_writeup[fresh_writeup.index("## Solutions") :],),
                )
        return expectations
    writeup_link = WRITEUP_LINK_TEMPLATE.format(slug=slug)
    return {
        DOCS_DIR / f"{slug}.md": ScaffoldExpectation(
            prefix=f"# [{entry['title']}]({entry['url']})\n"
        ),
        PRACTICE_DIR / slug / "solution.py": ScaffoldExpectation(
            prefix=(
                f'"""{entry["title"]} — {entry["url"]}\n'
                f"\nWrite-up & approaches: {writeup_link}\n"
            ),
            required=(render_command_block(slug),),
        ),
        PRACTICE_DIR / slug / f"test_{slug}.py": ScaffoldExpectation(
            prefix=(
                f'"""Tests for {entry["title"]} — your attempt (solution.py) against'
                f" cases.json.\n\nThe worked approaches live in {writeup_link}.\n"
            )
        ),
    }


def _json_list_file(path: Path) -> Optional[list]:
    """Parse a file into a JSON list.

    Args:
        path: Path to the candidate JSON file.

    Returns:
        The parsed list, or None when the file is absent, unreadable,
        malformed JSON, or not a list.
    """
    if not path.exists():
        return None
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return parsed if isinstance(parsed, list) else None


def _displays(path: Path) -> str:
    """Render a scaffold path for check output, repo-relative when possible."""
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def check(manifest: Sequence[dict]) -> int:
    """Exit 0 when every scaffold on disk matches the manifest-driven state.

    Read-only: nothing is fetched, written, or rewritten; the committed
    manifest's `parse_status` drives the expectation per slug, so the check
    never depends on the /tmp bank pages or the fastprep cache. A folder
    whose committed parse_status is not `parsed-with-cases` and whose
    cases.json is an authored (non-empty) list keeps its
    stub, cases.json, and test module exempt from the generator-owned
    fragment pins (the cases.json list-validity check still applies),
    mirroring emission's authored protection.

    Args:
        manifest: The manifest entries to verify.

    Returns:
        A process exit code: 0 when identical, 1 with a diff summary otherwise.
    """
    stale: List[str] = []
    for entry in manifest:
        slug = entry["slug"]
        cases_path = PRACTICE_DIR / slug / "cases.json"
        authored_cases = committed_cases_are_authored(entry, cases_path)
        writeup_path = DOCS_DIR / f"{slug}.md"
        for path, expectation in expected_scaffold_fragments(entry).items():
            if authored_cases and path != writeup_path:
                # Hand-owned content stays unpinned, but the files must
                # exist: deleting a preserved folder's stub, cases.json, or
                # test module must fail the check like any missing scaffold.
                if not path.exists():
                    stale.append(_displays(path))
                continue
            content = path.read_text(encoding="utf-8") if path.exists() else ""
            if not content.startswith(expectation.prefix) or any(
                fragment not in content for fragment in expectation.required
            ):
                stale.append(_displays(path))
        if entry.get("parse_status") != "page-unparseable" or authored_cases:
            if _json_list_file(cases_path) is None:
                stale.append(_displays(cases_path))
    expected_index = render_index(manifest)
    index_path = DOCS_DIR / "index.md"
    if not index_path.exists() or index_path.read_text(encoding="utf-8") != expected_index:
        stale.append(_displays(DOCS_DIR / "index.md"))
    if stale:
        print(f"--check: {len(stale)} scaffold file(s) differ from the manifest-driven state:")
        for path in stale[:20]:
            print(f"  {path}")
        return 1
    print(f"--check: {len(manifest)} problems up to date")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run the generator CLI.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Process exit code.
    """
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--bank-page",
        action="append",
        type=Path,
        default=None,
        help="Bank page markdown (default: the three cached Tech-OA coding pages)",
    )
    parser.add_argument("--limit", type=int, default=None, help="Scaffold only the first N entries")
    parser.add_argument("--manifest-only", action="store_true", help="Write only the manifest")
    parser.add_argument("--no-fetch", action="store_true", help="Never hit the network (cache-only)")
    parser.add_argument("--check", action="store_true", help="Verify scaffolds match the manifest-driven state; exit 0 when up to date")
    args = parser.parse_args(argv)

    bank_pages = args.bank_page or list(DEFAULT_BANK_PAGES)
    bank_available = all(path.exists() for path in bank_pages)
    if not bank_available and args.bank_page:
        missing = next(path for path in bank_pages if not path.exists())
        raise SystemExit(f"bank page not found: {missing}")
    if args.check or not bank_available:
        # The committed manifest is the source of truth: --check never
        # depends on the bank pages or the fastprep cache, and a fresh
        # clone (no recon-scratch bank pages) still runs from the commit.
        # Offline, the committed manifest is itself the hold list: every
        # slug is held and emission is a no-op.
        manifest = load_committed_manifest(MANIFEST_PATH)
        held_slugs = {entry["slug"] for entry in manifest}
        source = "committed manifest fallback"
    else:
        manifest = build_manifest([path.read_text(encoding="utf-8") for path in bank_pages])
        source = "built from bank pages"
        # The committed manifest classifies, the bank pages enrich: a built
        # entry carries no parse_status, and emission's preservation and
        # conflict predicates read the committed classification, so the
        # seed must land before emission. Only genuinely classified
        # committed slugs are held: a null parse_status (a --manifest-only
        # bootstrap, a --limit overshoot, a --no-fetch skip) stays
        # fetchable, and the next bank-available run classifies it.
        committed_by_slug = {
            entry["slug"]: entry for entry in load_committed_manifest(MANIFEST_PATH)
        }
        held_slugs = {
            slug
            for slug, committed in committed_by_slug.items()
            if committed["parse_status"] is not None
        }
        for entry in manifest:
            committed = committed_by_slug.get(entry["slug"])
            if committed is not None:
                entry["parse_status"] = committed["parse_status"]
    print(f"manifest: {len(manifest)} Amazon-tagged coding problems ({source})")
    if args.manifest_only:
        write_manifest(manifest)
        return 0

    entries = manifest[: args.limit] if args.limit else manifest
    if args.check:
        # --check is read-only verification: it must not rewrite the manifest.
        return check(entries)

    ensure_nav_entry()
    write_index(entries if args.limit else manifest)
    stats = emit_scaffolds(
        entries, fetch=not args.no_fetch and bank_available, held_slugs=held_slugs
    )
    # Written after emission so entries carry the parse_status set there.
    write_manifest(manifest)
    print(
        "scaffolds: {generated} generated | cases: {parsed} parsed, {empty} empty"
        " (skip with reason) | pages failed to parse: {failed}".format(
            generated=stats["generated"],
            parsed=stats["cases_parsed"],
            empty=stats["cases_empty"],
            failed=len(stats["parse_failures"]),
        )
    )
    if stats["parse_failures"]:
        print("parse failures: " + ", ".join(stats["parse_failures"]))
    if stats["transient_parse_guard"]:
        print(
            "transient parse guard (committed parsed-with-cases kept, live"
            " parse yielded nothing; manual decision owed): "
            + ", ".join(stats["transient_parse_guard"])
        )
    if stats["held_skipped"]:
        print(
            "held (committed copies authoritative, untouched): "
            f"{len(stats['held_skipped'])}"
        )
    if stats["skipped_no_cache"]:
        print(
            "skipped (no cache, fetch disabled, existing scaffolds kept): "
            + ", ".join(stats["skipped_no_cache"])
        )
    if stats["writeups_preserved"]:
        print(
            "write-ups preserved (authored, left untouched): "
            + ", ".join(stats["writeups_preserved"])
        )
    if stats["writeups_preserved_dead_page"]:
        print(
            "write-ups preserved (dead page, archived sections kept): "
            + ", ".join(stats["writeups_preserved_dead_page"])
        )
    if stats["death_merge_union"]:
        print(
            "death merge union (committed-only archived sections carried): "
            + ", ".join(stats["death_merge_union"])
        )
    if stats["cases_preserved"]:
        print(
            "practice cases preserved (authored, left untouched): "
            + ", ".join(stats["cases_preserved"])
        )
    if stats["cases_conflicted"]:
        print(
            "practice cases conflicted (authored cases.json met a non-empty"
            " upstream parse and was overwritten): "
            + ", ".join(stats["cases_conflicted"])
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
