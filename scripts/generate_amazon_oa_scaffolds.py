"""Generate the Amazon OA coding problem bank for grind75.

Pipeline:
  1. Parse the cached Tech-OA bank pages, keep Amazon-tagged coding rows,
     dedup by FastPrep slug, and sort most-recently-updated first.
  2. Write scripts/amazon_oa_manifest.json.
  3. For each manifest entry, fetch the FastPrep problem page (disk cache,
     polite delay), parse the statement/examples/constraints, and emit:
       - docs/problems/amazon_oa/<slug>.md   (statement write-up scaffold)
       - practice/amazon_oa/<slug>/solution.py   (NotSolved stub)
       - practice/amazon_oa/<slug>/cases.json    (parseable examples, else [])
       - practice/amazon_oa/<slug>/test_<slug>.py (harness-driven tests)

Cases contract: a case is emitted only when every example value parses to a
JSON-representable literal assertable with `==` against the method's return
value. Trees, linked lists, graphs, design-operation sequences, and free-text
outputs produce an empty cases.json and a test module that skips with a reason
naming the slug. Empty is never a silent pass.

Offline contract: the committed scripts/amazon_oa_manifest.json (with its
per-slug parse_status) is the source of truth. When the bank pages under /tmp
are absent (any fresh clone), every mode falls back to the committed manifest,
and --check compares the tree against manifest-driven expectations, never
against a re-render from the unversioned fastprep cache.

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
from typing import Any, Dict, List, Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "scripts" / "amazon_oa_manifest.json"
DOCS_DIR = REPO_ROOT / "docs" / "problems" / "amazon_oa"
PRACTICE_DIR = REPO_ROOT / "practice" / "amazon_oa"
TEMPLATE_PATH = REPO_ROOT / "docs" / "problems" / "_TEMPLATE.md"
MKTABS_PATH = REPO_ROOT / "mkdocs.yml"

DEFAULT_BANK_PAGES = (
    Path("/tmp/opencode/tech-oa/coding.md"),
    Path("/tmp/opencode/tech-oa/coding-page-2.md"),
)
FASTPREP_CACHE_DIR = Path("/tmp/opencode/fastprep-cache")
FASTPREP_URL_TEMPLATE = "https://www.fastprep.io/problems/{slug}"
FETCH_DELAY_SECONDS = 0.5
AMAZON_TAG = "Amazon"
WRITEUP_LINK_TEMPLATE = "../../../docs/problems/amazon_oa/{slug}.md"
# Site-relative links cannot reach the practice/ tree outside the mkdocs
# docs_dir; the published site gets the absolute repo URL instead.
PRACTICE_INDEX_URL = (
    "https://github.com/ThoDHa/tech-interview-prep/tree/main/practice/amazon_oa/"
)

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
        page_text: Raw markdown of a bank page (coding.md / coding-page-2.md).

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

    Args:
        page_texts: Raw markdown of each bank page, in any order.

    Returns:
        Manifest entries (`slug`, `title`, `url`, `companies`, `updated`)
        sorted by `updated` descending with slug-ascending tie-break. When a
        slug appears on several pages the most recently updated row wins.
    """
    by_slug: Dict[str, dict] = {}
    for page_text in page_texts:
        for row in parse_bank_rows(page_text):
            if AMAZON_TAG not in row["companies"]:
                continue
            existing = by_slug.get(row["slug"])
            if existing is None or row["updated"] > existing["updated"]:
                by_slug[row["slug"]] = row
    entries = sorted(by_slug.values(), key=lambda row: row["slug"])
    entries.sort(key=lambda row: row["updated"], reverse=True)
    return [
        {
            "slug": row["slug"],
            "title": row["title"],
            "url": row["url"],
            "companies": row["companies"],
            "updated": row["updated"],
        }
        for row in entries
    ]


def load_committed_manifest(path: Path = MANIFEST_PATH) -> List[dict]:
    """Load the committed manifest, the offline source of truth.

    The bank pages under /tmp are recon scratch, absent on any fresh clone;
    every generation mode must be able to run from the committed manifest
    alone.

    Args:
        path: Path to the manifest JSON (default: scripts/amazon_oa_manifest.json).

    Returns:
        The manifest entries in committed order, each carrying its
        `parse_status`.

    Raises:
        SystemExit: When the manifest file is missing or is not valid JSON.
    """
    try:
        entries = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, UnicodeDecodeError) as error:
        raise SystemExit(f"committed manifest unusable: {error}; run the generator once with the bank pages present")
    except json.JSONDecodeError as error:
        raise SystemExit(f"committed manifest {path} is not valid JSON: {error}")
    if not isinstance(entries, list):
        raise SystemExit(f"committed manifest {path} must be a JSON list")
    return entries


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
    if len(html_to_markdown(raw)) >= MIN_PLAUSIBLE_STATEMENT_LENGTH:
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
        Write-up markdown following the docs/problems/_TEMPLATE.md section
        order, with solution sections left as explicit placeholders.
    """
    if statement_html is None:
        statement_html = str((problem or {}).get("problemStatement") or "")
    statement = html_to_markdown(statement_html)
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
            "<!-- Scaffold placeholder: the worked derivation and solutions land",
            "     on the solutions branch later. See ../_TEMPLATE.md for the",
            "     expected layout, naming, and ordering conventions. -->",
            "",
        ]
    )
    return "\n".join(parts).rstrip() + "\n"


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


def render_constraints(problem: Optional[dict], slug: str) -> List[str]:
    """Render the Constraints section from parsed constraints or a placeholder."""
    raw_constraints = str((problem or {}).get("constraints") or "").strip()
    if not raw_constraints:
        return [
            f"<!-- Constraints not parseable from FastPrep for {slug}; fill them in. -->",
            "",
        ]
    lines = [f"- `{text}`" for text in split_constraints(raw_constraints)]
    return lines + [""]


def html_to_markdown(fragment: str) -> str:
    """Convert the small HTML subset FastPrep uses to plain markdown text."""
    text = re.sub(r"<!--.*?-->", "", fragment, flags=re.S)
    text = re.sub(r"<sup>(.*?)</sup>", r"^\1", text, flags=re.S | re.I)
    text = text.replace("</p>", "\n\n")
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"</?(p|code|pre|strong|em|b|i|ul|li|sup)[^>]*>", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    # Source indentation after a blank line would render as markdown code
    # blocks; statement prose always sits at the left margin.
    text = re.sub(r"(?m)^[ \t]+", "", text)
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


def render_solution_stub(
    entry: dict,
    problem: Optional[dict],
    parsed_cases: CasesResult,
    statement_html: Optional[str] = None,
) -> str:
    """Render the NotSolved practice stub in the two_sum house style."""
    if statement_html is None:
        statement_html = str((problem or {}).get("problemStatement") or "")
    rendered_summary = html_to_markdown(statement_html).split("\n")[0]
    summary = (
        rendered_summary[:200] if len(rendered_summary) >= MIN_PLAUSIBLE_STATEMENT_LENGTH else ""
    ) or "Amazon OA problem."
    case_id = parsed_cases.cases[0]["id"] if parsed_cases.cases else "example_1"
    function_name = parsed_cases.function_name
    args_signature = _signature_args(problem)
    writeup_link = WRITEUP_LINK_TEMPLATE.format(slug=entry["slug"])
    return f'''"""{entry["title"]} — {entry["url"]}

Write-up & approaches: {writeup_link}

{summary}

  uv run python amazon_oa/{entry["slug"]}/solution.py   # debug one case (see CASE below)
  uv run pytest amazon_oa/{entry["slug"]}/              # run the test sets
"""

from harness import NotSolved, pick_case


class Solution:
    def {function_name}(self{args_signature}):
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


if __name__ == "__main__":
    # Debug playground: set a breakpoint in {function_name} above, then run this file.
    # Pick a case by id (ids are in cases.json).
    CASE = "{case_id}"
    case = pick_case(__file__, CASE)
    result = Solution().{function_name}(*case["args"])
    print(f"case {{case['id']}}: args = {{case['args']}}")
    print(f"expected: {{case['expected']}}")
    print(f"got:      {{result}}")
'''


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


def render_index(manifest: Sequence[dict]) -> str:
    """Render docs/problems/amazon_oa/index.md, most-recent first."""
    lines = [
        "# Amazon OA Problems",
        "",
        "Amazon-tagged coding problems from the"
        " [Tech-OA-Interview-Questions](https://github.com/perixtar/Tech-OA-Interview-Questions)"
        " bank (statement pages on fastprep.io), most recently updated first."
        f" Practice stubs live under [`practice/amazon_oa/`]({PRACTICE_INDEX_URL}).",
        "",
        "| Updated | Problem | Companies |",
        "|---------|---------|-----------|",
    ]
    for entry in manifest:
        title = f"[{entry['title']}]({entry['slug']}.md)"
        companies = ", ".join(entry["companies"])
        lines.append(
            f"| {entry['updated']} | {title} | {companies} |"
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
        return f"<!-- fetch failed: HTTP {error.code} for {slug} -->"
    except Exception as error:
        raise RuntimeError(f"fetching {slug} failed: {error}") from error
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(body, encoding="utf-8")
    return body


# ---------------------------------------------------------------------------
# Emission
# ---------------------------------------------------------------------------


def emit_scaffolds(entries: Sequence[dict], fetch: bool = True) -> dict:
    """Write docs and practice scaffolds for the given manifest entries.

    Args:
        entries: Manifest entries to scaffold, most-recent first.
        fetch: When False, never hit the network and never overwrite an
            existing non-placeholder scaffold for a slug whose page is not
            cached; such slugs are reported as `skipped_no_cache` instead.

    Returns:
        Stats: `generated` (n), `cases_parsed` (n), `cases_empty` (n),
        `parse_failures` (slugs whose FastPrep page did not parse),
        `skipped_no_cache` (slugs left untouched under fetch=False).
    """
    stats = {
        "generated": 0,
        "cases_parsed": 0,
        "cases_empty": 0,
        "parse_failures": [],
        "skipped_no_cache": [],
    }
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    PRACTICE_DIR.mkdir(parents=True, exist_ok=True)
    for entry in entries:
        slug = entry["slug"]
        cached = has_cached_page(slug)
        if not fetch and not cached:
            # The entry was not emitted; its existing parse_status (from a
            # previous full generation) stays authoritative.
            stats["skipped_no_cache"].append(slug)
            continue
        page_html = fetch_problem_page(slug, delay=fetch, network=fetch)
        problem = extract_problem_record(page_html)
        parsed_cases = cases_from_record(problem) if problem else unparsed_page_cases(slug)
        if problem is None:
            stats["parse_failures"].append(slug)
        statement_html = resolve_statement(problem, page_html)
        (PRACTICE_DIR / slug).mkdir(parents=True, exist_ok=True)
        for path, content in render_all(entry, problem, parsed_cases, statement_html).items():
            path.write_text(content, encoding="utf-8")
        if parsed_cases.cases:
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
    """Write scripts/amazon_oa_manifest.json, most-recent first."""
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(list(manifest), indent=2) + "\n", encoding="utf-8")


def write_index(manifest: Sequence[dict]) -> None:
    """Write docs/problems/amazon_oa/index.md."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "index.md").write_text(render_index(manifest), encoding="utf-8")


def ensure_nav_entry() -> bool:
    """Add the single Amazon OA nav entry to mkdocs.yml when missing.

    Returns:
        True when mkdocs.yml was modified, False when the entry already exists.
    """
    text = MKTABS_PATH.read_text(encoding="utf-8")
    nav_line = '    - "Amazon OA": problems/amazon_oa/index.md\n'
    if "problems/amazon_oa/index.md" in text:
        return False
    marker = "  - Problems:\n"
    if marker not in text:
        raise SystemExit("mkdocs.yml has no Problems nav section to extend")
    text = text.replace(marker, marker + nav_line, 1)
    MKTABS_PATH.write_text(text, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Idempotency check
# ---------------------------------------------------------------------------


def expected_scaffold_fragments(entry: dict) -> Dict[Path, str]:
    """Manifest-driven scaffold expectations for one problem.

    A `page-unparseable` entry was rendered entirely from the manifest, so
    its four scaffolds are compared byte-for-byte. Every other entry was
    rendered from FastPrep data that lives only in the unversioned /tmp
    cache; the fragments the generator owns end to end (the write-up
    header, the stub/test header and write-up link docstrings) are compared
    exactly instead of re-rendering from the cache.

    Args:
        entry: Manifest entry carrying `slug`, `title`, `url`, and
            `parse_status`.

    Returns:
        Expected text fragments keyed by scaffold path; a file matches when
        it starts with the expected fragment.
    """
    slug = entry["slug"]
    if entry.get("parse_status") == "page-unparseable":
        return render_all(entry, None, unparsed_page_cases(slug), "")
    writeup_link = WRITEUP_LINK_TEMPLATE.format(slug=slug)
    return {
        DOCS_DIR / f"{slug}.md": f"# [{entry['title']}]({entry['url']})\n",
        PRACTICE_DIR / slug / "solution.py": (
            f'"""{entry["title"]} — {entry["url"]}\n'
            f"\nWrite-up & approaches: {writeup_link}\n"
        ),
        PRACTICE_DIR / slug / f"test_{slug}.py": (
            f'"""Tests for {entry["title"]} — your attempt (solution.py) against'
            f" cases.json.\n\nThe worked approaches live in {writeup_link}.\n"
        ),
    }


def _is_json_list_file(path: Path) -> bool:
    """Report whether the file exists and parses to a JSON list."""
    if not path.exists():
        return False
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return False
    return isinstance(parsed, list)


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
    never depends on the /tmp bank pages or the fastprep cache.

    Args:
        manifest: The manifest entries to verify.

    Returns:
        A process exit code: 0 when identical, 1 with a diff summary otherwise.
    """
    stale: List[str] = []
    for entry in manifest:
        slug = entry["slug"]
        for path, expected in expected_scaffold_fragments(entry).items():
            if not path.exists() or not path.read_text(encoding="utf-8").startswith(expected):
                stale.append(_displays(path))
        if entry.get("parse_status") != "page-unparseable":
            cases_path = PRACTICE_DIR / slug / "cases.json"
            if not _is_json_list_file(cases_path):
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
        help="Bank page markdown (default: the two cached Tech-OA coding pages)",
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
        manifest = load_committed_manifest(MANIFEST_PATH)
        source = "committed manifest fallback"
    else:
        manifest = build_manifest([path.read_text(encoding="utf-8") for path in bank_pages])
        source = "built from bank pages"
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
    stats = emit_scaffolds(entries, fetch=not args.no_fetch and bank_available)
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
    if stats["skipped_no_cache"]:
        print(
            "skipped (no cache, fetch disabled, existing scaffolds kept): "
            + ", ".join(stats["skipped_no_cache"])
        )
        if not bank_available:
            print(
                "warning: the Tech-OA bank pages are absent and the fastprep"
                " cache has no entry for the skipped slug(s); their existing"
                " scaffolds were left untouched"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
