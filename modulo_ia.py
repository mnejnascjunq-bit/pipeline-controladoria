# =====================================================================
# LEGALSHIELD ANALYTICS - MÓDULO DE INTELIGÊNCIA ARTIFICIAL (FASE 4)
# Desenvolvido por: Merecele Nascimento dos Reis
# Objetivo: Realizar triagem cognitiva e retornar dados estritamente em JSON
# Proteção: Credenciais isoladas via arquivo oculto .env e load_dotenv
# =====================================================================

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega a chave de API direto do cofre seguro .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configura o cliente oficial do Google com a sua credencial protegida
genai.configure(api_key=GEMINI_API_KEY)

def analisar_intimacao_com_ia(texto_intimacao):
    """
    Envia o texto simulado da intimação para o Gemini 3.5 Flash Lite
    e retorna a classificação estruturada estritamente em formato JSON.
    """
    if not GEMINI_API_KEY:
        print("❌ Erro: Chave GEMINI_API_KEY não encontrada no arquivo .env!")
        return "Erro de Credencial"

    try:
        # Inicializa o modelo rápido e econômico selecionado no AI Studio
        model = genai.GenerativeModel("gemini-3.5-flash-lite")
        
        # Engenharia de Prompt Estrita para Forçar Resposta em JSON puro
        prompt_sistema = f"""
        Você é um robô de triagem da Controladoria Jurídica do projeto LegalShield.
        Analise a intimação fornecida e extraia o banco réu e o tipo de ato processual.
        
        REGRA ABSOLUTA: Responda APENAS e ESTREITAMENTE um objeto JSON válido.
        Não inclua saudações, explicações, introduções ou aspas de bloco de código (como ```json).
        A sua resposta deve conter exatamente esta estrutura de chaves:
        {{
            "banco": "Nome do Banco Identificado (Ex: Banco X, Banco Y ou Banco Z)",
            "tipo_intimacao": "Classificação curta do ato processual"
        }}

        ---
        TEXTO DA INTIMAÇÃO PARA ANÁLISE:
        "{texto_intimacao}"
        """
        
        # Dispara o texto para o cérebro da Inteligência Artificial
        resposta = model.generate_content(prompt_sistema)
        
        # Limpa possíveis espaços vazios ou quebras de linha antes de retornar
        return resposta.text.strip()

    except Exception as erro:
        return f"❌ Falha na conexão com a IA: {str(erro)}"

# =====================================================================
# BLOCO DE TESTE LOCAL - Executa uma simulação rápida no terminal
# =====================================================================
if __name__ == "__main__":
    print("\n🤖 Iniciando Teste Local do Módulo de IA (Modo JSON)...")
    
    texto_teste = "Fica o Banco X devidamente intimado para, em querendo, apresentar Contestação no prazo legal de 15 dias nos autos da ação revisional de contrato bancário."
    
    resultado = analisar_intimacao_com_ia(texto_teste)
    
    print("\n================ ANSWER FROM GEMINI (JSON) ================")
    print(resultado)
    print("===========================================================\n")
