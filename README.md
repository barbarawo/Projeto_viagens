# Pipeline de Dados - Viagens a Serviço

## 📑 Contextualização do mini-projeto
<p align="justify">Trata-se de projeto desenvolvido com o objetivo analisar dados  utilizando arquitetura Medallion (Bronze, Silver e Gold).
  
<p align="justify">O objetivo é extrair, transformar e analisar dados de viagens à serviço obtidos do Portal da Transparência.

<p align="justify">O projeto foi executado utilizando a IDE Visual Studio Code (VsCode) e contém comentários explicativos ao longo do código-fonte.

  ---

## 📐 Arquitetura
Fluxo desenvolvido:
Dados CSV
|
Bronze
|
Silver
|
Gold
|
Análises

---

## 💻 Tecnologias utilizadas
- Python
- Pandas
- SQLAlchemy
- MySQL
- Jupyter Notebook
- Matplotlib

---
## 📌 Estrutura do projeto
```
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
```

---

## ▶️ Execução

### 1. Instalar dependências
Instale as bibliotecas necessárias para execução do projeto:
pip install -r requirements.txt

### 2. Crie o banco de dados
Executar o script '0_criar_banco.sql'.

### 3. Configurar banco
Criar arquivo `.env` com as informações do MySQL.

### 4. Executar extração
python 1_extrair.py

### 5. Executar transformação
python 2_transformar.py

### 6. Executar análises
Executar o script: '3_analise.ipynb'.

---

## 🎯 Camadas
O projeto utiliza arquitetura de dados em camadas, seguindo o modelo Medallion.

### Bronze
Dados carregados originalmente do CSV.

Tabelas:

    raw_viagem
    
    raw_pagamento
    
    raw_passagem
    
    raw_trecho
  
Quantidade:
    341.860 registros

### Silver
Dados tratados e padronizados para utilização analítica.

Tabelas:

    silver_viagem
    
    silver_pagamento
    
    silver_passagem
    
    silver_trecho

### Gold
Camada direcionada para análise dos dados.

Tabela:

    gold_indicadores_viagem

---

##👥 Autor
_Mini-Projeto elaborado como atividade avaliativa do Curso de Análise de Dados com Python oferecido pela SCTEC em parceria com o SENAI._

Jun/2026.
