# LegalShield Analytics - Pipeline de ETL Jurídico & Triagem Cognitiva com Inteligência Artificial

**Desenvolvido por:** Merecele Nascimento dos Reis  
**Escopo:** Controladoria Jurídica, Engenharia de Dados & IA  
**Status do Projeto:** 100% Concluído e Validado em Ambiente Local  

---

## 📌 1. O Desafio de Negócio
No dia a dia de Controladorias Jurídicas de grande porte e bancas que gerenciam carteiras massivas de contencioso de escala, o volume diário de intimações gera dois riscos críticos: a falha humana no agendamento de prazos fatais e a necessidade de adequação estrita à **LGPD (Lei Geral de Proteção de Dados)** ao lidar com segredos de justiça e dados sensíveis de pessoas físicas.

Para solucionar essas dores de mercado, desenvolvi este ecossistema completo de **Hiperautomação local em Python**, estruturado sob as melhores práticas de Engenharia de Dados e Inteligência Artificial.

---

## 🔄 2. Arquitetura da Solução: O Pipeline de ETL Jurídico
O motor do projeto foi desenhado sob o conceito de **ETL (Extract, Transform, Load)**, garantindo que informações brutas se transformem em Business Intelligence (BI) estratégico:

*   **Extract (Extração / Ingestão):** Ingestão automatizada de dados em lote através da biblioteca *Pandas*, realizando a leitura de relatórios brutos de publicações para centralizar o tráfego em ambiente seguro local.
*   **Transform (Transformação e IA):** A camada mais robusta do código, onde ocorrem o saneamento e a inteligência analítica:
    1. *Saneamento:* Limpeza automática de inconsistências cadastrais e remoção de duplicidades de processos.
    2. *Compliance e LGPD (Privacy by Design):* Utilização de **Expressões Regulares (Regex)** para localizar e mascarar dados sensíveis de pessoas físicas (CPFs e nomes), garantindo anonimização total na origem antes de qualquer tráfego externo.
    3. *Triagem Cognitiva com IA:* Integração via API protegida com o modelo estável **Gemini 3.5 Flash Lite** do Google. Através de Engenharia de Prompt Avançada, a IA realiza a leitura contextual das intimações e entrega o parecer estruturado **estritamente em formato JSON**, identificando o banco réu e a classificação jurídica do ato.
    4. *Regra de Ouro Jurídica (Margem de 48h):* Motor matemático que calcula o prazo fatal do tribunal com base no Código de Processo Civil e gera automaticamente um recuo preventivo de 48 horas úteis, criando uma janela de segurança para revisão técnica das lideranças antes do protocolo.
*   **Load (Carga e Entrega):** A distribuição automatizada dos dados inteligentes ocorre em três pontas:
    1. *Persistência Relacional SQL:* Gravação imediata dos IDs e prazos calculados na tabela oficial `tb_compliance` do Banco de Dados SQLite (`juris_database.db`).
    2. *Geração do Produto Final:* Exportação da planilha de BI, injetando o objeto JSON gerado pela IA diretamente na Coluna H (`triagem_cognitiva_ia`).
    3. *Delivery:* Disparo autônomo por e-mail em segundo plano através da biblioteca `yagmail`, enviando o relatório final higienizado diretamente para a gestão.

---

## 🛠️ 3. Estrutura do Repositório (Arquivos do Projeto)
*   `modulo_compliance.py`: Core do pipeline de ETL, regras de LGPD, cálculos matemáticos e rotina de e-mail.
*   `modulo_ia.py`: Conector com o Gemini 3.5 Flash Lite configurado para respostas estruturadas in JSON.
*   `consulta_banco.py`: Camada de persistência relacional responsável pela inserção dos dados no SQL.
*   `relatorio_banco.py`: Módulo analítico de Business Intelligence que consome a tabela `tb_compliance` e gera métricas estatísticas de produtividade com *Pandas* e *NumPy*.
*   `reset_banco.py`: Utilitário de manutenção para higienização e limpeza de dados históricos de testes.
*   `.gitignore`: Filtro de segurança que impede o upload acidental do cofre de credenciais (`.env`) e do banco físico para a internet.

---

## 🔒 4. Protocolos de Segurança e Governança
*   **Human-in-the-Loop (Humano no Controle):** A IA atua como assistente analítico preditivo. Nenhuma informação entra em produção ou é agendada no sistema final sem passar por uma mesa de validação visual e aprovação com um clique do analista controlador humano.
*   **Isolamento de Credenciais:** Todas as chaves de API e senhas rodam sob variáveis de ambiente ocultas (`.env`), em total conformidade com os padrões corporativos de segurança da informação.
