# Checklist de Revisão de IA (AI Review Checklist)

Esta checklist é utilizada por agentes de IA (e humanos) para validar a qualidade, conformidade e segurança do código ou das especificações antes de serem mesclados ou implantados.

## Geral:
- [ ] A implementação está em conformidade com a especificação (`specs/requirements.md`)?
- [ ] Todos os critérios de validação (`specs/validation.md`) foram atendidos?
- [ ] Os princípios do projeto (`principles.md`) foram respeitados?
- [ ] O código é legível, claro e bem estruturado?
- [ ] Foram adicionados ou atualizados testes unitários/de integração relevantes?
- [ ] A documentação (interna e externa) foi atualizada, se necessário?

## Segurança:
- [ ] Foram considerados os riscos de segurança identificados em (`specs/security.md`)?
- [ ] O código está livre das vulnerabilidades comuns da OWASP Top 10 (Injeção, XSS, Autenticação Quebrada, etc.)?
- [ ] Nenhuma credencial, chave ou segredo está hardcoded ou exposto no código ou logs?
- [ ] A validação de entrada está robusta contra ataques (SQL Injection, XSS, etc.)?
- [ ] As permissões e controles de acesso estão corretamente implementados?
- [ ] As dependências de terceiros foram verificadas quanto a vulnerabilidades conhecidas (SCA)?

## Performance e Escalabilidade:
- [ ] O código evita gargalos de desempenho conhecidos (ex: N+1 queries)?
- [ ] O tratamento de erros e a resiliência estão adequadamente implementados?
- [ ] O uso de recursos (memória, CPU) é otimizado?

## Boas Práticas e Padrões:
- [ ] Os padrões de implementação aprovados (`.harness/patterns/`) foram seguidos?
- [ ] O glossário de domínio (`.harness/domain-glossary.md`) foi consultado para terminologia?
- [ ] Decisões arquiteturais relevantes foram documentadas em ADRs (`.harness/adr/`)?

## Observações para IAs:
- Fornecer feedback específico com referências a linhas de código ou seções da especificação.
- Sugerir melhorias e correções diretamente.
- Em caso de dúvidas, pedir esclarecimento ao humano responsável (`[HITL]`).