# -*- coding: utf-8 -*-
import os
import time
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

try:
    from google.colab import userdata
    OPENAI_API_KEY = userdata.get('OPENAI_API_KEY')
except ImportError:
    from dotenv import load_dotenv
    load_dotenv(override=True)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def run_comparison():
    print("\n" + "="*65)
    print("  🧪 COMPARAÇÃO DE MODELOS (LangChain)")
    print("="*65 + "\n")
    
    system_prompt = """Você é o Goole, assistente de recarga de VEs da GoodWe.
Responda de forma concisa e direta."""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])
    
    models = [
        {"name": "GPT-4o-Mini (Temp 0.2)", "model_id": "gpt-4o-mini", "temp": 0.2},
        {"name": "GPT-4o-Mini (Temp 0.8)", "model_id": "gpt-4o-mini", "temp": 0.8}
    ]
    
    test_questions = [
        "Qual é a tarifa padrão de recarga?",
        "Quem ganhou a copa do mundo de 2022?"
    ]
    
    for model_info in models:
        print(f"\n🚀 Testando Modelo: {model_info['name']} ({model_info['model_id']})")
        print(f"🌡️ Temperature: {model_info['temp']}")
        
        chat_model = ChatOpenAI(model=model_info['model_id'], temperature=model_info['temp'])
        chain = prompt | chat_model
        
        for q in test_questions:
            print(f"  ❓ Pergunta: {q}")
            
            start_time = time.time()
            response = chain.invoke({"question": q})
            latency = time.time() - start_time
            
            print(f"  🤖 Resposta ({latency:.2f}s): {response.content.strip()}")
            print("-" * 50)

if __name__ == "__main__":
    run_comparison()
