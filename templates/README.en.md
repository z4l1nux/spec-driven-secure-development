# SDSD Templates

Ready-to-use copies of the files referenced by the [SDSD technical guide](../GUIA-SDSD.en.md). They bootstrap a consumer project; replace `[placeholders]` after the Grill.

## Contents

| File | Destination | When to use |
|---|---|---|
| [`specs/mission.md`](specs/mission.md) | `specs/mission.md` | Constitution: mission and audience |
| [`specs/principles.md`](specs/principles.md) | `specs/principles.md` | Always: inviolable constraints |
| [`specs/tech-stack.md`](specs/tech-stack.md) | `specs/tech-stack.md` | Constitution: stack and security checks |
| [`specs/roadmap.md`](specs/roadmap.md) | `specs/roadmap.md` | Constitution: ordered work phases |
| [`specs/STATE.md`](specs/STATE.md) | `specs/STATE.md` | Persistent session memory |
| [`specs/_feature/`](specs/_feature/) | `specs/YYYY-MM-DD-name/` | Feature artifact stubs |
| [`AGENTS.md`](AGENTS.md) · [`AGENTS.en.md`](AGENTS.en.md) | `AGENTS.md` | Single source for agent coding rules; English reference included |
| [`.pre-commit-config.yaml`](.pre-commit-config.yaml) | `.pre-commit-config.yaml` | Local shift-left checks |
| [`.claude/agents/`](.claude/agents/) | `.claude/agents/` | `security-auditor`, `code-reviewer`, `feature-developer`, and `performance-optimizer` |
| [`skills/`](skills/) | `skills/` | Reusable changelog and feature-spec workflows |

## Quick setup

```bash
# 1. Copy the templates into the consumer project
cp -r templates/specs        /path/to/your/project/
cp    templates/AGENTS.md    /path/to/your/project/
cp    templates/.pre-commit-config.yaml /path/to/your/project/
cp -r templates/.claude      /path/to/your/project/
cp -r templates/skills       /path/to/your/project/

# 2. Enable pre-commit
cd /path/to/your/project
pipx install pre-commit
pre-commit install

# 3. Read specs/ and run the Grill described in the guide
# 4. Fill [placeholders] in specs/ and AGENTS.md
# 5. Export AGENTS.md to the tools used by the team
```

> This directory does not install the kit's CI. Create or adapt consumer-project
> workflows in `.github/workflows/` according to `specs/tech-stack.md`. The kit's
> `.harness/` is maintenance context and is not copied by default.

## Next steps

1. Complete the constitution files in `specs/`.
2. Copy `specs/_feature/` into a dated feature directory.
3. Run the Grill and complete the feature artifacts before writing code.
4. Execute `EXECUTE.md`, validate, then confirm with changelog, ADR, and `STATE.md`.
5. Synchronize `AGENTS.md` to `CLAUDE.md` and the other team tools.
