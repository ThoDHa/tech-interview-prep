"""Generate the docs/problems/index.md landing page and the mkdocs.yml
Problems nav for grind75.

Pipeline:
  1. Validate the three committed data sources: scripts/grind75_table.json
     (the 77 hand-maintained Grind 75 rows extracted from the original hand
     table), scripts/neetcode150_manifest.json (the 150-entry NeetCode
     track), and scripts/amazon_oa_manifest.json (the 350-entry Amazon OA
     bank, most recently updated first).
  2. Merge the two LeetCode tracks into one unified table: 168 unique
     problems, 59 of them on both tracks (one row, both credited). The
     Grind 75 sequence is the study-order backbone; each NeetCode-only
     problem is slotted next to the most related Grind 75 problem (or at
     the section boundary where its topic first appears) per the pinned
     anchor tables below. Rows carry no sequence numbers: the table is a
     study order, not a numbering scheme.
  3. Cross-reference the Amazon OA bank: rows whose problem also appears
     there (amazon slug minus the amazon- prefix matching a NeetCode
     lcSlug) carry an "Amazon OA" marker with a legend under the table.
  4. Emit three marker-bounded sections into docs/problems/index.md: the
     unified LeetCode table, the separate Amazon OA table, and the Sources
     credits. --check compares the marker spans against a fresh render, so
     the tables stay generator-owned and refreshable.
  5. Emit the mkdocs.yml Problems nav: the landing page as section parent
     (navigation.indexes) with two subsections, LeetCode (all 168 problem
     pages at one level, in the same interleaved study order) and Amazon
     OA (a section-with-page: the bank index is the section's own entry,
     with all 350 problem pages at one level beneath it, most recently
     updated first). --check verifies the nav shape, so the subsections
     stay generator-owned and refreshable.

Offline contract: the committed sources (JSON manifests and write-up
headers) are the only inputs; nothing is fetched, and the marker-bounded
spans (plus the nav's Problems section) are the only text ever rewritten.

Usage (from the repository root):
  cd practice && uv run pytest ../scripts/          # run the generator tests
  python3 scripts/generate_index_tables.py [--check]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import AbstractSet, List, Mapping, Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent
GRIND_TABLE_PATH = REPO_ROOT / "scripts" / "grind75_table.json"
NEETCODE_MANIFEST_PATH = REPO_ROOT / "scripts" / "neetcode150_manifest.json"
AMAZON_MANIFEST_PATH = REPO_ROOT / "scripts" / "amazon_oa_manifest.json"
AMAZON_DIFFICULTY_OVERRIDES_PATH = (
    REPO_ROOT / "scripts" / "amazon_difficulty_overrides.json"
)
PROBLEMS_INDEX_PATH = REPO_ROOT / "docs" / "problems" / "index.md"
MKDOCS_PATH = REPO_ROOT / "mkdocs.yml"

UNIFIED_SECTION_START = "<!-- unified-leetcode:start -->"
UNIFIED_SECTION_END = "<!-- unified-leetcode:end -->"
AMAZON_SECTION_START = "<!-- amazon-oa:start -->"
AMAZON_SECTION_END = "<!-- amazon-oa:end -->"
SOURCES_SECTION_START = "<!-- sources:start -->"
SOURCES_SECTION_END = "<!-- sources:end -->"
# Fresh splices land immediately before this heading; marker-bounded
# replacements keep their in-place position instead.
LANDING_ANCHOR = "## Study Guide and Practice"

NAV_PROBLEMS_MARKER = "  - Problems:\n"
NAV_LANDING_ENTRY = "    - problems/index.md\n"
NAV_LEETCODE_HEADER = '    - "LeetCode":\n'
NAV_AMAZON_HEADER = '    - "Amazon OA":\n'
NAV_AMAZON_INDEX_ENTRY = "      - problems/amazon_oa/index.md\n"
NAV_LEETCODE_CHILD_PATTERN = re.compile(r'^      - "(.+?)": problems/(.+?)\.md$')
NAV_AMAZON_CHILD_PATTERN = re.compile(r'^      - "(.+?)": problems/amazon_oa/(.+?)\.md$')
NAV_NEXT_TOP_PATTERN = re.compile(r"^  - ", re.M)

GRIND_TRACK = "Grind 75"
NEETCODE_TRACK = "NeetCode 150"
BOTH_TRACKS = "Grind 75 + NeetCode 150"

GRIND_ROW_COUNT = 77
NUMBERED_GRIND_COUNT = 75
NEETCODE_TRACK_SIZE = 150
AMAZON_ROW_COUNT = 350
GRIND_ONLY_COUNT = 18
OVERLAP_COUNT = 59
NEETCODE_ONLY_COUNT = 91
UNIQUE_PROBLEM_COUNT = GRIND_ROW_COUNT + NEETCODE_ONLY_COUNT

GRIND_TABLE_FIELDS = ("number", "slug", "title", "difficulty", "category", "time")
NEETCODE_MANIFEST_FIELDS = (
    "order",
    "section",
    "title",
    "lcSlug",
    "dirSlug",
    "difficulty",
    "ncSlug",
    "leetcodePremium",
)
AMAZON_MANIFEST_FIELDS = (
    "slug",
    "title",
    "url",
    "companies",
    "updated",
    "parse_status",
)
DIFFICULTIES = ("Easy", "Medium", "Hard")

# One category vocabulary for the unified table's emitted cells: the
# Grind 75 category names are the canonical tag set, and NeetCode
# section names that differ map onto them. A value may carry several
# comma-separated tags ("Arrays & Hashing" -> "Array, Hash Table"),
# decomposing the row so it matches every topic filter it belongs to;
# NeetCode's section granularity stays queryable in
# scripts/neetcode150_manifest.json. Unknown tags (the dash filler) pass
# through verbatim.
CATEGORY_CANONICAL = {
    "Trees": "Tree",
    "Graphs": "Graph",
    "Tries": "Trie",
    "Arrays & Hashing": "Array, Hash Table",
    "Heap / Priority Queue": "Heap",
    "1-D Dynamic Programming": "Dynamic Programming",
    "2-D Dynamic Programming": "Dynamic Programming",
    "Advanced Graphs": "Graph",
    "Math & Geometry": "Math",
}

AMAZON_SLUG_PREFIX = "amazon-"
LEETCODE_PROBLEM_URL = "https://leetcode.com/problems/"
NEETCODE_PROBLEM_URL = "https://neetcode.io/problems/"
GRIND_TRACK_URL = "https://www.techinterviewhandbook.org/grind75?order=grind75-order"
NEETCODE_TRACK_URL = "https://neetcode.io/practice/practice/neetcode150"
PRACTICE_LEETCODE = "LeetCode"
PRACTICE_NEETCODE = "NeetCode"
PRACTICE_FASTPREP = "FastPrep"

# The seven LeetCode-premium problems on the NeetCode track, pinned as
# lcSlug -> ncSlug: their "Practice at" cell links the NeetCode page (the
# free mirror) instead of the paywalled LeetCode one.
EXPECTED_PREMIUM_NC_SLUGS = {
    "encode-and-decode-strings": "string-encode-and-decode",
    "walls-and-gates": "islands-and-treasure",
    "graph-valid-tree": "valid-tree",
    "number-of-connected-components-in-an-undirected-graph": "count-connected-components",
    "alien-dictionary": "foreign-dictionary",
    "meeting-rooms": "meeting-schedule",
    "meeting-rooms-ii": "meeting-schedule-ii",
}

UNIFIED_TABLE_HEADER = "| Problem | Difficulty | Category | Practice at | Tracks | Time |"
UNIFIED_TABLE_SEPARATOR = "|---|---------|------------|----------|--------|------|"
AMAZON_TABLE_HEADER = "| Problem | Updated | Practice at | Time |"
AMAZON_TABLE_SEPARATOR = "|---|---------|---------|------|"
AMAZON_MARKER = "· Amazon OA"
AMAZON_LEGEND = (
    f"Rows marked {AMAZON_MARKER} also appear in the"
    " [Amazon OA bank](amazon_oa/index.md)."
)

# Difficulty-based Time estimates shared by every bank: the write-up
# header convention (Easy 15 / Medium 25 / Hard 40 minutes). The unknown
# marker mirrors the scaffold generator's header when FastPrep publishes
# no difficulty; its Time cell falls back to the hand-table's "-" filler.
ESTIMATED_MINUTES_BY_DIFFICULTY = {"Easy": 15, "Medium": 25, "Hard": 40}
UNKNOWN_DIFFICULTY_MARKER = "unknown difficulty"
UNKNOWN_TIME_CELL = "-"
AMAZON_WRITEUP_DIR = REPO_ROOT / "docs" / "problems" / "amazon_oa"
AMAZON_WRITEUP_DIFFICULTY_LINE = 3
AMAZON_WRITEUP_HEADER_PATTERN = re.compile(r"^\*\*(.+?)\*\* \| ")

# The interleave anchor tables pin how each NeetCode section attaches to
# the Grind 75 backbone. Resolution per section, in track order:
#   1. SECTION_SLUG_ANCHORS: right after the named Grind 75 problem.
#   2. SECTION_TAG_ANCHORS: right after the first Grind 75 problem whose
#      comma-separated Category shares one of the tags.
#   3. Fallback: right after the first Grind 75 problem that itself sits
#      in the section (opener), when neither table matches.
#   4. No anchor at all: the section's rows append at the end.
# SECTION_AFTER_ANCHORS overrides the outcome instead: the section lands
# immediately after the last row of its target topic block (the target
# section's own rows plus any Grind 75 rows in its tags), which keeps
# boundary topics after everything they extend. Only NeetCode-only rows
# move; overlap problems keep their Grind 75 slots.
SECTION_TAG_ANCHORS = {
    "Arrays & Hashing": ("Array", "Hash Table"),
    "Two Pointers": ("Two Pointers", "Sliding Window"),
    "Sliding Window": ("Sliding Window",),
    "Stack": ("Stack",),
    "Binary Search": ("Binary Search",),
    "Linked List": ("Linked List",),
    "Trees": ("Tree",),
    "Tries": ("Trie",),
    "Heap / Priority Queue": ("Heap",),
    "Backtracking": ("Backtracking",),
    "Graphs": ("Graph", "DFS", "BFS"),
    "1-D Dynamic Programming": ("Dynamic Programming",),
    "Greedy": ("Greedy",),
    "Math & Geometry": ("Math", "Geometry"),
}
SECTION_SLUG_ANCHORS = {
    # Pinned to the first Medium/Hard window problem on purpose: the tag
    # rule would otherwise anchor at best-time-to-buy-and-sell-stock (an
    # Easy backbone row in the first 20) and park the whole window block
    # ahead of its difficulty peers.
    "Sliding Window": "longest-substring-without-repeating-characters",
}
SECTION_AFTER_ANCHORS = {
    "Advanced Graphs": "Graphs",
    "2-D Dynamic Programming": "1-D Dynamic Programming",
    "Intervals": "Greedy",
    "Bit Manipulation": "Intervals",
}


class SourceError(ValueError):
    """Raised when a committed data source violates its contract."""


# ---------------------------------------------------------------------------
# Loading and validation
# ---------------------------------------------------------------------------


def _load_json_list(path: Path, source_name: str) -> list:
    """Read a JSON list file, raising SourceError with context on failure.

    Args:
        path: Path to the JSON file.
        source_name: Human-readable source name for error messages.

    Returns:
        The parsed JSON list.

    Raises:
        SourceError: When the file is missing, unreadable, invalid JSON,
            or not a JSON list.
    """
    if not path.exists():
        raise SourceError(f"{source_name} not found: {path}")
    try:
        entries = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise SourceError(f"{source_name} {path} is not valid JSON: {error}") from error
    if not isinstance(entries, list):
        raise SourceError(f"{source_name} {path} must be a JSON list")
    return entries


def _require_fields(entries: Sequence[dict], fields: Sequence[str], source_name: str) -> None:
    """Check that every entry carries the required fields.

    Args:
        entries: The manifest entries.
        fields: Required field names.
        source_name: Human-readable source name for error messages.

    Raises:
        SourceError: When an entry misses a field or is not an object.
    """
    for entry in entries:
        if not isinstance(entry, dict):
            raise SourceError(f"{source_name} entries must be JSON objects, got {type(entry).__name__}")
        missing = [field for field in fields if field not in entry]
        if missing:
            raise SourceError(
                f"{source_name} entry is missing field(s) {', '.join(missing)}: {entry}"
            )


def load_grind_table(path: Path = GRIND_TABLE_PATH) -> List[dict]:
    """Load the committed Grind 75 metadata table.

    Args:
        path: Path to grind75_table.json (default: scripts/grind75_table.json).

    Returns:
        The 77 rows in hand-table order.

    Raises:
        SourceError: When the file is missing or not a JSON list.
    """
    return _load_json_list(path, "Grind 75 table")


def validate_grind_table(rows: Sequence[dict]) -> None:
    """Check the Grind 75 table against the hand-table contract.

    The contract: exactly GRIND_ROW_COUNT rows with the hand-table fields,
    unique slugs, rows 1..75 numbered in order followed by the unnumbered
    extra rows.

    Args:
        rows: The loaded grind75_table.json rows.

    Raises:
        SourceError: On any contract violation.
    """
    if len(rows) != GRIND_ROW_COUNT:
        raise SourceError(f"Grind 75 table must carry {GRIND_ROW_COUNT} rows, got {len(rows)}")
    _require_fields(rows, GRIND_TABLE_FIELDS, "Grind 75 table")
    slugs = [row["slug"] for row in rows]
    duplicates = sorted({slug for slug in slugs if slugs.count(slug) > 1})
    if duplicates:
        raise SourceError(f"Grind 75 table has duplicate slug(s): {', '.join(duplicates)}")
    numbers = [row["number"] for row in rows]
    numbered = [number for number in numbers if number is not None]
    if numbered != list(range(1, NUMBERED_GRIND_COUNT + 1)):
        raise SourceError(
            "Grind 75 table numbering must be 1..75 in order followed by unnumbered rows,"
            f" got {numbered}"
        )
    for row in rows:
        if not isinstance(row["number"], int) and row["number"] is not None:
            raise SourceError(f"Grind 75 row number must be an integer or null: {row}")
        for field in ("slug", "title", "difficulty", "category", "time"):
            if not isinstance(row[field], str) or not row[field]:
                raise SourceError(f"Grind 75 row field {field} must be a non-empty string: {row}")


def load_neetcode_manifest(path: Path = NEETCODE_MANIFEST_PATH) -> List[dict]:
    """Load the committed NeetCode 150 manifest.

    Args:
        path: Path to neetcode150_manifest.json (default: scripts/neetcode150_manifest.json).

    Returns:
        The 150 entries in track order.

    Raises:
        SourceError: When the file is missing or not a JSON list.
    """
    return _load_json_list(path, "NeetCode 150 manifest")


def validate_neetcode_manifest(entries: Sequence[dict]) -> None:
    """Check the NeetCode 150 manifest against the merge-relevant contract.

    The full track contract (sections, difficulty totals) is owned by the
    NeetCode generator; this validates what the unified table consumes:
    NEETCODE_TRACK_SIZE entries, orders 1..150, unique lcSlugs and
    dirSlugs, canonical difficulties, a non-empty ncSlug per entry, and a
    leetcodePremium flag of True, False, or None.

    Args:
        entries: The loaded manifest entries.

    Raises:
        SourceError: On any contract violation.
    """
    if len(entries) != NEETCODE_TRACK_SIZE:
        raise SourceError(
            f"NeetCode 150 manifest must carry {NEETCODE_TRACK_SIZE} entries, got {len(entries)}"
        )
    _require_fields(entries, NEETCODE_MANIFEST_FIELDS, "NeetCode 150 manifest")
    orders = [entry["order"] for entry in entries]
    if orders != list(range(1, NEETCODE_TRACK_SIZE + 1)):
        raise SourceError(f"NeetCode 150 orders must be 1..{NEETCODE_TRACK_SIZE} in order")
    for slug_field in ("lcSlug", "dirSlug", "ncSlug"):
        slugs = [entry[slug_field] for entry in entries]
        if not all(isinstance(slug, str) and slug for slug in slugs):
            raise SourceError(f"NeetCode 150 {slug_field} must be a non-empty string")
        duplicates = sorted({slug for slug in slugs if slugs.count(slug) > 1})
        if duplicates:
            raise SourceError(
                f"NeetCode 150 manifest has duplicate {slug_field}(s): {', '.join(duplicates)}"
            )
    for entry in entries:
        if entry["difficulty"] not in DIFFICULTIES:
            raise SourceError(
                f"NeetCode 150 difficulty must be one of {', '.join(DIFFICULTIES)}: {entry}"
            )
        if entry["leetcodePremium"] not in (True, False, None):
            raise SourceError(
                f"NeetCode 150 leetcodePremium must be a boolean or null: {entry}"
            )


def load_amazon_manifest(path: Path = AMAZON_MANIFEST_PATH) -> List[dict]:
    """Load the committed Amazon OA manifest.

    Args:
        path: Path to amazon_oa_manifest.json (default: scripts/amazon_oa_manifest.json).

    Returns:
        The 350 entries, most recently updated first.

    Raises:
        SourceError: When the file is missing or not a JSON list.
    """
    return _load_json_list(path, "Amazon OA manifest")


def validate_amazon_manifest(entries: Sequence[dict]) -> None:
    """Check the Amazon OA manifest against the table contract.

    The contract: exactly AMAZON_ROW_COUNT entries with the manifest
    fields, unique slugs, sorted most recently updated first.

    Args:
        entries: The loaded Amazon OA manifest entries.

    Raises:
        SourceError: On any contract violation.
    """
    if len(entries) != AMAZON_ROW_COUNT:
        raise SourceError(f"Amazon OA manifest must carry {AMAZON_ROW_COUNT} entries, got {len(entries)}")
    _require_fields(entries, AMAZON_MANIFEST_FIELDS, "Amazon OA manifest")
    slugs = [entry["slug"] for entry in entries]
    if len(set(slugs)) != len(slugs):
        duplicates = sorted({slug for slug in slugs if slugs.count(slug) > 1})
        raise SourceError(f"Amazon OA manifest has duplicate slug(s): {', '.join(duplicates)}")
    updated = [entry["updated"] for entry in entries]
    if updated != sorted(updated, reverse=True):
        raise SourceError(
            "Amazon OA manifest must be sorted most recently updated first"
            f" (first out-of-order pair near {updated[0]!r})"
        )


# ---------------------------------------------------------------------------
# Time estimates
# ---------------------------------------------------------------------------


def estimated_time_cell(difficulty: Optional[str]) -> str:
    """Render the difficulty-based Time cell used wherever no minutes are
    published.

    The estimate reuses the write-up header convention: Easy 15,
    Medium 25, Hard 40 minutes. A difficulty outside that mapping (the
    Amazon write-ups' unknown-difficulty marker, or None) falls back to
    the hand-table's "-" filler.

    Args:
        difficulty: The canonical difficulty name, the unknown-difficulty
            marker, or None.

    Returns:
        The Time cell text ("NN minutes" or "-").
    """
    minutes = ESTIMATED_MINUTES_BY_DIFFICULTY.get(difficulty) if difficulty else None
    if minutes is None:
        return UNKNOWN_TIME_CELL
    return f"{minutes} minutes"


# ---------------------------------------------------------------------------
# Track merger
# ---------------------------------------------------------------------------


def merge_tracks(grind: Sequence[dict], neetcode: Sequence[dict]) -> List[dict]:
    """Merge the Grind 75 rows and the NeetCode 150 track into unified rows.

    Grind 75 rows keep their hand-table metadata verbatim and come first in
    hand-table order; NeetCode-only problems follow in track order with the
    section as category and a difficulty-based Time estimate (NeetCode
    publishes no minutes; the estimate reuses the write-up header
    convention via `estimated_time_cell`). Overlaps merge by lcSlug into
    one row carrying both track names, keeping the Grind 75 metadata.
    Every row records which NeetCode section it belongs to (None for
    Grind 75 rows) and whether the NeetCode track flags it as LeetCode
    premium (only NeetCode-only rows can be); the study order and the
    Practice-at column consume both.

    Args:
        grind: The validated grind75_table.json rows.
        neetcode: The validated neetcode150_manifest.json entries.

    Returns:
        Unified rows with slug, dirSlug, title, difficulty, category,
        tracks, time, section, and premium.
    """
    neet_by_lc_slug = {entry["lcSlug"]: entry for entry in neetcode}
    grind_slugs = {row["slug"] for row in grind}
    rows: List[dict] = []
    for row in grind:
        rows.append(
            {
                "slug": row["slug"],
                "dirSlug": row["slug"].replace("-", "_"),
                "title": row["title"],
                "difficulty": row["difficulty"],
                "category": row["category"],
                "tracks": BOTH_TRACKS if row["slug"] in neet_by_lc_slug else GRIND_TRACK,
                "time": row["time"],
                "section": None,
                "premium": False,
            }
        )
    for entry in neetcode:
        if entry["lcSlug"] in grind_slugs:
            continue
        rows.append(
            {
                "slug": entry["lcSlug"],
                "dirSlug": entry["dirSlug"],
                "title": entry["title"],
                "difficulty": entry["difficulty"],
                "category": entry["section"],
                "tracks": NEETCODE_TRACK,
                "time": estimated_time_cell(entry["difficulty"]),
                "section": entry["section"],
                "premium": entry["leetcodePremium"] is True,
            }
        )
    return rows


def verify_merge_shape(rows: Sequence[dict], neetcode: Sequence[dict]) -> None:
    """Check the committed merge against the expected universe split.

    Guards the constants against upstream data drift: a Grind 75 or
    NeetCode refresh that changes the overlap must update the constants
    consciously. The premium guard compares the full lcSlug -> ncSlug
    mapping of the premium rows against EXPECTED_PREMIUM_NC_SLUGS, so a
    changed NeetCode page slug for a premium problem is caught too.

    Args:
        rows: The merged rows.
        neetcode: The validated NeetCode manifest entries (ncSlug source).

    Raises:
        SourceError: When the track split or the premium mapping no longer
            matches the constants.
    """
    tracks = [row["tracks"] for row in rows]
    actual = {
        "unique": len(rows),
        "both": tracks.count(BOTH_TRACKS),
        "grind-only": tracks.count(GRIND_TRACK),
        "neetcode-only": tracks.count(NEETCODE_TRACK),
    }
    expected = {
        "unique": UNIQUE_PROBLEM_COUNT,
        "both": OVERLAP_COUNT,
        "grind-only": GRIND_ONLY_COUNT,
        "neetcode-only": NEETCODE_ONLY_COUNT,
    }
    if actual != expected:
        raise SourceError(
            "merged track split drifted from the constants"
            f" (expected {expected}, got {actual});"
            " refresh grind75_table.json / neetcode150_manifest.json and the constants together"
        )
    nc_slug_by_lc_slug = {entry["lcSlug"]: entry["ncSlug"] for entry in neetcode}
    actual_premium = {
        row["slug"]: nc_slug_by_lc_slug[row["slug"]] for row in rows if row["premium"]
    }
    if actual_premium != EXPECTED_PREMIUM_NC_SLUGS:
        raise SourceError(
            "premium rows drifted from EXPECTED_PREMIUM_NC_SLUGS"
            f" (expected {EXPECTED_PREMIUM_NC_SLUGS}, got {actual_premium});"
            " refresh the constant and the manifest together"
        )


# ---------------------------------------------------------------------------
# Interleaved study order
# ---------------------------------------------------------------------------


def category_tags(category: str) -> tuple:
    """Split a Grind 75 Category cell into its whitespace-trimmed tags.

    Args:
        category: The comma-separated category string (e.g. "Graph, DFS").

    Returns:
        The individual tags.
    """
    return tuple(tag.strip() for tag in category.split(","))


def canonical_category_cell(category: str) -> str:
    """Canonicalize one Category cell against CATEGORY_CANONICAL.

    Each comma-separated tag maps through the pinned vocabulary; a
    replacement value may itself carry several comma-separated tags and
    is split back into individual tags. Unknown tags (the dash filler)
    pass through verbatim.

    Args:
        category: The comma-separated category string as stored on the row.

    Returns:
        The canonical category string for the emitted cell.
    """
    canonical: List[str] = []
    for tag in category_tags(category):
        canonical.extend(
            replacement.strip()
            for replacement in CATEGORY_CANONICAL.get(tag, tag).split(",")
        )
    return ", ".join(canonical)


def _section_anchor_slug(
    section: str, backbone: Sequence[dict], section_members: dict
) -> Optional[str]:
    """Resolve the Grind 75 slug one section's rows slot in after.

    Resolution order: the pinned slug anchor, then the first backbone row
    sharing a pinned category tag, then the first backbone row that itself
    sits in the section (opener), then None (append at the end).

    Args:
        section: The NeetCode section name.
        backbone: The Grind 75 rows in study order.
        section_members: lcSlugs per NeetCode section (overlaps included).

    Returns:
        The anchor slug, or None when the section has no anchor.

    Raises:
        SourceError: When the pinned slug anchor is absent from the
            backbone (the pin and the Grind 75 table drifted apart).
    """
    if section in SECTION_SLUG_ANCHORS:
        slug = SECTION_SLUG_ANCHORS[section]
        if slug not in {row["slug"] for row in backbone}:
            raise SourceError(
                f"pinned anchor {slug!r} for {section!r} is not a Grind 75 row;"
                " refresh SECTION_SLUG_ANCHORS"
            )
        return slug
    tags = set(SECTION_TAG_ANCHORS.get(section, ()))
    if tags:
        for row in backbone:
            if tags & set(category_tags(row["category"])):
                return row["slug"]
    backbone_slugs = {row["slug"] for row in backbone}
    for slug in section_members.get(section, []):
        if slug in backbone_slugs:
            return slug
    return None


def _section_end_index(merged: Sequence[dict], target: str) -> int:
    """Find the last row of a target topic block in the merged order.

    The block spans the target section's own rows plus any Grind 75 rows
    in its pinned category tags.

    Args:
        merged: The rows merged so far.
        target: The section name whose block the caller extends past.

    Returns:
        The index of the block's last row.

    Raises:
        SourceError: When the target owns no rows and no Grind 75 category
            matches, so the boundary cannot be resolved.
    """
    tags = set(SECTION_TAG_ANCHORS.get(target, ()))
    candidates = [
        index
        for index, row in enumerate(merged)
        if row["section"] == target
        or (row["section"] is None and tags and tags & set(category_tags(row["category"])))
    ]
    if not candidates:
        raise SourceError(
            f"cannot place the section after {target!r}: the topic block is empty;"
            " refresh SECTION_AFTER_ANCHORS"
        )
    return max(candidates)


def interleave_study_order(rows: Sequence[dict], neetcode: Sequence[dict]) -> List[dict]:
    """Reorder merged rows into the interleaved study order.

    The Grind 75 sequence stays the backbone. Each NeetCode-only section's
    rows (kept contiguous, in track order) slot in after the anchor that
    `_section_anchor_slug` resolves; a SECTION_AFTER_ANCHORS entry moves
    the whole group past its target topic block instead. Only NeetCode-only
    rows move; overlap problems keep their Grind 75 slots.

    Args:
        rows: The merged rows (see `merge_tracks`).
        neetcode: The validated NeetCode manifest entries (section order).

    Returns:
        The interleaved rows.

    Raises:
        SourceError: When an anchor cannot be resolved.
    """
    sections = list(dict.fromkeys(entry["section"] for entry in neetcode))
    section_members: dict = {}
    for entry in neetcode:
        section_members.setdefault(entry["section"], []).append(entry["lcSlug"])
    backbone = [row for row in rows if row["section"] is None]
    groups: dict = {}
    for row in rows:
        if row["section"] is not None:
            groups.setdefault(row["section"], []).append(row)
    pending: dict = {}
    tail: List[dict] = []
    for section in sections:
        if section in SECTION_AFTER_ANCHORS or section not in groups:
            continue
        anchor = _section_anchor_slug(section, backbone, section_members)
        if anchor is None:
            tail.extend(groups[section])
        else:
            pending.setdefault(anchor, []).extend(groups[section])
    merged: List[dict] = []
    for row in backbone:
        merged.append(row)
        merged.extend(pending.get(row["slug"], []))
    merged.extend(tail)
    for section in sections:
        target = SECTION_AFTER_ANCHORS.get(section)
        if target is None or section not in groups:
            continue
        end = _section_end_index(merged, target)
        merged[end + 1 : end + 1] = groups[section]
    return merged


def study_order_rows(grind: Sequence[dict], neetcode: Sequence[dict]) -> List[dict]:
    """Merge the tracks and interleave them into the study order.

    Shared by the landing renderer and the nav renderer so the table and
    the sidebar can never disagree.

    Args:
        grind: The validated grind75_table.json rows.
        neetcode: The validated neetcode150_manifest.json entries.

    Returns:
        The interleaved unified rows.
    """
    merged = merge_tracks(grind, neetcode)
    verify_merge_shape(merged, neetcode)
    return interleave_study_order(merged, neetcode)


# ---------------------------------------------------------------------------
# Amazon overlap
# ---------------------------------------------------------------------------


def amazon_overlap_lc_slugs(
    neetcode: Sequence[dict], amazon: Sequence[dict]
) -> AbstractSet[str]:
    """Find the unified-table problems that also appear in the Amazon bank.

    The match rule: an Amazon slug minus the ``amazon-`` prefix equals a
    NeetCode lcSlug. Requiring the lcSlug match keeps the marker on the
    rows a reader reaches through the unified table's problem set; Grind-only
    problems absent from the NeetCode track stay unmarked.

    Args:
        neetcode: The NeetCode manifest entries.
        amazon: The Amazon OA manifest entries.

    Returns:
        The matching LeetCode slugs.
    """
    lc_slugs = {entry["lcSlug"] for entry in neetcode}
    return {
        stripped
        for entry in amazon
        if entry["slug"].startswith(AMAZON_SLUG_PREFIX)
        and (stripped := entry["slug"].removeprefix(AMAZON_SLUG_PREFIX)) in lc_slugs
    }


def amazon_writeup_difficulty(slug: str, docs_dir: Optional[Path] = None) -> Optional[str]:
    """Parse one Amazon OA write-up's difficulty from its committed header.

    The write-up's scaffold layout pins the metadata line at line 3:
    ``**<Difficulty>** | **NN minutes** | **<Topics>**``. The header's
    minutes are a literal placeholder, so the difficulty is the only
    parseable field; the unknown-difficulty marker maps to None and the
    Time column falls back to "-". Reading the committed tree keeps the
    whole pipeline offline and deterministic.

    Args:
        slug: The manifest slug (the write-up file name without .md).
        docs_dir: Overrides the docs/problems/amazon_oa directory
            (default: module constant).

    Returns:
        The canonical difficulty, or None when the header carries the
        unknown-difficulty marker.

    Raises:
        SourceError: When the write-up is missing, the header line does
            not match the scaffold layout, or the difficulty is not
            canonical.
    """
    docs_dir = docs_dir if docs_dir is not None else AMAZON_WRITEUP_DIR
    writeup_path = docs_dir / f"{slug}.md"
    if not writeup_path.exists():
        raise SourceError(f"Amazon OA write-up not found: {writeup_path}")
    lines = writeup_path.read_text(encoding="utf-8").splitlines()
    header = (
        lines[AMAZON_WRITEUP_DIFFICULTY_LINE - 1]
        if len(lines) >= AMAZON_WRITEUP_DIFFICULTY_LINE
        else None
    )
    match = AMAZON_WRITEUP_HEADER_PATTERN.match(header) if header is not None else None
    if match is None:
        raise SourceError(
            f"Amazon OA write-up {slug} has no **difficulty** header at line"
            f" {AMAZON_WRITEUP_DIFFICULTY_LINE}: {writeup_path}"
        )
    difficulty = match.group(1)
    if difficulty == UNKNOWN_DIFFICULTY_MARKER:
        return None
    if difficulty not in DIFFICULTIES:
        raise SourceError(
            f"Amazon OA write-up {slug} header difficulty must be one of"
            f" {', '.join(DIFFICULTIES)} or {UNKNOWN_DIFFICULTY_MARKER!r}:"
            f" got {difficulty!r} in {writeup_path}"
        )
    return difficulty


# ---------------------------------------------------------------------------
# Amazon difficulty overrides
# ---------------------------------------------------------------------------


def load_amazon_difficulty_overrides(
    path: Path = AMAZON_DIFFICULTY_OVERRIDES_PATH,
) -> dict:
    """Load the committed slug -> difficulty overrides for the Amazon rows.

    FastPrep publishes no difficulty on 24 bank pages, so their write-up
    headers carry the unknown-difficulty marker and their table rows dash.
    This file, populated from FastPrep's own pages as they become
    available, is consulted before the header parse. An absent file is
    the empty mapping (the revert path: deleting it and regenerating
    restores the old dashes); anything present must be one JSON object.

    Args:
        path: Path to amazon_difficulty_overrides.json (default: module
            constant).

    Returns:
        The slug -> difficulty mapping, empty when the file is absent.

    Raises:
        SourceError: When the file is unreadable, invalid JSON, or not a
            JSON object.
    """
    if not path.exists():
        return {}
    try:
        overrides = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise SourceError(f"Amazon difficulty overrides {path} is not valid JSON: {error}") from error
    if not isinstance(overrides, dict):
        raise SourceError(f"Amazon difficulty overrides {path} must be a JSON object")
    return overrides


def validate_amazon_difficulty_overrides(
    overrides: dict, amazon: Sequence[dict]
) -> None:
    """Check the overrides against the manifest they decorate.

    The contract: every slug is a manifest slug (the override addresses a
    real bank row) and every difficulty is canonical (it feeds the Time
    estimate and the filter's Difficulty select directly).

    Args:
        overrides: The slug -> difficulty mapping.
        amazon: The validated Amazon OA manifest entries.

    Raises:
        SourceError: When a slug is absent from the manifest or a
            difficulty is not canonical.
    """
    slugs = {entry["slug"] for entry in amazon}
    for slug, difficulty in overrides.items():
        if slug not in slugs:
            raise SourceError(
                f"Amazon difficulty override names an unknown slug {slug!r};"
                f" the manifest carries {len(slugs)} slugs"
            )
        if difficulty not in DIFFICULTIES:
            raise SourceError(
                f"Amazon difficulty override for {slug!r} must be one of"
                f" {', '.join(DIFFICULTIES)}: got {difficulty!r}"
            )


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------


def practice_at_cell(row: dict) -> str:
    """Render a unified row's Practice-at cell.

    LeetCode-premium rows link the problem's NeetCode page (the free
    mirror); every other row links the canonical leetcode.com page.

    Args:
        row: One unified row.

    Returns:
        The markdown link for the cell.
    """
    if row["premium"]:
        slug = EXPECTED_PREMIUM_NC_SLUGS[row["slug"]]
        return f"[{PRACTICE_NEETCODE}]({NEETCODE_PROBLEM_URL}{slug})"
    return f"[{PRACTICE_LEETCODE}]({LEETCODE_PROBLEM_URL}{row['slug']}/)"


def track_link(track: str) -> str:
    """Render one track name as a link to its curator's list page.

    Args:
        track: The track name (Grind 75 or NeetCode 150).

    Returns:
        The markdown link for the track.
    """
    url = GRIND_TRACK_URL if track == GRIND_TRACK else NEETCODE_TRACK_URL
    return f"[{track}]({url})"


def tracks_cell(row: dict) -> str:
    """Render a unified row's Tracks cell, linking each curator's list.

    Args:
        row: One unified row.

    Returns:
        The track names joined with " + ", each linking its list page.
    """
    if row["tracks"] == BOTH_TRACKS:
        tracks = (GRIND_TRACK, NEETCODE_TRACK)
    else:
        tracks = (row["tracks"],)
    return " + ".join(track_link(track) for track in tracks)


def render_unified_section(rows: Sequence[dict], overlap: AbstractSet[str]) -> str:
    """Render the marker-bounded unified LeetCode table section.

    Columns `| Problem | Difficulty | Category | Practice at | Tracks |
    Time |`; rows carry no sequence numbers. `Category` renders through
    `canonical_category_cell` so both tracks share one topic vocabulary.
    `Problem` links the write-up,
    `Practice at` links where the problem lives (LeetCode, or the NeetCode
    page for premium problems), and `Tracks` links each curator's list.
    `Time` carries the Grind 75 suggested minutes where published and
    difficulty-based estimates elsewhere. Rows in the overlap set carry
    the Amazon OA marker in the Tracks cell, with a legend under the table.

    Args:
        rows: The interleaved unified rows.
        overlap: LeetCode slugs from these rows also in the Amazon OA bank.

    Returns:
        The section text: start marker through end marker, trailing newline.
    """
    overlap_count = sum(1 for row in rows if row["tracks"] == BOTH_TRACKS)
    lines = [
        UNIFIED_SECTION_START,
        "## Problem List",
        "",
        f"The unified LeetCode problem set across the"
        f" [Grind 75](https://www.techinterviewhandbook.org/grind75)"
        f" and the [NeetCode 150](https://neetcode.io/practice/practice/neetcode150):"
        f" {len(rows)} unique problems, {overlap_count} on both tracks and credited to each."
        " Rows follow one interleaved study order: the Grind 75 sequence as the backbone,"
        " with each NeetCode-only problem slotted next to its closest Grind 75 topic."
        " Practice at links where the problem lives:"
        f" {PRACTICE_LEETCODE} for free problems, {PRACTICE_NEETCODE} for LeetCode-premium ones."
        " Tracks names the plan(s) a problem belongs to and links each curator's list;"
        " Time carries the Grind 75 suggested minutes where published and"
        " difficulty-based estimates elsewhere (Easy 15 / Medium 25 / Hard 40 minutes,"
        " a dash where the difficulty is unknown).",
        "",
        UNIFIED_TABLE_HEADER,
        UNIFIED_TABLE_SEPARATOR,
    ]
    for row in rows:
        problem = f"[{row['title']}]({row['dirSlug']}.md)"
        category = canonical_category_cell(row["category"])
        tracks = tracks_cell(row)
        if row["slug"] in overlap:
            tracks = f"{tracks} {AMAZON_MARKER}"
        lines.append(
            f"| {problem} | {row['difficulty']}"
            f" | {category} | {practice_at_cell(row)} | {tracks} | {row['time']} |"
        )
    if any(row["slug"] in overlap for row in rows):
        lines.append("")
        lines.append(AMAZON_LEGEND)
    lines.append(UNIFIED_SECTION_END)
    return "\n".join(lines) + "\n"


def render_amazon_section(
    entries: Sequence[dict], overrides: Mapping[str, str]
) -> str:
    """Render the marker-bounded Amazon OA table section.

    Separate from the LeetCode tables: columns `| Problem | Updated |
    Practice at | Time |`, most recently updated first, `Problem` linking
    the write-up page, `Practice at` linking the problem's FastPrep page,
    and `Time` carrying the difficulty-based estimate. The difficulty
    comes from the slug -> difficulty overrides when one addresses the
    row (FastPrep publishes none on some pages; the committed
    amazon_difficulty_overrides.json fills them) and the write-up header
    parse otherwise.

    Args:
        entries: The validated Amazon OA manifest entries.
        overrides: Slug -> difficulty consulted before each write-up's
            header parse; pass the loader's result, or an empty mapping
            when no overrides apply.

    Returns:
        The section text: start marker through end marker, trailing newline.

    Raises:
        SourceError: When an override names an unknown slug or a
            non-canonical difficulty, or a write-up header fails its
            parse.
    """
    validate_amazon_difficulty_overrides(overrides, entries)
    lines = [
        AMAZON_SECTION_START,
        "## Amazon OA Problems",
        "",
        "The Amazon OA coding bank, separate from the LeetCode tables above:"
        f" {len(entries)} Amazon-tagged online-assessment problems, most recently"
        " updated first. The problems come from"
        " [perixtar/Tech-OA-Interview-Questions](https://github.com/perixtar/Tech-OA-Interview-Questions)"
        " with statement pages on [FastPrep](https://www.fastprep.io)."
        " The full bank index with companies lives at"
        " [problems/amazon_oa/index.md](amazon_oa/index.md);"
        " practice stubs live under the"
        " [`practice/amazon_oa/`](https://github.com/ThoDHa/tech-interview-prep/tree/main/practice/amazon_oa)"
        " workspace. Time carries difficulty-based estimates"
        " (Easy 15 / Medium 25 / Hard 40 minutes, a dash where the difficulty"
        " is unknown), from the committed difficulty overrides where present"
        " and each write-up's difficulty header otherwise.",
        "",
        AMAZON_TABLE_HEADER,
        AMAZON_TABLE_SEPARATOR,
    ]
    for entry in entries:
        problem = f"[{entry['title']}](amazon_oa/{entry['slug']}.md)"
        practice = f"[{PRACTICE_FASTPREP}]({entry['url']})"
        difficulty = overrides.get(entry["slug"]) or amazon_writeup_difficulty(
            entry["slug"]
        )
        time_cell = estimated_time_cell(difficulty)
        lines.append(f"| {problem} | {entry['updated']} | {practice} | {time_cell} |")
    lines.append(AMAZON_SECTION_END)
    return "\n".join(lines) + "\n"


def render_sources_section() -> str:
    """Render the marker-bounded Sources credits section.

    Credits all three upstream list curators; static by design (the credits
    do not depend on the data files).

    Returns:
        The section text: start marker through end marker, trailing newline.
    """
    lines = [
        SOURCES_SECTION_START,
        "## Sources",
        "",
        "The three problem banks are curated elsewhere; this site adds the"
        " write-ups, pattern guides, and practice workspace.",
        "",
        "- [Grind 75](https://www.techinterviewhandbook.org/grind75), curated by the"
        " [Tech Interview Handbook](https://www.techinterviewhandbook.org/) team.",
        "- [NeetCode 150](https://neetcode.io/practice/practice/neetcode150), curated by the"
        " [NeetCode](https://neetcode.io/) team.",
        "- The Amazon OA bank, from"
        " [perixtar/Tech-OA-Interview-Questions](https://github.com/perixtar/Tech-OA-Interview-Questions)"
        " with problem pages on [FastPrep](https://www.fastprep.io).",
        SOURCES_SECTION_END,
    ]
    return "\n".join(lines) + "\n"


def load_validated_sources() -> tuple:
    """Load and validate all three committed data sources.

    Shared by the render, emission, and check paths so every consumer sees
    the same contract enforcement.

    Returns:
        The (grind rows, neetcode entries, amazon entries) triple.

    Raises:
        SourceError: When any source violates its contract.
    """
    grind = load_grind_table()
    neetcode = load_neetcode_manifest()
    amazon = load_amazon_manifest()
    validate_grind_table(grind)
    validate_neetcode_manifest(neetcode)
    validate_amazon_manifest(amazon)
    return grind, neetcode, amazon


def render_sections() -> List[tuple]:
    """Render every docs/problems/index.md section this generator owns.

    Shared by the emission and check paths so the two can never drift.

    Returns:
        One (name, start marker, end marker, rendered text) tuple per
        section, in document order.
    """
    grind, neetcode, amazon = load_validated_sources()
    merged = study_order_rows(grind, neetcode)
    overlap = amazon_overlap_lc_slugs(neetcode, amazon)
    return [
        (
            "unified-leetcode",
            UNIFIED_SECTION_START,
            UNIFIED_SECTION_END,
            render_unified_section(merged, overlap),
        ),
        (
            "amazon-oa",
            AMAZON_SECTION_START,
            AMAZON_SECTION_END,
            render_amazon_section(amazon, load_amazon_difficulty_overrides()),
        ),
        ("sources", SOURCES_SECTION_START, SOURCES_SECTION_END, render_sources_section()),
    ]


# ---------------------------------------------------------------------------
# Emission
# ---------------------------------------------------------------------------


def write_sections(landing_path: Optional[Path] = None) -> bool:
    """Emit the three marker-bounded sections into docs/problems/index.md.

    Present marker spans are replaced in place; absent sections are spliced
    as one block immediately before the landing anchor. Only the marker
    spans (and the fresh splice point) are ever rewritten.

    Args:
        landing_path: Overrides the docs/problems/index.md path (default:
            module constant).

    Returns:
        True when the file was modified, False when it already matched.

    Raises:
        SystemExit: When markers are unclosed or no landing anchor exists.
    """
    landing_path = landing_path if landing_path is not None else PROBLEMS_INDEX_PATH
    text = landing_path.read_text(encoding="utf-8")
    original = text
    missing: List[str] = []
    for _name, start_marker, end_marker, rendered in render_sections():
        start_at = text.find(start_marker)
        if start_at == -1:
            missing.append(rendered)
            continue
        end_at = text.find(end_marker, start_at)
        if end_at == -1:
            raise SystemExit(f"{landing_path} has {start_marker!r} without {end_marker!r}")
        text = text[:start_at] + rendered.rstrip() + text[end_at + len(end_marker) :]
    if missing:
        anchor_at = text.find(LANDING_ANCHOR)
        if anchor_at == -1:
            raise SystemExit(
                f"{landing_path} has no {LANDING_ANCHOR!r} anchor to splice the"
                f" {len(missing)} missing section(s) against"
            )
        block = "\n\n".join(missing)
        text = text[:anchor_at] + block + "\n\n" + text[anchor_at:]
    if text == original:
        return False
    landing_path.write_text(text, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# mkdocs.yml Problems nav
# ---------------------------------------------------------------------------


def render_problems_nav(merged: Sequence[dict], amazon: Sequence[dict]) -> str:
    """Render the Problems nav block: landing parent plus two subsections.

    The landing page is the section parent (mkdocs-material's
    navigation.indexes renders it as the Problems index); the LeetCode
    subsection carries every merged row at one level in the interleaved
    study order (the unified table's order); the Amazon OA subsection
    carries the bank index as its own link (the section's first entry,
    which navigation.indexes turns into the subsection link) with every
    bank entry beneath it at one level, most recently updated first (the
    manifest order, the bank table's order).

    Args:
        merged: The validated interleaved rows (see `study_order_rows`).
        amazon: The validated Amazon OA manifest entries.

    Returns:
        The nav block from the Problems marker through the last Amazon OA
        child, each line newline-terminated.
    """
    lines = [
        NAV_PROBLEMS_MARKER,
        NAV_LANDING_ENTRY,
        NAV_LEETCODE_HEADER,
    ]
    lines.extend(
        f'      - "{row["title"]}": problems/{row["dirSlug"]}.md\n' for row in merged
    )
    lines.append(NAV_AMAZON_HEADER)
    lines.append(NAV_AMAZON_INDEX_ENTRY)
    lines.extend(
        f'      - "{entry["title"]}": problems/amazon_oa/{entry["slug"]}.md\n'
        for entry in amazon
    )
    return "".join(lines)


def write_problems_nav(mkdocs_path: Optional[Path] = None) -> bool:
    """Replace the mkdocs.yml Problems nav section with the generated shape.

    Everything between the Problems marker and the next top-level nav entry
    (a line starting with exactly two spaces, a hyphen, and a space) or the
    end of file is regenerated; everything outside the section is untouched.

    Args:
        mkdocs_path: Overrides the mkdocs.yml path (default: module constant).

    Returns:
        True when the file was modified, False when it already matched.

    Raises:
        SystemExit: When mkdocs.yml has no Problems nav section.
    """
    mkdocs_path = mkdocs_path if mkdocs_path is not None else MKDOCS_PATH
    text = mkdocs_path.read_text(encoding="utf-8")
    marker_at = text.find(NAV_PROBLEMS_MARKER)
    if marker_at == -1:
        raise SystemExit("mkdocs.yml has no Problems nav section to replace")
    section_at = marker_at + len(NAV_PROBLEMS_MARKER)
    next_top_at = len(text)
    for match in NAV_NEXT_TOP_PATTERN.finditer(text[section_at:]):
        next_top_at = section_at + match.start()
        break
    _grind, _neetcode, _amazon = load_validated_sources()
    merged = study_order_rows(_grind, _neetcode)
    updated = text[:marker_at] + render_problems_nav(merged, _amazon) + text[next_top_at:]
    if updated == text:
        return False
    mkdocs_path.write_text(updated, encoding="utf-8")
    return True


# ---------------------------------------------------------------------------
# Idempotency check
# ---------------------------------------------------------------------------


def check(landing_path: Optional[Path] = None) -> int:
    """Exit 0 when every owned landing section matches a fresh render.

    Read-only: nothing is written or rewritten.

    Args:
        landing_path: Overrides the docs/problems/index.md path (default:
            module constant).

    Returns:
        A process exit code: 0 when identical, 1 with a diff summary otherwise.
    """
    landing_path = landing_path if landing_path is not None else PROBLEMS_INDEX_PATH
    stale: List[str] = []
    sections = render_sections()
    if not landing_path.exists():
        stale.append("docs/problems/index.md (missing)")
        text = ""
    else:
        text = landing_path.read_text(encoding="utf-8")
    for name, start_marker, end_marker, rendered in sections:
        start_at = text.find(start_marker)
        if start_at == -1:
            stale.append(f"docs/problems/index.md (no {name} markers)")
            continue
        end_at = text.find(end_marker, start_at)
        if end_at == -1:
            stale.append(f"docs/problems/index.md ({name} markers unclosed)")
            continue
        if text[start_at : end_at + len(end_marker)] != rendered.rstrip():
            stale.append(f"docs/problems/index.md ({name} section differs)")
    if stale:
        print(f"--check: {len(stale)} index section(s) differ from a fresh generation:")
        for item in stale[:20]:
            print(f"  {item}")
        return 1
    print(f"--check: {len(sections)} index sections up to date")
    return check_problems_nav()


def check_problems_nav(mkdocs_path: Optional[Path] = None) -> int:
    """Exit 0 when the committed mkdocs.yml Problems nav matches a fresh render.

    The audit compares the whole Problems span in mkdocs.yml (from the
    Problems marker through the next top-level nav entry, or the end of
    file) against a fresh render: rogue entries inside the section, child
    order, duplicates, extras, and omissions are all drift. The landing
    parent line, both subsection headers, and the Amazon OA children must
    all sit exactly where the fresh render puts them.

    Args:
        mkdocs_path: Overrides the mkdocs.yml path (default: module constant).

    Returns:
        A process exit code: 0 when the nav matches, 1 with a diff summary
        otherwise.
    """
    mkdocs_path = mkdocs_path if mkdocs_path is not None else MKDOCS_PATH
    stale: List[str] = []
    text = mkdocs_path.read_text(encoding="utf-8") if mkdocs_path.exists() else ""
    _grind, _neetcode, _amazon = load_validated_sources()
    merged = study_order_rows(_grind, _neetcode)
    fresh = render_problems_nav(merged, _amazon)
    if not text:
        stale.append("mkdocs.yml (missing)")
    elif text.count(NAV_PROBLEMS_MARKER) != 1:
        stale.append("mkdocs.yml (Problems nav section not found exactly once)")
    else:
        at = text.find(NAV_PROBLEMS_MARKER)
        section_at = at + len(NAV_PROBLEMS_MARKER)
        next_top_at = len(text)
        for match in NAV_NEXT_TOP_PATTERN.finditer(text[section_at:]):
            next_top_at = section_at + match.start()
            break
        if text[at:next_top_at] != fresh:
            stale.append(
                "mkdocs.yml (Problems nav drift: "
                + nav_child_drift_detail(text[at:], merged, _amazon)
                + ")"
            )
    if stale:
        print(f"--check: {len(stale)} nav audit finding(s):")
        for item in stale[:20]:
            print(f"  {item}")
        return 1
    print(
        f"--check: mkdocs Problems nav up to date ({len(merged)} LeetCode children,"
        f" {len(_amazon)} Amazon OA children)"
    )
    return 0


def nav_child_drift_detail(
    problems_text: str, merged: Sequence[dict], amazon: Sequence[dict]
) -> str:
    """Describe how one Problems nav span drifts from a fresh render.

    Compares both subsections' children against the fresh renders of the
    committed sources and names the first recognizable kind of drift.

    Args:
        problems_text: The mkdocs.yml text starting at the Problems marker.
        merged: The merged rows from the committed sources (the LeetCode
            subsection's expected children).
        amazon: The Amazon OA manifest entries (the Amazon subsection's
            expected children).

    Returns:
        A short human-readable drift summary.
    """
    actual_leetcode = nav_leetcode_children(problems_text)
    expected_leetcode = [row["dirSlug"] for row in merged]
    actual_amazon = nav_amazon_children(problems_text)
    expected_amazon = [entry["slug"] for entry in amazon]
    detail = []
    for label, source, actual, expected in (
        ("LeetCode", "unified table", actual_leetcode, expected_leetcode),
        ("Amazon OA", "manifest table", actual_amazon, expected_amazon),
    ):
        if len(actual) != len(set(actual)):
            dupes = sorted({slug for slug in actual if actual.count(slug) > 1})
            detail.append(f"{label} duplicates: {', '.join(dupes[:5])}")
        extras = sorted(set(actual) - set(expected))
        if extras:
            detail.append(f"{label} extra: {', '.join(extras[:5])}")
        missing = sorted(set(expected) - set(actual))
        if missing:
            detail.append(f"{label} missing: {', '.join(missing[:5])}")
        if not detail and actual != expected:
            detail.append(f"{label} child order drifts from the {source}")
    if not detail:
        if NAV_LANDING_ENTRY not in problems_text:
            detail.append("no problems/index.md landing parent")
        else:
            detail.append("unrecognized entries inside the Problems section")
    return "; ".join(detail)


def bounded_nav_children(text: str, child_pattern: re.Pattern) -> List[str]:
    """Collect the child slugs a nav child pattern matches, line by line.

    Shared by both subsection scanners: the bounded scan starts at the
    beginning of `text` and stops at the first line the pattern does not
    match, so a span ending at the next top-level nav entry or the end of
    file cannot leak trailing entries into the list.

    Args:
        text: The mkdocs.yml text starting just after the subsection's
            anchor (the subsection header, or the bank index entry).
        child_pattern: The child line pattern; match group 2 carries the
            child slug.

    Returns:
        The child slugs in file order; empty when none match.
    """
    children: List[str] = []
    for line in text.splitlines():
        match = child_pattern.match(line)
        if match is None:
            break
        children.append(match.group(2))
    return children


def nav_leetcode_children(problems_text: str) -> List[str]:
    """Extract the LeetCode subsection's dirSlugs in file order.

    Args:
        problems_text: The mkdocs.yml text starting at the Problems marker.

    Returns:
        The child dirSlugs between the LeetCode header and the first line
        that is not a LeetCode child; empty when the header is absent.
    """
    header_at = problems_text.find(NAV_LEETCODE_HEADER)
    if header_at == -1:
        return []
    return bounded_nav_children(
        problems_text[header_at + len(NAV_LEETCODE_HEADER) :],
        NAV_LEETCODE_CHILD_PATTERN,
    )


def nav_amazon_children(problems_text: str) -> List[str]:
    """Extract the Amazon OA subsection's bank slugs in file order.

    The subsection opens with the bank index entry (the subsection's own
    link); the bounded child scan starts after it.

    Args:
        problems_text: The mkdocs.yml text starting at the Problems marker.

    Returns:
        The child bank slugs between the bank index entry and the first
        line that is not an Amazon child; empty when the header or the
        index entry is absent.
    """
    header_at = problems_text.find(NAV_AMAZON_HEADER)
    if header_at == -1:
        return []
    body_at = header_at + len(NAV_AMAZON_HEADER)
    if not problems_text.startswith(NAV_AMAZON_INDEX_ENTRY, body_at):
        return []
    return bounded_nav_children(
        problems_text[body_at + len(NAV_AMAZON_INDEX_ENTRY) :],
        NAV_AMAZON_CHILD_PATTERN,
    )


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
    parser.add_argument("--check", action="store_true", help="Verify the index sections match a fresh generation; exit 0 when up to date")
    args = parser.parse_args(argv)

    grind, neetcode, amazon = load_validated_sources()
    print(
        f"sources: {len(grind)} Grind 75 rows, {len(neetcode)} NeetCode 150 entries,"
        f" {len(amazon)} Amazon OA entries validated"
    )

    if args.check:
        # --check is read-only verification: it never writes.
        return check()

    landing_written = write_sections()
    print(
        "landing: sections written"
        if landing_written
        else "landing: sections already up to date"
    )
    if write_problems_nav():
        print("nav: Problems section written")
    else:
        print("nav: Problems section already up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
