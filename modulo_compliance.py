# =====================================================================
# LEGALSHIELD ANALYTICS - MÓDULO COMPLIANCE (PRIVACY BY DESIGN)
# Desenvolvido por: Merecele Nascimento dos Reis
# Objetivo: Sanar deficiências de auditoria de dados e garantir a LGPD
# Evoluções: Integração automática com Banco de Dados SQL e Alertas por E-mail
# Proteção: Credenciais ocultas via Variáveis de Ambiente (.env) e yagmail
# =====================================================================

import os
import pandas as pd
import logging
import sqlite3
import yagmail  # Biblioteca moderna que resolve bloqueios de rede e firewalls
from sklearn.preprocessing import MinMaxScaler
from dotenv import load_dotenv
from datetime import datetime, timedelta
from consulta_banco import salvar_prazos_calculados
from modulo_ia import analisar_intimacao_com_ia

# Carrega as variáveis de ambiente do arquivo oculto .env
load_dotenv()

# 1. MAPEAMENTO DE CAMINHOS SEGUROS (AMBIENTE LOCAL)
pasta_dados = os.path.join(os.path.dirname(__file__), "dados")
caminho_entrada = os.path.join(pasta_dados, "relatorio_bruto.csv")
caminho_saida = os.path.join(pasta_dados, "dados_anonimizados_e_normalizados.csv")
caminho_banco = os.path.join(pasta_dados, "juris_database.db")

# Garantir que a pasta 'dados' existe
os.makedirs(pasta_dados, exist_ok=True)

# 2. CONFIGURAÇÃO DO SISTEMA DE LOGS (Auditoria Automática dentro da pasta dados)
logging.basicConfig(
    filename=os.path.join(pasta_dados, "execucao_robot.log"),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

print("\n🔄 Iniciando o Pipeline de Controladoria Jurídica Avançado e Seguro...\n")
logging.info("Iniciando o Pipeline de Controladoria Jurídica Avançado e Seguro...")

def salvar_no_banco_sql(df):
    """Função responsável por persistir os dados processados em um banco SQL local"""
    try:
        logging.info("Conectando ao banco de dados SQL local...")
        conexao = sqlite3.connect(caminho_banco)
        df.to_sql('tb_compliance', conexao, if_exists='append', index=False)
        conexao.close()
        print("🗄️ Banco de Dados: Registros históricos salvos com sucesso na tabela SQL.")
        logging.info("Dados históricos persistidos com sucesso na tabela 'tb_compliance'.")
    except Exception as e:
        logging.error(f"Falha ao salvar no banco de dados SQL: {str(e)}")
        print("⚠️ Aviso: Não foi possível salvar os dados no Banco SQL.")

def enviar_relatorio_email():
    """Função responsável por disparar o e-mail coletando as credenciais do .env via yagmail"""
    REMETENTE_EMAIL = os.getenv("EMAIL_REMETENTE")
    REMETENTE_SENHA = os.getenv("EMAIL_SENHA")
    DESTINATARIO_EMAIL = os.getenv("EMAIL_DESTINATARIO")
    
    if not REMETENTE_EMAIL or REMETENTE_EMAIL == "seu_email_real@gmail.com":
        logging.warning("Envio de e-mail pulado: Credenciais ausentes ou padrão no arquivo .env.")
        print("📧 E-mail: Rotina pulada (configure o arquivo .env para ativar o envio automático).")
        return

    try:
        logging.info("Iniciando conexão segura e simplificada com o Gmail via yagmail...")
        yag = yagmail.SMTP(REMETENTE_EMAIL, REMETENTE_SENHA)
        
        assunto = "🤖 LEGALSHIELD - Triagem e Compliance de Dados Concluída"
        corpo = """
        Prezada equipe de Controladoria Jurídica,
        
        O robô de conformidade executou o pipeline com sucesso total de ponta a ponta.
        Os dados sensíveis foram anonimizados (LGPD) e as métricas foram devidamente normalizadas.
        A planilha higienizada e pronta para auditoria segue em anexo a este e-mail.
        
        Atenciosamente,
        Robô LegalShield Analytics
        """
        
        yag.send(
            to=DESTINATARIO_EMAIL,
            subject=assunto,
            contents=[corpo, "dados/dados_com_prazos_calculados.csv"]
        )
        print(f"📧 E-mail: Relatório enviado com sucesso para {DESTINATARIO_EMAIL}!")
    except Exception as e:
        print(f"⚠️ Aviso: O envio do e-mail falhou. Motivo real: {str(e)}")

try:
    if not os.path.exists(caminho_entrada):
        print(f"❌ Erro crítico: O arquivo relatorio_bruto.csv não foi encontrado.")
    else:
        df_bruto = pd.read_csv(caminho_entrada)
        df_sanado = df_bruto.drop_duplicates(subset=['numero_processo'], keep='first').copy()
        df_sanado['status_auditoria'] = df_sanado['status_auditoria'].fillna('Corrigido por Robô')
        df_anonimizado = df_sanado.drop(columns=['numero_processo', 'nome_cliente']).copy()
        
        scaler = MinMaxScaler()
        df_anonimizado[['dias_para_prazo', 'valor_causa']] = scaler.fit_transform(df_anonimizado[['dias_para_prazo', 'valor_causa']])
        df_banco = df_anonimizado.copy()

        for coluna in ['dias_para_prazo', 'valor_causa']:
            df_anonimizado[coluna] = df_anonimizado[coluna].apply(lambda x: str(round(x, 4)).replace('.', ','))
        
        df_anonimizado.to_csv(caminho_saida, index=False, sep=';', encoding='utf-8-sig')
        salvar_no_banco_sql(df_banco)
        print("\n🚀 O robô liberou os advogados das tarefas repetitivas de triagem!")

except Exception as e:
    print(f"❌ Falha inesperada: {str(e)}")
# --- INICIANDO CONTAGEM E VOLUMETRIA DE PRAZOS ---
df_analise = pd.read_csv(caminho_saida, sep=';')
print("\n--- INICIANDO CONTAGEM E VOLUMETRIA DE PRAZOS ---")
print(df_analise['tipo_intimacao'].value_counts())

# --- FASE 3: REGRAS DE NEGÓCIO E CALCULO DE PRAZOS COM MARGEM DE SEGURANÇA ---
print("\n--- INICIANDO REGRA DE NEGÓCIO: PRAZOS FATAIS (MARGEM 48H) ---")
data_atual = datetime.now()
df_analise['data_publicacao_simulada'] = data_atual.strftime('%Y-%m-%d %H:%M:%S')
df_analise['dias_para_prazo'] = pd.to_numeric(df_analise['dias_para_prazo'], errors='coerce').fillna(0).astype(int)

datas_fatais_tribunal = []
datas_limite_seguranca = []
respostas_triagem_ia = []

for index, linha in df_analise.iterrows():
    dias_prazo = linha['dias_para_prazo']
    prazo_tribunal = data_atual + timedelta(days=int(dias_prazo))
    prazo_seguranca = prazo_tribunal - timedelta(hours=48)
    
    datas_fatais_tribunal.append(prazo_tribunal.strftime('%Y-%m-%d %H:%M:%S'))
    datas_limite_seguranca.append(prazo_seguranca.strftime('%Y-%m-%d %H:%M:%S'))
    
    # 🤖 FASE 4: Acionando a Inteligência Artificial
    texto_para_ia = linha['tipo_intimacao']
    resultado_ia = analisar_intimacao_com_ia(texto_para_ia)
    print(f"\n🧠 [IA Gemini] Resultado da análise da linha {index}:\n{resultado_ia}")
    respostas_triagem_ia.append(resultado_ia)
    
    # 💾 Gravando no Banco SQL
    salvar_prazos_calculados(id_intimacao=index, prazo_tribunal=prazo_tribunal, prazo_seguranca=prazo_seguranca)

# Injetando as listas de volta na tabela do Pandas
df_analise['prazo_fatal_tribunal'] = datas_fatais_tribunal
df_analise['prazo_limite_controladoria'] = datas_limite_seguranca
df_analise['triagem_cognitiva_ia'] = respostas_triagem_ia

# Salvando a tabela final física na pasta dados
df_analise.to_csv("dados/dados_com_prazos_calculados.csv", sep=';', index=False)
print("\nNovo arquivo gerado com sucesso em: dados/dados_com_prazos_calculados.csv")

# 📧 ACIONANDO O DISPARO DO EMAIL LOGO APÓS A PLANILHA SALVAR COM A COLUNA H
print("\n📬 Acionando a rotina de envio de e-mail...")
enviar_relatorio_email()
