# AGENTS.md — Regras de Código deste Projeto

> **Fonte única de verdade para todos os agentes de IA do time.**
> Editar AQUI e re-exportar para `CLAUDE.md`, `.cursor/rules/`, `.github/copilot-instructions.md`, `.windsurf/rules/`.
> Nunca edite os arquivos de destino diretamente — eles divergem.

---

## 0. Antes de qualquer mudança

1. Leia `specs/principles.md` — restrições invioláveis
2. Identifique a fase no `specs/roadmap.md` ou crie uma nova feature spec
3. **Nunca codifique sem spec.** Se não existe spec, crie antes de codar
4. **Nunca mude código sem atualizar o spec.** Eles andam juntos

---

## 1. Convenções de código

- **Naming:** [definir — camelCase / snake_case / kebab-case por contexto]
- **Imports:** [agrupados por origem (stdlib / terceiros / locais), ordenados]
- **Erros:** nunca silenciosos; sempre logar com contexto suficiente para diagnóstico
- **Comentários:** apenas quando o "porquê" não é óbvio do código
- **Testes:** colocados em `[caminho da convenção]`, nomeados `*.test.[ext]` ou `test_*.py`

---

## 2. Comandos do projeto

| O que | Comando |
|---|---|
| Instalar | `[cmd]` |
| Rodar dev | `[cmd]` |
| Testar | `[cmd]` |
| Type check | `[cmd]` |
| Lint | `[cmd]` |
| SAST | `[cmd ex: semgrep --config auto src/]` |
| SCA | `[cmd ex: trivy fs --severity HIGH,CRITICAL .]` |
| Secrets | `[cmd ex: trufflehog filesystem . --since-commit main]` |
| Pre-commit (manual) | `pre-commit run --all-files` |

---

## 3. Gates obrigatórios antes de commit

1. Pre-commit hook passa (não usar `--no-verify`)
2. Type check em zero erros
3. Suite de testes em verde
4. Specs atualizadas se o comportamento mudou

## Gates obrigatórios antes de merge

1. Todos os gates de commit acima
2. CI verde (incluindo workflows de SAST, SCA, Secrets)
3. `QA_CHECKLIST.md` da feature revisado por humano
4. `CHANGELOG.md` atualizado via `skill changelog`
5. ADR criado em `specs/adr/` se a decisão for irreversível

---

## 4. Estrutura de specs (resumida)

Veja `GUIA-SDSD.md` para detalhes. Em resumo, toda feature vive em `specs/YYYY-MM-DD-nome/` com:
- `EXECUTE.md` — prompt para iniciar a implementação
- `plan.md` — fatias verticais com tags `[AFK]` e `[HITL]`
- `requirements.md` — escopo, decisões, NFRs (incluindo failure modes)
- `test-cases.yaml` — quando há regra de negócio
- `evals.yaml` — quando há LLM/RAG
- `QA_CHECKLIST.md` — validação humana
- `validation.md` — definition of done automatizado
- `security.md` — entry points, riscos, requisitos

---

## 5. O que NÃO fazer

- Não usar `--no-verify` em commits
- Não instalar dependência sem fixar versão (`^`, `~`, `latest` proibidos em produção)
- Não criar rota pública sem documentar a decisão em `requirements.md`
- Não fazer merge sem atualizar `CHANGELOG.md`
- Não amar/silenciar erros (try/catch sem log é proibido)
- Não introduzir cache em memória sem TTL explícito
- Não escrever código que viole `specs/principles.md` — abrir ADR antes
- Não criar arquivos de documentação (`*.md`) sem ser solicitado

---

## 6. Subagents disponíveis

Localizados em `.claude/agents/<nome>.md`:
- `security-auditor` — revisão pré-merge para entry points
- `code-reviewer` — qualidade de código, tipagem, anti-patterns
- `performance-optimizer` — N+1, memory leaks, profiling
- `feature-developer` — implementação seguindo `plan.md`

**Como invocar (Claude Code):** `@security-auditor revise as mudanças desta branch`

---

## 7. Skills disponíveis

Localizadas em `skills/<nome>/SKILL.md`:
- `changelog` — atualiza `CHANGELOG.md` a partir do git log
- `feature-spec` — bootstrapa nova feature a partir do roadmap

**Como invocar:** `Use sua skill changelog para atualizar o changelog.`

---

## 8. STATE.md — memória entre sessões

Ao pausar trabalho, atualize `specs/STATE.md` com decisões, pendências e próximo passo granular.
Ao retomar, leia `specs/STATE.md` antes de qualquer outra coisa.

---

## 9. Exportação para outras ferramentas

Quando este arquivo mudar, re-exporte:

```
Leia AGENTS.md e crie/atualize:
- CLAUDE.md (formato Claude Code)
- .cursor/rules/AGENTS.mdc (formato Cursor)
- .github/copilot-instructions.md (formato Copilot)
- .windsurf/rules/agents.md (formato Windsurf)
Mantenha o conteúdo idêntico, ajustando apenas o formato esperado por cada ferramenta.
```
