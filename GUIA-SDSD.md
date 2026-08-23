# Guia Técnico: Spec-Driven Secure Development (SDSD)

> Referência hands-on para qualquer analista do time.
> Cobre projetos **novos** e projetos **em andamento (legado)**.
> Compatível com Claude Code, Cursor, Copilot, Windsurf e Codex.

---

## O que é SDSD?

Spec-Driven Secure Development é um fluxo de trabalho onde **toda funcionalidade começa com especificações escritas antes do código**. O agente de IA trabalha a partir dos specs — não de prompts soltos. Isso garante rastreabilidade, alinhamento entre stakeholders e código revisável.

**Princípio central:** o spec é a fonte da verdade. O código implementa o spec. O changelog registra o histórico.

**Inversão de controle:** a especificação é o ativo primário; o código é um subproduto (muitas vezes descartável).

---

## 🚀 Por onde começar (Onboarding)

Se você é novo no projeto ou no fluxo SDSD:

1. **Instale o agente** que o time usa (Claude Code, Cursor, Copilot, etc.)
2. **Leia nesta ordem:** `specs/mission.md` → `specs/principles.md` → `specs/tech-stack.md` → `specs/roadmap.md`
3. **Entenda o fluxo:** toda tarefa segue o ciclo P→E→V (ou completo P→R→E→V→C para features grandes — veja a tabela de escala abaixo)
4. **Nunca escreva código sem spec.** Se não existe spec, crie antes de codar.
5. **Nunca mude código sem atualizar o spec.** Eles andam juntos, sempre.

> Se o projeto ainda não tem `specs/`, você está no **Projeto Novo** (PARTE 1). Se já tem código mas não tem specs, você está no **Projeto Legado** (PARTE 2).

---

## Estrutura de Arquivos

O layout abaixo descreve o projeto consumidor depois que os templates forem
copiados. Este repositório contém o guia, os templates em `templates/` e o
contexto compartilhado em `.harness/`; ele não pretende ser uma aplicação já
instalada.

```
projeto/
├── specs/                          ← Constituição + specs de funcionalidades
│   ├── mission.md                  ← Por que o projeto existe
│   ├── principles.md               ← Restrições invioláveis (security, compliance, UX)
│   ├── tech-stack.md               ← Decisões técnicas e suas razões
│   ├── roadmap.md                  ← Fases de trabalho em ordem
│   ├── STATE.md                    ← Memória contínua entre sessões do agente
│   ├── adr/                        ← Architecture Decision Records (decisões irreversíveis pós-merge)
│   │   └── 0001-titulo.md
│   └── YYYY-MM-DD-nome-feature/    ← Uma pasta por funcionalidade
│       ├── EXECUTE.md              ← Prompt pronto para colar no chat e iniciar a implementação
│       ├── plan.md                 ← Fatias verticais (Slices) numeradas, classificadas como [AFK] ou [HITL]
│       ├── requirements.md         ← Escopo, decisões, contexto, NFRs
│       ├── test-cases.yaml         ← Pares input/output agnósticos (obrigatório p/ regra de negócio; opcional p/ CRUD puro)
│       ├── evals.yaml              ← (Apenas features de IA/LLM/RAG) Casos de avaliação não-determinísticos
│       ├── QA_CHECKLIST.md         ← Validações manuais focadas em UX, regressões e edge cases
│       ├── validation.md           ← Definition of Done automatizado (CI, type check, scans)
│       └── security.md             ← Entry points, riscos, critérios de segurança
├── .claude/
│   ├── agents/                     ← Subagents especializados (arquivos .md por perfil)
│   ├── settings.json               ← Hooks, permissões, env vars
│   └── commands/                   ← Slash commands customizados (opcional)
├── skills/                         ← Skills reutilizáveis (progressive disclosure)
│   ├── changelog/
│   │   ├── SKILL.md                ← Frontmatter + descrição (sempre carregado)
│   │   └── scripts/changelog.py    ← Carregado só quando a skill é invocada
│   └── feature-spec/
│       └── SKILL.md
├── AGENTS.md                       ← Fonte única das regras de código (exportada para cada ferramenta)
├── CLAUDE.md                       ← Espelho do AGENTS.md no formato do Claude Code
├── .pre-commit-config.yaml         ← Hooks locais (semgrep/trivy/trufflehog/lint)
├── CHANGELOG.md                    ← Gerado pela skill changelog
└── src/                            ← Código
```

---

## Escala do Workflow — Qual fluxo usar?

Nem toda tarefa precisa do fluxo completo. Use a tabela abaixo para decidir:

| Escala | Fases | Artefatos mínimos | Quando usar |
|---|---|---|---|
| **QUICK** | E → V | nenhum (commit + changelog) | Bugfix, ajuste de texto, correção visual pequena |
| **SMALL** | P → E → V | `plan.md` + `validation.md` | Feature simples, nova rota sem lógica complexa |
| **MEDIUM** | P → R → E → V | + `requirements.md` + `security.md` | Feature regular, nova entidade, integração externa |
| **LARGE** | P → R → E → V → C | + `test-cases.yaml`/`evals.yaml` + `QA_CHECKLIST.md` + ADR | Sistema complexo, múltiplos stakeholders, compliance |

**Fases:**
- **P (Planning):** escrever specs antes de qualquer código
- **R (Review):** validar arquitetura, decisões e riscos antes de implementar
- **E (Execution):** implementar seguindo as fatias do `plan.md`
- **V (Validation):** rodar testes, scans de segurança, verificação manual
- **C (Confirmation):** atualizar changelog, registrar ADR (se aplicável), merge, comunicar

> **Regra prática:** em caso de dúvida, use MEDIUM. O custo de escrever um spec é menor que o de refatorar código sem rastreabilidade.

> **Atalho no Claude Code:** o **Plan Mode** (`Shift+Tab` para alternar, ou `/plan`) já força o agente a planejar antes de tocar em arquivo — use-o como rede de segurança da fase P.

---

## PARTE 1 — Projeto Novo

### Passo 1: Criar a Constituição

A constituição são os **quatro arquivos base** que todo projeto SDSD precisa antes de qualquer código.

**Prompt para o agente:**
```
Estamos construindo [nome do projeto]. Consulte o README.md para entrada das partes interessadas.
Crie uma "constituição" em um diretório specs/:
- mission.md         (por que existimos)
- principles.md      (restrições invioláveis: security, compliance, UX)
- tech-stack.md      (linguagem, framework, banco, esteira de verificação)
- roadmap.md         (fases pequenas e independentes)

Importante: use a técnica de Grill (uma pergunta por vez, com sugestão de resposta) antes de escrever no disco.
No Claude Code, prefira ativar o Plan Mode (Shift+Tab) durante o Grill.
```

**O que o agente vai perguntar na Sessão de Grill (uma por vez):**
1. **Missão** — tom, propósito, o que o produto faz
2. **Princípios** — regras que nunca devem ser violadas (ex: "todo dado pessoal criptografado em repouso")
3. **Stack** — linguagem, framework, banco, esteira de segurança
4. **Roadmap** — como estruturar as fases (incremental, vertical, etc.)

**Resultado esperado:**

`specs/mission.md`:
```markdown
# Mission
[Por que o produto existe]
## What We Do
[O que entregamos]
## Target Audience
[Para quem]
## What Success Looks Like
[Critério de sucesso mensurável]
```

`specs/principles.md`:
```markdown
# Princípios Invioláveis

> Restrições que se aplicam a TODA feature, sem exceção. Mudanças aqui exigem ADR.

## Segurança
- Nenhum secret no código ou em logs
- Toda rota é autenticada por padrão; rotas públicas exigem decisão explícita no requirements.md
- Inputs sempre validados server-side; nunca confiar no cliente

## Privacidade / Compliance
- [ex: dados pessoais criptografados em repouso e em trânsito]
- [ex: consentimento explícito antes de coletar dado sensível]

## Qualidade
- Specs e código são commitados juntos — nunca um sem o outro
- Toda feature tem failure modes documentados antes de ser implementada
- Versões de dependências fixas; lockfile commitado

## UX
- [ex: feedback visível em ações > 200ms]
- [ex: mensagens de erro acionáveis, nunca códigos crus]
```

`specs/tech-stack.md`:
```markdown
# Tech Stack
## Core
| Layer | Choice | Rationale |
|---|---|---|
| Language | [Linguagem] | [motivo] |
| Framework | [Framework] | [motivo] |
| Database | [Banco] | [motivo] |
## Testing
- [Framework de testes] — [característica principal]
## CSS / UI
[Abordagem: mobile-first, design system, etc.]
## Security (esteira escolhida — ver PARTE 4 para alternativas)
- SAST: [ferramenta] — comando local: `[comando]`
- SCA: [ferramenta] — comando local: `[comando]`
- Secrets: [ferramenta] — comando local: `[comando]`
- Pre-commit: [framework] — config: `.pre-commit-config.yaml`
```

`specs/roadmap.md`:
```markdown
# Roadmap
## Phase 1 — Nome pequeno e entregável
- [ ] Tarefa A
- [ ] Tarefa B
## Phase 2 — ...
```

> **Regra de granularidade:** cada fase do roadmap deve ser implementável em uma sessão focada e independentemente mergeável. Máximo de 5 grupos no `plan.md`, máximo de 3 entidades novas ou 5 rotas por fase. Se ultrapassar, divida.

---

### Passo 2: Especificar uma Funcionalidade (Feature Spec)

Antes de implementar qualquer fase, crie o spec da funcionalidade.

**Prompt para o agente:**
```
Encontre a próxima fase em specs/roadmap.md e crie uma branch.
Crie um novo diretório YYYY-MM-DD-nome-da-funcionalidade em specs com:
- EXECUTE.md       — o prompt final para eu copiar e colar para iniciar a implementação
- plan.md          — fatias verticais de tarefas numeradas, marcadas com [AFK] ou [HITL]
- requirements.md  — escopo, decisões, contexto, NFRs
- test-cases.yaml  — (obrigatório p/ regra de negócio; opcional p/ CRUD puro) pares input/output
- evals.yaml       — (apenas features de IA/LLM/RAG) casos de avaliação não-determinísticos
- QA_CHECKLIST.md  — validações manuais humanas (UX, edge cases complexos)
- validation.md    — definition of done automatizada (CI, testes, scans)
- security.md      — entry points, riscos, critérios de segurança

Consulte specs/mission.md, specs/principles.md e specs/tech-stack.md para orientação.
Use a técnica de Grill (uma pergunta por vez com sugestão de resposta) ANTES de escrever no disco.
```

**O que o agente faz:**
1. Lê `specs/roadmap.md`, identifica a primeira fase com itens `[ ]`
2. Cria branch: `git checkout -b YYYY-MM-DD-nome-kebab`
3. Inicia o Grill, fazendo uma pergunta por vez (com sugestão) sobre:

| Cabeçalho | Foco |
|---|---|
| **Escopo** | O que a feature coleta, expõe ou faz — campos, comportamento |
| **Decisões** | Escolhas de implementação — storage, validação, padrão de UX |
| **Contexto** | Tom, restrições, padrões existentes a seguir |

**Resultado esperado:**

`specs/YYYY-MM-DD-nome/plan.md`:
```markdown
# Plan — Nome da Feature

## Slice 1: Estrutura Básica [AFK]
1. Criar migration SQL
2. Endpoint GET /rota simples
3. Teste GET /rota → status 200

## Slice 2: Criação pelo Usuário [HITL]
4. Endpoint POST /rota com validação
5. Teste POST /rota
6. Criar componente Lista e Formulário
7. Revisão humana da UX do formulário
```

> **Tags:**
> - `[AFK] (Away From Keyboard)`: o agente pode implementar, rodar testes e seguir em frente sem perguntar.
> - `[HITL] (Human-In-The-Loop)`: o agente implementa, mas DEVE parar e pedir validação humana antes de prosseguir (ex: decisões de arquitetura, UX).

`specs/YYYY-MM-DD-nome/requirements.md`:
```markdown
# Requirements — Nome

## Scope
### Incluído
- [lista do que entra]
### Fora de Escopo
- [lista do que não entra nesta fase]

## Data Model
| Column | Type | Notes |
|---|---|---|

## Decisions
| Decisão | Escolha | Motivo |
|---|---|---|

## Non-Functional Requirements

### Performance
- Budget de queries: esta rota não deve exceder [N] queries por requisição
- [Tempo de resposta esperado, se relevante]

### Confiabilidade (Failure Modes)
- [ex: banco fora → 503 com mensagem clara, não 500 cru]
- [ex: timeout externo → fallback para cache; sem fallback → erro acionável]
- [ex: dado ausente → 404, não 500]

### Concorrência
- Risco de race condition: [Sim / Não / Baixo]
- Se Sim: [cenário e mitigação — transaction, lock, idempotency key]

## Context
Tom, stack, padrões existentes a seguir.
```

`specs/YYYY-MM-DD-nome/QA_CHECKLIST.md`:
```markdown
# QA Checklist — Nome

> Apenas validações que **só um humano** consegue julgar. O que pode virar teste automatizado pertence ao validation.md.

## Validação Humana
- [ ] A experiência de erro no formulário é clara para o usuário?
- [ ] A animação de loading está fluida?
- [ ] O texto está alinhado com o tom da marca?
- [ ] Edge cases de usabilidade (ex: clique duplo no botão) foram mitigados visualmente?
```

`specs/YYYY-MM-DD-nome/validation.md`:
```markdown
# Validation — Nome

> Apenas critérios **automatizáveis** (CI, testes, scans). Validação humana subjetiva pertence ao QA_CHECKLIST.md.

## Definition of Done

### 1. Código compila sem erros
`[verificação de tipos]` → exit 0

### 2. Testes passam
`[suite de testes]` → exit 0
Deve cobrir: [lista de rotas/comportamentos]

### 3. Performance
- [ ] Rota X não ultrapassa [N] queries por requisição
- [ ] Sem alocações sem TTL identificadas no profiling local

### 4. Segurança (shift-left)
- [ ] `semgrep --config auto` → 0 HIGH/CRITICAL
- [ ] `trivy fs .` → 0 HIGH/CRITICAL
- [ ] `trufflehog filesystem .` → 0 secrets expostos
```

`specs/YYYY-MM-DD-nome/security.md`:
```markdown
# Security — Nome da Feature

## Entry Points
- [ex: POST /rota, query params, upload de arquivo]

## Riscos Identificados
- [ ] Injeção (SQL / XSS / Command)
- [ ] Dados sensíveis expostos em logs ou resposta
- [ ] Input não validado no servidor
- [ ] Secrets no código ou variáveis de ambiente
- [ ] Quebra de algum item de specs/principles.md

## Requisitos de Segurança
- [ ] Todos os inputs validados server-side
- [ ] Saída sanitizada antes de renderizar no HTML
- [ ] Nenhum secret hardcoded
- [ ] Autenticação obrigatória (se rota protegida)

## Definition of Done (Security)
- [ ] semgrep → 0 HIGH/CRITICAL
- [ ] trivy → 0 HIGH/CRITICAL
- [ ] trufflehog → 0 findings
```

`specs/YYYY-MM-DD-nome/EXECUTE.md`:
```markdown
# EXECUTE — Nome

Implemente a funcionalidade lendo os arquivos desta pasta:
1. Leia `requirements.md`, `principles.md` (raiz) e `security.md` para entender o comportamento esperado.
2. Se houver `test-cases.yaml`: gere a suíte de testes na linguagem do projeto a partir dele.
3. Se houver `evals.yaml`: gere o harness de avaliação correspondente.
4. Implemente em fatias conforme o `plan.md`. Em cada `[HITL]`, pare e peça aprovação.
5. Rode os scans locais (PARTE 4) antes de cada commit.
6. Ao final, valide o `validation.md` inteiro e me apresente o `QA_CHECKLIST.md` para revisão.
```

---

### Passo 3: Implementar

Com o spec pronto, o agente implementa seguindo os slices do `plan.md`.

**Prompt para o agente:**
```
Execute o EXECUTE.md desta feature.
```

O agente executa os slices em ordem. Cada slice é uma fatia vertical coesa que entrega valor fim a fim (ex: banco + rota + testes para GET). Ao encontrar `[HITL]`, ele para e pede aprovação.

> **Recomendação:** rode pre-commit (PARTE 4) localmente antes de cada commit. O CI é a rede de segurança — o ponto primário de detecção é a sua máquina.

---

### Passo 4: Atualizar o Spec quando a Implementação Mudar

Se durante a implementação uma decisão mudar (ex: nova estrutura de componente, escopo expandido):

**Prompt para o agente:**
```
Atualize specs/YYYY-MM-DD-nome/plan.md e a implementação para refletir [mudança].
Sincronize requirements.md, validation.md e security.md.
```

**Regra de resolução de conflito spec vs. código:** se spec e código divergirem, a pergunta é *qual está mais atualizado*. Se o código mudou por uma razão válida durante a implementação → atualize o spec para refletir o que foi feito e documente o motivo em `requirements.md` na seção Decisions. Se o spec mudou por decisão do time após a implementação → atualize o código para seguir o spec. Nunca deixe os dois divergirem sem registrar a decisão.

> **Decisões irreversíveis pós-merge** (mudança de banco, de esquema de auth, de paradigma de cache) viram um ADR em `specs/adr/NNNN-titulo.md`, não uma edição do `requirements.md` antigo.

---

### Passo 5: Marcar Fase como Concluída e Fazer Merge

**Prompt para o agente:**
```
Marque esta fase em specs/roadmap.md como concluída.
Use a skill changelog para atualizar o CHANGELOG.md.
Se houve decisão arquitetural irreversível, crie specs/adr/NNNN-titulo.md.
Faça commit, mude para main, faça merge --no-ff e exclua a branch.
```

**O que acontece:**
1. Agente edita `roadmap.md` → adiciona `✅` na fase concluída
2. Roda `python3 skills/changelog/scripts/changelog.py` → atualiza `CHANGELOG.md`
3. (Se aplicável) Cria ADR em `specs/adr/`
4. `git add` → `git commit` → `git checkout main` → `git merge --no-ff` → `git branch -d`

---

## PARTE 2 — Projeto em Andamento (Legado)

Quando o código já existe mas as specs não (ou estão desatualizadas):

### Passo 1: Reconstruir a Constituição

**Prompt para o agente:**
```
Temos um projeto [nome] já implementado. Consulte o README.md para entrada das partes interessadas.
Crie uma constituição em specs/ baseada no que já existe:
- mission.md
- principles.md   (extraia regras implícitas do código: estilo de validação, padrão de auth, etc.)
- tech-stack.md
- roadmap.md      (com fases já implementadas marcadas como ✅)

Entreviste-me sobre missão, público-alvo, lacunas na stack.
Use AskUserQuestion agrupada em 3 antes de escrever no disco.
```

**O agente vai:**
1. Ler o código existente (routes, components, db, middleware)
2. Perguntar sobre missão, público-alvo, lacunas
3. Criar specs que **refletem o estado real do código** — não o que estava planejado

**Dica para o roadmap legado:**
```markdown
## Phase 1 — Feature A ✅   ← já implementada
## Phase 2 — Feature B ✅   ← já implementada
## Phase 3 — Próxima Feature   ← próximo trabalho
- [ ] Tarefa pendente
```

### Passo 2: Reconstruir Specs de Features Existentes (Opcional)

Para features críticas já implementadas, vale criar specs retroativos para documentar decisões:

**Prompt:**
```
O código já está implementado.
Crie um spec retroativo em specs/YYYY-MM-DD-nome/ que documente:
- O que foi implementado (plan.md com tarefas concluídas)
- As decisões que foram tomadas (requirements.md)
- Como validar que ainda funciona (validation.md)
- Quais riscos de segurança já existem (security.md, marcando os já mitigados)
```

### Passo 3: Primeiro Scan de Segurança (Legado)

Projetos legados costumam ter dívida de segurança acumulada. O primeiro scan é diferente dos scans de feature: o objetivo não é bloquear o trabalho, mas **mapear o estado real** e criar um plano de remediação.

**Estratégia em 3 etapas:**

**Etapa 1 — Mapear (não bloquear):**
```
Rode o scan de segurança completo no projeto:
- [SAST escolhido] em todo o diretório src/
- [SCA escolhido] no manifesto de dependências
- [Secrets escolhido] em todo o histórico git

Não corrija ainda. Gere um relatório agrupado por:
1. Severidade (CRITICAL → HIGH → MEDIUM → LOW)
2. Categoria (injeção, secrets, dependências, etc.)
3. Arquivo e linha de cada finding
```

**Etapa 2 — Triagem:**
```
Com base no relatório de segurança gerado, crie um backlog de remediação:
- CRITICAL/HIGH: criar itens no roadmap.md para correção imediata (próximas 2 semanas)
- MEDIUM: criar itens para o roadmap com prazo definido
- LOW/INFO: aceitar ou ignorar conscientemente, documentando a decisão em specs/principles.md
```

**Etapa 3 — Estabelecer linha de base:**
```
Configure os workflows de CI/CD de segurança para este projeto legado.
Use como linha de base os findings já mapeados — o CI não deve bloquear por issues já conhecidas,
mas deve bloquear qualquer novo finding de severidade HIGH ou CRITICAL.
Documente os comandos locais em specs/tech-stack.md.
```

> **Regra para legado:** nunca exija zero findings no dia 1. Exija que nenhum finding *novo* entre. A dívida existente entra no roadmap como trabalho planejado.

### Passo 4: Continuar com Feature Spec Normal

Após constituição reconstruída e primeiro scan feito, o fluxo é idêntico ao projeto novo (Passo 2 da PARTE 1 em diante).

---

## PARTE 3 — Qualidade e Resiliência

> Esta parte cobre as quatro patologias mais comuns no código gerado por agentes. Documente os critérios em `requirements.md` ANTES da implementação — não depois.

### 3.1 Problema N+1 (Excesso de Queries)

**O problema:** o agente cria loops que fazem uma query por item em vez de uma query com JOIN ou batch. Em desenvolvimento funciona; em produção, o banco colapsa.

**Como documentar no spec:**

Em `requirements.md`, seção Non-Functional Requirements:
```
Budget de queries: GET /rota não deve exceder 3 queries por requisição
```

Em `validation.md`:
```
- [ ] GET /rota: verificado com [query counter / logging de queries] → ≤ 3 queries
```

**Prompt para o agente:**
```
Analise as rotas implementadas e identifique potenciais problemas N+1.
Para cada rota com loop sobre coleção, mostre o número de queries gerado
e proponha a query consolidada equivalente (JOIN ou batch).
```

**Técnica de detecção:** configure um middleware de contagem de queries que loga ou alerta quando o limite for ultrapassado. O threshold seguro varia por rota — documente o valor no `requirements.md`.

---

### 3.2 Race Conditions

**O problema:** operações assíncronas simultâneas podem se atropelar — saldos negativos, reservas duplas, deadlocks.

**Como documentar no spec:**

Em `requirements.md`, seção Concorrência:
```
Risco de race condition: Sim
Cenário: dois usuários reservando o mesmo horário simultaneamente
Mitigação: transaction com lock no nível do banco / idempotency key
```

**Técnica — Property-Based Testing:**

Em vez de testar com uma entrada estática, bibliotecas de property-based testing bombardeiam o sistema com combinações aleatórias para garantir que invariantes se mantenham:

| Linguagem | Biblioteca |
|---|---|
| Python | Hypothesis |
| JavaScript / TypeScript | fast-check |
| Java | jqwik |
| Go | gopter |
| Elixir | StreamData |

**Propriedade a testar:**
```
Para qualquer sequência de N requisições simultâneas de reserva,
o sistema nunca deve criar mais reservas do que vagas disponíveis.
```

**Prompt para o agente:**
```
Identifique operações de escrita que podem sofrer race condition.
Para cada uma, proponha: a propriedade invariante a garantir,
a estratégia de mitigação (lock, transaction, idempotency key)
e um teste property-based que a valide.
```

---

### 3.3 Memory Leaks

**O problema:** caches sem TTL, event listeners não removidos, conexões não fechadas. A memória cresce ao longo do dia até derrubar a aplicação.

**Sinais de alerta no código gerado pelo agente:**
- Cache em memória sem limite de tamanho ou tempo de expiração
- Conexões de banco abertas fora de um pool
- Event listeners registrados dentro de loops

**Técnicas de detecção por linguagem:**

| Linguagem | Ferramenta |
|---|---|
| Go | pprof |
| Python | py-spy, tracemalloc |
| Node.js | --inspect + Chrome DevTools heap snapshot |
| JVM | async-profiler, VisualVM |
| Android | LeakCanary |

**Prompt para o agente:**
```
Revise o código em busca de:
- Caches em memória sem TTL ou limite de tamanho
- Conexões ou recursos abertos que não são fechados explicitamente
- Event listeners ou callbacks registrados sem remoção correspondente
Liste cada ocorrência com o risco associado e a correção recomendada.
```

---

### 3.4 Fault Tolerance (Tolerância a Falhas)

**O problema:** o agente escreve o caminho feliz. Não pensa no que acontece quando o banco cai, o serviço externo não responde ou o dado esperado não está lá.

**Como documentar no spec:**

Em `requirements.md`, seção Confiabilidade (Failure Modes):
```
- Banco indisponível → retornar 503, não 500 sem mensagem
- Serviço externo com timeout → fallback para cache ou mensagem de erro clara
- Dado ausente (registro deletado) → 404 com mensagem descritiva
```

**Checklist de revisão:**

```
[ ] Cada rota tem tratamento explícito para dado ausente (404 vs 500)
[ ] Conexões externas têm timeout configurado
[ ] Erros de banco são capturados e logados sem vazar stack trace para o cliente
[ ] A aplicação inicia mesmo se uma dependência opcional estiver fora
```

**Prompt para o agente:**
```
Para cada rota implementada, liste os failure modes possíveis
(banco fora, dado ausente, timeout externo) e o comportamento atual.
Proponha o comportamento correto para cada caso e implemente as correções.
```

---

## PARTE 4 — CI/CD e Shift-Left de Segurança

O shift-left funciona em **dois momentos**: localmente, antes do commit (pre-commit hook), e no pipeline, antes do merge (CI). Ambos são obrigatórios — o CI é a rede de segurança, não o ponto primário de detecção.

### 4.0 Escolha de Ferramentas por Stack

O guia usa Semgrep, Trivy e TruffleHog como referência, mas cada categoria tem alternativas. Escolha uma por categoria e documente em `specs/tech-stack.md`.

#### SAST — Análise Estática de Código

| Ferramenta | Melhor para | Observação |
|---|---|---|
| **Semgrep** | Qualquer stack | Multilíngua, regras customizáveis, open source |
| Bandit | Python | Nativo do ecossistema Python |
| gosec | Go | Integrado ao go toolchain |
| Brakeman | Ruby on Rails | Especializado em Rails |
| ESLint + plugin-security | JavaScript / TypeScript | Reutiliza o linter já existente |
| Checkov | IaC (Terraform, k8s) | Foca em misconfigurações de infraestrutura |

#### SCA — Análise de Dependências

| Ferramenta | Melhor para | Observação |
|---|---|---|
| **Trivy** | Qualquer stack | Multilíngua, também varre imagens Docker |
| OWASP Dependency-Check | Java, .NET, multi | Referência do OWASP, relatórios detalhados |
| Snyk | Qualquer stack | SaaS com IDE plugin; free tier limitado |
| pip-audit | Python | Nativo do ecossistema Python |
| npm audit | JavaScript / TypeScript | Embutido no npm, sem instalação extra |
| govulncheck | Go | Ferramenta oficial do Go team |
| bundler-audit | Ruby | Nativo do ecossistema Ruby/Bundler |

#### Secrets — Detecção de Credenciais Expostas

| Ferramenta | Melhor para | Observação |
|---|---|---|
| **TruffleHog** | Git history | Varre histórico completo de commits |
| Gitleaks | Git history | Alternativa open source, config via TOML |
| detect-secrets | Pre-commit local | Plugin de pre-commit hook, não varre histórico |
| git-secrets | Pre-commit local | Foco em credenciais AWS, leve |

> **Regra:** documente a ferramenta escolhida em `specs/tech-stack.md` na seção Security. O scan local e o CI devem cobrir a mesma categoria e ter severidade equivalente; se usarem ferramentas diferentes, documente o motivo e os comandos de ambos.

---

### 4.1 Pre-commit Local (ponto primário de detecção)

O CI roda em minutos; o pre-commit roda em segundos. Falha rápido, custa barato.

**Setup com `pre-commit` (framework Python multi-stack):**

`.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/returntocorp/semgrep
    rev: v1.92.0
    hooks:
      - id: semgrep
        args: ["--config=auto", "--error", "--severity=ERROR"]

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.x.x
    hooks:
      - id: detect-secrets
        args: ["--baseline", ".secrets.baseline"]

  - repo: https://github.com/aquasecurity/trivy
    rev: v0.57.0
    hooks:
      - id: trivy
        args: ["fs", "--severity", "HIGH,CRITICAL", "--exit-code", "1", "."]

  - repo: local
    hooks:
      - id: lint
        name: lint
        entry: [comando do linter da stack]
        language: system
        pass_filenames: false
```

**Instalação (uma vez por dev):**
```bash
pipx install pre-commit
pre-commit install   # instala o hook em .git/hooks/pre-commit
```

**Alternativas por ecossistema:**
- JavaScript/TypeScript: `husky` + `lint-staged`
- Go: hook bash simples chamando `gosec`/`govulncheck`
- Polyglot: `lefthook` (binário único, config em YAML)

> **Regra:** o pre-commit nunca deve ser pulado com `--no-verify`. Se um hook falha por bug do hook (não do seu código), corrija o hook — nunca o ignore.

---

### 4.2 Prompts para Rodar Localmente (manual)

Antes de qualquer commit em uma branch de feature, o analista deve rodar o scan local. Use estes prompts:

**Scan completo (projeto novo ou feature em andamento):**
```
Rode o scan de segurança completo no diretório src/:
- [SAST escolhido] — análise estática do código
- [SCA escolhido] — vulnerabilidades em dependências
- [Secrets escolhido] — credenciais expostas no histórico git
Reporte os findings por ferramenta e severidade.
Para cada HIGH ou CRITICAL, proponha a correção antes de continuarmos.
```

**Scan rápido (antes de cada commit):**
```
Rode o scan de segurança local nas mudanças desta branch:
- [SAST]: semgrep --config auto src/
- [SCA]: [comando da ferramenta escolhida]
- [Secrets]: [comando da ferramenta escolhida] --since [hash do último commit em main]
Mostre apenas HIGH e CRITICAL.
```

**Configurar ferramentas no projeto (primeira vez):**
```
Configure as ferramentas de segurança para este projeto:
- Identifique qual SAST, SCA e Secrets scanner é mais adequado para a stack documentada em specs/tech-stack.md
- Instale as ferramentas necessárias
- Crie .pre-commit-config.yaml com hooks para todas
- Crie os workflows em .github/workflows/ para cada uma
- Documente os comandos locais em specs/tech-stack.md na seção Security
```

---

### 4.3 O que fazer quando um secret é encontrado

Quando o TruffleHog (ou qualquer scanner de secrets) retorna um finding, siga este protocolo:

**1. Revogar imediatamente** — acesse o painel do serviço (AWS, GitHub, Stripe, etc.) e invalide a credencial encontrada. Não espere confirmar se foi usado de forma maliciosa.

**2. Rotar** — gere uma nova credencial e atualize nos ambientes necessários (`.env`, secrets manager, CI/CD).

**3. Limpar o histórico git** — se o secret foi commitado, ele persiste no histórico mesmo após remoção do arquivo. Use:
```bash
# Instalar
pip install git-filter-repo

# Remover o secret do histórico (substitua pelo valor real)
git filter-repo --replace-text <(echo "SECRET_VALOR==>SECRET_VALOR_REDACTED")

# Forçar push (coordenar com o time — reescreve histórico)
git push --force --all
```

**4. Auditar o acesso** — verifique nos logs do serviço se a credencial foi usada por alguém além do time. Documente a conclusão.

**5. Adicionar ao pre-commit** — configure `detect-secrets` ou `gitleaks` como pre-commit hook para impedir reincidência.

> **Regra:** nunca commitar um secret, mesmo em repositório privado. Se aconteceu, o secret está comprometido — revogar é obrigatório, não opcional.

---

### 4.4 Semgrep (SAST) — workflow CI

`.github/workflows/semgrep-scan.yml`:

```yaml
name: Semgrep Security Scan

on:
  pull_request:
    branches:
      - "**"

jobs:
  semgrep_scan:
    runs-on: ubuntu-latest

    steps:
      - name: Check out code
        uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4

      - name: Set up Python
        uses: actions/setup-python@7f4fc3e22c37d6ff65e88745f38bd3157c663f7c # v4
        with:
          python-version: "3.12"

      - name: Install Semgrep
        run: |
          python -m pip install --upgrade pip
          pip install setuptools==80.9.0 semgrep==1.92.0

      - name: Run Semgrep (Enforce by PARANOIA_LEVEL)
        run: |
          PARANOIA_LEVEL=2   # ajuste aqui: 1 = critical/high (ERROR), 2 = high/medium (WARNING)

          if [ "$PARANOIA_LEVEL" -eq 1 ]; then
            echo "Rodando em modo PARANOIA 1 (trava apenas ERROR)"
            semgrep --config auto --severity=ERROR --error
          elif [ "$PARANOIA_LEVEL" -eq 2 ]; then
            echo "Rodando em modo PARANOIA 2 (trava WARNING e acima)"
            semgrep --config auto --severity=WARNING --error
          else
            echo "Rodando em modo PARANOIA 3 (trava INFO e acima)"
            semgrep --config auto --severity=INFO --error
          fi
```

**PARANOIA_LEVEL:** controla o nível de ruído aceitável.
- `1` — só trava em `ERROR` (HIGH/CRITICAL). Adequado para times que ainda estão adotando o processo.
- `2` — trava em `WARNING` e acima. Recomendado para projetos maduros.
- `3` — trava em qualquer finding, incluindo `INFO`. Para ambientes de alta criticidade.

---

### 4.5 TruffleHog (Secrets) — workflow CI

`.github/workflows/trufflehog.yml`:

```yaml
name: TruffleHog Secret Scanner

on:
  push:
    branches: [ "main", "master" ]
  pull_request:
    branches: [ "main", "master" ]
  workflow_dispatch:

jobs:
  trufflehog:
    name: Scan for Secrets
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4
        with:
          fetch-depth: 0  # necessário para varrer todo o histórico git

      - name: TruffleHog OSS
        uses: trufflesecurity/trufflehog@3ab759fef4bb5935d4fe9ac68b503d05346b8364 # pinned commit
        with:
          path: ./
          base: ${{ github.event_name == 'pull_request' && github.event.pull_request.base.sha || github.event.before }}
          head: ${{ github.event_name == 'pull_request' && github.event.pull_request.head.sha || github.sha }}
          extra_args: --results=verified,unknown,unverified --debug
```

**Pontos críticos:**
- `fetch-depth: 0` é obrigatório — sem histórico completo, secrets em commits antigos não são detectados.
- `base`/`head` dinâmicos garantem que PRs e pushes diretos usem o delta correto.
- `--results=verified,unknown,unverified` inclui secrets não confirmados — conservador por design.

---

### 4.6 vet (SCA — Dependências) — workflow CI deste repositório

O workflow deste kit usa `vet` para SCA no CI. Um projeto consumidor pode escolher Trivy ou outra alternativa, mas deve registrar a escolha em `specs/tech-stack.md` e manter o gate de severidade equivalente.

`.github/workflows/vet-sca.yml`:

```yaml
name: vet OSS Components

on:
  pull_request:
  push:
    branches: [main]

jobs:
  vet:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6
      - name: vet (SCA)
        uses: safedep/vet-action@803d55e5de51766bd92c106d6bc1eb1a1858e4a3 # v1
        with:
          policy: .github/policies/vet-policy.yml
```

`vet` é o SCA do CI deste repositório; o pre-commit usa Trivy como feedback local rápido. Essa diferença é intencional e deve ser registrada no `tech-stack.md` de qualquer consumidor que adote o mesmo arranjo.

---

### 4.7 Pipeline de Validação de Código

`.github/workflows/ci.yml` — jobs de compilação e testes (adaptável por stack):

```yaml
name: CI

on:
  push:
    branches: ["**"]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4.2.2

      - name: Setup [Linguagem/Runtime]
        uses: actions/setup-[runtime]@v4
        with:
          [versão]

      - name: Instalar dependências
        run: [comando de instalação]

      - name: Verificação de tipos
        run: [verificação de tipos]

      - name: Testes
        run: [suite de testes]
```

---

### 4.8 Estratégia de Fixação de Dependências

O agente tende a instalar a versão mais recente de tudo. Isso é um vetor de ataque de supply chain — uma atualização maliciosa de um pacote pode comprometer seu build.

**Prática recomendada:**
- Commitar o lockfile (`package-lock.json`, `poetry.lock`, `go.sum`, `Gemfile.lock`, etc.)
- Usar versões fixas (sem `^` ou `~` em manifests de produção)
- Auditar atualizações antes de aplicar — não deixar o bot de atualização automática fazer merge sem revisão

**Prompt para o agente:**
```
Revise o manifesto de dependências (package.json, requirements.txt, go.mod, etc.).
Liste qualquer dependência com versão flutuante (^, ~, latest).
Proponha as versões fixas equivalentes e explique o risco de cada dependência com versão aberta.
```

---

## PARTE 5 — Skills Reutilizáveis

Skills são arquivos `SKILL.md` que encapsulam workflows repetitivos. O padrão moderno usa **progressive disclosure**: o agente carrega só o frontmatter + descrição até decidir invocar a skill — só então abre os scripts/instruções completas.

### Estrutura recomendada

```
skills/feature-spec/
├── SKILL.md              ← Frontmatter + descrição (sempre em contexto)
├── INSTRUCTIONS.md       ← Detalhes carregados sob demanda (opcional)
├── scripts/              ← Scripts auxiliares (opcional)
└── examples/             ← Exemplos de uso (opcional)
```

### Skill: changelog

**Quando usar:** antes de todo merge, para registrar o que mudou.

**Como invocar:**
```
Use sua skill changelog para atualizar o changelog.
```

**O que faz:**
- Se não existe `CHANGELOG.md`: lê todo `git log`, cria o arquivo
- Se existe: encontra a data mais recente, adiciona apenas commits novos

**Formato gerado:**
```markdown
# Changelog

## 2026-04-20
- feat: adicionar página About Us
- fix: corrigir validação do formulário

## 2026-04-19
- feat: implementar dashboard
```

### Skill: feature-spec

**Quando usar:** para iniciar qualquer nova funcionalidade sem redigitar o prompt longo.

**Como invocar:**
```
Use sua skill feature-spec para trabalhar na próxima funcionalidade do roadmap.
```

**O que faz:**
1. Lê `specs/roadmap.md` — acha a primeira fase com `[ ]`
2. Cria branch `YYYY-MM-DD-nome`
3. Faz Grill (Escopo / Decisões / Contexto)
4. Lê `specs/mission.md`, `specs/principles.md` e `specs/tech-stack.md`
5. Cria `specs/YYYY-MM-DD-nome/` com **todos os artefatos**: `EXECUTE.md`, `plan.md`, `requirements.md`, `test-cases.yaml` (se aplicável), `evals.yaml` (se aplicável), `QA_CHECKLIST.md`, `validation.md`, `security.md`

### Criando uma Nova Skill

**Prompt:**
```
Quero parar de repetir este prompt: [cole o prompt repetitivo].
Ajude-me a escrever uma skill local chamada "[nome]" usando progressive disclosure
(SKILL.md mínimo + INSTRUCTIONS.md detalhado carregado sob demanda).
```

**Estrutura mínima do SKILL.md:**
```markdown
---
name: nome-da-skill
description: Uma frase clara sobre quando usar esta skill (triggers e contexto).
---

# Nome da Skill

## Quando usar
[Critério curto e específico]

## Workflow (resumido)
1. [Passo um]
2. [Passo dois]

## Detalhes
Veja `INSTRUCTIONS.md` para o passo-a-passo completo.
```

---

## PARTE 6 — Subagents Especializados (arquivos versionados)

O agente de IA pode assumir **perspectivas especializadas** dependendo da fase do trabalho. No Claude Code, isso vira um arquivo em `.claude/agents/<nome>.md` — não um simples "aja como X". Subagents reais têm tools, contexto e modelo próprios.

### Quando usar cada perfil

| Perfil | Fase ideal | Foco |
|---|---|---|
| **architect-specialist** | P, R | Estrutura, padrões, decisões de longo prazo, trade-offs |
| **feature-developer** | E | Implementação seguindo spec, slices do plan.md em ordem |
| **security-auditor** | R, V | Entry points, OWASP Top 10, critérios do security.md |
| **performance-optimizer** | V | N+1, budget de queries, memory leaks, profiling |
| **code-reviewer** | V | Qualidade, tipagem, anti-patterns, cobertura de testes |
| **bug-fixer** | E (hotfix) | Isolamento, reprodução mínima, fix cirúrgico |
| **test-writer** | E, V | Cobertura, property-based testing, edge cases |
| **documentation-writer** | C | README, howtos, atualização de specs retroativos |

### Estrutura de um subagent

`.claude/agents/security-auditor.md`:
```markdown
---
name: security-auditor
description: Revisa código para vulnerabilidades OWASP Top 10. Usar antes de qualquer merge que toque entry points.
tools: Read, Grep, Bash
---

# Security Auditor

Você é um auditor de segurança. Para cada arquivo modificado:

1. Identifique entry points (rotas, handlers, parsers)
2. Para cada um, valide:
   - Input validation server-side
   - Saída sanitizada
   - Auth obrigatória (a menos que documentado em principles.md)
   - Sem secrets hardcoded
3. Rode os scans configurados em specs/tech-stack.md
4. Reporte findings por severidade. Para HIGH/CRITICAL, pare e exija correção.

Critérios: specs/principles.md (segurança) + specs/YYYY-MM-DD-feature/security.md.
```

### Como invocar

No Claude Code:
```
@security-auditor revise as mudanças desta branch
```

Em outras ferramentas (sem suporte nativo a subagents), use o fallback textual:
```
Aja como security-auditor (perfil em .claude/agents/security-auditor.md). Contexto: [estado atual].
Seu objetivo nesta sessão: [objetivo específico da fase].
```

---

## PARTE 7 — Revisão com Múltiplos Subagentes

Para revisões profundas antes de merge, use subagentes paralelos com perspectivas diferentes.

**Prompt:**
```
Faça uma revisão profunda: dispare em paralelo os subagents code-reviewer, security-auditor
e performance-optimizer sobre as mudanças desta branch. Compile um relatório único com
findings agrupados por severidade.
```

**Perspectivas recomendadas para cada review:**
1. **Qualidade de Código** — tipagem, padrões, anti-patterns, testes
2. **Segurança** — entry points, OWASP, princípios violados
3. **Alinhamento Specs vs Implementação** — o que o spec promete vs o que foi entregue
4. **CSS / UX / Design** — responsividade, brand, acessibilidade

> **Gate sugerido:** todo PR de escala MEDIUM ou LARGE passa por pelo menos 3 perspectivas antes de merge.

---

## PARTE 8 — STATE.md (Memória entre Sessões)

Quando você for pausar o trabalho para continuar no dia seguinte ou quando o limite de contexto do agente for atingido, salve o contexto para não perder as decisões tácitas.

**Prompt ao encerrar:**
```
Atualize specs/STATE.md com o contexto atual:
- Decisões tomadas hoje
- O que está pendente
- Bloqueios encontrados
- Próximos passos exatos (granulares, acionáveis)
```

**Prompt ao retomar:**
```
Leia specs/STATE.md para recuperar o contexto do nosso trabalho e retome a execução
a partir dos próximos passos definidos.
```

**Formato sugerido para STATE.md:**
```markdown
# STATE — última atualização: YYYY-MM-DD

## Contexto atual
[1-2 parágrafos sobre o que está em andamento]

## Branch ativa
YYYY-MM-DD-nome-feature

## Decisões recentes
- [data] [decisão] — motivo

## Pendências
- [ ] Tarefa específica 1
- [ ] Tarefa específica 2

## Bloqueios
- [item] aguardando [pessoa/decisão]

## Próximo passo (granular)
[Exatamente qual comando rodar ou arquivo abrir ao retomar]
```

---

## PARTE 9 — Lógica Pura e Código Descartável (whenwords)

Inspirado no conceito de "Bibliotecas Sem Código", o SDSD eleva a especificação ao nível de código-fonte quando lidamos com lógicas de negócio pesadas, cálculos ou formatações complexas.

**O Princípio:** o código é volátil e descartável; a Spec é imutável.

### 9.1 Testes Declarativos Agnósticos (`test-cases.yaml`)

Quando uma feature não for apenas um CRUD, mas envolver transformações de dados ou regras de negócio:
- A pasta da feature DEVE conter um `test-cases.yaml`.
- O arquivo deve ter apenas arrays de `input` e `expected_output`.
- Nenhuma referência a frameworks (Jest, PyTest, etc.) deve existir na spec.

**Exemplo:**
```yaml
cases:
  - name: desconto pequeno
    input: { valor: 100, tipo_cliente: regular }
    expected_output: { desconto: 0, total: 100 }

  - name: desconto VIP
    input: { valor: 100, tipo_cliente: vip }
    expected_output: { desconto: 15, total: 85 }
```

### 9.2 Avaliações para Features de IA (`evals.yaml`)

Para features que usam LLM, RAG ou qualquer componente não-determinístico, `test-cases.yaml` não basta — você precisa avaliar **propriedades** da resposta, não igualdade exata.

**Exemplo:**
```yaml
cases:
  - name: pergunta sobre política de troca
    input:
      query: "posso trocar um produto comprado há 30 dias?"
    properties:
      - mentions: ["troca", "30 dias"]
      - tone: profissional
      - max_tokens: 200
      - no_pii_in_response: true
    threshold: 0.8   # 80% das execuções devem passar
```

> Se a feature **não** envolve IA, omita `evals.yaml`.

### 9.3 O Spec "Executável" (`EXECUTE.md`)

O `EXECUTE.md` é o "botão de play" da feature. Ele empacota as instruções de execução para o agente — gerado junto com os outros artefatos no Step 2 da PARTE 1.

Se o projeto for reescrito em outra linguagem no futuro, basta rodar o `EXECUTE.md` novamente: a especificação gerará código novo automaticamente.

---

## PARTE 10 — Sincronização Multi-Ferramenta

O time pode usar diferentes agentes (Claude Code, Cursor, Copilot, Windsurf). Os specs do SDSD funcionam em qualquer ferramenta, mas as **regras de código** precisam estar acessíveis em cada uma.

### Estratégia de sincronização

**Fonte da verdade:** `AGENTS.md` na raiz do repositório. Toda regra de código vive aqui.

**Exportar para cada ferramenta:**

| Ferramenta | Onde colocar as regras |
|---|---|
| Claude Code | `CLAUDE.md` na raiz (ou `.claude/`) |
| Cursor | `.cursor/rules/` |
| Copilot | `.github/copilot-instructions.md` |
| Windsurf | `.windsurf/rules/` |
| Codex | `AGENTS.md` (já lido nativamente) |

### Template `AGENTS.md`

```markdown
# AGENTS.md — Regras de Código deste Projeto

> Fonte única. Editar AQUI e re-exportar para CLAUDE.md, .cursor/rules/, etc.

## Antes de qualquer mudança
- Leia specs/principles.md (restrições invioláveis)
- Identifique a fase no roadmap.md
- Crie ou atualize a feature spec ANTES de codar

## Convenções de código
- Naming: [camelCase | snake_case | kebab-case por contexto]
- Imports: [agrupados / ordenados como X]
- Erros: nunca silenciosos; sempre logar com contexto

## Comandos do projeto
| O que | Comando |
|---|---|
| Instalar | `[cmd]` |
| Rodar dev | `[cmd]` |
| Testar | `[cmd]` |
| Type check | `[cmd]` |
| SAST | `[cmd]` |
| SCA | `[cmd]` |
| Secrets | `[cmd]` |

## Gates obrigatórios antes de commit
1. Pre-commit hook passa
2. Type check em zero
3. Testes em verde
4. Specs atualizadas se o comportamento mudou

## O que NÃO fazer
- Não usar `--no-verify` em commits
- Não instalar dependência sem fixar versão
- Não criar rota pública sem documentar em requirements.md
- Não fazer merge sem atualizar CHANGELOG.md via skill
```

**Prompt para manter sincronizado:**
```
Leia o AGENTS.md na raiz do projeto.
Exporte as regras para [ferramenta]: crie [arquivo de destino] com o mesmo conteúdo
adaptado para o formato que [ferramenta] espera.
```

> **Regra:** nunca edite os arquivos de destino diretamente. Sempre edite o `AGENTS.md` e re-exporte. Isso evita regras divergentes entre ferramentas.

---

## PARTE 11 — O Prompt "Arquiteto de Produto" (Master Prompt)

Quando a funcionalidade for complexa e você quiser fazer um bootstrap unificado (ao invés de seguir os passos 1 e 2 manualmente), use o **Master Prompt** abaixo. Ele já embute Grill, Slices Verticais e Separação Humano/IA:

**Prompt:**
```text
Você é um Engenheiro de Software Sênior operando em modo Spec-Driven Secure Development (SDSD).
Sua missão é atuar como Arquiteto de Produto e criar os arquivos de especificação ANTES de qualquer implementação.

Regras absolutas:
1. NÃO escreva código de produção nesta etapa.
2. Primeiro elimine ambiguidades (Grill).
3. Depois gere os arquivos de spec.
4. Pare e aguarde minha aprovação para iniciar a implementação.

## Etapa 1: A Sessão de "Grill" (Clarificação)
Faça perguntas sobre a feature abaixo.
- UMA pergunta por vez.
- Para cada pergunta, proponha uma resposta recomendada baseada no contexto, em specs/principles.md e nas melhores práticas.
- Resolva ambiguidades sobre UX, APIs, Segurança (entry points) e Edge Cases.
- Só avance para a geração de arquivos quando eu disser que o escopo está claro.

[INSIRA A DESCRIÇÃO DA FEATURE AQUI]

## Etapa 2: Geração de Arquivos
Após o Grill, gere/atualize os arquivos em `specs/YYYY-MM-DD-nome-feature/`:
1. EXECUTE.md       — prompt exato para iniciar a implementação
2. test-cases.yaml  — (se houver lógica de negócio) inputs/outputs agnósticos
3. evals.yaml       — (se houver IA/LLM/RAG) casos de avaliação não-determinísticos
4. requirements.md  — contexto, data model, NFRs (Failure modes, Concorrência), Fora de Escopo
5. security.md      — entry points, vetores de ataque, requisitos de validação
6. plan.md          — fatias verticais (DB + Backend + UI), classificadas como [AFK] ou [HITL]
7. QA_CHECKLIST.md  — checklist focado em validação manual humana

## Etapa 3: Resumo Executivo
Ao finalizar a geração, me entregue:
- As 3 principais premissas assumidas.
- Os 3 maiores riscos técnicos.
- O que o agente fará sozinho (AFK) e onde precisará de mim (HITL).
- Quais princípios de specs/principles.md são especialmente relevantes para esta feature.
```

---

## PARTE 12 — Replanejamento do Roadmap

Quando o escopo muda (features combinadas, depriorizadas ou divididas):

**Prompt:**
```
Vá para o roadmap.md e combine as fases X-Y-Z em uma nova fase única.
```

ou

```
A UI web do produto deve seguir design responsivo.
Atualize as especificações do produto e todas as especificações de funcionalidades para refletir isso,
bem como qualquer código.
```

**Regra:** sempre que specs mudarem, o código muda junto — e vice-versa. Eles nunca ficam dessincronizados.

---

## PARTE 13 — Análise de Cobertura de Testes & Evals

**Prompt para testes determinísticos:**
```
Quais partes do nosso código precisam de mais testes?
Analise: rotas testadas vs não testadas, componentes com/sem unit tests,
lógica de banco e middleware. Liste as top 5 lacunas de risco.
```

**Prompt para evals (features de IA):**
```
Para cada feature em specs/ que tenha evals.yaml, rode o harness e reporte:
- Taxa de aprovação por feature
- Casos que passaram do threshold mas estão próximos do limite
- Regressões em relação à última execução
```

---

## Referência Rápida de Prompts

| Situação | Prompt |
|---|---|
| Projeto novo — iniciar | "Crie uma constituição em specs/ com mission.md, principles.md, tech-stack.md e roadmap.md. Use Grill (1 pergunta por vez) antes de escrever." |
| Próxima funcionalidade | "Use sua skill feature-spec para trabalhar na próxima funcionalidade do roadmap." |
| Implementar | "Execute o EXECUTE.md desta feature." |
| Spec mudou | "Atualize plan.md e a implementação para refletir [mudança]. Sincronize requirements.md, validation.md e security.md." |
| Antes do merge | "Use sua skill changelog para atualizar o changelog. Crie ADR se a decisão for irreversível." |
| Merge e limpeza | "Marque esta fase como concluída no roadmap. Faça commit, mude para main, faça merge e exclua a branch." |
| Revisão profunda | "Dispare em paralelo code-reviewer, security-auditor e performance-optimizer. Compile um relatório único." |
| Projeto legado | "Crie uma constituição baseada no código existente, incluindo principles.md extraído das convenções implícitas." |
| Cobertura de testes | "Quais partes do nosso código precisam de mais testes?" |
| Replanejamento | "Combine as fases X-Y em uma única fase no roadmap." |
| N+1 / queries | "Analise as rotas e identifique problemas N+1. Mostre o número de queries por rota e proponha a query consolidada." |
| Race conditions | "Identifique operações de escrita com risco de race condition, proponha a invariante a garantir e implemente a mitigação." |
| Memory leaks | "Revise o código em busca de caches sem TTL, conexões não fechadas e listeners sem remoção correspondente." |
| Fault tolerance | "Para cada rota, liste os failure modes possíveis e o comportamento atual. Proponha e implemente o tratamento correto." |
| Dependências fixas | "Revise o manifesto de dependências. Liste versões flutuantes e proponha versões fixas equivalentes." |
| Subagent especializado | "@[nome-do-agent] revise/execute [contexto]." (Claude Code) ou "Aja como [perfil] em .claude/agents/[nome].md." |
| **Segurança — configurar ferramentas** | "Identifique SAST, SCA, Secrets e pre-commit framework adequados para a stack. Instale, configure e crie os workflows. Documente em specs/tech-stack.md." |
| **Segurança — pre-commit local** | "Crie .pre-commit-config.yaml com hooks para SAST, SCA, Secrets e linter. Instale e ative o hook." |
| **Segurança — scan local (feature)** | "Rode scan local: SAST em src/, SCA no manifesto, Secrets no histórico desta branch. Reporte HIGH/CRITICAL e proponha correções." |
| **Segurança — primeiro scan (legado)** | "Rode o scan completo sem bloquear. Gere relatório por severidade e categoria. Crie backlog de remediação no roadmap.md." |
| **Segurança — adicionar CI** | "Crie os workflows .github/workflows/ para SAST, SCA e Secrets escolhidos. Use os exemplos da PARTE 4 como base." |
| **Secret encontrado** | "Um secret foi encontrado. Revogue em [serviço], rode git filter-repo para limpar o histórico e configure pre-commit para prevenir reincidência." |
| **Sincronizar regras** | "Leia o AGENTS.md e exporte para [Cursor / Copilot / Windsurf], criando o arquivo de destino no formato correto." |
| **Salvar contexto** | "Atualize specs/STATE.md com decisões, pendências, bloqueios e próximo passo granular." |
| **Retomar contexto** | "Leia specs/STATE.md e retome do próximo passo." |

---

## Checklist por Feature

```
[ ] Branch criada com nome YYYY-MM-DD-nome-kebab
[ ] specs/YYYY-MM-DD-nome/EXECUTE.md criado (prompt de execução pronto)
[ ] specs/YYYY-MM-DD-nome/plan.md criado (fatias verticais com tags [AFK] e [HITL])
[ ] specs/YYYY-MM-DD-nome/requirements.md criado (escopo, decisões, contexto, NFRs)
[ ] specs/YYYY-MM-DD-nome/test-cases.yaml criado (se houver regra de negócio/transformação)
[ ] specs/YYYY-MM-DD-nome/evals.yaml criado (se a feature usa IA/LLM/RAG)
[ ] specs/YYYY-MM-DD-nome/QA_CHECKLIST.md criado (validação humana de UX e regressões)
[ ] specs/YYYY-MM-DD-nome/validation.md criado (definition of done automatizado)
[ ] specs/YYYY-MM-DD-nome/security.md criado (entry points, riscos, requisitos)
[ ] Implementação completa (todas as fatias do plan.md testadas)
[ ] Pre-commit hook ativo e passando localmente
[ ] [verificação de tipos] → exit 0
[ ] [suite de testes] → todos passam
[ ] Verificação manual no browser
[ ] Spec atualizado se algo mudou durante implementação
--- Qualidade e Resiliência ---
[ ] Rotas com coleção revisadas para N+1 — budget de queries documentado
[ ] Operações de escrita concorrente têm mitigação (lock / transaction / idempotency key)
[ ] Failure modes documentados e tratados no código
[ ] Sem caches sem TTL ou conexões não fechadas
--- Segurança ---
[ ] [SAST] → 0 HIGH/CRITICAL
[ ] [SCA] → 0 HIGH/CRITICAL
[ ] [Secrets] → 0 findings
[ ] Dependências com versão fixa (sem ^ ou ~ em produção)
[ ] Workflows de CI/CD de segurança ativos em .github/workflows/
[ ] Ferramentas escolhidas documentadas em specs/tech-stack.md
[ ] Nenhum princípio de specs/principles.md violado
--- Merge ---
[ ] Fase marcada como ✅ no roadmap.md
[ ] CHANGELOG.md atualizado via skill changelog
[ ] ADR criado em specs/adr/ (se decisão irreversível)
[ ] Commit feito com mensagem descritiva
[ ] Merge em main com --no-ff
[ ] Branch deletada
--- Multi-ferramenta (se aplicável) ---
[ ] AGENTS.md atualizado com novas regras (se houver)
[ ] Regras re-exportadas para as ferramentas do time (Cursor, Copilot, etc.)
```

---

## Anti-patterns a Evitar

| Anti-pattern | Por quê evitar | O que fazer |
|---|---|---|
| Codar sem spec | Sem rastreabilidade, sem alinhamento | Sempre criar spec da feature antes |
| Spec e código dessincronizados | Futuro analista não sabe o que é real | Atualizar spec sempre que implementação mudar; registrar decisão em requirements.md |
| Commit sem changelog | Histórico perdido | Rodar skill changelog antes de todo merge |
| Branch longa com muitas features | Dificulta revisão e rollback | Uma feature = uma branch = um merge |
| Roadmap com fases grandes | Feature demora, feedback tardio | Fases implementáveis em uma sessão (máx. 5 grupos no plan.md) |
| Perguntas depois de escrever no disco | Desperdício se o usuário quer algo diferente | Sempre Grill ANTES de criar arquivos |
| Segurança só no CI/CD | Feedback tardio, PR vira campo de batalha | Pre-commit local é o ponto primário; CI é rede de segurança |
| Feature sem security.md | Riscos não documentados, sem critério de aceite | Todo spec de feature inclui security.md obrigatório |
| Rotas sem budget de queries | N+1 invisível em dev, colapso em produção | Documentar limite de queries no requirements.md e validar |
| Sem failure modes no spec | Código trata só o caminho feliz | Seção Confiabilidade no requirements.md com cenários de falha |
| Versões flutuantes de dependências | Supply chain: atualização maliciosa entra sem revisão | Fixar versões e commitar lockfile |
| Sem property-based testing em escrita concorrente | Race conditions passam despercebidas | Identificar invariantes e usar property-based testing |
| Secret encontrado → só remover do código | Secret no histórico git continua exposto | Revogar credencial + git filter-repo + auditar acesso |
| Regras de código só em um arquivo de ferramenta | Time diverge entre Cursor/Copilot/Claude | AGENTS.md como fonte única, exportar para cada ferramenta |
| Fluxo completo P→R→E→V→C para todo bugfix | Overhead desnecessário | Usar escala de workflow: QUICK para fixes, LARGE só para sistemas complexos |
| Subagent como string "aja como X" | Sem persistência, sem tools dedicadas | Criar arquivo `.claude/agents/<nome>.md` versionado |
| Skill monolítica | Consome contexto desnecessariamente | Progressive disclosure: SKILL.md mínimo + INSTRUCTIONS.md sob demanda |
| Editar CLAUDE.md sem editar AGENTS.md | Times com várias ferramentas divergem | Editar AGENTS.md e re-exportar |
| Pular pre-commit com --no-verify | Findings entram no histórico | Corrigir o hook ou o código; nunca pular |
| Usar test-cases.yaml para feature de IA | Outputs não-determinísticos não casam por igualdade | Usar evals.yaml com propriedades + threshold |
