# Princípios Invioláveis

> Restrições que se aplicam a TODA feature deste projeto, sem exceção.
> Mudanças aqui exigem um ADR em `specs/adr/` (não basta editar este arquivo).
> Toda feature spec é validada contra este documento em `security.md` e na revisão pré-merge.

---

## Segurança

- Nenhum secret no código, em logs ou em mensagens de erro voltadas ao cliente
- Toda rota é autenticada por padrão; rotas públicas exigem decisão explícita registrada em `requirements.md` (seção Decisions)
- Inputs sempre validados server-side; validação no cliente é apenas UX, nunca segurança
- Saída sanitizada antes de renderizar em HTML, SQL ou shell
- Dependências com versão fixa; lockfile commitado; sem `^` ou `~` em manifestos de produção
- Dados pessoais nunca aparecem em logs sem mascaramento

## Privacidade / Compliance

- [ex: LGPD — base legal documentada para cada coleta de dado pessoal]
- [ex: dados pessoais criptografados em repouso e em trânsito]
- [ex: consentimento explícito antes de coletar dado sensível]
- [ex: retenção máxima de N dias para logs com PII]

## Qualidade

- Specs e código são commitados juntos — nunca um sem o outro
- Toda feature tem failure modes documentados em `requirements.md` ANTES de ser implementada
- Type check e suite de testes em verde são pré-requisitos de qualquer commit
- Pre-commit hook nunca é pulado com `--no-verify`

## UX

- [ex: feedback visível em ações > 200ms (loading, skeleton, etc.)]
- [ex: mensagens de erro acionáveis, nunca códigos crus]
- [ex: nenhuma ação destrutiva sem confirmação ou undo]
- [ex: acessibilidade WCAG 2.1 nível AA como linha de base]

## Operação

- [ex: toda métrica de negócio crítica tem alerta configurado antes do release]
- [ex: rollback documentado para cada migration de schema]

---

## Como usar este arquivo

1. Ao criar uma feature, leia este arquivo antes de iniciar o Grill
2. Em `security.md`, marque qual princípio aplica e como será garantido
3. Se um princípio precisar ser quebrado, **pare** — abra um ADR descrevendo o motivo, alternativas consideradas e prazo de remediação. Sem ADR, não há quebra
