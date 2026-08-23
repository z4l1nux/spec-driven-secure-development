# Kit Harness Context

`.harness/` stores operational context for maintaining the SDSD kit. It is not a consumer application's constitution and is not copied by default when bootstrapping a project.

- `context.md`: project purpose and scope.
- `boundaries.md`: supported and unsupported responsibilities.
- `domain-glossary.md`: shared terminology.
- `patterns/`: approved implementation patterns.
- `integrations/`: external integration records.
- `adr/`: decisions affecting this kit.
- `rfc/`: proposals for significant changes.
- `tech-debt/`: known technical debt.
- `incident-log/`: significant incident records.
- `ai-review-checklist.md`: review gates for code and specifications.

Consumer-project decisions belong in `specs/adr/`, not in this directory.
