# Tech Stack

## Repository

- Documentation: Markdown.
- Validation: `python scripts/validate_docs.py`.
- Automation: GitHub Actions.
- Security checks: Semgrep, TruffleHog, and vet.

## Security

Actions use pinned references. Local and CI scans intentionally use tools suited to their execution context, while preserving equivalent security categories and documented severity gates.

## Documentation contract

The guide, templates, and English editions must describe the same workflow and artifact ownership. Changes to one public contract require reviewing the others.
