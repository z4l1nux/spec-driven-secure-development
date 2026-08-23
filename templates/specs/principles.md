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

Substitua os itens abaixo pelas regras aprovadas para o seu produto antes de
iniciar uma feature. Eles são exemplos, não controles implementados:

- [TODO: LGPD — base legal documentada para cada coleta de dado pessoal]
- [TODO: dados pessoais criptografados em repouso e em trânsito]
- [TODO: consentimento explícito antes de coletar dado sensível]
- [TODO: retenção máxima de N dias para logs com PII]

## Qualidade

- Specs e código são commitados juntos — nunca um sem o outro
- Toda feature tem failure modes documentados em `requirements.md` ANTES de ser implementada
- Type check e suite de testes em verde são pré-requisitos de qualquer commit
- Pre-commit hook nunca é pulado com `--no-verify`

## UX

- [TODO: feedback visível em ações > 200ms (loading, skeleton, etc.)]
- [TODO: mensagens de erro acionáveis, nunca códigos crus]
- [TODO: nenhuma ação destrutiva sem confirmação ou undo]
- [TODO: acessibilidade WCAG 2.1 nível AA como linha de base]

## Operação

- [TODO: toda métrica de negócio crítica tem alerta configurado antes do release]
- [TODO: rollback documentado para cada migration de schema]

---

## Como usar este arquivo

1. Ao criar uma feature, leia este arquivo antes de iniciar o Grill
2. Em `security.md`, marque qual princípio aplica e como será garantido
3. Se um princípio precisar ser quebrado, **pare** — abra um ADR descrevendo o motivo, alternativas consideradas e prazo de remediação. Sem ADR, não há quebra
