# Limites e Restrições do Kit

Este documento descreve os limites do repositório `spec-driven-secure-development`, que é um guia e kit de templates. Ele não é uma aplicação nem executa agentes, gera código ou gerencia infraestrutura por conta própria.

## O Sistema PODE Fazer:
- Oferecer orientação e templates para gerar código baseado em especificações.
- Fornecer checklists e perfis de agentes para revisão humana ou automatizada no projeto consumidor.
- Fornecer exemplos de workflows e validação documental.
- Organizar decisões e contexto deste kit em `.harness/`.
- Definir uma estrutura para especificações de features no projeto consumidor.

## O Sistema NÃO PODE Fazer:
- Executar ou hospedar agentes, aplicações, testes ou pipelines de um projeto consumidor.
- Tomar decisões arquiteturais críticas sem validação humana.
- Criar especificações de produto sem diretrizes claras ou "grill sessions" com humanos.
- Garantir 100% de segurança contra todas as ameaças.
- Substituir a supervisão e o julgamento humano em fases críticas.

## Restrições Importantes:
- **Contrato público:** mudanças no guia devem refletir nos templates ou ser justificadas.
- **Clareza:** exemplos devem identificar se são metodologia, template ou configuração deste kit.
- **Segurança:** ferramentas, versões e limites da esteira devem estar documentados.
- **Manutenibilidade:** documentação e templates devem ser verificáveis por `scripts/validate_docs.py`.