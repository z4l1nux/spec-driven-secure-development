# Templates SDSD

[English](README.en.md)

Cópias prontas dos arquivos referenciados no [GUIA-SDSD.md](../GUIA-SDSD.md). Eles materializam o bootstrap do projeto consumidor; ajuste os placeholders entre `[colchetes]` depois do Grill.

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
| [`.claude/agents/`](.claude/agents/) | `.claude/agents/` | Perfis `security-auditor`, `code-reviewer`, `feature-developer` e `performance-optimizer` (PARTE 6) |
| [`skills/`](skills/) | `skills/` | Skills reutilizáveis de changelog e feature spec |

## Setup rápido

```bash
# 1. Copie os templates para a raiz do seu projeto
cp -r templates/specs        /caminho/do/seu/projeto/
cp    templates/AGENTS.md    /caminho/do/seu/projeto/
cp    templates/.pre-commit-config.yaml /caminho/do/seu/projeto/
cp -r templates/.claude      /caminho/do/seu/projeto/
cp -r templates/skills       /caminho/do/seu/projeto/

# 2. Ative o pre-commit
cd /caminho/do/seu/projeto
pipx install pre-commit
pre-commit install

# 3. Leia specs/ e faça o Grill descrito no guia
# 4. Preencha os placeholders [entre colchetes] em specs/ e AGENTS.md
# 5. Exporte AGENTS.md para as ferramentas usadas pelo time
```

> Este diretório não instala o CI do kit. Crie ou adapte os workflows do projeto
> consumidor em `.github/workflows/`, conforme a stack definida em
> `specs/tech-stack.md`. O `.harness/` deste repositório também não é copiado por
> padrão: ele guarda contexto de manutenção do kit.

## Próximos passos

1. Complete `specs/mission.md`, `principles.md`, `tech-stack.md` e `roadmap.md`.
2. Escolha a próxima fase e copie `specs/_feature/` para uma pasta datada.
3. Faça o Grill e preencha os artefatos da feature antes de escrever código.
4. Execute `EXECUTE.md`, valide e só então confirme com changelog, ADR e `STATE.md`.
5. Sincronize `AGENTS.md` para `CLAUDE.md` e demais ferramentas (PARTE 10 do guia).
