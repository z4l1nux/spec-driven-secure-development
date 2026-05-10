# Templates SDSD

Cópias prontas dos arquivos referenciados no [GUIA-SDSD.md](../GUIA-SDSD.md). Copie para a raiz do seu projeto e ajuste os placeholders entre `[colchetes]`.

## Conteúdo

| Arquivo | Destino no seu projeto | Quando usar |
|---|---|---|
| [`specs/principles.md`](specs/principles.md) | `specs/principles.md` | Sempre — é o 2º arquivo da constituição (PARTE 1, Passo 1 do guia) |
| [`AGENTS.md`](AGENTS.md) | `AGENTS.md` (raiz) | Sempre — fonte única das regras de código (PARTE 10) |
| [`.pre-commit-config.yaml`](.pre-commit-config.yaml) | `.pre-commit-config.yaml` (raiz) | Quando configurar o shift-left local (PARTE 4.1) |
| [`.claude/agents/security-auditor.md`](.claude/agents/security-auditor.md) | `.claude/agents/security-auditor.md` | Quando usar Claude Code com subagents reais (PARTE 6) |

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

1. Crie a constituição completa: `mission.md`, `tech-stack.md`, `roadmap.md` (ao lado de `principles.md`)
2. Sincronize `AGENTS.md` para `CLAUDE.md` e demais ferramentas (PARTE 10 do guia)
3. Crie subagents adicionais conforme necessidade: `code-reviewer`, `performance-optimizer`, `feature-developer`
