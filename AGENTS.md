# AGENTS.md

## Papel do repositório

Este repositório é um guia e kit de templates para Spec-Driven Secure Development (SDSD). Não é uma aplicação e não contém backend, autenticação, pagamentos ou domínio de produto.

## Regras

- Mantenha o conteúdo normativo em português; documentação pública pode ter edição inglesa, que deve permanecer semanticamente alinhada.
- Trate `GUIA-SDSD.md` e `templates/` como contrato público: mudanças no guia devem refletir nos templates.
- Decisões deste kit ficam em `.harness/adr/`; decisões de um projeto consumidor ficam em `specs/adr/`.
- Valide documentação com `python scripts/validate_docs.py` antes de abrir um PR.
- Não introduza exemplos de produto fictício como se fossem capacidades do kit.
