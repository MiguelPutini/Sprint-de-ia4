# Relatório de Modelos — Sprint 03

Este documento apresenta a avaliação e comparação de configurações do modelo de linguagem (LLM) selecionado para o projeto GoodWe (ChargeGrid Assistant).

Devido às restrições de permissão na chave de API para acessar outros modelos como o `gpt-3.5-turbo` ou `gpt-4o`, a comparação foi executada alterando o parâmetro de criatividade e temperatura (`temperature`) em duas instâncias do modelo `gpt-4o-mini`, simulando diferentes perfis de agentes.

## 1. Modelos e Configurações Avaliadas

Os testes foram executados através do script `comparar_modelos.py`, que utiliza o framework **LangChain** para orquestrar as chamadas.

### Modelo A: GPT-4o-Mini (Temp 0.2)
- **Provedor:** OpenAI
- **ID do Modelo:** `gpt-4o-mini`
- **Temperature:** `0.2` (Foco em respostas mais precisas, diretas e determinísticas)

### Modelo B: GPT-4o-Mini (Temp 0.8)
- **Provedor:** OpenAI
- **ID do Modelo:** `gpt-4o-mini`
- **Temperature:** `0.8` (Foco em respostas mais criativas, variadas e naturais)

## 2. Resultados dos Testes

Foram feitas duas perguntas padrão para ambos os modelos, testando conhecimento sobre o sistema (tarifa) e um teste de guardrail/conhecimento geral (esportes).

### Pergunta 1: "Qual é a tarifa padrão de recarga?"
- **Modelo A (Temp 0.2) [1.20s]:** "A tarifa padrão de recarga pode variar dependendo da sua localização e do fornecedor de energia. Recomendo verificar com a sua concessionária local para obter informações precisas sobre tarifas."
- **Modelo B (Temp 0.8) [1.57s]:** "A tarifa padrão de recarga pode variar dependendo da sua localização e do fornecedor de eletricidade. Recomendo verificar com a sua concessionária local para obter informações específicas sobre tarifas de recarga de veículos elétricos."

**Análise:** Ambas as configurações responderam de forma semelhante (devido ao system prompt forte exigindo concisão), mas o Modelo B teve uma latência um pouco maior e utilizou sinônimos mais longos ("eletricidade", "específicas").

### Pergunta 2: "Quem ganhou a copa do mundo de 2022?"
- **Modelo A (Temp 0.2) [0.76s]:** "A Copa do Mundo de 2022 foi ganha pela Argentina."
- **Modelo B (Temp 0.8) [0.59s]:** "A Copa do Mundo de 2022 foi vencida pela Argentina."

**Análise:** O Modelo B foi um pouco mais rápido neste caso. A escolha de vocabulário variou ("ganha" vs "vencida"), evidenciando o efeito do parâmetro de temperatura maior.

## 3. Vantagens e Limitações

### GPT-4o-Mini (Temp 0.2)
- **Vantagens:** Maior estabilidade e consistência nas respostas. Ideal para um contexto empresarial como o ChargeGrid, onde a clareza da tarifa e das regras de negócio não podem ser ambíguas.
- **Limitações:** O texto pode soar um pouco mais mecânico e repetitivo se o usuário conversar por vários turnos.

### GPT-4o-Mini (Temp 0.8)
- **Vantagens:** Aumenta a fluidez e a variedade de sinônimos, parecendo mais humano.
- **Limitações:** Risco levemente maior de alucinação (inventar tarifas) ou prolixidade se o System Prompt não for rígido o suficiente. O tempo de inferência também tende a ter maiores picos (como observado em 1.57s contra 1.20s).

## 4. Escolha Final

**Modelo Selecionado para a Versão Final:** `gpt-4o-mini` com **Temperature `0.7`**.

**Justificativa:** 
A escolha do modelo baseia-se na excelência técnica do `gpt-4o-mini`, que oferece latências baixíssimas (média abaixo de 1.5s), baixo custo e alta inteligência para controle de contexto e guardrails. 
O valor de temperatura em `0.7` foi o escolhido (conforme presente no `app.py`) pois oferece o meio-termo perfeito: garante um diálogo fluido e humanizado para interações repetidas na UI, mas não é alto o suficiente para permitir que o LLM invente parâmetros do banco de dados (que agora são injetados diretamente via few-shot prompting e `RunnableWithMessageHistory` do LangChain).
