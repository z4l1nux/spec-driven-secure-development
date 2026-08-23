# Templates SDSD

Cópias prontas dos arquivos referenciados no [GUIA-SDSD.md](../GUIA-SDSD.md). Copie para a raiz do seu projeto e ajuste os placeholders entre `[colchetes]`.

## Conteúdo

| Arquivo | Destino no seu projeto | Quando usar |
|---|---|---|
| [`specs/mission.md`](specs/mission.md) | `specs/mission.md` | Constituição — missão e público |
| [`specs/principles.md`](specs/principles.md) | `specs/principles.md` | Sempre — é o 2º arquivo da constituição (PARTE 1, Passo 1 do guia) |
| [`specs/tech-stack.md`](specs/tech-stack.md) | `specs/tech-stack.md` | Constituição — stack e esteira de segurança |
| [`specs/roadmap.md`](specs/roadmap.md) | `specs/roadmap.md` | Constituição — fases do trabalho |
| [`specs/STATE.md`](specs/STATE.md) | `specs/STATE.md` | Memória contínua entre sessões |
| [`specs/_feature/`](specs/_feature/) | `specs/YYYY-MM-DD-nome/` | Stubs de todos os artefatos de uma feature |
| [`AGENTS.md`](AGENTS.md) | `AGENTS.md` (raiz) | Sempre — fonte única das regras de código (PARTE 10) |
| [`.pre-commit-config.yaml`](.pre-commit-config.yaml) | `.pre-commit-config.yaml` (raiz) | Quando configurar o shift-left local (PARTE 4.1) |
| [`.claude/agents/security-auditor.md`](.claude/agents/security-auditor.md) | `.claude/agents/security-auditor.md` | Quando usar Claude Code com subagents reais (PARTE 6) |
| [`skills/`](skills/) | `skills/` | Skills reutilizáveis de changelog e feature spec |

## Setup rápido

```bash
# 1. Copie os templates para a raiz do seu projeto
cp -r templates/specs        /caminho/do/seu/projeto/
cp    templates/AGENTS.md    /caminho/do/seu/projeto/
cp    templates/.pre-commit-config.yaml /caminho/do/seu/projeto/
cp -r templates/.claude      /caminho/do/seu/projeto/

# 2. Ative o pre-commit
cd /caminho/do/seu/projeto
pipx install pre-commit
pre-commit install

# 3. Edite os placeholders [entre colchetes] em principles.md e AGENTS.md
```

## Próximos passos

1. Edite os placeholders da constituição e do `AGENTS.md`.
2. Copie `specs/_feature/` para uma pasta datada quando iniciar uma feature.
3. Sincronize `AGENTS.md` para `CLAUDE.md` e demais ferramentas (PARTE 10 do guia).
