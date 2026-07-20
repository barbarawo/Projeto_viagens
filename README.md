# Pipeline de Dados - Viagens a Serviço

## Descrição
Projeto de Análise de Dados desenvolvido utilizando arquitetura Medallion (Bronze, Silver e Gold).
O objetivo é extrair, transformar e analisar dados de viagens a serviço obtidos do Portal da Transparência.

---

## Arquitetura
Fluxo desenvolvido:
Dados CSV
|
v
Bronze
|
v
Silver
|
v
Gold
|
v
Análises

---

## Tecnologias utilizadas
- Python
- Pandas
- SQLAlchemy
- MySQL
- Jupyter Notebook
- Matplotlib

---
## Estrutura do projeto
projeto_viagens/

├── 0_criar_banco.sql
├── 1_extrair.py
├── 2_transformar.py
├── 3_analise.ipynb
├── banco.py
├── config.py
├── requirements.txt
├── README.md

└── dados/

---

## Execução

### 1. Instalar dependências
pip install -r requirements.txt


### 2. Configurar banco
Criar arquivo `.env` com as informações do MySQL.

### 3. Executar extração
python 1_extrair.py

### 4. Executar transformação
python 2_transformar.py

### 5. Executar análises
Abrir:
3_analise.ipynb

---

## Camadas

### Bronze
Dados carregados originalmente do CSV.
Tabela:
bronze_viagem
Quantidade:
341.860 registros

### Silver
Dados tratados:
- conversão de datas;
- tratamento de valores;
- cálculo de dias de viagem;
- cálculo do valor total.
Tabela:
silver_viagem

### Gold
Tabela agregada por órgão:
gold_viagens_orgao
Indicadores:
- quantidade de viagens;
- valor total gasto;
- valor médio por viagem.
Quantidade:
207 órgãos

---

## Autor
Projeto desenvolvido para atividade de Análise de Dados.