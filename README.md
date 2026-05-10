# Spec-Driven Secure Development (SDSD)

Bem-vindo ao repositório de **Spec-Driven Secure Development (SDSD)**, um guia prático e opinativo para times que constroem software moderno integrando Agentes de IA, segurança nativa e excelência técnica.

## 🧠 O que é SDSD?

SDSD é um fluxo de trabalho onde **toda funcionalidade começa com especificações rigorosas escritas ANTES do código**. Em vez de usar "prompts soltos" ou tratar a Inteligência Artificial como um adivinho de ideias vagas, a IA é usada para materializar e codificar especificações formais, mantendo o humano estritamente no controle da direção do produto, da arquitetura e da qualidade final (UX).

O princípio central da metodologia é a inversão de controle tradicional: **A especificação é a verdadeira fonte da verdade e o código é apenas um subproduto (muitas vezes descartável).**

## 💡 Por que usar?

- **Fim da "Caixa Preta" da IA:** O código gerado deixa de ser um "código alienígena". Você sabe exatamente *por que* algo foi construído, pois a decisão e os requisitos arquiteturais estão documentados nas specs.
- **Lógica e Testes Agnósticos:** Para lógica de negócio complexa, nós adotamos a filosofia de "Bibliotecas Sem Código". O comportamento do sistema é amarrado por testes puros de input/output (`test-cases.yaml`). A IA itera o código da linguagem escolhida até a matemática fechar.
- **Segurança Shift-Left Nativa:** Modelagem de ameaças e tratamento de exceções (*Failure modes*) não são pensados após a codificação, mas planejados e documentados na base da *feature*.
- **Orquestração Híbrida Inteligente:** A quebra de tarefas classifica o esforço de implementação em duas vias de responsabilidade — o que a IA executa sozinha sem supervisão (`[AFK]`) e o que necessita de interrupção com revisão humana explícita a cada passo (`[HITL]`).
- **Redução da Carga Cognitiva e Repetição:** As próprias especificações geram um "prompt encapsulado" (`EXECUTE.md`), restando ao humano apenas dar o play no Agente.

## 🚀 Como Funciona o Fluxo (Resumo)

O workflow completo, incluindo a resolução de dívida técnica em projetos legados, é destrinchado no [Guia Completo de SDSD](GUIA-SDSD.md). Abaixo estão as etapas principais:

1. **A Constituição do Projeto:**
   O projeto se inicia estabelecendo a fundação da engenharia:
   - `mission.md`: Qual é o problema a ser resolvido e o que define sucesso.
   - `tech-stack.md`: As escolhas de arquitetura, frameworks e esteira de verificação (SAST, SCA, Secrets).
   - `roadmap.md`: O agrupamento das entregas em fases independentes.
   - `STATE.md`: Um log de contexto ativo para manter a memória persistente dos agentes entre as sessões.

2. **O Grill de Especificação:**
   O humano não perde horas montando especificações enormes. Aciona-se um *Master Prompt* para que o Agente IA conduza uma rigorosa entrevista ("Sessão de Grill"). Com perguntas granulares, resolvem-se ambiguidades arquitetônicas.

3. **Geração das Especificações Executáveis:**
   O Agente cria a pasta com o artefato da *Feature* contendo `requirements.md`, fatias de execução verticalizadas (`plan.md`), checklist de UX focado no avaliador humano (`QA_CHECKLIST.md`), vetores de ataque (`security.md`) e os casos de teste.

4. **Implementação Autônoma via "Botão de Play":**
   Junto aos artefatos, um arquivo `EXECUTE.md` é gerado contendo o prompt definitivo daquela *feature*. Você insere no chat do seu Agente e ele consome a documentação técnica para construir os testes, banco e interface no repositório final.

5. **Acompanhamento Tático:**
   Durante o *loop* de código, o humano verifica a qualidade intervindo nas fatias delimitadas e acionando as auditorias de dependência. Ao fim, um changelog rastreável documenta o final do ciclo de trabalho.

## 📖 Documentação Completa

Para aprofundar na estruturação de prompts, fluxos de prevenção contra problemas de arquitetura comuns gerados por agentes (N+1, Memory Leaks e Race Conditions) e setup de testes, consulte o guia oficial:

👉 **[LEIA O GUIA TÉCNICO COMPLETO AQUI (GUIA-SDSD.md)](GUIA-SDSD.md)**

---
*"Escreva boas especificações. Deixe a IA cuidar da digitação."*
