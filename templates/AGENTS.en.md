# AGENTS.md - Project Coding Rules

> Single source of truth for the project's AI coding agents.
> Edit `AGENTS.md` and export it to the formats used by the team.

## Before any change

1. Read `specs/principles.md`.
2. Identify the phase in `specs/roadmap.md` or create a feature spec.
3. Never write code without a spec.
4. Update the spec whenever behavior changes.

## Required gates

Before commit: pre-commit, type check, tests, and synchronized specs.
Before merge: all commit gates, green CI, human QA, changelog, and an ADR for irreversible decisions.

## Feature artifacts

Every feature uses `EXECUTE.md`, `plan.md`, `requirements.md`, `validation.md`, and `security.md`. Add `test-cases.yaml`, `evals.yaml`, and `QA_CHECKLIST.md` when applicable.

## Agent profiles and skills

Profiles live in `.claude/agents/`. Reusable workflows live in `skills/`. Implement slices in order, stop at `[HITL]`, and let `[AFK]` work proceed autonomously.

The Portuguese template remains the source file copied as `AGENTS.md`; this English file is a reference translation.
