# Technical Guide: Spec-Driven Secure Development (SDSD)

[Portuguese edition](GUIA-SDSD.md)

> Hands-on reference for project teams.
> Covers new and legacy projects.
> Compatible with Claude Code, Cursor, Copilot, Windsurf, and Codex.

## What is SDSD?

Spec-Driven Secure Development is a workflow where every feature starts with a written specification before code. The AI agent works from specs rather than loose prompts, preserving traceability, stakeholder alignment, and reviewable code.

**Core principle:** the spec is the source of truth. Code implements the spec. The changelog records history.

## Onboarding

1. Install the agent used by the team.
2. Read `specs/mission.md`, `specs/principles.md`, `specs/tech-stack.md`, and `specs/roadmap.md` in that order.
3. Use P -> E -> V for small work, or the full P -> R -> E -> V -> C cycle for larger features.
4. Never write code without a spec.
5. Update the spec whenever implementation behavior changes.

If the project has no `specs/`, follow the New Project path. If it already has code but no specs, follow the Legacy Project path.

## Kit and consumer project boundary

This repository is the kit. A consumer project is the product repository that adopts it.

| Layer | Consumer artifacts | Responsibility |
|---|---|---|
| Methodology | `GUIA-SDSD.md` | Workflow, prompts, gates, and scale |
| Bootstrap | `templates/` | Initial files for a consumer project |
| Constitution | `specs/mission.md`, `principles.md`, `tech-stack.md`, `roadmap.md` | Purpose, constraints, stack, and sequence |
| Feature | `specs/YYYY-MM-DD-name/` | Requirements, plan, security, and validation |
| Agent governance | `AGENTS.md`, `.claude/`, `skills/` | Rules, profiles, and repeatable workflows |
| Verification | `.pre-commit-config.yaml`, `.github/workflows/` | Local and pre-merge gates |
| Memory and history | `specs/STATE.md`, `specs/adr/`, `CHANGELOG.md` | Context, irreversible decisions, and history |

The root `specs/`, `.harness/`, and `.github/workflows/` in this repository belong to the maintenance of the SDSD kit. They are not automatically the constitution, context, or CI of a consumer application.

For the bootstrap procedure, read [templates/README.en.md](templates/README.en.md).

## Workflow scale

| Scale | Stages | Minimum artifacts | Use when |
|---|---|---|---|
| QUICK | E -> V | Commit and changelog | Bugfix or small copy/visual change |
| SMALL | P -> E -> V | `plan.md`, `validation.md` | Simple feature or route |
| MEDIUM | P -> R -> E -> V | Plus `requirements.md`, `security.md` | Regular feature or integration |
| LARGE | P -> R -> E -> V -> C | Plus tests/evals, QA checklist, and ADR | Complex system or compliance work |

Stages are: **P** Plan, **R** Review, **E** Execute, **V** Validate, and **C** Confirm. When uncertain, use MEDIUM.

## Part 1 - New project

### Step 1: Create the constitution

Complete these four files before production code:

- `specs/mission.md`: why the project exists, what it does, audience, and measurable success.
- `specs/principles.md`: inviolable security, privacy, quality, UX, and operational constraints.
- `specs/tech-stack.md`: language, framework, database, tests, and SAST/SCA/secrets commands.
- `specs/roadmap.md`: small, independently mergeable phases.

Use the Grill before writing the files: ask one question at a time, with a recommended answer. Cover mission, principles, stack, and roadmap.

### Step 2: Create a feature spec

Read the next unchecked phase in `specs/roadmap.md`, create a branch, and create `specs/YYYY-MM-DD-name/` with:

- `EXECUTE.md`: ready-to-run implementation prompt.
- `plan.md`: vertical slices marked `[AFK]` or `[HITL]`.
- `requirements.md`: scope, decisions, context, and non-functional requirements.
- `test-cases.yaml`: deterministic input/output cases when business logic requires them.
- `evals.yaml`: non-deterministic evaluations for AI, LLM, or RAG features.
- `QA_CHECKLIST.md`: human UX, regression, and edge-case checks.
- `validation.md`: automated definition of done.
- `security.md`: entry points, risks, and security requirements.

Run the Grill before creating the feature files. Cover scope, decisions, context, UX, APIs, security entry points, and edge cases.

### Step 3: Implement

Execute the feature's `EXECUTE.md`. Implement slices in order. At every `[HITL]` slice, stop and request human approval. Run local pre-commit checks before each commit.

### Step 4: Keep spec and code synchronized

When a decision changes, update `plan.md`, `requirements.md`, `validation.md`, and `security.md` together. If code changed for a valid reason, document that reason in `requirements.md`. Irreversible post-merge decisions belong in `specs/adr/`.

### Step 5: Confirm and merge

Mark the roadmap phase complete, invoke the `changelog` skill, create an ADR when applicable, update `specs/STATE.md`, commit, and merge the branch according to team policy.

## Part 2 - Legacy project

For an existing project without reliable specs:

1. Reconstruct the constitution from the code and interview stakeholders about mission, audience, and stack gaps.
2. Optionally create retrospective specs for critical existing features.
3. Run an initial non-blocking SAST, SCA, and secrets scan; triage findings into the roadmap.
4. Establish a baseline so new HIGH or CRITICAL findings are blocked.
5. Continue with the normal feature-spec flow.

Never require zero findings on day one of a legacy migration. Require that no new high-severity finding enters the project.

## Part 3 - Quality and resilience

Document and test the failure modes before implementation. Review collection routes for N+1 queries and define a query budget. Protect concurrent writes with transactions, locks, or idempotency keys. Give caches explicit TTLs, close connections, remove listeners, and define fault-tolerant behavior for every route.

## Part 4 - CI/CD and shift-left security

Use two gates: local pre-commit for fast feedback and CI before merge. Choose and document one tool for each category in `specs/tech-stack.md`:

- SAST: Semgrep, Bandit, gosec, Brakeman, ESLint security plugins, or Checkov.
- SCA: Trivy, Dependency-Check, Snyk, pip-audit, npm audit, govulncheck, or bundler-audit.
- Secrets: TruffleHog, Gitleaks, detect-secrets, or git-secrets.

Local and CI checks must cover the same categories with equivalent severity. Never bypass a failing hook with `--no-verify`. Revoke exposed credentials, clean the history, and audit access when a secret is found.

## Part 5 - Reusable skills

Skills are `SKILL.md` files that package repeatable workflows. Keep the frontmatter and short description minimal, and load detailed instructions only when the skill is invoked. The kit provides `changelog` and `feature-spec` skills.

## Part 6 - Specialized agents

Version specialized profiles in `.claude/agents/`:

- `feature-developer`: implements the feature from `plan.md`.
- `security-auditor`: reviews entry points and `security.md`.
- `performance-optimizer`: reviews N+1, query budgets, and memory leaks.
- `code-reviewer`: reviews quality, typing, anti-patterns, and test coverage.

## Part 7 - Multi-agent review

For complex changes, run `code-reviewer`, `security-auditor`, and `performance-optimizer` in parallel, then consolidate findings before merge.

## Part 8 - STATE.md

Update `specs/STATE.md` when pausing work. Record current context, active branch, recent decisions, pending work, blockers, and the next granular action. Read it before resuming.

## Part 9 - Declarative tests and evals

Use `test-cases.yaml` for deterministic business rules and pure transformations. Use `evals.yaml` for AI features whose outputs are non-deterministic; define properties, rubrics, and thresholds instead of exact string equality.

`EXECUTE.md` connects the spec to implementation: it tells the agent what to read, which slices to execute, where to stop for human approval, and which validations to run.

## Part 10 - Multi-tool synchronization

`AGENTS.md` is the single source of coding rules. Export it to the formats used by the team: `CLAUDE.md`, `.cursor/rules/`, `.github/copilot-instructions.md`, and `.windsurf/rules/`. Edit `AGENTS.md` first so tools do not diverge.

## Part 11 - Product architect prompt

For complex features, use the master prompt to enforce three steps: Grill, spec generation, and an approval pause before implementation. It must generate `EXECUTE.md`, tests or evals, requirements, security, plan, and QA checklist.

## Part 12 - Roadmap replanning

When scope changes, split, combine, or reprioritize roadmap phases. Keep phases independently implementable and update affected feature specs before coding.

## Part 13 - Coverage and review checklist

Before merge, confirm that the feature spec, implementation, tests, local security checks, manual QA, spec synchronization, changelog, ADR, roadmap, and `STATE.md` are complete. Review N+1 risk, concurrent writes, failure modes, cache TTLs, fixed dependency versions, and tool synchronization.

## Quick reference

| Situation | Action |
|---|---|
| New project | Create the constitution with the Grill |
| Next feature | Invoke `feature-spec` from the roadmap |
| Implementation | Execute the feature's `EXECUTE.md` |
| Spec changed | Synchronize plan, requirements, validation, and security |
| Before merge | Run validation, changelog, review, and applicable ADR |
| Save context | Update `specs/STATE.md` |
| Resume work | Read `specs/STATE.md` and continue from its next step |

The Portuguese edition remains available at [GUIA-SDSD.md](GUIA-SDSD.md).
