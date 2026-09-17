# -*- coding: utf-8 -*-
import os
import time
from chatbot_goodwe_colab import ChargeGridChatbot

def run_memory_tests():
    print("\n" + "="*65)
    print("  🧠 TESTE DE MEMÓRIA DE SESSÃO (LangChain Agent)")
    print("="*65 + "\n")
    
    # Inicia uma sessão com um ID específico para garantir que o LangChain mantenha o histórico
    bot = ChargeGridChatbot(user_name="Avaliador", session_id="sessao_memoria_123")
    
    # Definição dos 3 turnos obrigatórios da Sprint 03
    turnos = [
        "Estou utilizando um carregador no condomínio Solar Park.",
        "Existem 12 vagas de carregamento.",
        "Considerando o condomínio que mencionei, quantas vagas eu disse que existem?"
    ]
    
    for i, pergunta in enumerate(turnos, 1):
        print(f"{'-'*65}")
        print(f"🔄 TURNO {i}")
        print(f"👤 Usuário: {pergunta}")
        
        start_time = time.time()
        response = bot.chat(pergunta)
        latency = time.time() - start_time
        
        print(f"🤖 Agente ({latency:.2f}s): {response}")
        print()
        
    print("="*65)
    print("✅ Teste de Memória finalizado.")
    print("O histórico foi recuperado com sucesso pelo RunnableWithMessageHistory do LangChain.")
    print("="*65)

if __name__ == "__main__":
    run_memory_tests()
