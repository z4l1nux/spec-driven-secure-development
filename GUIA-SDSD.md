# Guia Técnico: Spec-Driven Secure Development (SDSD)

> Referência hands-on para qualquer analista do time.  
> Cobre projetos **novos** e projetos **em andamento (legado)**.

---

## O que é SDSD?

Spec-Driven Secure Development é um fluxo de trabalho onde **toda funcionalidade começa com especificações escritas antes do código**. O agente de IA trabalha a partir dos specs — não de prompts soltos. Isso garante rastreabilidade, alinhamento entre stakeholders e código revisável.

**Princípio central:** O spec é a fonte da verdade. O código implementa o spec. O changelog registra o histórico.

---

## Estrutura de Arquivos

```
projeto/
├── specs/                          ← Constituição + specs de funcionalidades
│   ├── mission.md                  ← Por que o projeto existe
│   ├── tech-stack.md               ← Decisões técnicas e suas razões
│   ├── roadmap.md                  ← Fases de trabalho em ordem
│   └── YYYY-MM-DD-nome-feature/    ← Uma pasta por funcionalidade
│       ├── plan.md                 ← Grupos de tarefas numerados
│       ├── requirements.md         ← Escopo, decisões, contexto
│       ├── validation.md           ← Como saber que está pronto para merge
│       └── security.md             ← Entry points, riscos, critérios de segurança
├── skills/                         ← Skills reutilizáveis (opcionais)
│   ├── changelog/
│   │   ├── SKILL.md
│   │   └── scripts/changelog.py
│   └── feature-spec/
│       └── SKILL.md
├── CHANGELOG.md                    ← Gerado pela skill changelog
└── src/                            ← Código
```

---

## PARTE 1 — Projeto Novo

### Passo 1: Criar a Constituição

A constituição são os três arquivos base que todo projeto SDSD precisa antes de qualquer código.

**Prompt para o agente:**
```
Estamos construindo [nome do projeto]. Consulte o README.md para entrada das partes interessadas.
Crie uma "constituição" em um diretório specs:
- mission.md
- tech-stack.md
- roadmap.md (fases de trabalho pequenas e independentes)

Importante: você DEVE usar AskUserQuestion, agrupada em 3 perguntas, antes de escrever no disco.
```

**O que o agente vai perguntar (3 perguntas agrupadas):**
1. **Missão** — tom, propósito, o que o produto faz
2. **Stack** — linguagem, framework, banco de dados
3. **Roadmap** — como estruturar as fases (incremental, vertical, etc.)

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
[Critério de sucesso]
```

`specs/tech-stack.md`:
```markdown
# Tech Stack
## Core
| Layer | Choice | Rationale |
|---|---|---|
| Language | TypeScript | ... |
| Framework | Hono | ... |
| Database | SQLite | ... |
## Testing
- Vitest — rápido, TypeScript-native
## CSS Approach
Mobile-first, custom properties
```

`specs/roadmap.md`:
```markdown
# Roadmap
## Phase 1 — Nome pequeno e entregável
- [ ] Tarefa A
- [ ] Tarefa B
## Phase 2 — ...
```

> **Regra:** cada fase do roadmap deve ser implementável em uma sessão focada e independentemente mergeável.

---

### Passo 2: Especificar uma Funcionalidade (Feature Spec)

Antes de implementar qualquer fase, crie o spec da funcionalidade.

**Prompt para o agente:**
```
Encontre a próxima fase em specs/roadmap.md e crie uma branch.
Crie um novo diretório YYYY-MM-DD-nome-da-funcionalidade em specs com:
- plan.md — grupos de tarefas numerados
- requirements.md — escopo, decisões, contexto
- validation.md — como saber se pode ser mergeado

Consulte specs/mission.md e specs/tech-stack.md para orientação.
Importante: use AskUserQuestion agrupada em 3 antes de escrever no disco.
```

**O que o agente faz:**
1. Lê `specs/roadmap.md`, identifica a primeira fase com itens `[ ]`
2. Cria branch: `git checkout -b YYYY-MM-DD-nome-kebab`
3. Pergunta 3 perguntas antes de escrever qualquer arquivo:

| Cabeçalho | Foco |
|---|---|
| **Escopo** | O que a feature coleta, expõe ou faz — campos, comportamento |
| **Decisões** | Escolhas de implementação — storage, validação, padrão de UX |
| **Contexto** | Tom, restrições, padrões existentes a seguir |

**Resultado esperado:**

`specs/YYYY-MM-DD-nome/plan.md`:
```markdown
# Plan — Nome da Feature

## Group 1 — Banco de Dados
1. Criar migration SQL
2. Criar seed data

## Group 2 — Rotas
3. GET /rota → render página
4. POST /rota → persistir dados

## Group 3 — Componentes UI
5. Criar componente Lista
6. Criar componente Form

## Group 4 — Testes
7. Teste GET /rota → status 200
8. Teste POST /rota → redirect ou confirmação

## Group 5 — Verificação
9. npm run typecheck → 0 erros
10. npm test → todos passam
```

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

## Context
Tom, stack, padrões existentes a seguir.
```

`specs/YYYY-MM-DD-nome/validation.md`:
```markdown
# Validation — Nome

## Definition of Done

### 1. TypeScript compila
`npm run typecheck` → exit 0

### 2. Testes passam
`npm test` → exit 0
Deve cobrir: [lista de rotas/comportamentos]

### 3. Verificação manual
- [ ] Página X carrega em http://localhost:3000/x
- [ ] Formulário Y envia e persiste
- [ ] Layout responsivo em mobile (≤ 640px)

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

---

### Passo 3: Implementar

Com o spec pronto, o agente implementa seguindo os grupos do `plan.md`.

**Prompt para o agente:**
```
Implemente os grupos de tarefas do plan.md.
```

O agente executa os grupos em ordem. Cada grupo é uma unidade coesa (ex: banco → rotas → UI → testes).

---

### Passo 4: Atualizar o Spec quando a Implementação Mudar

Se durante a implementação uma decisão mudar (ex: nova estrutura de componente, escopo expandido):

**Prompt para o agente:**
```
Atualize specs/YYYY-MM-DD-nome/plan.md e a implementação para refletir [mudança].
Sincronize o restante da especificação.
```

O agente atualiza `plan.md`, `requirements.md` e `validation.md` juntos — specs e código sempre em sincronia.

---

### Passo 5: Marcar Fase como Concluída e Fazer Merge

**Prompt para o agente:**
```
Marque esta fase em specs/roadmap.md como concluída.
Use sua skill changelog para atualizar o changelog.
Faça commit deste trabalho, mude para main e faça merge desta branch, depois exclua-a.
```

**O que acontece:**
1. Agente edita `roadmap.md` → adiciona `✅` na fase concluída
2. Roda `python3 skills/changelog/scripts/changelog.py` → atualiza `CHANGELOG.md`
3. `git add` → `git commit` → `git checkout main` → `git merge --no-ff` → `git branch -d`

---

## PARTE 2 — Projeto em Andamento (Legado)

Quando o código já existe mas as specs não (ou estão desatualizadas):

### Passo 1: Reconstruir a Constituição

**Prompt para o agente:**
```
Temos um projeto [nome] já implementado. Consulte o README.md para entrada das partes interessadas.
Crie uma constituição em specs/ baseada no que já existe:
- mission.md
- tech-stack.md
- roadmap.md — baseado no código existente, com fases já implementadas marcadas como ✅

Entreviste-me sobre missão, público-alvo, lacunas na stack de tecnologia.
Importante: use AskUserQuestion agrupada em 3 antes de escrever no disco.
```

**O agente vai:**
1. Ler o código existente (routes, components, db, middleware)
2. Perguntar sobre missão, público-alvo, lacunas na stack
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
O código em src/routes/agents.tsx e src/components/AgentsList.tsx já está implementado.
Crie um spec retroativo em specs/YYYY-MM-DD-agents/ que documente:
- O que foi implementado (plan.md com tarefas concluídas)
- As decisões que foram tomadas (requirements.md)
- Como validar que ainda funciona (validation.md)
```

### Passo 3: Continuar com Feature Spec Normal

Após a constituição reconstruída, o fluxo é idêntico ao projeto novo (Passo 2 em diante).

---

## PARTE 3 — Skills Reutilizáveis

Skills são arquivos `SKILL.md` que encapsulam workflows repetitivos para que o analista não precise redigitar o mesmo prompt.

### Skill: changelog

**Arquivo:** `skills/changelog/SKILL.md` + `skills/changelog/scripts/changelog.py`

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

**Arquivo:** `skills/feature-spec/SKILL.md`

**Quando usar:** para iniciar qualquer nova funcionalidade sem redigitar o prompt longo.

**Como invocar:**
```
Use sua skill feature-spec para trabalhar na próxima funcionalidade do roadmap.
```

**O que faz:**
1. Lê `specs/roadmap.md` — acha a primeira fase com `[ ]`
2. Cria branch `YYYY-MM-DD-nome`
3. Faz AskUserQuestion com 3 perguntas (Escopo / Decisões / Contexto)
4. Lê `specs/mission.md` e `specs/tech-stack.md`
5. Cria `specs/YYYY-MM-DD-nome/` com `plan.md`, `requirements.md`, `validation.md`

### Criando uma Nova Skill

**Prompt:**
```
Quero parar de repetir este prompt: [cole o prompt repetitivo].
Ajude-me a escrever uma skill local chamada "[nome]".
```

**Estrutura do arquivo SKILL.md:**
```markdown
---
name: nome-da-skill
description: Uma frase clara sobre quando usar esta skill.
---

# Nome da Skill

## Workflow

### 1. Passo um
[instrução]

### 2. Passo dois
[instrução]

## Constraints
- [restrição 1]
- [restrição 2]
```

---

## PARTE 4 — Revisão com Múltiplos Subagentes

Para revisões profundas antes de merge, use subagentes paralelos com perspectivas diferentes.

**Prompt:**
```
Faça uma revisão profunda: crie múltiplos subagentes para passar por todas as mudanças
desta branch de três perspectivas diferentes e ver se algo não faz sentido, poderia ser melhor, etc.
```

**Perspectivas recomendadas:**
1. **TypeScript / Qualidade de Código** — tipagem, padrões, anti-patterns, testes
2. **Alinhamento Specs vs Implementação** — o que o spec promete vs o que foi entregue
3. **CSS / UX / Design** — responsividade, brand, acessibilidade

---

## PARTE 5 — Replanejamento do Roadmap

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

## PARTE 6 — Análise de Cobertura de Testes

**Prompt:**
```
Quais partes do nosso código precisam de mais testes?
```

O agente analisa:
- Rotas testadas vs não testadas
- Componentes com e sem testes unitários
- Lógica de banco e middleware
- Top lacunas de risco (o que quebraria em produção sem ser detectado)

---

## Referência Rápida de Prompts

| Situação | Prompt |
|---|---|
| Projeto novo — iniciar | "Crie uma constituição em specs/ com mission.md, tech-stack.md e roadmap.md. Use AskUserQuestion agrupada em 3 antes de escrever." |
| Próxima funcionalidade | "Use sua skill feature-spec para trabalhar na próxima funcionalidade do roadmap." |
| Implementar | "Implemente os grupos de tarefas restantes." |
| Spec mudou | "Atualize o plan.md e a implementação para refletir [mudança]. Sincronize o resto da spec." |
| Antes do merge | "Use sua skill changelog para atualizar o changelog." |
| Merge e limpeza | "Marque esta fase como concluída no roadmap. Faça commit, mude para main, faça merge e exclua a branch." |
| Revisão profunda | "Faça uma revisão profunda com múltiplos subagentes: qualidade de código, alinhamento de specs, CSS/UX." |
| Projeto legado | "Crie uma constituição baseada no código existente. Entreviste-me sobre missão, público-alvo e lacunas na stack." |
| Cobertura de testes | "Quais partes do nosso código precisam de mais testes?" |
| Replanejamento | "Combine as fases X-Y em uma única fase no roadmap." |

---

## Checklist por Feature

```
[ ] Branch criada com nome YYYY-MM-DD-nome-kebab
[ ] specs/YYYY-MM-DD-nome/plan.md criado (grupos de tarefas)
[ ] specs/YYYY-MM-DD-nome/requirements.md criado (escopo, decisões, contexto)
[ ] specs/YYYY-MM-DD-nome/validation.md criado (definition of done)
[ ] specs/YYYY-MM-DD-nome/security.md criado (entry points, riscos, requisitos)
[ ] Implementação completa (todos os grupos do plan.md)
[ ] npm run typecheck → exit 0
[ ] npm test → todos passam
[ ] Verificação manual no browser
[ ] Spec atualizado se algo mudou durante implementação
[ ] semgrep → 0 HIGH/CRITICAL
[ ] trivy fs . → 0 HIGH/CRITICAL
[ ] trufflehog filesystem . → 0 secrets
[ ] Fase marcada como ✅ no roadmap.md
[ ] CHANGELOG.md atualizado via skill changelog
[ ] Commit feito com mensagem descritiva
[ ] Merge em main com --no-ff
[ ] Branch deletada
```

---

## Anti-patterns a Evitar

| Anti-pattern | Por quê evitar | O que fazer |
|---|---|---|
| Codar sem spec | Sem rastreabilidade, sem alinhamento | Sempre criar plan.md + requirements.md + validation.md antes |
| Spec e código dessincronizados | Futuro analista não sabe o que é real | Atualizar spec sempre que implementação mudar |
| Commit sem changelog | Histórico perdido | Rodar skill changelog antes de todo merge |
| Branch longa com muitas features | Dificulta revisão e rollback | Uma feature = uma branch = um merge |
| Roadmap com fases grandes | Feature demora, feedback tardio | Fases devem ser implementáveis em uma sessão |
| Perguntas depois de escrever no disco | Desperdício se o usuário quer algo diferente | Sempre AskUserQuestion ANTES de criar arquivos |
| Segurança só no CI/CD | Feedback tardio, PR vira campo de batalha | Rodar semgrep/trivy/trufflehog localmente antes do commit |
| Feature sem security.md | Riscos não documentados, sem critério de aceite | Todo spec de feature inclui security.md obrigatório |
