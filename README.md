# Spec-Driven Secure Development (SDSD)

Bem-vindo ao repositório de **Spec-Driven Secure Development (SDSD)**, um guia prático e opinativo para times que constroem software moderno integrando Agentes de IA, segurança nativa e excelência técnica.

## 🧠 O que é SDSD?

SDSD é um fluxo de trabalho onde **toda funcionalidade começa com especificações rigorosas escritas ANTES do código**. Em vez de usar "prompts soltos" ou tratar a Inteligência Artificial como um adivinho de ideias vagas, a IA é usada para materializar e codificar especificações formais, mantendo o humano estritamente no controle da direção do produto, da arquitetura e da qualidade final (UX).

O princípio central da metodologia é a inversão de controle tradicional: **A especificação é a verdadeira fonte da verdade e o código é apenas um subproduto (muitas vezes descartável).**

## 💡 Por que usar?

- **Fim da "Caixa Preta" da IA:** O código gerado deixa de ser "código alienígena". Você sabe exatamente *por que* algo foi construído, porque decisão e requisitos estão documentados nas specs.
- **Princípios Invioláveis em Primeiro Lugar:** Um arquivo `principles.md` na raiz da constituição declara o que nunca pode ser violado (segurança, compliance, UX). Toda feature é validada contra ele.
- **Lógica e Testes Agnósticos:** Para lógica de negócio complexa, "Bibliotecas Sem Código" — o comportamento é amarrado por `test-cases.yaml` (input/output puros) ou `evals.yaml` (para features de IA com saídas não-determinísticas). A IA itera até a matemática fechar.
- **Segurança Shift-Left em Dois Momentos:** Pre-commit local (segundos, ponto primário) + CI (minutos, rede de segurança). Modelagem de ameaças e *failure modes* na base da feature, nunca depois.
- **Orquestração Híbrida com Subagents Versionados:** Tarefas classificadas como `[AFK]` (autônomo) ou `[HITL]` (revisão humana obrigatória). Perfis especializados (`security-auditor`, `code-reviewer`, etc.) ficam em `.claude/agents/` versionados com o projeto.
- **Memória Persistente entre Sessões:** `STATE.md` preserva contexto, decisões e próximo passo granular. ADRs em `specs/adr/` registram decisões irreversíveis.
- **Multi-Ferramenta por Padrão:** `AGENTS.md` é a fonte única — exportável para Claude Code, Cursor, Copilot, Windsurf e Codex sem divergência.
- **Redução da Carga Cognitiva:** O `EXECUTE.md` gerado é o "botão de play" — copy-paste no chat e o agente executa.

## 🚀 Como Funciona o Fluxo (Resumo)

Toda tarefa segue o ciclo **P → R → E → V → C** (Planejar → Revisar → Executar → Validar → Confirmar). Bugfixes pequenos podem pular etapas; features complexas usam o ciclo completo. A escala detalhada (QUICK / SMALL / MEDIUM / LARGE) está no [guia](GUIA-SDSD.md).

**P — Planejar (Constituição + Feature Spec)**
A constituição do projeto vive em `specs/`: `mission.md`, `principles.md` (restrições invioláveis de segurança/UX/compliance), `tech-stack.md` (incluindo SAST, SCA, Secrets, pre-commit) e `roadmap.md`. Para cada feature, uma sessão de *Grill* (uma pergunta por vez) elimina ambiguidades antes de qualquer arquivo ser escrito.

**R — Revisar (gerar specs executáveis)**
O agente cria a pasta da feature com: `EXECUTE.md` (prompt-botão de play), `plan.md` (fatias verticais marcadas como `[AFK]` autônomo ou `[HITL]` com revisão humana), `requirements.md` (escopo + NFRs), `test-cases.yaml`/`evals.yaml`, `security.md`, `validation.md` e `QA_CHECKLIST.md`.

**E — Executar (implementação a partir do EXECUTE.md)**
Você cola o `EXECUTE.md` no chat do agente. Ele implementa fatia por fatia, parando nos `[HITL]`. Pre-commit local roda SAST/SCA/Secrets antes de cada commit — o CI é rede de segurança, não ponto primário.

**V — Validar (gates antes do merge)**
Type check, testes, scans de segurança, checklist humano de UX e revisão multi-subagente (`code-reviewer`, `security-auditor`, `performance-optimizer` em paralelo) garantem que nada passa batido.

**C — Confirmar (merge + memória)**
Skill `changelog` atualiza o `CHANGELOG.md`. Decisões irreversíveis viram um ADR em `specs/adr/`. `STATE.md` preserva o contexto entre sessões para o próximo dia.

## 📖 Documentação e Templates

- 👉 **[Guia técnico completo (GUIA-SDSD.md)](GUIA-SDSD.md)** — fluxo detalhado, prompts, prevenção de N+1/race conditions/memory leaks, CI/CD
- 📁 **[Templates prontos (`templates/`)](templates/)** — `principles.md`, `AGENTS.md`, `.pre-commit-config.yaml` e subagent `security-auditor` para copiar direto no seu projeto

---
*"Escreva boas especificações. Deixe a IA cuidar da digitação."*
