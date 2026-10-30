"""Layout guard for command lines embedded in practice sources.

Commands embedded in practice docstrings and prose resolve from `practice/`,
so every `uv run python|pytest` path argument must start with a bank
directory (`leetcode/`, `amazon/`). The root tooling is invoked from
`practice/` itself and is allowlisted by bare filename. Run with:

    cd practice && uv run pytest ../scripts/
"""

import re
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
PRACTICE_DIR = SCRIPTS_DIR.parent / "practice"

ALLOWED_ROOT_FILES = {"progress.py", "test_progress.py"}
COMMAND_PATH = re.compile(r"uv run (?:python|pytest) (\S+)")


def command_path_violations():
    """Collect every embedded command path that is neither bank-prefixed nor allowlisted."""
    violations = []
    for path in sorted(PRACTICE_DIR.rglob("*.py")):
        # Hidden and virtualenv directories hold environment-owned content
        # (`.venv` site-packages alone is hundreds of files), not the repo
        # sources this guard protects.
        directory_parts = path.relative_to(PRACTICE_DIR).parts[:-1]
        if any(part.startswith(".") or part == "venv" for part in directory_parts):
            continue
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            for match in COMMAND_PATH.finditer(line):
                target = match.group(1)
                if target.startswith("-") or re.match(r"^(leetcode|amazon)/", target):
                    continue
                if target not in ALLOWED_ROOT_FILES:
                    violations.append(f"{path}: line {line_number}: {target}")
    return violations


def test_embedded_command_paths_use_bank_prefix_or_root_allowlist():
    violations = command_path_violations()
    assert not violations, "\n".join(violations)
