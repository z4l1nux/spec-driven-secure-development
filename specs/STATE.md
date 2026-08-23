# State

## Current Focus
Alinhar o guia, os templates e a esteira de segurança do kit.

## Decisions
- ADRs do kit ficam em `.harness/adr/`; ADRs de consumidores ficam em `specs/adr/`.
- O CI usa vet como SCA e o pre-commit usa Trivy para feedback local.

## Next Step
Revisar novas mudanças com `python scripts/validate_docs.py`.
