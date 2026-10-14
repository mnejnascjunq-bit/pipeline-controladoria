# =====================================================================
# LEGALSHIELD ANALYTICS - MÓDULO DE ANALYTICS E RELATÓRIOS (FASE 5)
# Desenvolvido por: Merecele Nascimento dos Reis
# Objetivo: Conectar ao Banco SQL, extrair o histórico e gerar métricas de BI
# Proteção: Processamento local e seguro dos dados acumulados da controladoria
# =====================================================================

import os
import sqlite3
import pandas as pd
import numpy as np

# 1. MAPEAMENTO DO CAMINHO DO BANCO DE DADOS
pasta_dados = os.path.join(os.path.dirname(__file__), "dados")
caminho_banco = os.path.join(pasta_dados, "juris_database.db")

def gerar_relatorio_executivo_banco():
    """
    Conecta ao Banco SQLite local, extrai os registros históricos da tabela 
    tb_compliance e consolida as métricas usando Pandas e NumPy.
    """
    if not os.path.exists(caminho_banco):
        print(f"❌ Erro: O arquivo de banco de dados '{caminho_banco}' não foi localizado!")
        return

    print("\n🔍 Conectando de forma segura ao Banco de Dados SQL...")
    
    try:
        # 2. ABRIR CONEXÃO COM O BANCO JURIS_DATABASE.DB
        conexao = sqlite3.connect(caminho_banco)
        
        # Comando SQL para puxar o histórico da tabela oficial
        comando_sql = "SELECT * FROM tb_compliance"
        
        # 3. EXTRAÇÃO DE LOGS COM PANDAS (FASE 5.1)
        df_historico = pd.read_sql_query(comando_sql, conexao)
        
        # Fechar a conexão de forma limpa e segura
        conexao.close()
        
        total_registros = len(df_historico)
        
        print("📊 Histórico extraído com sucesso do Banco SQL!")
        print("=======================================================================")
        print(f"📈 TOTAL DE REGISTROS ACUMULADOS NO BANCO DE DADOS: {total_registros}")
        print("=======================================================================\n")
        
        if total_registros == 0:
            print("⚠️ O banco de dados está ativo, mas não possui nenhuma linha gravada ainda.")
            return

        # 4. TRATAMENTO E HIGIENIZAÇÃO DE DADOS (FASE 5.2)
        # Substitui vírgulas por pontos nas colunas numéricas que vieram formatadas regionalmente
        if 'dias_para_prazo' in df_historico.columns:
            df_historico['dias_para_prazo_num'] = df_historico['dias_para_prazo'].astype(str).str.replace(',', '.')
            df_historico['dias_para_prazo_num'] = pd.to_numeric(df_historico['dias_para_prazo_num'], errors='coerce').fillna(0)
            
        if 'valor_causa' in df_historico.columns:
            df_historico['valor_causa_num'] = df_historico['valor_causa'].astype(str).str.replace(',', '.')
            df_historico['valor_causa_num'] = pd.to_numeric(df_historico['valor_causa_num'], errors='coerce').fillna(0)

        # 5. CONSOLIDAÇÃO DE MÉTRICAS OPERACIONAIS E BI (FASE 5.3)
        print("--- DASHBOARD EXECUTIVO DE PRODUTIVIDADE JURÍDICA ---")
        
        # Métrica A: Carga de Trabalho e Volumetria por Status do Robô
        print("\n[Métrica] Volumetria consolidada por Status de Processamento:")
        print(df_historico['status_auditoria'].value_counts())
        
        # Métrica B: Tratamento Estatístico com NumPy para Média Geral de Dias de Prazos
        if 'dias_para_prazo_num' in df_historico.columns:
            # Usando NumPy para calcular a média ignorando distorções
            media_dias_normalizados = np.mean(df_historico['dias_para_prazo_num'])
            print(f"\n[NumPy] Média Matemática dos Prazos Normalizados: {media_dias_normalizados:.4f}")
            
        # Métrica C: Valor Médio das Causas Higienizadas na Controladoria
        if 'valor_causa_num' in df_historico.columns:
            media_valor_normalizado = np.mean(df_historico['valor_causa_num'])
            print(f"[NumPy] Valor Médio das Causas Normalizadas (Escala IA): {media_valor_normalizado:.4f}")

        print("\n=======================================================================")
        print("🎉 Relatório analítico de Business Intelligence gerado com absoluto sucesso!")
        print("=======================================================================\n")

    except Exception as e:
        print(f"❌ Falha crítica ao extrair dados do Banco SQL: {str(e)}")

# Bloco que permite rodar o arquivo diretamente
if __name__ == "__main__":
    gerar_relatorio_executivo_banco()
