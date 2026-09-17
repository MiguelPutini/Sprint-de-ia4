# -*- coding: utf-8 -*-
"""
╔==============================================================================╗
║         CHATBOT GOODWE - ChargeGrid Assistant | EV Challenge 2026          ║
║         Sprint 2 - Implementação com Histórico e Few-Shot Prompting         ║
╚==============================================================================╝

Este arquivo é a versão standalone do chatbot para execução no Google Colab.
A versão completa com interface web está no repositório principal (app.py).

COMO USAR NO GOOGLE COLAB:
  1. Acesse: https://colab.research.google.com/
  2. Crie um novo notebook.
  3. Execute as células na ordem indicada (CÉLULA 1, CÉLULA 2, etc.)
  4. Configure a API Key em: Painel lateral → Secrets → OPENAI_API_KEY

SEGURANÇA:
  - Nunca cole sua API Key diretamente no código.
  - Use SEMPRE os Secrets do Colab (ícone de chave no painel lateral).
"""

# ============================================================================
# CÉLULA 1 - Instalação de Dependências
# ============================================================================
# Cole este bloco na primeira célula do Colab e execute:
# !pip install openai langchain langchain-openai python-dotenv --quiet
# ============================================================================
# CÉLULA 2 - Importações e Configuração da API Key via Secrets
# ============================================================================

import os
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

# -- Carrega a API Key com segurança ------------------------------------------
# No Google Colab: acesse o ícone de chave no painel lateral → Secrets
# Crie um secret chamado "OPENAI_API_KEY" com sua chave.
try:
    from google.colab import userdata
    OPENAI_API_KEY = userdata.get('OPENAI_API_KEY')
    print("✅ API Key carregada via Google Colab Secrets.")
except ImportError:
    # Fallback para execução local (usa variável de ambiente)
    from dotenv import load_dotenv
    load_dotenv(override=True)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if OPENAI_API_KEY:
        print("✅ API Key carregada via variável de ambiente.")
    else:
        raise ValueError(
            "❌ OPENAI_API_KEY não encontrada!\n"
            "No Colab: adicione em Secrets → 'OPENAI_API_KEY'.\n"
            "Localmente: defina a variável de ambiente OPENAI_API_KEY."
        )

# Define a API Key nas variáveis de ambiente para o LangChain
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

print("🚀 Dependências carregadas com sucesso!")

# ============================================================================
# CÉLULA 3 - Definição do System Prompt (Contexto GoodWe / ChargeGrid)
# ============================================================================

def build_system_prompt(user_name: str = "Usuário") -> str:
    """
    Constrói o system prompt com contexto completo do projeto GoodWe.
    
    Técnicas utilizadas:
    - Context Injection: dados do usuário injetados no prompt
    - Few-Shot Prompting: exemplos de Q&A para guiar o comportamento
    - Scope Control: restrições explícitas de escopo
    """
    return f"""Você é o **Goole**, o assistente inteligente da plataforma de \
Recarga de Veículos Elétricos da GoodWe - desenvolvido para o EV Challenge 2026.

Sua missão é auxiliar usuários a gerenciar suas recargas de VEs na cidade de \
São Paulo de forma eficiente, sustentável e personalizada.

=======================================================
📋 DIRETRIZES DE COMPORTAMENTO (REGRAS RÍGIDAS):
=======================================================
1. Sempre se dirija ao usuário pelo nome: **{user_name}**.
2. Responda APENAS sobre: recargas de VEs, saldo, planos, reservas, \
sustentabilidade e tecnologia de carregamento elétrico.
3. Se perguntado sobre temas externos (esportes, política, culinária, etc.), \
recuse SEMPRE educadamente e redirecione ao contexto de VEs.
4. Nunca invente dados. Se não souber, diga que não tem a informação.
5. Formate respostas com Markdown: **negrito**, listas com -.
6. Seja conciso, objetivo e profissional.

=======================================================
ℹ️ INFORMAÇÕES DO SISTEMA ChargeGrid (GoodWe):
=======================================================
- Rede de carregadores em: Zona Sul, Leste, Oeste e Norte de São Paulo.
- Tarifa padrão: R$ 1,80 por kWh.
- Reserva de vaga: Totalmente gratuita.
- Cancelamento: Gratuito a qualquer momento antes do horário agendado.
- Multa por No-Show: R$ 15,00 (se o usuário não comparecer sem cancelar).
- Planos disponíveis:
  * Básico: 7 kW (R$ 0/mês - padrão)
  * Intermediário: 11 kW
  * Premium: 22 kW
- Tecnologia: Carregadores trifásicos 380V / 32A (~21,4 kW máx. físico).
- Projeto alinhado ao EV Challenge 2026 da GoodWe.

=======================================================
💡 EXEMPLOS DE RESPOSTAS (Few-Shot Prompting):
=======================================================
Exemplo 1:
  Usuário: "Qual é a tarifa de recarga?"
  Assistente: "Olá, **{user_name}**! A tarifa do ChargeGrid é de **R$ 1,80 por kWh**. \
Por exemplo, uma recarga de 30 minutos no plano Básico (7kW) custaria \
aproximadamente **R$ 6,30** (3,5 kWh × R$ 1,80). Posso ajudar com mais alguma coisa?"

Exemplo 2:
  Usuário: "Quem ganhou a Copa do Mundo?"
  Assistente: "Desculpe, **{user_name}**, mas meu escopo é exclusivamente o sistema \
ChargeGrid de recargas de VEs. Não tenho acesso a informações sobre \
eventos esportivos. Posso te ajudar a verificar seu saldo, planos disponíveis \
ou como reservar uma vaga de recarga?"

Exemplo 3:
  Usuário: "Como faço para não pagar a multa de no-show?"
  Assistente: "Ótima pergunta, **{user_name}**! Para evitar a multa de **R$ 15,00**, \
basta cancelar sua reserva antes do horário agendado. O cancelamento é \
**totalmente gratuito** e pode ser feito a qualquer momento pela aba \
'Minhas Reservas' na plataforma. A multa só é aplicada quando a reserva \
não é cancelada e o usuário não comparece."
"""


# ============================================================================
# CÉLULA 4 - Classe do Chatbot com Gerenciamento de Histórico
# ============================================================================

class ChargeGridChatbot:
    """
    Chatbot ChargeGrid com memória de conversa (histórico de mensagens) via LangChain.
    
    Implementa:
    - Gerenciamento de histórico de mensagens via RunnableWithMessageHistory
    - System prompt com contexto GoodWe + few-shot prompting
    - Controle de escopo (rejeita perguntas fora do tema)
    """
    
    def __init__(self, user_name: str = "Usuário", session_id: str = "default_session"):
        self.user_name = user_name
        self.session_id = session_id
        self.system_prompt = build_system_prompt(user_name)
        self.store = {}

        # Configurações do Agente LangChain
        self.chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, max_tokens=600)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_prompt}"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}")
        ])
        self.chain = self.prompt | self.chat_model
        self.agent_with_history = RunnableWithMessageHistory(
            self.chain,
            self.get_session_history,
            input_messages_key="question",
            history_messages_key="history",
        )
        
        print(f"\n{'='*60}")
        print(f"  🤖 ChargeGrid Assistant Iniciado (LangChain Agent)")
        print(f"  👤 Usuário: {user_name}")
        print(f"  📡 Modelo: gpt-4o-mini (temperatura: 0.7)")
        print(f"{'='*60}")
        print("  Digite sua pergunta e pressione Enter.")
        print("  Comandos: 'sair' para encerrar | 'limpar' para resetar histórico")
        print(f"{'='*60}\n")

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]

    def chat(self, user_message: str) -> str:
        """
        Envia uma mensagem e retorna a resposta da IA.
        Mantém o histórico de conversa automaticamente via LangChain.
        """
        try:
            response = self.agent_with_history.invoke(
                {"system_prompt": self.system_prompt, "question": user_message},
                config={"configurable": {"session_id": self.session_id}}
            )
            
            return response.content
            
        except Exception as e:
            error_msg = f"❌ Erro ao chamar a API: {type(e).__name__}: {e}"
            print(f"[ERROR] {error_msg}")
            return error_msg

    def clear_history(self):
        """Limpa o histórico de conversa (inicia nova sessão)."""
        count = 0
        if self.session_id in self.store:
            count = len(self.store[self.session_id].messages)
            self.store[self.session_id].clear()
        print(f"🗑️ Histórico limpo. {count} mensagens removidas. Nova sessão iniciada.")

    def show_history(self):
        """Exibe o histórico de conversa formatado."""
        if self.session_id not in self.store or not self.store[self.session_id].messages:
            print("📭 Histórico vazio - nenhuma conversa registrada.")
            return
        
        history = self.store[self.session_id].messages
        print(f"\n{'-'*50}")
        print(f"📜 HISTÓRICO DE CONVERSA ({len(history)} mensagens):")
        print(f"{'-'*50}")
        for i, msg in enumerate(history, 1):
            role = "👤 Você" if msg.type == "human" else "🤖 IA"
            print(f"\n[{i}] {role}:\n{msg.content[:200]}{'...' if len(msg.content) > 200 else ''}")
        print(f"{'-'*50}\n")

    def run_interactive(self):
        """Inicia o loop interativo de conversa."""
        print("💬 Iniciando modo interativo...\n")
        
        while True:
            try:
                user_input = input("Você: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n\n👋 Encerrando chatbot. Até logo!")
                break
            
            if not user_input:
                continue
            
            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("\n👋 Encerrando chatbot. Até logo!")
                break
            
            if user_input.lower() in ['limpar', 'clear', 'reset']:
                self.clear_history()
                continue
            
            if user_input.lower() in ['historico', 'histórico', 'history']:
                self.show_history()
                continue
            
            print("\n🤖 ChargeGrid Assistant:", end=" ")
            response = self.chat(user_input)
            print(response)
            
            history_len = len(self.store[self.session_id].messages) if self.session_id in self.store else 0
            print(f"\n[🧠 Memória: {history_len//2} trocas]\n")


# ============================================================================
# CÉLULA 5 - Execução dos 5 Casos de Teste (Sprint 1)
# ============================================================================

def run_test_suite():
    """
    Executa os 5 casos de teste definidos no ai_test_model.md da Sprint 1.
    Registra pergunta, resposta e avaliação qualitativa.
    """
    print("\n" + "="*65)
    print("  🧪 MODELO DE TESTE - ChargeGrid Assistant (Sprint 2)")
    print("  Baseado no modelo de testes da Sprint 1")
    print("="*65 + "\n")
    
    # Cria instância de teste com dados simulados (sem banco de dados)
    test_bot = ChargeGridChatbot(user_name="João Silva")
    
    # -- Injetar dados simulados no system prompt para testes --------------
    test_bot.system_prompt = build_system_prompt("João Silva") + """

=======================================================
📊 DADOS SIMULADOS PARA TESTE (sem banco de dados):
=======================================================
- 💰 Saldo Atual: R$ 87,50
- 📅 Membro desde: 15/03/2025
- ⚡ Plano Ativo: Intermediário (11kW)
- 💸 Total Gasto em Recargas: R$ 142,20
- 🌱 Energia Consumida: 78,99 kWh
- 🔌 Total de Sessões: 12

ÚLTIMAS RECARGAS:
- Shopping Interlagos (Zona Sul), Vaga A2, 11 kWh, R$ 19,80 - 05/06/2025
- Metrô Jabaquara (Zona Sul), Vaga B1, 5,5 kWh, R$ 9,90 - 01/06/2025
- Shopping Aricanduva (Zona Leste), Vaga A3, 7,33 kWh, R$ 13,20 - 28/05/2025

RESERVAS RECENTES:
- Shopping Iguatemi (Zona Oeste), Vaga B2, status: ativa - 10/06/2025 14:00
"""
    
    # -- Definição dos casos de teste --------------------------------------
    test_cases = [
        {
            "id": 1,
            "nome": "Consulta de Saldo e Data de Cadastro",
            "pergunta": "Olá! Qual é o meu saldo atual e quando eu me cadastrei?"
        },
        {
            "id": 2,
            "nome": "Histórico de Gastos",
            "pergunta": "Quanto eu já gastei no total com recargas até agora?"
        },
        {
            "id": 3,
            "nome": "Detalhes do Plano",
            "pergunta": "Qual é o meu plano atual e qual a potência máxima que posso usar?"
        },
        {
            "id": 4,
            "nome": "Localização e Reservas",
            "pergunta": "Onde foram minhas últimas recargas e eu tenho alguma reserva recente?"
        },
        {
            "id": 5,
            "nome": "Teste de Escopo (Out-of-Scope)",
            "pergunta": "Quem ganhou o jogo de futebol ontem à noite?"
        }
    ]
    
    results = []
    
    for tc in test_cases:
        print(f"{'-'*65}")
        print(f"📋 CASO DE TESTE {tc['id']}: {tc['nome']}")
        print(f"{'-'*65}")
        print(f"❓ Pergunta: {tc['pergunta']}")
        print(f"\n🤖 Resposta da IA:")
        
        response = test_bot.chat(tc['pergunta'])
        print(response)
        
        # Avaliação manual (o usuário deve preencher após ver a resposta)
        print(f"\n📊 Avaliação: [adequada / parcialmente adequada / inadequada]")
        print(f"   (Registre manualmente no relatório de testes)")
        
        results.append({
            "caso": tc['id'],
            "nome": tc['nome'],
            "pergunta": tc['pergunta'],
            "resposta": response
        })
        
        print()
    
    print("="*65)
    print("✅ Todos os 5 casos de teste executados com sucesso!")
    print("📝 Documente as avaliações no arquivo: sprint2_test_results.md")
    print("="*65)
    
    return results


# ============================================================================
# CÉLULA 6 - Ponto de Entrada Principal
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*65)
    print("  🔋 ChargeGrid Assistant - GoodWe EV Challenge 2026")
    print("  Sprint 2: Chatbot com Memória e Few-Shot Prompting")
    print("="*65)
    
    print("\nEscolha o modo de execução:")
    print("  [1] Chat interativo")
    print("  [2] Executar suite de testes (Sprint 1)")
    print("  [3] Ambos (testes primeiro, depois chat)")
    
    try:
        choice = input("\nOpção (1/2/3): ").strip()
    except (EOFError, KeyboardInterrupt):
        choice = "1"
    
    if choice == "2":
        run_test_suite()
    elif choice == "3":
        run_test_suite()
        print("\n" + "="*65)
        print("Iniciando modo interativo...")
        print("="*65 + "\n")
        nome = input("Digite seu nome para personalizar a experiência: ").strip() or "Usuário"
        bot = ChargeGridChatbot(user_name=nome)
        bot.run_interactive()
    else:
        # Padrão: chat interativo
        nome = input("Digite seu nome para personalizar a experiência: ").strip() or "Usuário"
        bot = ChargeGridChatbot(user_name=nome)
        bot.run_interactive()
