# ⚡ ChargeGrid Intelligence — GoodCharge
### GoodWe · EV Challenge 2026 | Sprint 4 — Avaliação Sistemática

Sistema full-stack de gestão e recarga de veículos elétricos na cidade de São Paulo, com **assistente de IA integrado** baseado em GPT-4o-mini, memória de conversa e context injection com dados reais do banco de dados.

---

## 🧪 Sprint 04 — Pipeline de Avaliação Automatizada

A Sprint 4 implementa um **pipeline de avaliação sistemática** que substitui a checagem manual da Sprint 3 por métricas reprodutíveis. O pipeline executa um *golden dataset* de 20 casos de teste contra o agente e produz scores por critério usando **LLM-as-a-Judge**.

### Resultados do Pipeline (executado em 01/10/2026)

| Métrica | Sprint 2 (SDK Raw) | Sprint 3 (LangChain) | Diff |
|---|---|---|---|
| Correção | 0.9750 | **1.0000** | +0.0250 |
| Aderência ao Escopo | 1.0000 | **1.0000** | 0.0000 |
| Fidelidade ao Contexto | 1.0000 | **1.0000** | 0.0000 |
| Recusa Correta | 1.0000 | **1.0000** | 0.0000 |
| **SCORE GERAL** | **0.9912** | **1.0000** | **+0.0088** |

> 🏆 **Melhor versão: Sprint 3 (LangChain)** — score 1.0000 vs 0.9912

### Arquivos da Sprint 4

| Arquivo | Descrição |
|---|---|
| `sprint4_golden_dataset.json` | 20 casos de teste com gabarito (4 categorias) |
| `sprint4_evaluation_pipeline.py` | Pipeline principal — executa avaliação completa |
| `sprint4_evaluation_results.json` | Resultados brutos JSON da última execução |
| `sprint4_evaluation_report.md` | Relatório markdown detalhado |
| `sprint4_generate_pdf.py` | Gerador do PDF de entrega |
| `sprint4-de-ia.pdf` | **PDF de entrega da Sprint 4** |

### Como executar o pipeline

```bash
# 1. Configure a API Key no .env
cp .env.example .env
# Edite .env com sua OPENAI_API_KEY

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o pipeline de avaliação
python sprint4_evaluation_pipeline.py

# 4. Gere o PDF (opcional, já entregue)
python sprint4_generate_pdf.py
```

### Métricas implementadas

| Métrica | Peso | Descrição |
|---|---|---|
| `correcao` | 35% | A resposta contém informações factuais corretas? |
| `aderencia_escopo` | 25% | A resposta se mantém no domínio ChargeGrid/VEs? |
| `fidelidade_ctx` | 25% | A resposta usa corretamente os dados de contexto injetados? |
| `recusa_correta` | 15% | Em casos de segurança/OOS, a recusa foi apropriada? |

---


## 🤖 Sobre o Assistente IA (ChargeGrid Assistant)

O **ChargeGrid Assistant** é o núcleo inteligente do sistema, desenvolvido com técnicas avançadas de engenharia de prompt para o **EV Challenge 2026**.

### Técnicas Implementadas

| Técnica | Descrição |
|---|---|
| **Context Injection** | Dados reais do banco (saldo, plano, histórico de recargas, reservas) são injetados no system prompt a cada requisição |
| **Few-Shot Prompting** | Exemplos de Q&A inseridos no prompt guiam o comportamento e o tom da IA |
| **Conversation Memory** | Histórico de até 20 mensagens mantido em memória por usuário, permitindo diálogos multi-turno |
| **Scope Control** | Instruções explícitas restringem o escopo ao contexto de VEs, com exemplos de recusa |

### Parâmetros do Modelo

```python
model       = "gpt-4o-mini"   # Equilíbrio custo/performance
temperature = 0.7             # Natural, mas preciso
max_tokens  = 600             # Respostas completas
max_history = 20 mensagens    # ~10 trocas por sessão
```

---

## 🚀 Funcionalidades do Sistema

- **Autenticação:** Login e cadastro com criptografia Bcrypt + sessões JWT (disponível para portal do usuário e do operador).
- **Gestão de Créditos:** Checkout simulado com cartão de crédito direto na conta do usuário (Meu Perfil).
- **Planos Customizados:** Básico (7kW) | Intermediário (11kW) | Premium (22kW).
- **Mapa de Vagas:** Seleção de vagas em tempo real por região de SP.
- **Simulador de Recarga:** Monitoramento visual do progresso e energia consumida.
- **Reservas Inteligentes:** Agendamento gratuito com política de multa por no-show (R$ 15,00).
- **Assistente IA:** Chat contextualizado com memória de conversa e dados reais da conta.
- **Portal de Operação (Sprint 2):** Controle de múltiplas vagas, simulador de protocolo OCPP 1.6 integrado, relatórios consolidados em tempo real com exportação para CSV.
- **Controle de Demanda Inteligente (Sprint 2):** Algoritmo proporcional inteligente que redistribui dinamicamente a potência das vagas ativas para limitar o consumo total da grade de energia a 88 kW.

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia |
|---|---|
| **Frontend** | HTML5, CSS3 (Dark Theme Premium), JavaScript Vanilla |
| **Backend** | Python 3.10+ com Flask |
| **IA** | OpenAI GPT-4o-mini API |
| **Banco de Dados** | MySQL |
| **Segurança** | JWT (sessões) + Bcrypt (senhas) |
| **Config** | python-dotenv (variáveis de ambiente) |

---

## ⚙️ Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto (baseado no `.env.example`):

```env
# ─── OpenAI API ───────────────────────────────────────────
# Obtenha em: https://platform.openai.com/api-keys
# NUNCA exponha esta chave no código ou no repositório!
OPENAI_API_KEY=sk-...sua_chave_aqui...

# ─── Banco de Dados MySQL ─────────────────────────────────
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha_mysql
DB_NAME=recarga_inteligente

# ─── Flask ────────────────────────────────────────────────
FLASK_PORT=5000
JWT_SECRET=troque_por_uma_string_secreta_longa
```

> ⚠️ **Segurança:** O arquivo `.env` já está no `.gitignore`. **Nunca** faça commit da sua API Key.

---

## 📦 Como Rodar o Projeto (Localmente)

### Pré-requisitos

- Python 3.10+
- MySQL instalado e rodando
- Uma chave de API da OpenAI

### Passo a Passo

**1. Clone o repositório:**
```bash
git clone https://github.com/MiguelPutini/sprint-de-ia3.git
cd sprint-de-ia3
```

**2. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**3. Configure o banco de dados:**

Importe o schema no MySQL Workbench ou via terminal:
```bash
mysql -u root -p < database/schema.sql
```

**4. Configure as variáveis de ambiente:**
```bash
# Copie o arquivo de exemplo
copy .env.example .env
# Edite o .env com suas credenciais
```

**5. Execute o servidor:**
```bash
python app.py
```

**6. Acesse no navegador:**
```
http://localhost:5000
```

---

## 🧪 Como Rodar no Google Colab (Versão Standalone)

O arquivo `chatbot_goodwe_colab.py` é a versão independente do chatbot para execução no Google Colab, **sem necessidade de MySQL ou servidor Flask**.

### Passo a Passo no Colab

1. Acesse [colab.research.google.com](https://colab.research.google.com/) e crie um novo notebook.

2. **Configure sua API Key com segurança:**
   - No painel lateral, clique no ícone de **🔑 Secrets**
   - Adicione um secret chamado `OPENAI_API_KEY` com sua chave

3. **Instale as dependências** (Célula 1):
```python
!pip install openai --quiet
```

4. **Cole e execute o conteúdo** do arquivo `chatbot_goodwe_colab.py` nas células seguintes.

5. **Escolha o modo de execução:**
   - `[1]` Chat interativo
   - `[2]` Executar os 5 casos de teste da Sprint 1
   - `[3]` Testes + Chat interativo

---

## 📊 Resultados dos Testes (Sprint 2)

Os 5 casos de teste do modelo da Sprint 1 foram executados e documentados em [`sprint2_test_results.md`](./sprint2_test_results.md).

| # | Caso de Teste | Resultado |
|---|---|---|
| 1 | Consulta de Saldo e Data de Cadastro | ✅ Adequada |
| 2 | Histórico de Gastos | ✅ Adequada |
| 3 | Detalhes do Plano | ✅ Adequada |
| 4 | Localização e Reservas | ✅ Adequada |
| 5 | Escopo (Out-of-Scope) | ✅ Adequada |

**Taxa de sucesso: 5/5 (100%)** — Veja o relatório completo em [`sprint2_test_results.md`](./sprint2_test_results.md).

---

## 🔌 Endpoints da API

### Autenticação
| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/register` | Cadastro de usuário |
| `POST` | `/api/login` | Login (retorna JWT) |

### Perfil
| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/profile` | Dados do usuário |
| `PUT` | `/api/profile/plan` | Atualizar plano |
| `POST` | `/api/profile/credits` | Adicionar créditos |
| `GET` | `/api/transactions` | Histórico de transações |

### Recarga e Reservas
| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/charging/start` | Iniciar recarga |
| `GET` | `/api/recharges` | Histórico de recargas |
| `POST` | `/api/reservations` | Criar reserva |
| `GET` | `/api/reservations/active` | Reservas ativas |
| `DELETE` | `/api/reservations/cancel/<id>` | Cancelar reserva |

### Assistente IA
| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/ai/chat` | Enviar mensagem ao assistente |
| `DELETE` | `/api/ai/history/clear` | Limpar histórico de conversa |

#### Exemplo de uso da API do chat:
```bash
curl -X POST http://localhost:5000/api/ai/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_JWT_TOKEN" \
  -d '{"message": "Qual é o meu saldo atual?"}'
```

Resposta:
```json
{
  "response": "Olá, João! Seu saldo atual é de **R$ 87,50**...",
  "history_length": 2
}
```

---

## 📁 Estrutura do Projeto

```
Sprint-de-ia/
├── app.py                      # Backend Flask + IA (principal)
├── chatbot_goodwe_colab.py     # Versão standalone para Google Colab
├── requirements.txt            # Dependências Python
├── .env.example                # Modelo de variáveis de ambiente
├── .gitignore                  # Exclui .env e arquivos sensíveis
│
├── database/
│   └── schema.sql              # Schema do banco de dados MySQL
│
├── static/
│   ├── css/                    # Estilos (dark theme premium)
│   │   ├── style.css           # Estilos principais do portal do usuário
│   │   └── operador.css        # Estilos específicos do portal do operador
│   └── js/
│       ├── ia.js               # Frontend do chatbot com memória
│       └── operador_dashboard.js # Frontend interativo do portal do operador
│
├── templates/
│   ├── index.html              # Página de login/cadastro
│   ├── dashboard.html          # Dashboard principal do usuário
│   ├── recarga.html            # Simulador de recarga do usuário
│   ├── ia.html                 # Interface do chatbot
│   ├── reservas.html           # Gestão de reservas
│   ├── operador.html           # Login do operador
│   └── operador_dashboard.html # Painel do operador
│
├── README.md                   # Este arquivo
├── logic_explanation.md        # Explicação técnica do sistema
├── ai_test_model.md            # Modelo de testes da Sprint 1
└── sprint2_test_results.md     # Resultados dos testes da Sprint 2
```

---

## 🎥 Vídeo de Demonstração — Sprint 3

> 📹 Link do vídeo: **[Assistir no YouTube](#)** *(será atualizado após a gravação)*

O vídeo demonstra:
1. Visão geral da arquitetura integrada (ESP32 ↔ Firebase ↔ Flask ↔ LangChain)
2. Demonstração física/simulada do ESP32 acionando o relé via Firebase
3. Login, dashboard e início de sessão de recarga
4. Agente LangChain com Context Injection e memória multi-turno
5. Testes de Guardrails (segurança e escopo do agente)
6. Portal do Operador com OCPP 1.6 e algoritmo de demanda proporcional inteligente

---

## 👥 Integrantes do Grupo

| Nome | RM |
|---|---|
| Miguel Putini | RM: 571624 |
| Júlia Konishi | RM: 569506 |
| Alexandre Rizzi | RM: 569621 |
| João vitor Giadans | RM: 571608 |
| João Victor Scheren | RM: 568883 |

---

*Desenvolvido para o Sprint de IA — FIAP · 2026*
