"""Generate the NeetCode 150 track scaffolds for grind75.

Pipeline:
  1. Validate the committed scripts/neetcode150_manifest.json (150 entries,
     18 canonical sections, Easy 28 / Medium 102 / Hard 20, unique slugs).
  2. For each delta problem (no existing docs write-up and practice folder),
     fetch its metadata from neetcode.io (disk cache, polite delay), parse
     the statement markdown, and emit:
       - docs/problems/<dirSlug>.md        (statement write-up scaffold)
       - practice/<dirSlug>/solution.py    (NotSolved stub)
       - practice/<dirSlug>/cases.json     (parseable examples, else [])
       - practice/<dirSlug>/test_<dirSlug>.py (harness-driven tests)
  3. Once every delta problem is scaffolded, the mkdocs.yml Problems nav
       and the docs/problems/index.md landing page are updated by their
       owners: the nav's Problems section is owned by
       scripts/generate_index_tables.py (which merges this track with the
       Grind 75 rows into one flat "Grind 75 + NeetCode 150" subsection),
       and the landing
       page tables are owned by the same generator.

Overlap problems (already in the bank) keep their single write-up and
practice folder and are never scaffolded or modified.

Cases contract: a case is emitted only when every example value parses to a
JSON-representable literal assertable with `==` against the method's return
value. Trees, linked lists, graphs, design-operation sequences, free-text
outputs, any-order outputs, and in-place mutation problems produce an empty
cases.json and a test module that skips with a reason naming the slug. Empty
is never a silent pass. `cases_full.json` is never scaffolded: the Submit
gauntlet is hand-authored when the problem is practiced.

Usage (from the repository root):
  cd practice && uv run pytest ../scripts/          # run the generator tests
  python3 scripts/generate_neetcode150_scaffolds.py \
      [--limit N | --check] [--no-fetch]
"""

from __future__ import annotations

import argparse
import ast
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
MANIFEST_PATH = REPO_ROOT / "scripts" / "neetcode150_manifest.json"
DOCS_DIR = REPO_ROOT / "docs" / "problems"
PRACTICE_DIR = REPO_ROOT / "practice"

METADATA_URL = "https://neetcode.io/api/getProblemMetadataFunctionHttp"
METADATA_CACHE_DIR = Path("/tmp/opencode/neetcode-cache")
FETCH_DELAY_SECONDS = 0.5
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)

LC_PROBLEM_URL_TEMPLATE = "https://leetcode.com/problems/{slug}/"
NC_PROBLEM_URL_TEMPLATE = "https://neetcode.io/problems/{slug}"
# Write-ups live flat in docs/problems/, so the template is a sibling.
TEMPLATE_LINK = "_TEMPLATE.md"

TRACK_SIZE = 150
DIFFICULTY_TOTALS = {"Easy": 28, "Medium": 102, "Hard": 20}
SECTION_COUNTS = {
    "Arrays & Hashing": 9,
    "Two Pointers": 5,
    "Sliding Window": 6,
    "Stack": 6,
    "Binary Search": 7,
    "Linked List": 11,
    "Trees": 15,
    "Heap / Priority Queue": 7,
    "Backtracking": 10,
    "Tries": 3,
    "Graphs": 13,
    "Advanced Graphs": 6,
    "1-D Dynamic Programming": 12,
    "2-D Dynamic Programming": 11,
    "Greedy": 8,
    "Intervals": 6,
    "Math & Geometry": 8,
    "Bit Manipulation": 7,
}
MANIFEST_FIELDS = (
    "order",
    "section",
    "title",
    "lcSlug",
    "dirSlug",
    "ncSlug",
    "difficulty",
    "leetcodePremium",
)

EXAMPLE_HEADER_PATTERN = re.compile(r"^\*\*Example\s*(\d+):?\*\*\s*$", re.M)
FENCE_PATTERN = re.compile(r"^```.*?$", re.M)
CONSTRAINTS_HEADER = "**Constraints:**"
EXPLANATION_LABEL = "Explanation:"
FOLLOW_UP_HEADER_PATTERN = re.compile(r"^\*\*Follow[- ]?up:?\*\*", re.M)
ANY_ORDER_PATTERNS = (
    "any order",
    "any of them",
    "multiple valid answers",
    "would still be accepted",
    "all words that are present in the grid",
)
HINT_ACCORDION_PATTERN = re.compile(r"<details\s+class=\"hint-accordion\".*?</details>", re.S)
COMPANY_ACCORDION_PATTERN = re.compile(r"<details\s+class=\"company-tags-accordion\".*?</details>", re.S)
TOPICS_ACCORDION_PATTERN = re.compile(r"<details\s+class=\"hint-accordion\">\s*<summary>Topics</summary>.*?</details>", re.S)
DEFAULT_FUNCTION_NAME = "solve"

SCALAR_ANNOTATIONS = {
    "int",
    "integer",
    "long",
    "float",
    "double",
    "str",
    "string",
    "char",
    "bool",
    "boolean",
    "any",
}
MUTATION_RETURN_ANNOTATIONS = {"none", "void"}
MIN_PLAUSIBLE_STATEMENT_LENGTH = 40


class ManifestError(ValueError):
    """Raised when the committed NeetCode 150 manifest violates the track contract."""


@dataclass
class CasesResult:
    """Outcome of converting NeetCode examples into harness cases.

    Attributes:
        function_name: The method name solutions implement (e.g. `groupAnagrams`).
        cases: JSON-representable cases `[{"id", "args", "expected"}]`.
        skip_reason: Why no cases exist, naming the slug; None when cases exist.
    """

    function_name: str
    cases: List[dict]
    skip_reason: Optional[str]


_UNPARSEABLE = object()


# ---------------------------------------------------------------------------
# Manifest validation
# ---------------------------------------------------------------------------


def load_manifest(path: Path = MANIFEST_PATH) -> List[dict]:
    """Load the committed NeetCode 150 manifest.

    Args:
        path: Path to the manifest JSON (default: scripts/neetcode150_manifest.json).

    Returns:
        The 150 manifest entries in track order.

    Raises:
        ManifestError: When the file is missing or is not a JSON list.
    """
    if not path.exists():
        raise ManifestError(f"manifest not found: {path}")
    try:
        entries = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ManifestError(f"manifest {path} is not valid JSON: {error}") from error
    if not isinstance(entries, list):
        raise ManifestError(f"manifest {path} must be a JSON list")
    return entries


def validate_manifest(entries: Sequence[dict]) -> None:
    """Check the manifest against the NeetCode 150 track contract.

    The contract: exactly 150 entries numbered 1..150 in canonical section
    order; every required field present; unique lcSlugs and dirSlugs; each
    dirSlug derived from its lcSlug; difficulties in {Easy, Medium, Hard}
    totalling Easy 28 / Medium 102 / Hard 20; sections from the canonical 18
    with per-section counts matching the track. All violations are collected
    before raising; the input is never mutated.

    Args:
        entries: The manifest entries to validate.

    Raises:
        ManifestError: Naming every violation found.
    """
    problems: List[str] = []
    if len(entries) != TRACK_SIZE:
        problems.append(f"expected {TRACK_SIZE} entries, found {len(entries)}")

    seen_lc_slugs: Dict[str, int] = {}
    seen_dir_slugs: Dict[str, int] = {}
    difficulty_totals = {"Easy": 0, "Medium": 0, "Hard": 0}
    section_runs: List[str] = []

    for index, entry in enumerate(entries, start=1):
        label = f"entry {index}"
        missing = [field for field in MANIFEST_FIELDS if field not in entry]
        if missing:
            problems.append(f"{label}: missing field(s) {', '.join(missing)}")
            continue
        if entry["order"] != index:
            problems.append(f"{label}: order is {entry['order']!r}, expected {index}")
        section = entry["section"]
        if section not in SECTION_COUNTS:
            problems.append(f"{label}: unknown section {section!r}")
        if not section_runs or section_runs[-1] != section:
            section_runs.append(section)
        lc_slug = entry["lcSlug"]
        seen_lc_slugs[lc_slug] = seen_lc_slugs.get(lc_slug, 0) + 1
        dir_slug = entry["dirSlug"]
        seen_dir_slugs[dir_slug] = seen_dir_slugs.get(dir_slug, 0) + 1
        if dir_slug != lc_slug.replace("-", "_"):
            problems.append(
                f"{label}: dirSlug {dir_slug!r} is not {lc_slug!r} with hyphens as underscores"
            )
        difficulty = entry["difficulty"]
        if difficulty not in difficulty_totals:
            problems.append(f"{label}: unknown difficulty {difficulty!r}")
        else:
            difficulty_totals[difficulty] += 1

    duplicates = sorted(slug for slug, count in seen_lc_slugs.items() if count > 1)
    if duplicates:
        problems.append(f"duplicate lcSlug entries: {', '.join(duplicates)}")
    duplicates = sorted(slug for slug, count in seen_dir_slugs.items() if count > 1)
    if duplicates:
        problems.append(f"duplicate dirSlug entries: {', '.join(duplicates)}")

    for section, expected in SECTION_COUNTS.items():
        actual = sum(1 for entry in entries if entry.get("section") == section)
        if actual != expected:
            problems.append(
                f"section counts: {section!r} has {actual} entries, expected {expected}"
            )
    if section_runs and section_runs != list(SECTION_COUNTS):
        problems.append(
            "sections are not in canonical order: "
            f"{[s for s in section_runs if s in SECTION_COUNTS]}"
        )
    for difficulty, expected in DIFFICULTY_TOTALS.items():
        actual = difficulty_totals[difficulty]
        if actual != expected:
            problems.append(
                f"difficulty totals: {difficulty} has {actual}, expected {expected}"
            )

    if problems:
        raise ManifestError(
            "manifest contract violations:\n  - " + "\n  - ".join(problems)
        )


# ---------------------------------------------------------------------------
# Track derivation: overlap vs delta
# ---------------------------------------------------------------------------


def derive_delta(
    entries: Sequence[dict],
    docs_dir: Optional[Path] = None,
    practice_dir: Optional[Path] = None,
) -> List[dict]:
    """Split the manifest into delta problems in track order.

    A problem is delta when it has neither a `docs/problems/<dirSlug>.md`
    write-up nor a `practice/<dirSlug>/` folder; overlap problems (the shared
    LeetCode universe) keep their existing files untouched.

    Args:
        entries: The validated manifest entries.
        docs_dir: Overrides the docs/problems directory (default: module constant).
        practice_dir: Overrides the practice directory (default: module constant).

    Returns:
        The manifest entries whose write-up and practice folder are both absent.

    Raises:
        ManifestError: When a problem has exactly one of the two files, which
            would leave the bank half-scaffolded.
    """
    docs_dir = docs_dir if docs_dir is not None else DOCS_DIR
    practice_dir = practice_dir if practice_dir is not None else PRACTICE_DIR
    delta: List[dict] = []
    for entry in entries:
        dir_slug = entry["dirSlug"]
        has_doc = (docs_dir / f"{dir_slug}.md").exists()
        has_practice = (practice_dir / dir_slug).exists()
        if has_doc != has_practice:
            raise ManifestError(
                f"partial overlap for {entry['lcSlug']!r}: write-up present={has_doc}, "
                f"practice folder present={has_practice}; the bank expects both or neither"
            )
        if not has_doc:
            delta.append(entry)
    return delta


# ---------------------------------------------------------------------------
# Metadata fetching
# ---------------------------------------------------------------------------


def _urlopen(request: Any, timeout: int) -> Any:
    """Indirect urllib.urlopen so tests can fake the network."""
    return urllib.request.urlopen(request, timeout=timeout)


# Tests patch this name instead of urllib.request.urlopen.
urllib_request_urlopen = _urlopen


def fetch_problem_metadata(
    nc_slug: str,
    cache_dir: Optional[Path] = None,
    delay: bool = True,
    network: bool = True,
) -> Optional[dict]:
    """Fetch one problem's metadata from neetcode.io through a disk cache.

    Args:
        nc_slug: The NeetCode problem slug (differs from the LeetCode slug).
        cache_dir: Directory holding cached responses keyed by `<slug>.json`.
        delay: Sleep politely before a network fetch (cache hits never wait).
        network: When False, never hit the network: a cache miss returns None.

    Returns:
        The parsed `data` record, or None when the site answers with an HTTP
        error or fetching is disabled; the caller emits placeholder scaffolds
        and records the slug as a parse failure.

    Raises:
        RuntimeError: When the network fetch fails for a non-HTTP reason.
    """
    cache_root = cache_dir if cache_dir is not None else METADATA_CACHE_DIR
    cache_path = cache_root / f"{nc_slug}.json"
    if cache_path.exists():
        try:
            return parse_metadata(json.loads(cache_path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Truncated or corrupt cache entry: fall through to a fresh
            # fetch, which rewrites the file.
            pass
    if not network:
        return None
    if delay:
        time.sleep(FETCH_DELAY_SECONDS)
    body = json.dumps({"data": {"problemId": nc_slug}}).encode("utf-8")
    request = urllib.request.Request(
        METADATA_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "User-Agent": BROWSER_USER_AGENT,
        },
        method="POST",
    )
    try:
        with urllib_request_urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError:
        return None
    except Exception as error:
        raise RuntimeError(f"fetching metadata for {nc_slug} failed: {error}") from error
    metadata = parse_metadata(payload)
    if metadata is not None:
        cache_root.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return metadata


# ---------------------------------------------------------------------------
# Metadata parsing and description decomposition
# ---------------------------------------------------------------------------


def parse_metadata(payload: Optional[dict]) -> Optional[dict]:
    """Return the API's `data` record, or None when the lookup came back empty."""
    if not isinstance(payload, dict):
        return None
    data = payload.get("data")
    return data if isinstance(data, dict) else None


def strip_accordions(description: str) -> str:
    """Drop the hint/company-tag/Topics accordion tails NeetCode appends."""
    text = HINT_ACCORDION_PATTERN.sub("", description)
    text = COMPANY_ACCORDION_PATTERN.sub("", text)
    text = TOPICS_ACCORDION_PATTERN.sub("", text)
    text = re.sub(r"<details.*?</details>", "", text, flags=re.S)
    text = re.sub(r"<br\s*/?>", "", text)
    text = re.sub(r"</?p[^>]*>", "", text)
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    return text.strip()


def parse_description(description: str) -> dict:
    """Decompose a NeetCode `description` into statement, examples, and constraints.

    The description is markdown: statement prose (possibly with a `$...$`
    LaTeX subset), `**Example N:**` blocks whose fenced body holds
    `Input:`/`Output:` lines, a `**Constraints:**` bullet list, an optional
    `**Follow-up:**` question, then HTML accordions (hints, topics, company
    tags) that are dropped.

    Args:
        description: The raw description markdown.

    Returns:
        A dict with `statement` (markdown), `examples` (list of dicts with
        `index`, `input`, `output`, `explanation`), `constraints` (list of
        markdown strings), and `follow_up` (prose, possibly empty).
    """
    text = strip_accordions(description)
    if not text:
        return {"statement": "", "examples": [], "constraints": [], "follow_up": ""}

    follow_up = ""
    follow_match = FOLLOW_UP_HEADER_PATTERN.search(text)
    if follow_match:
        # Bound the capture at the next structural marker (**Example N:** or
        # **Constraints:**); some descriptions place the Follow-up before
        # the examples, and an unbounded capture would swallow them.
        follow_body = text[follow_match.end() :]
        next_marker = len(follow_body)
        example_after = EXAMPLE_HEADER_PATTERN.search(follow_body)
        constraints_after = follow_body.find(CONSTRAINTS_HEADER)
        if example_after:
            next_marker = min(next_marker, example_after.start())
        if constraints_after != -1:
            next_marker = min(next_marker, constraints_after)
        follow_up = " ".join(follow_body[:next_marker].split())
        text = (
            text[: follow_match.start()]
            + text[follow_match.end() :][next_marker:]
        )

    constraints = []
    constraints_at = text.find(CONSTRAINTS_HEADER)
    if constraints_at != -1:
        constraints_block = text[constraints_at + len(CONSTRAINTS_HEADER) :]
        text = text[:constraints_at]
        for line in constraints_block.splitlines():
            line = line.strip()
            if line.startswith("* ") or line.startswith("- "):
                constraints.append(line[2:].strip())

    examples: List[dict] = []
    statement = text
    example_matches = list(EXAMPLE_HEADER_PATTERN.finditer(text))
    if example_matches:
        statement = text[: example_matches[0].start()]
        for position, match in enumerate(example_matches):
            end = (
                example_matches[position + 1].start()
                if position + 1 < len(example_matches)
                else len(text)
            )
            examples.append(
                build_example(int(match.group(1)), text[match.end() : end])
            )

    return {
        "statement": statement.strip(),
        "examples": examples,
        "constraints": constraints,
        "follow_up": follow_up,
    }


def build_example(index: int, block: str) -> dict:
    """Split one example block into its fenced input/output/explanation parts.

    The explanation keeps its fenced code (rendered as markdown fences);
    stray bold markers left by the source (`**Explanation:** **`) are
    dropped rather than emitted unclosed.
    """
    explanation = ""
    explanation_at = block.find(EXPLANATION_LABEL)
    if explanation_at != -1:
        explanation = block[explanation_at + len(EXPLANATION_LABEL) :].strip()
        block = block[:explanation_at]
    fences = list(FENCE_PATTERN.finditer(block))
    if fences:
        fenced = block[fences[0].end() : fences[1].start() if len(fences) > 1 else len(block)]
    else:
        fenced = block
    explanation = normalize_explanation(explanation)
    return {
        "index": index,
        "input": extract_example_field(fenced, "Input"),
        "output": extract_example_field(fenced, "Output"),
        "explanation": explanation,
    }


def normalize_explanation(explanation: str) -> str:
    """Clean an explanation body for write-up rendering.

    The source explanation may be fenced (` ```java ... ``` `) code, plain
    prose, or prose around fenced code. A stray `**` bold marker (unclosed
    in the source) may lead the body; it is dropped, code stays fenced,
    prose stays plain.
    """
    text = re.sub(r"^(?:\*\*\s*)+", "", explanation.strip())
    if "```" not in text:
        return text.strip()
    segments = re.split(r"```[a-z]*", text)
    prose = segments[0].strip()
    code = "\n\n".join(segment.strip() for segment in segments[1:] if segment.strip())
    if not code:
        return prose
    fenced = "```java\n" + code + "\n```"
    if prose:
        return prose + "\n\n" + fenced
    return fenced


def extract_example_field(fenced: str, field: str) -> str:
    """Extract one `Field:` value from a fenced example body.

    The value runs to the next top-level `Field:` label or the end of the
    fence, so multiline grid literals stay intact with their `name =` lead.
    Single-line values keep the `name = value` spelling the bank's write-ups
    use.
    """
    match = re.search(
        rf"^{field}:\s*(.*?)(?=^\s*(?:Input|Output|Explanation):|\Z)",
        fenced,
        flags=re.S | re.M,
    )
    return match.group(1).strip() if match else ""


def function_name_from_starter(metadata: Optional[dict]) -> str:
    """Read the method name out of the Python starter code.

    Multi-method starters (design problems like encode/decode) return the
    first name; the caller refuses to emit cases for those.
    """
    starter = str((metadata or {}).get("starterCode", {}).get("python", ""))
    match = re.search(r"def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", starter)
    return match.group(1) if match else DEFAULT_FUNCTION_NAME


# ---------------------------------------------------------------------------
# Example-to-cases conversion (the cases contract)
# ---------------------------------------------------------------------------


def unparseable_cases(slug: str, reason: str) -> CasesResult:
    """Build the empty cases result with a slug-naming skip reason."""
    return CasesResult(DEFAULT_FUNCTION_NAME, [], f"{reason} for {slug}")


def cases_from_metadata(metadata: Optional[dict], dir_slug: str) -> CasesResult:
    """Convert NeetCode examples into harness cases under the cases contract.

    Thin wrapper over `cases_from_parsed` for callers that hold only the
    metadata record; the render path uses `cases_from_parsed` directly so
    the description is parsed once.

    Args:
        metadata: The parsed metadata record, or None when unparseable.
        dir_slug: The problem's dirSlug, for skip-reason naming.

    Returns:
        A CasesResult with the function name, the cases, and a skip reason
        (None) exactly when at least one case exists.
    """
    return cases_from_parsed(
        parse_description(str((metadata or {}).get("description") or "")),
        metadata,
        dir_slug,
    )


def cases_from_parsed(
    parsed: Optional[dict], metadata: Optional[dict], dir_slug: str
) -> CasesResult:
    """Convert a parsed description into harness cases under the contract.

    Cases exist only when every example parses to JSON-representable literals
    assertable with `==` against the method's return. Any-order outputs,
    multi-method starters, in-place mutation problems, structural (tree /
    linked-list / graph) annotations, and free-text values all yield an empty
    case list with a skip reason naming the slug.

    Args:
        parsed: The `parse_description` result (statement, examples,
            constraints, follow_up); None means the description was empty.
        metadata: The parsed metadata record (starter code is read here),
            or None when unparseable, which yields the metadata skip reason.
        dir_slug: The problem's dirSlug, for skip-reason naming.

    Returns:
        A CasesResult with the function name, the cases, and a skip reason
        (None) exactly when at least one case exists.
    """
    if metadata is None:
        return unparseable_cases(dir_slug, "metadata did not parse")
    if parsed is None:
        parsed = {"statement": "", "examples": [], "constraints": [], "follow_up": ""}
    signature = starter_signature(metadata)
    if signature.multi_method:
        return unparseable_cases(
            dir_slug,
            f"multi-method starter ({', '.join(signature.methods)}) is not a single "
            "`==`-assertable call",
        )
    if signature.returns_mutation:
        return unparseable_cases(
            dir_slug, "in-place mutation return is not `==`-assertable"
        )
    if signature.structural:
        return unparseable_cases(
            dir_slug,
            f"structural signature ({', '.join(signature.structural)}) is not "
            "JSON-representable",
        )
    function_name = signature.name

    if not parsed["examples"]:
        return unparseable_cases(dir_slug, "no examples in the description")
    if declares_any_order(parsed):
        return unparseable_cases(
            dir_slug, "any-order output is not `==`-assertable; compare as sets"
        )

    cases: List[dict] = []
    for example in parsed["examples"]:
        if not example["input"]:
            return unparseable_cases(dir_slug, "example has no Input block")
        args = parse_input_values(example["input"])
        if any(value is _UNPARSEABLE for value in args):
            return unparseable_cases(
                dir_slug, "example input is not JSON-representable"
            )
        if any(contains_null(value) for value in args):
            return unparseable_cases(
                dir_slug, "example input carries null; no case may hinge on None"
            )
        expected = parse_scalar_literal(example["output"])
        if expected is _UNPARSEABLE:
            return unparseable_cases(
                dir_slug, "example output is not `==`-assertable"
            )
        if contains_null(expected):
            return unparseable_cases(
                dir_slug, "example output carries null; no case may hinge on None"
            )
        cases.append(
            {
                "id": f"example_{example['index']}",
                "args": args,
                "expected": expected,
            }
        )
    if not cases:
        return unparseable_cases(dir_slug, "no parseable examples")
    return CasesResult(function_name, cases, None)


@dataclass
class StarterSignature:
    """What the Python starter code says about the solution shape.

    Attributes:
        name: The single method name, or the first when multi-method.
        methods: Every method name the starter defines.
        returns_mutation: The return annotation is None/void (in-place).
        structural: Annotation fragments that are not JSON-representable.
        multi_method: More than one method is defined.
    """

    name: str
    methods: List[str]
    returns_mutation: bool
    structural: List[str]
    multi_method: bool


def starter_signature(metadata: dict) -> StarterSignature:
    """Classify the starter code's method names and annotations."""
    starter = str((metadata or {}).get("starterCode", {}).get("python", ""))
    methods = re.findall(r"def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)", starter)
    if not methods:
        return StarterSignature(
            name=function_name_from_starter(metadata),
            methods=[],
            returns_mutation=False,
            structural=[],
            multi_method=False,
        )
    returns_mutation = False
    structural: List[str] = []
    for _, arg_text in methods:
        for annotation in re.findall(r":\s*([^=),]+)", arg_text):
            cleaned = annotation.strip()
            if cleaned.lower() in MUTATION_RETURN_ANNOTATIONS:
                returns_mutation = True
            if not is_scalar_annotation(cleaned):
                structural.append(cleaned)
    return_annotation = re.search(r"->\s*([^:]+):", starter)
    if return_annotation:
        cleaned = return_annotation.group(1).strip()
        if cleaned.lower() in MUTATION_RETURN_ANNOTATIONS:
            returns_mutation = True
        if not is_scalar_annotation(cleaned):
            structural.append(cleaned)
    structural = dedupe(structural)
    names = [name for name, _ in methods]
    return StarterSignature(
        name=names[0],
        methods=names,
        returns_mutation=returns_mutation,
        structural=structural,
        multi_method=len(methods) > 1,
    )


def is_scalar_annotation(annotation: str) -> bool:
    """Report whether an annotation is a JSON-representable scalar spelling.

    `Optional[int]`, `List[List[str]]`, `Dict[str, int]` and their typing
    spellings count as scalar containers; TreeNode, ListNode, Node, and
    bare unknown names are structural.
    """
    text = re.sub(r"Optional\[|List\[|Dict\[|Set\[|Sequence\[|\]", "", annotation)
    text = re.sub(r"typing\.", "", text).strip()
    if not text:
        return False
    base_names = [name.strip().lower() for name in re.split(r"[\[\], ]+", text) if name.strip()]
    return all(name in SCALAR_ANNOTATIONS for name in base_names)


def declares_any_order(parsed: dict) -> bool:
    """Report whether the parsed description promises an any-order answer.

    NeetCode phrases the same contract in several ways ("return the output
    in any order", "return **any** of them", "multiple valid answers",
    "would still be accepted"), often with bold markers inside the phrase;
    any spelling makes the example output one of many valid answers, which
    `==` must not pin. The word-search shape ("return all words present in
    the grid") also admits several outputs, so its phrasing is included.
    """
    texts = [parsed["statement"].lower()]
    texts.extend(example["output"].lower() for example in parsed["examples"])
    texts.extend(example["explanation"].lower() for example in parsed["examples"])
    texts = [text.replace("*", "") for text in texts]
    return any(pattern in text for text in texts for pattern in ANY_ORDER_PATTERNS)


def parse_input_values(input_text: str) -> List[Any]:
    """Parse an example `Input:` body into a positional argument list.

    Handles both `name = value` spellings and anonymous multiline literals
    (grid problems), in declaration order.
    """
    stripped = input_text.strip()
    assignments = re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*", stripped)
    if not assignments:
        value = parse_scalar_literal(stripped)
        return [value] if value is not _UNPARSEABLE else [_UNPARSEABLE]
    values: List[Any] = []
    pattern = re.compile(
        r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)(?=\s*,\s*[A-Za-z_][A-Za-z0-9_]*\s*=|\Z)",
        flags=re.S,
    )
    for match in pattern.finditer(stripped):
        values.append(parse_scalar_literal(match.group(2).strip()))
    return values


def parse_scalar_literal(raw: str) -> Any:
    """Parse a literal that may be JSON or Python spelling.

    Args:
        raw: The raw literal text (e.g. `[1,2]`, `\"abc\"`, `10`).

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
    if parsed is not None and contains_null(parsed):
        return _UNPARSEABLE
    return parsed


def contains_null(value: Any) -> bool:
    """Report whether a parsed JSON value contains `null` anywhere."""
    if value is None:
        return True
    if isinstance(value, list):
        return any(contains_null(item) for item in value)
    if isinstance(value, dict):
        return any(contains_null(item) for item in value.values())
    return False


def dedupe(values: Sequence[str]) -> List[str]:
    """Drop repeats while preserving order."""
    seen = set()
    out = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


# ---------------------------------------------------------------------------
# Scaffold rendering
# ---------------------------------------------------------------------------


def difficulty_line(entry: dict, metadata: Optional[dict]) -> str:
    """Render the template's metadata line, bracketed when data is missing."""
    difficulty = (metadata or {}).get("difficulty") or entry["difficulty"]
    topics = (metadata or {}).get("topics") or []
    difficulty_text = f"**{str(difficulty).capitalize()}**" if difficulty else "**unknown difficulty**"
    minutes_text = "**NN minutes**"
    topics_text = ", ".join(str(topic) for topic in topics) if topics else "unknown topics"
    return f"{difficulty_text} | {minutes_text} | **{topics_text}**"


def premium_note(entry: dict) -> List[str]:
    """Note the NeetCode fallback for LeetCode-premium problems."""
    if not entry.get("leetcodePremium"):
        return []
    nc_url = NC_PROBLEM_URL_TEMPLATE.format(slug=entry["ncSlug"])
    return [
        f"> This problem is locked behind [LeetCode Premium]({LC_PROBLEM_URL_TEMPLATE.format(slug=entry['lcSlug'])});"
        f" read it free on [NeetCode]({nc_url}).",
        "",
    ]


def render_statement(parsed: dict, dir_slug: str) -> str:
    """Render the statement prose, falling back to an explicit placeholder."""
    statement = parsed["statement"]
    if len(statement) < MIN_PLAUSIBLE_STATEMENT_LENGTH:
        return f"<!-- Statement not parseable from NeetCode for {dir_slug}; fill it in. -->"
    return statement


def render_examples(parsed: dict, dir_slug: str) -> List[str]:
    """Render the Examples section from parsed examples or a placeholder."""
    examples = parsed["examples"]
    if not examples:
        return [
            f"<!-- Examples not parseable from NeetCode for {dir_slug}; fill them in. -->",
            "",
        ]
    lines: List[str] = []
    for example in examples:
        lines.append(f"### Example {example['index']}")
        lines.append("")
        lines.extend(render_input_output(example["input"], example["output"]))
        lines.append("")
        if example["explanation"]:
            # pymdownx.superfences needs the fence at line start: a fenced
            # explanation becomes its own block under the bold label instead
            # of being glued onto it (which renders the code unfenced).
            explanation = example["explanation"]
            if explanation.startswith("```"):
                lines.append("**Explanation:**")
                lines.append("")
                lines.append(explanation)
            else:
                lines.append(f"**Explanation:** {explanation}")
            lines.append("")
    return lines


def render_input_output(input_text: str, output_text: str) -> List[str]:
    """Render Input/Output lines, fencing multiline literals like the bank does."""
    if "\n" in input_text or "\n" in output_text:
        return [
            "**Input:**",
            "",
            "```",
            input_text,
            "```",
            "",
            "**Output:**",
            "",
            "```",
            output_text,
            "```",
        ]
    return [f"**Input:** `{input_text}`", "", f"**Output:** `{output_text}`"]


def render_constraints(parsed: dict, dir_slug: str) -> List[str]:
    """Render the Constraints section from parsed bullets or a placeholder."""
    constraints = parsed["constraints"]
    if not constraints:
        return [
            f"<!-- Constraints not parseable from NeetCode for {dir_slug}; fill them in. -->",
            "",
        ]
    lines = [f"- {text}" for text in constraints]
    return lines + [""]


def render_writeup(entry: dict, metadata: Optional[dict], parsed: Optional[dict] = None) -> str:
    """Render the statement write-up scaffold for one problem.

    Args:
        entry: Manifest entry for the problem.
        metadata: Parsed NeetCode metadata, or None when unparseable.
        parsed: Pre-parsed description (shared by the render path); when
            None, the metadata description is parsed here.

    Returns:
        Write-up markdown following the docs/problems/_TEMPLATE.md section
        order, with solutions left as an explicit placeholder.
    """
    if parsed is None:
        parsed = parse_description(str((metadata or {}).get("description") or ""))
    lc_url = LC_PROBLEM_URL_TEMPLATE.format(slug=entry["lcSlug"])
    parts: List[str] = [
        f"# [{entry['title']}]({lc_url})",
        "",
        difficulty_line(entry, metadata),
        "",
        *premium_note(entry),
        render_statement(parsed, entry["dirSlug"]),
        "",
        "## Examples",
        "",
        *render_examples(parsed, entry["dirSlug"]),
        "## Constraints",
        "",
        *render_constraints(parsed, entry["dirSlug"]),
    ]
    if parsed["follow_up"]:
        parts.extend(["## Follow-up", "", parsed["follow_up"], ""])
    parts.extend(
        [
            "## Solutions",
            "",
            "<!-- Scaffold placeholder: the worked derivation and solutions land",
            f"     on the solutions branch later. See {TEMPLATE_LINK} for the",
            "     expected layout, naming, and ordering conventions. -->",
            "",
        ]
    )
    return "\n".join(parts).rstrip() + "\n"


def render_solution_stub(
    entry: dict,
    metadata: Optional[dict],
    parsed_cases: CasesResult,
    parsed: Optional[dict] = None,
) -> str:
    """Render the NotSolved practice stub in the two_sum house style."""
    if parsed is None:
        parsed = parse_description(str((metadata or {}).get("description") or ""))
    statement = parsed["statement"]
    summary = (
        " ".join(statement.split())[:200]
        if len(statement) >= MIN_PLAUSIBLE_STATEMENT_LENGTH
        else ""
    ) or f"NeetCode 150 problem ({entry['section']})."
    lc_url = LC_PROBLEM_URL_TEMPLATE.format(slug=entry["lcSlug"])
    case_id = parsed_cases.cases[0]["id"] if parsed_cases.cases else "example_1"
    function_name = parsed_cases.function_name
    args_signature = _signature_args(parsed, parsed_cases)
    dir_slug = entry["dirSlug"]
    return f'''"""{entry["title"]} — {lc_url}

Write-up & approaches: ../../docs/problems/{dir_slug}.md

{summary}

  uv run python {dir_slug}/solution.py   # debug one case (see CASE below)
  uv run pytest {dir_slug}/              # run the test sets
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


def _signature_args(parsed: dict, parsed_cases: CasesResult) -> str:
    """Build the plain-argument list for the stub signature.

    With cases parsed, the names come from the example's `name = value`
    assignments (Python keywords suffixed with `_`); otherwise the stub takes
    `*args` so it stays syntactically valid before the user writes anything.
    """
    if not parsed_cases.cases:
        return ", *args"
    first_input = parsed["examples"][0]["input"] if parsed["examples"] else ""
    names = re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*", first_input.strip())
    if not names:
        return ", *args"
    return "".join(
        f", {name}_" if keyword.iskeyword(name) else f", {name}" for name in names
    )


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


def render_test(
    entry: dict, function_name: str, cases: List[dict], skip_reason: Optional[str]
) -> str:
    """Render the harness-driven test module in the house scaffold style.

    No local pytest.ini: the root practice/pytest.ini governs nested
    directories. `cases_full.json` is intentionally not scaffolded; the
    Submit gauntlet is authored when the problem is practiced. With an empty
    case list the module skips with a reason naming the slug so an
    unparseable problem never silently passes.
    """
    reason = skip_reason or "no cases parsed"
    case_list = _python_literal(cases)
    dir_slug = entry["dirSlug"]
    title = entry["title"]
    return f'''"""Tests for {title} — your attempt (solution.py) against cases.json.

The worked approaches live in ../../docs/problems/{dir_slug}.md.
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


def render_all(
    entry: dict,
    metadata: Optional[dict],
    parsed_cases: CasesResult,
    parsed: Optional[dict] = None,
) -> Dict[Path, str]:
    """Render every scaffold file for one problem, keyed by target path.

    `parsed` threads a single `parse_description` result through the render
    path (the write-up, stub, and signature all read the same dict), so the
    description is parsed once per problem. Callers without one leave None
    and each renderer parses lazily.

    Shared by the emission and idempotency-check paths so the two can never
    drift apart.
    """
    if parsed is None:
        parsed = parse_description(str((metadata or {}).get("description") or ""))
    dir_slug = entry["dirSlug"]
    return {
        DOCS_DIR / f"{dir_slug}.md": render_writeup(entry, metadata, parsed),
        PRACTICE_DIR / dir_slug / "solution.py": render_solution_stub(
            entry, metadata, parsed_cases, parsed
        ),
        PRACTICE_DIR / dir_slug / "cases.json": render_cases_file(parsed_cases),
        PRACTICE_DIR / dir_slug / f"test_{dir_slug}.py": render_test(
            entry,
            parsed_cases.function_name,
            parsed_cases.cases,
            parsed_cases.skip_reason,
        ),
    }


# ---------------------------------------------------------------------------
# Emission
# ---------------------------------------------------------------------------


def emit_scaffolds(entries: Sequence[dict], fetch: bool = True) -> dict:
    """Write docs and practice scaffolds for the given delta entries.

    Args:
        entries: Delta manifest entries to scaffold, in track order.
        fetch: When False, never hit the network and never overwrite an
            existing scaffold for a slug whose metadata is not cached; such
            slugs are reported as `skipped_no_cache` instead.

    Returns:
        Stats: `generated` (n), `cases_parsed` (n), `cases_empty` (n),
        `parse_failures` (dirSlugs whose metadata did not parse),
        `skipped_no_cache` (dirSlugs left untouched under fetch=False).
    """
    stats = {
        "generated": 0,
        "cases_parsed": 0,
        "cases_empty": 0,
        "parse_failures": [],
        "skipped_no_cache": [],
    }
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    for entry in entries:
        dir_slug = entry["dirSlug"]
        cached = (METADATA_CACHE_DIR / f"{entry['ncSlug']}.json").exists()
        if not fetch and not cached:
            # The entry was not emitted; its existing parse_status (from a
            # previous full generation) stays authoritative.
            stats["skipped_no_cache"].append(dir_slug)
            continue
        metadata = fetch_problem_metadata(entry["ncSlug"], delay=fetch, network=fetch)
        parsed = parse_description(str((metadata or {}).get("description") or ""))
        parsed_cases = cases_from_parsed(parsed, metadata, dir_slug)
        if metadata is None:
            stats["parse_failures"].append(dir_slug)
        # Record before rendering: the write-up's premium note reads the flag.
        if metadata is not None:
            entry["leetcodePremium"] = bool((metadata or {}).get("leetcodePremium"))
        (PRACTICE_DIR / dir_slug).mkdir(parents=True, exist_ok=True)
        for path, content in render_all(entry, metadata, parsed_cases, parsed).items():
            path.write_text(content, encoding="utf-8")
        if parsed_cases.cases:
            entry["parse_status"] = "parsed-with-cases"
            stats["cases_parsed"] += 1
        else:
            entry["parse_status"] = (
                "parsed-empty-cases" if metadata else "metadata-unparseable"
            )
            stats["cases_empty"] += 1
        stats["generated"] += 1
    return stats


# ---------------------------------------------------------------------------
# Emission
# ---------------------------------------------------------------------------


def check(entries: Sequence[dict]) -> int:
    """Exit 0 when every scaffold on disk matches a fresh in-memory generation.

    Read-only: nothing is fetched, written, or rewritten. Cache misses do not
    mutate anything; they surface as stale files if the on-disk scaffold
    disagrees with what the cache regenerates.

    Args:
        entries: The delta manifest entries to verify.

    Returns:
        A process exit code: 0 when identical, 1 with a diff summary otherwise.
    """
    stale: List[str] = []
    for entry in entries:
        dir_slug = entry["dirSlug"]
        metadata = fetch_problem_metadata(entry["ncSlug"], delay=False, network=False)
        parsed = parse_description(str((metadata or {}).get("description") or ""))
        parsed_cases = cases_from_parsed(parsed, metadata, dir_slug)
        for path, expected in render_all(entry, metadata, parsed_cases, parsed).items():
            if not path.exists() or path.read_text(encoding="utf-8") != expected:
                try:
                    display = str(path.relative_to(REPO_ROOT))
                except ValueError:
                    display = str(path)
                stale.append(display)
    if stale:
        print(f"--check: {len(stale)} scaffold file(s) differ from a fresh generation:")
        for path in stale[:20]:
            print(f"  {path}")
        return 1
    print(f"--check: {len(entries)} problems up to date")
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
    parser.add_argument("--limit", type=int, default=None, help="Scaffold only the first N delta entries")
    parser.add_argument("--no-fetch", action="store_true", help="Never hit the network (cache-only)")
    parser.add_argument("--check", action="store_true", help="Verify scaffolds match a fresh generation; exit 0 when up to date")
    args = parser.parse_args(argv)

    manifest = load_manifest()
    validate_manifest(manifest)
    print(f"manifest: {len(manifest)} NeetCode 150 problems validated")
    delta = derive_delta(manifest)
    print(f"delta: {len(delta)} problems to scaffold")

    if args.check:
        # --check is read-only verification: it never fetches or writes.
        # It covers the generated scaffolds; the mkdocs Problems nav and
        # the landing-page tables are owned by generate_index_tables.py.
        return check(delta[: args.limit] if args.limit else delta)

    entries = delta[: args.limit] if args.limit else delta
    stats = emit_scaffolds(entries, fetch=not args.no_fetch)
    write_manifest(manifest)
    print(
        "scaffolds: {generated} generated | cases: {parsed} parsed, {empty} empty"
        " (skip with reason) | metadata failed to parse: {failed}".format(
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
    return 0


def write_manifest(manifest: Sequence[dict]) -> None:
    """Write scripts/neetcode150_manifest.json with the parse_status and premium flags."""
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(list(manifest), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    sys.exit(main())
