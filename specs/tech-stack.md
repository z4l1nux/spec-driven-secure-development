# Tech Stack

## Natureza
- Formato: Markdown, YAML e Python
- Validação: `python scripts/validate_docs.py`
- CI: workflows GitHub Actions em `.github/workflows/`
	- `.github/workflows/docs-validation.yml`
	- `.github/workflows/semgrep-scan.yml`
	- `.github/workflows/trufflehog.yml`
	- `.github/workflows/vet-sca.yml`

## Security
- SAST: Semgrep 1.92.0, somente em pull requests
- SCA: vet OSS Components no CI; Trivy 0.57.0 no pre-commit como feedback local
- Secrets: TruffleHog fixado por commit no CI; detect-secrets no pre-commit
- Actions: referências fixadas por SHA

A diferença entre SCA local e CI é intencional: Trivy fornece feedback local rápido e vet é o gate do CI. Alterações devem manter as categorias e severidades documentadas.
