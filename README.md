# Spec-Driven Secure Development (SDSD)

[Português](#português) · [English](#english)

<a name="português"></a>

Bem-vindo ao repositório de **Spec-Driven Secure Development (SDSD)**, um guia prático e opinativo para times que constroem software moderno integrando Agentes de IA, segurança nativa e excelência técnica.

Este repositório é o **manual e o kit de templates** da metodologia. Ele não é um
projeto de aplicação já configurado: a estrutura `specs/`, os agentes e as skills
descritos no guia são criados no projeto que adota o SDSD, a partir de `templates/`.

## 🧭 Como as partes se conectam

Existem dois contextos que não devem ser misturados:

| Contexto | Fonte | Responsabilidade |
|---|---|---|
| Kit SDSD | `GUIA-SDSD.md`, `templates/`, `.harness/`, `.github/workflows/` | Ensinar, fornecer e validar a metodologia |
| Projeto consumidor | `specs/`, `AGENTS.md`, `skills/`, `.claude/`, `.pre-commit-config.yaml` e código | Aplicar a metodologia a um produto real |

O caminho semântico é:

`GUIA-SDSD.md` define o fluxo → `templates/` materializa o bootstrap →
`specs/` registra a constituição e cada feature → `AGENTS.md` governa os agentes
→ `skills/` automatiza tarefas repetíveis → `.claude/` fornece perfis de agente
→ pre-commit e CI validam → `CHANGELOG.md`, ADRs e `STATE.md` preservam o resultado.

O diretório `.harness/` contém o contexto operacional deste kit. Ele orienta a
manutenção do próprio repositório e só deve ser levado a um projeto consumidor
quando o time decidir adotar esse contexto como parte de sua governança.

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

- 👉 **[Guia técnico completo (GUIA-SDSD.md)](GUIA-SDSD.md)** · [English edition](GUIA-SDSD.en.md) — fluxo detalhado, prompts, prevenção de N+1/race conditions/memory leaks, CI/CD
- 📁 **[Templates prontos (`templates/`)](templates/)** · [English edition](templates/README.en.md) — constituição, specs de feature, skills, agentes e pre-commit para copiar direto no seu projeto
- 🧩 **Contexto do kit:** [`specs/`](specs/) · [English index](specs/README.en.md) · [`.harness/`](.harness/) · [English index](.harness/README.en.md)

O diretório [`.harness/`](.harness/) contém contexto operacional reutilizável,
como glossário, limites, padrões e modelos de registros. Ele complementa os
templates de um projeto consumidor; não substitui a pasta `specs/` descrita no guia.

---
*"Escreva boas especificações. Deixe a IA cuidar da digitação."*

---

<a name="english"></a>

# Spec-Driven Secure Development (SDSD)

Welcome to **Spec-Driven Secure Development (SDSD)**, a practical and opinionated guide for teams building modern software with AI agents, built-in security, and technical excellence.

This repository is the methodology's **manual and template kit**. It is not a preconfigured application: the `specs/` structure, agents, and skills described in the guide are created in the project adopting SDSD, from `templates/`.

## 🧭 How the parts connect

There are two contexts that should not be mixed:

| Context | Source | Responsibility |
|---|---|---|
| SDSD kit | `GUIA-SDSD.md`, `templates/`, `.harness/`, `.github/workflows/` | Teach, provide, and validate the methodology |
| Consumer project | `specs/`, `AGENTS.md`, `skills/`, `.claude/`, `.pre-commit-config.yaml`, and code | Apply the methodology to a real product |

The semantic path is:

`GUIA-SDSD.md` defines the workflow → `templates/` bootstraps it → `specs/` records the constitution and each feature → `AGENTS.md` governs agents → `skills/` automates repeatable tasks → `.claude/` provides agent profiles → pre-commit and CI validate → `CHANGELOG.md`, ADRs, and `STATE.md` preserve the result.

The `.harness/` directory contains this kit's operational context. It guides maintenance of this repository and should only be brought into a consumer project when the team explicitly adopts that governance context.

## 🧠 What is SDSD?

SDSD is a workflow where **every feature starts with rigorous specifications written BEFORE code**. Instead of relying on loose prompts or treating AI as a guesser of vague ideas, AI materializes and implements formal specifications under strict human control of product direction, architecture, and final quality.

The methodology's central principle is an inversion of traditional control: **the specification is the source of truth and the code is only a byproduct, often disposable**.

## 💡 Why use it?

- **End the AI black box:** generated code is backed by documented decisions and requirements.
- **Put inviolable principles first:** `principles.md` declares what must never be violated, including security, compliance, and UX constraints.
- **Keep logic and tests framework-agnostic:** use `test-cases.yaml` for deterministic business logic or `evals.yaml` for non-deterministic AI features.
- **Shift security left twice:** local pre-commit provides fast feedback and CI provides the merge gate.
- **Version hybrid orchestration:** `[AFK]` tasks run autonomously and `[HITL]` tasks require human review; specialized profiles live in `.claude/agents/`.
- **Preserve session memory:** `STATE.md` carries context forward and ADRs record irreversible decisions.
- **Support multiple tools:** `AGENTS.md` is the single source exported to Claude Code, Cursor, Copilot, Windsurf, and Codex.
- **Reduce cognitive load:** `EXECUTE.md` is the feature's ready-to-run prompt.

## 🚀 Workflow summary

Every task follows **P → R → E → V → C**: Plan, Review, Execute, Validate, and Confirm. Small bug fixes may skip stages; complex features use the complete cycle. See the [technical guide](GUIA-SDSD.md) for the QUICK, SMALL, MEDIUM, and LARGE scales.

**P — Plan:** create the project constitution and feature spec. The Grill asks one question at a time before files are written.

**R — Review:** generate executable feature specs: `EXECUTE.md`, `plan.md`, `requirements.md`, tests or evals, `security.md`, `validation.md`, and `QA_CHECKLIST.md`.

**E — Execute:** run `EXECUTE.md`; the agent implements slices in order and stops at `[HITL]` checkpoints.

**V — Validate:** run type checks, tests, security scans, manual QA, and specialized reviews.

**C — Confirm:** update the changelog, record applicable ADRs, update `STATE.md`, and merge.

## 📖 Documentation and templates

- [Technical guide (English)](GUIA-SDSD.en.md) · [Portuguese edition](GUIA-SDSD.md) — detailed workflow, prompts, resilience, and CI/CD
- [Ready-to-use templates (English)](templates/README.en.md) · [Portuguese edition](templates/) — constitution, feature specs, skills, agents, and pre-commit
- [Kit context and specifications](specs/README.en.md) · [Harness context](.harness/README.en.md) — maintenance contracts for this repository

The English section of this README is the entry point for English-speaking contributors. File names, commands, and technical identifiers remain unchanged so both language versions describe the same repository structure.

---

*"Write good specifications. Let AI handle the typing."*
