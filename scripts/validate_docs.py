"""Validate the repository's documentation structure and relative links."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
REQUIRED_FILES = (
    "templates/AGENTS.md",
    "templates/.pre-commit-config.yaml",
    "templates/specs/principles.md",
    "templates/.claude/agents/security-auditor.md",
)


def check_required_files(errors: list[str]) -> None:
    for relative_path in REQUIRED_FILES:
        if not (ROOT / relative_path).is_file():
            errors.append(f"missing required template: {relative_path}")


def check_markdown_links(errors: list[str]) -> None:
    for markdown_file in ROOT.rglob("*.md"):
        if any(part in {".git", ".venv", "node_modules"} for part in markdown_file.parts):
            continue
        text = markdown_file.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            target = target.strip().split()[0]
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = (markdown_file.parent / target.split("#", 1)[0]).resolve()
            if not target_path.exists():
                errors.append(
                    f"broken link: {markdown_file.relative_to(ROOT)} -> {target}"
                )


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    check_markdown_links(errors)
    if errors:
        print("Documentation validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("Documentation validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())