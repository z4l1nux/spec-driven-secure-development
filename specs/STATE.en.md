# State

## Current Focus

Keep the guide, templates, public documentation, and security validation pipeline aligned.

## Decisions

- The repository is a methodology kit, not an application.
- Consumer projects own their `specs/`, `.harness/`, and CI configuration.
- Portuguese files remain canonical repository artifacts; English files provide equivalent public access.

## Next Step

Review new documentation changes with `python scripts/validate_docs.py` and update both language editions when public behavior changes.
