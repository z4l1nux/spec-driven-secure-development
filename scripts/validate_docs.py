"""Validate the repository's documentation structure and relative links."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
REQUIRED_FILES = (
    "AGENTS.md",
    "LICENSE",
    "templates/AGENTS.md",
    "templates/.pre-commit-config.yaml",
    "templates/specs/mission.md",
    "templates/specs/principles.md",
    "templates/specs/tech-stack.md",
    "templates/specs/roadmap.md",
    "templates/specs/STATE.md",
    "templates/specs/_feature/EXECUTE.md",
    "templates/specs/_feature/plan.md",
    "templates/specs/_feature/requirements.md",
    "templates/specs/_feature/security.md",
    "templates/specs/_feature/validation.md",
    "templates/specs/_feature/QA_CHECKLIST.md",
    "templates/specs/_feature/test-cases.yaml",
    "templates/specs/_feature/evals.yaml",
    "templates/skills/changelog/SKILL.md",
    "templates/skills/feature-spec/SKILL.md",
    "templates/.claude/agents/security-auditor.md",
    "templates/.claude/agents/code-reviewer.md",
    "templates/.claude/agents/performance-optimizer.md",
    "templates/.claude/agents/feature-developer.md",
)
WORKFLOW_REFERENCE = re.compile(r"`?(\.github/workflows/[A-Za-z0-9_.-]+\.ya?ml)`?")


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


def check_workflow_references(errors: list[str]) -> None:
    stack_file = ROOT / "specs/tech-stack.md"
    if not stack_file.is_file():
        return
    text = stack_file.read_text(encoding="utf-8")
    for workflow in WORKFLOW_REFERENCE.findall(text):
        if not (ROOT / workflow).is_file():
            errors.append(
                f"missing workflow reference: {stack_file.relative_to(ROOT)} -> {workflow}"
            )


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    check_markdown_links(errors)
    check_workflow_references(errors)
    if errors:
        print("Documentation validation failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("Documentation validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())