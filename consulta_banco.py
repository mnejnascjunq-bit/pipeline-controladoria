# =====================================================================
# LEGALSHIELD ANALYTICS - MÓDULO DE CONSULTA SQL (HISTÓRICO)
# Desenvolvido por: Merecele Nascimento dos Reis
# Objetivo: Conectar no Banco SQL e extrair relatórios históricos
# =====================================================================

import os
import sqlite3
import pandas as pd

# 1. MAPEAMENTO DO CAMINHO DO BANCO DE DADOS
pasta_dados = os.path.join(os.path.dirname(__file__), "dados")
caminho_banco = os.path.join(pasta_dados, "juris_database.db")

print("\n🔍 Conectando ao Banco de Dados SQL...")

try:
    # 2. ABRIR CONEXÃO COM O BANCO JURIS_DATABASE.DB
    conexao = sqlite3.connect(caminho_banco)
    
    # 3. COMANDO SQL PARA TRAZER TUDO DA TABELA DE COMPLIANCE
    # 'SELECT * FROM tb_compliance' significa: 'Selecione tudo da tabela'
    comando_sql = "SELECT * FROM tb_compliance"
    
    # 4. CARREGAR OS DADOS DO BANCO DIRETO NO PANDAS
    df_historico = pd.read_sql_query(comando_sql, conexao)
    
    # Fechar a conexão de forma segura
    conexao.close()
    
    print("📊 Histórico extraído com sucesso do Banco SQL!\n")
    print("=======================================================================")
    print(f"📈 TOTAL DE REGISTROS ACUMULADOS NO BANCO: {len(df_historico)}")
    print("=======================================================================\n")
    
    # Exibe a tabela completa acumulada direto na tela do seu terminal
    print(df_historico)
    print("\n=======================================================================")

except Exception as e:
    print(f"❌ Erro ao consultar o Banco de Dados: {str(e)}")


# =====================================================================
# 5. FUNÇÃO PARA SALVAR OS PRAZOS CALCULADOS DE VOLTA NO BANCO
# =====================================================================
def salvar_prazos_calculados(id_intimacao, prazo_tribunal, prazo_seguranca):
    """
    Pega os prazos calculados no modulo_compliance.py (usando Pandas/NumPy)
    e grava diretamente na tabela tb_compliance do banco relacional.
    """
    try:
        # Abre a conexão usando o mesmo caminho mapeado acima
        conexao = sqlite3.connect(caminho_banco)
        cursor = conexao.cursor()
        
        # Comando SQL adaptado para as colunas reais existentes na tabela do banco
        comando_sql = """
            UPDATE tb_compliance 
            SET status_auditoria = ?
            WHERE ROWID = ?
        """
        
        # Juntando o status original com o prazo de segurança calculado
        prazo_formatado = prazo_seguranca.strftime('%d/%m/%Y %H:%M') if hasattr(prazo_seguranca, 'strftime') else str(prazo_seguranca)
        status_combinado = f"Auditado | Margem: {prazo_formatado}"
        
        # Executa a gravação de forma segura relacionando com a linha (ROWID)
        cursor.execute(comando_sql, (status_combinado, id_intimacao + 1))
        
        # Confirma a gravação de forma definitiva (Commit)
        conexao.commit()
        conexao.close()
        print(f"💾 [Sucesso] Prazos da intimação ID {id_intimacao} gravados com segurança no Banco SQL!")
        
    except Exception as erro:
        print(f"❌ Erro ao gravar prazos no Banco de Dados: {str(erro)}")
