# Relatório de Evolução — Sprint 03: Arquitetura de Agentes de IA
**Projeto:** ChargeGrid (GoodWe EV Challenge 2026)

## 7.1 Resumo da Evolução (Sprints 1 e 2 ➔ Sprint 03)
Nas Sprints 1 e 2, o chatbot foi implementado como uma prova de conceito funcional, gerenciando a memória por meio de arrays de dicionários controlados manualmente pelo desenvolvedor na aplicação backend (`app.py`), além de chamadas cruas e diretas ao SDK oficial da OpenAI. 

Na Sprint 03, esse paradigma foi completamente refatorado para o uso de uma **Arquitetura de Agentes**, utilizando o framework **LangChain**. O LangChain agora orquestra o diálogo atuando não apenas como um canal de mensageria, mas empacotando o histórico de conversa em uma estrutura robusta via `RunnableWithMessageHistory`. Adicionalmente, foram introduzidos testes explícitos de segurança e Guardrails, garantindo que o Agente não atue fora de seu contexto funcional.

## 7.2 Refatoração e Decisões Técnicas
A principal decisão técnica tomada nesta migração foi a escolha do framework LangChain em vez de CrewAI ou LangGraph.
- **Motivação:** Para um sistema de perguntas e respostas contextual focado no usuário (Single-Agent/Chatbot de serviço), o LangChain oferece os componentes exatos (`ChatPromptTemplate`, `ChatMessageHistory`) com a complexidade certa, sem sobrecarga.
- **Implementação:** Substituímos a injeção manual da lista de dicionários no payload do modelo por um `agent_with_history`, configurável através do `session_id`.
- **Trade-offs:** O LangChain adiciona uma abstração substancial (cadeias com sintaxe `prompt | model`), o que exige que a equipe conheça seus tipos de dados internos (BaseChatMessageHistory, Runnable), diferentemente da simplicidade pura de chamar a API da OpenAI de forma RESTful. O tempo de setup aumentou, mas o ganho em manutenção e escalabilidade compensa.

## 7.3 Comparativo Antes × Depois

| Critério | Sprints 1 e 2 (Arquitetura Legada) | Sprint 03 (Agentes via LangChain) |
| :--- | :--- | :--- |
| **Framework Utilizado** | SDK Raw da OpenAI (`openai` lib) | Agente LangChain (`langchain-openai`) |
| **Gerenciamento de Memória** | Array em memória `conversation_history = defaultdict(list)` (Corte via slicing do Python) | Abstração `RunnableWithMessageHistory` vinculada a um session state interno. |
| **Escopo e Guardrails** | Controlados vagamente apenas pelo System Prompt | Validação e aprovação explícitas com testes automatizados de segurança (Prompt Injection/Riscos) |
| **Experimentação e Modelos** | Hardcoded no `app.py` (`gpt-4o-mini`) | Setup configurado para alternância e comparação paramétrica fácil. |

**Ganhos com a nova arquitetura:**
A nova arquitetura abstraiu a complexidade de controlar o histórico. Anteriormente, era necessário limpar mensagens com base em limites fixos de caracteres ou listas. O LangChain lida com a estrutura das "Messages" organicamente, facilitando a adição futura de ferramentas externas (Tool Calling), já que a espinha dorsal baseada em Agente já está montada.

## 7.4 Problemas Encontrados e Soluções

1. **Problema com Encoding ao Rodar Testes de Segurança**
   - *Problema:* Ocorreram erros de `SyntaxError` ao carregar prompts e scripts via terminal por conta de caracteres unicode nos arquivos Python do chatbot (ex: `═`, emojis).
   - *Alternativas:* Poderíamos tentar converter todos os arquivos para ANSI e remover todos os emojis e decorações ASCII, ou forçar o encoding padrão de leitura do Python.
   - *Solução Adotada:* Utilizar scripts auxiliares para remover caracteres de formatação ASCII complexos e inserir `# -*- coding: utf-8 -*-` nos scripts. Além disso, executar o ambiente de teste definindo a variável `PYTHONIOENCODING=utf-8`.
   - *Justificativa:* O ecossistema Windows exige atenção especial com unicode. Essa solução manteve a integridade do código fonte enquanto contornou as limitações do terminal local.

2. **Permissões Negadas para Comparação de Diferentes Modelos**
   - *Problema:* O projeto vinculado à chave API atual gerava erro HTTP 403 `model_not_found` ao tentar instanciar o `gpt-3.5-turbo` ou `gpt-4o`.
   - *Alternativas:* Usar chaves externas, adicionar fundos, ou comparar o mesmo modelo mudando parâmetros do hiper-espaço de geração de linguagem.
   - *Solução Adotada:* O teste de comparação de modelos foi feito mantendo-se o provedor e modelo (`gpt-4o-mini`), e alternando radicalmente o parâmetro `temperature` (0.2 vs 0.8) em instâncias separadas para atestar o funcionamento do comparador LangChain.
   - *Justificativa:* Cumpriu o requisito de validar que a plataforma suporta flexibilidade nas LLMs geradas, gerando insumos de análise suficientes sem exigir a aquisição de novos créditos da OpenAI.

## 7.5 Divisão da Equipe

- **Miguel Putini (RM:571624)**: Refatoração do `app.py` para LangChain e arquitetura do `RunnableWithMessageHistory`.
- **Alexandre Rizzi (RM:569621)**: Desenvolvimento dos Testes de Segurança de Agente (`testes_seguranca_agente.py`) e testes de injeção de prompt.
- **Júlia Konishi (RM:569506)**: Análise comparativa entre LLMs e compilação dos relatórios técnicos (`relatorio_modelos.md`).
- **João Victor Scheren (RM:568883)**: Análise comparativa entre LLMs e compilação dos relatórios técnicos (`relatorio_modelos.md`).
- **João Vitor Giadans (RM:571608)**: Análise comparativa entre LLMs e compilação dos relatórios técnicos (`relatorio_modelos.md`).
