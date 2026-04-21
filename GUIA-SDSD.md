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
| Language | [Linguagem] | [motivo] |
| Framework | [Framework] | [motivo] |
| Database | [Banco] | [motivo] |
## Testing
- [Framework de testes] — [característica principal]
## CSS / UI
[Abordagem: mobile-first, design system, etc.]
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
9. [verificação de tipos] → 0 erros
10. [suite de testes] → todos passam
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

## Non-Functional Requirements

### Performance
- Budget de queries: esta rota não deve exceder [N] queries por requisição
- [Tempo de resposta esperado, se relevante]

### Confiabilidade
- Failure modes identificados: [ex: o que acontece se o banco cair?]
- A feature deve ser resiliente a: [ex: timeout externo, dado ausente]

### Concorrência
- Risco de race condition: [Sim / Não / Baixo]
- Se Sim: [descrever o cenário e a mitigação, ex: transaction, lock, idempotency key]

## Context
Tom, stack, padrões existentes a seguir.
```

`specs/YYYY-MM-DD-nome/validation.md`:
```markdown
# Validation — Nome

## Definition of Done

### 1. Código compila sem erros
`[verificação de tipos]` → exit 0

### 2. Testes passam
`[suite de testes]` → exit 0
Deve cobrir: [lista de rotas/comportamentos]

### 3. Verificação manual
- [ ] Página X carrega em http://localhost:3000/x
- [ ] Formulário Y envia e persiste
- [ ] Layout responsivo em mobile (≤ 640px)

### 4. Performance
- [ ] Rota X não ultrapassa [N] queries por requisição
- [ ] Sem alocações sem TTL identificadas no profiling local

### 5. Segurança (shift-left)
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
- LOW/INFO: aceitar ou ignorar conscientemente, documentando a decisão em security.md
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

Após constituição reconstruída e primeiro scan feito, o fluxo é idêntico ao projeto novo (Passo 2 em diante).

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

O agente analiza:
- Rotas testadas vs não testadas
- Componentes com e sem testes unitários
- Lógica de banco e middleware
- Top lacunas de risco (o que quebraria em produção sem ser detectado)

---

## PARTE 7 — Qualidade e Resiliência

### 7.1 Problema N+1 (Excesso de Queries)

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

### 7.2 Race Conditions

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

### 7.3 Memory Leaks

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

### 7.4 Fault Tolerance (Tolerância a Falhas)

**O problema:** o agente escreve o caminho feliz. Não pensa no que acontece quando o banco cai, o serviço externo não responde ou o dado esperado não está lá.

**Como documentar no spec:**

Em `requirements.md`, seção Confiabilidade:
```
Failure modes identificados:
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

## PARTE 8 — Automação de CI/CD

O shift-left funciona em dois momentos: **localmente, antes do commit**, e **no pipeline, antes do merge**. Ambos são obrigatórios — o CI é a rede de segurança, não o ponto primário de detecção.

### 8.0 Escolha de Ferramentas por Stack

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

> **Regra:** documente a ferramenta escolhida em `specs/tech-stack.md` na seção Security. Todos no time e o CI usam a mesma.

---

### 8.1 Prompts para Rodar Localmente

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
- Crie os workflows em .github/workflows/ para cada uma
- Documente os comandos locais em specs/tech-stack.md na seção Security
```

---

### 8.2 Semgrep (SAST)

`.github/workflows/semgrep.yml`:

```yaml
name: Semgrep Security Scan

on:
  push:
    branches:
      - "**"
  pull_request:
    branches:
      - "**"

env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true

jobs:
  semgrep_scan:
    runs-on: ubuntu-latest

    steps:
      - name: Check out code
        uses: actions/checkout@v4.2.2

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Install Semgrep
        run: |
          python -m pip install --upgrade pip
          pip install semgrep

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

### 8.3 TruffleHog (Secrets)

`.github/workflows/trufflehog.yml`:

```yaml
name: TruffleHog Secret Scanner

on:
  push:
    branches: [ "main", "master" ]
  pull_request:
    branches: [ "main", "master" ]
  workflow_dispatch:

env:
  FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true

jobs:
  trufflehog:
    name: Scan for Secrets
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4.2.2
        with:
          fetch-depth: 0  # necessário para varrer todo o histórico git

      - name: TruffleHog OSS
        uses: trufflesecurity/trufflehog@main
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

### 8.4 Trivy (SCA — Dependências)

`.github/workflows/trivy.yml`:

```yaml
name: Trivy Dependency Scan

on:
  push:
    branches: ["**"]
  pull_request:
    branches: ["**"]

jobs:
  trivy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4.2.2

      - name: Trivy (SCA — filesystem)
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: fs
          severity: HIGH,CRITICAL
          exit-code: 1
```

---

### 8.5 Pipeline de Validação de Código

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

### Estratégia de Fixação de Dependências

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
| N+1 / queries | "Analise as rotas e identifique problemas N+1. Mostre o número de queries por rota e proponha a query consolidada." |
| Race conditions | "Identifique operações de escrita com risco de race condition, proponha a invariante a garantir e implemente a mitigação." |
| Memory leaks | "Revise o código em busca de caches sem TTL, conexões não fechadas e listeners sem remoção correspondente." |
| Fault tolerance | "Para cada rota, liste os failure modes possíveis e o comportamento atual. Proponha e implemente o tratamento correto." |
| Dependências fixas | "Revise o manifesto de dependências. Liste versões flutuantes e proponha versões fixas equivalentes." |
| **Segurança — configurar ferramentas** | "Identifique o SAST, SCA e Secrets scanner mais adequado para a stack em specs/tech-stack.md. Instale, configure e crie os workflows em .github/workflows/. Documente os comandos locais em specs/tech-stack.md." |
| **Segurança — scan local (feature)** | "Rode o scan de segurança local: [SAST] em src/, [SCA] no manifesto, [Secrets] no histórico desta branch. Reporte HIGH e CRITICAL. Para cada um, proponha a correção antes de continuarmos." |
| **Segurança — primeiro scan (legado)** | "Rode o scan completo sem bloquear. Gere relatório por severidade e categoria. Depois crie o backlog de remediação no roadmap.md separando imediato (CRITICAL/HIGH) de planejado (MEDIUM)." |
| **Segurança — adicionar CI** | "Crie os workflows .github/workflows/ para [SAST], [SCA] e [Secrets] escolhidos em specs/tech-stack.md. Use os exemplos da PARTE 8 do guia como base." |

---

## Checklist por Feature

```
[ ] Branch criada com nome YYYY-MM-DD-nome-kebab
[ ] specs/YYYY-MM-DD-nome/plan.md criado (grupos de tarefas)
[ ] specs/YYYY-MM-DD-nome/requirements.md criado (escopo, decisões, contexto, NFRs)
[ ] specs/YYYY-MM-DD-nome/validation.md criado (definition of done)
[ ] specs/YYYY-MM-DD-nome/security.md criado (entry points, riscos, requisitos)
[ ] Implementação completa (todos os grupos do plan.md)
[ ] [verificação de tipos] → exit 0
[ ] [suite de testes] → todos passam
[ ] Verificação manual no browser
[ ] Spec atualizado se algo mudou durante implementação
--- Qualidade e Resiliência ---
[ ] Rotas com coleção revisadas para N+1 — budget de queries documentado no requirements.md
[ ] Operações de escrita concorrente têm mitigação (lock / transaction / idempotency key)
[ ] Failure modes documentados no requirements.md e tratados no código
[ ] Sem caches sem TTL ou conexões não fechadas
--- Segurança ---
[ ] [SAST: semgrep / bandit / gosec / outro] → 0 HIGH/CRITICAL
[ ] [SCA: trivy / npm audit / pip-audit / outro] → 0 HIGH/CRITICAL
[ ] [Secrets: trufflehog / gitleaks / outro] → 0 findings
[ ] Dependências com versão fixa (sem ^ ou ~ em produção)
[ ] Workflows de CI/CD de segurança criados em .github/workflows/
[ ] Ferramentas escolhidas documentadas em specs/tech-stack.md
--- Merge ---
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
| Segurança só no CI/CD | Feedback tardio, PR vira campo de batalha | Rodar SAST/SCA/Secrets localmente antes do commit — CI é rede de segurança, não ponto primário |
| Feature sem security.md | Riscos não documentados, sem critério de aceite | Todo spec de feature inclui security.md obrigatório |
| Rotas sem budget de queries | N+1 invisível em dev, colapso em produção | Documentar limite de queries no requirements.md e validar |
| Sem failure modes no spec | Código trata só o caminho feliz | Seção Confiabilidade no requirements.md com cenários de falha |
| Versões flutuantes de dependências | Supply chain: atualização maliciosa entra sem revisão | Fixar versões no manifesto e commitar o lockfile |
| Sem property-based testing em escrita concorrente | Race conditions passam despercebidas nos testes unitários | Identificar invariantes e usar biblioteca de property-based testing |
