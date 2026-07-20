# FASE 0 - CRIAR BANCO E TABELAS

'''
COMO USAR
-- 1) Abra o MySQL Workbench
-- 2) Conecte ao servidor MySQL
-- 3) Abra uma nova aba SQL
-- 4) Cole todo o conteúdo deste arquivo
-- 5) Execute o script completo
-- 6) Após a criação do banco e das tabelas, executar:
    -- 1_extrair.py
    -- 2_transformar.py
'''

# BANCO DE DADOS
CREATE DATABASE IF NOT EXISTS viagens
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

USE viagens;

#CAMADA RAW -- Dados exatamente como são recebidos
DROP TABLE IF EXISTS raw_viagem;

CREATE TABLE raw_viagem (
    identificador_processo_viagem VARCHAR(255),
    numero_proposta_pcdp VARCHAR(255),
    situacao VARCHAR(255),
    viagem_urgente VARCHAR(255),
    justificativa_urgencia_viagem TEXT,
    codigo_orgao_superior VARCHAR(255),
    nome_orgao_superior VARCHAR(255),
    codigo_orgao_solicitante VARCHAR(255),
    nome_orgao_solicitante VARCHAR(255),
    cpf_viajante VARCHAR(255),
    nome VARCHAR(255),
    cargo VARCHAR(255),
    funcao VARCHAR(255),
    descricao_funcao VARCHAR(255),
    data_inicio VARCHAR(255),
    data_fim VARCHAR(255),
    destinos TEXT,
    motivo TEXT,
    valor_diarias VARCHAR(255),
    valor_passagens VARCHAR(255),
    valor_devolucao VARCHAR(255),
    valor_outros_gastos VARCHAR(255)
);

DROP TABLE IF EXISTS raw_pagamento;

CREATE TABLE raw_pagamento (
    identificador_processo_viagem VARCHAR(255),
    numero_proposta_pcdp VARCHAR(255),
    codigo_orgao_superior VARCHAR(255),
    nome_orgao_superior VARCHAR(255),
    codigo_orgao_pagador VARCHAR(255),
    nome_orgao_pagador VARCHAR(255),
    codigo_unidade_gestora_pagadora VARCHAR(255),
    nome_unidade_gestora_pagadora VARCHAR(255),
    tipo_pagamento VARCHAR(255),
    valor VARCHAR(255)
);

DROP TABLE IF EXISTS raw_passagem;

CREATE TABLE raw_passagem (
    identificador_processo_viagem VARCHAR(255),
    numero_proposta_pcdp VARCHAR(255),
    meio_transporte VARCHAR(255),
    pais_origem_ida VARCHAR(255),
    uf_origem_ida VARCHAR(255),
    cidade_origem_ida VARCHAR(255),
    pais_destino_ida VARCHAR(255),
    uf_destino_ida VARCHAR(255),
    cidade_destino_ida VARCHAR(255),
    pais_origem_volta VARCHAR(255),
    uf_origem_volta VARCHAR(255),
    cidade_origem_volta VARCHAR(255),
    pais_destino_volta VARCHAR(255),
    uf_destino_volta VARCHAR(255),
    cidade_destino_volta VARCHAR(255),
    valor_passagem VARCHAR(255),
    taxa_servico VARCHAR(255),
    data_emissao_compra VARCHAR(255),
    hora_emissao_compra VARCHAR(255)
);

DROP TABLE IF EXISTS raw_trecho;

CREATE TABLE raw_trecho (
    identificador_processo_viagem VARCHAR(255),
    numero_proposta_pcdp VARCHAR(255),
    sequencia_trecho VARCHAR(255),
    origem_data VARCHAR(255),
    origem_pais VARCHAR(255),
    origem_uf VARCHAR(255),
    origem_cidade VARCHAR(255),
    destino_data VARCHAR(255),
    destino_pais VARCHAR(255),
    destino_uf VARCHAR(255),
    destino_cidade VARCHAR(255),
    meio_transporte VARCHAR(255),
    numero_diarias VARCHAR(255),
    missao VARCHAR(255)
);

# CAMADA SILVER -- Dados tratados
DROP TABLE IF EXISTS silver_viagem;

CREATE TABLE silver_viagem (
    identificador_processo_viagem VARCHAR(30) PRIMARY KEY NOT NULL,
    numero_proposta_pcdp VARCHAR(50),
    situacao VARCHAR(50),
    viagem_urgente VARCHAR(10),
    justificativa_urgencia_viagem TEXT,
    codigo_orgao_superior INT,
    nome_orgao_superior VARCHAR(255),
    codigo_orgao_solicitante INT,
    nome_orgao_solicitante VARCHAR(255),
    cpf_viajante VARCHAR(20),
    nome VARCHAR(255),
    cargo VARCHAR(255),
    funcao VARCHAR(100),
    descricao_funcao VARCHAR(255),
    data_inicio DATE,
    data_fim DATE,
    destinos TEXT,
    motivo TEXT,
    valor_diarias DECIMAL(12,2),
    valor_passagens DECIMAL(12,2),
    valor_devolucao DECIMAL(12,2),
    valor_outros_gastos DECIMAL(12,2),
    dias_viagem INT,
    valor_total DECIMAL(12,2)

    CONSTRAINT chk_silver_viagem_valor_total
    CHECK (valor_total >= 0)  
);

DROP TABLE IF EXISTS silver_pagamento;

CREATE TABLE silver_pagamento (
    id INT PRIMARY KEY AUTO_INCREMENT,
    identificador_processo_viagem VARCHAR(30) NOT NULL,
    numero_proposta_pcdp VARCHAR(50),
    codigo_orgao_superior BIGINT,
    nome_orgao_superior VARCHAR(255),
    codigo_orgao_pagador BIGINT,
    nome_orgao_pagador VARCHAR(255),
    codigo_unidade_gestora_pagadora BIGINT,
    nome_unidade_gestora_pagadora VARCHAR(255),
    tipo_pagamento VARCHAR(100),
    valor DECIMAL(12,2),
    
    CONSTRAINT fk_pagamento_viagem
    FOREIGN KEY (
        identificador_processo_viagem
    )
    REFERENCES silver_viagem(
        identificador_processo_viagem
    ),
    CONSTRAINT chk_silver_pagamento_valor
    CHECK (valor >= 0)
);

DROP TABLE IF EXISTS silver_passagem;

CREATE TABLE silver_passagem (
    id INT PRIMARY KEY AUTO_INCREMENT,
    identificador_processo_viagem VARCHAR(30) NOT NULL,
    numero_proposta_pcdp VARCHAR(50),
    meio_transporte VARCHAR(100),
    pais_origem_ida VARCHAR(100),
    uf_origem_ida VARCHAR(100),
    cidade_origem_ida VARCHAR(100),
    pais_destino_ida VARCHAR(100),
    uf_destino_ida VARCHAR(100),
    cidade_destino_ida VARCHAR(100),
    pais_origem_volta VARCHAR(100),
    uf_origem_volta VARCHAR(100),
    cidade_origem_volta VARCHAR(100),
    pais_destino_volta VARCHAR(100),
    uf_destino_volta VARCHAR(100),
    cidade_destino_volta VARCHAR(100),
    valor_passagem DECIMAL(12,2),
    taxa_servico DECIMAL(12,2),
    data_emissao_compra DATE,
    hora_emissao_compra TIME,

    CONSTRAINT fk_passagem_viagem
    FOREIGN KEY (
        identificador_processo_viagem
    )
    REFERENCES silver_viagem(
        identificador_processo_viagem
    ),
    CONSTRAINT chk_silver_passagem_valor
    CHECK (valor_passagem >= 0)
);

DROP TABLE IF EXISTS silver_trecho;

CREATE TABLE silver_trecho (
    id INT PRIMARY KEY AUTO_INCREMENT,
    identificador_processo_viagem VARCHAR(30) NOT NULL,
    numero_proposta_pcdp VARCHAR(50),
    sequencia_trecho INT,
    origem_data DATE,
    origem_pais VARCHAR(100),
    origem_uf VARCHAR(100),
    origem_cidade VARCHAR(100),
    destino_data DATE,
    destino_pais VARCHAR(100),
    destino_uf VARCHAR(100),
    destino_cidade VARCHAR(100),
    meio_transporte VARCHAR(100),
    numero_diarias INT,
    missao VARCHAR(50),
    
    CONSTRAINT fk_trecho_viagem
    FOREIGN KEY (
        identificador_processo_viagem
    )
    REFERENCES silver_viagem(
        identificador_processo_viagem
    ),
    CONSTRAINT chk_silver_trecho_diarias
    CHECK (numero_diarias >= 0)
);

# CAMADA GOLD -- Análise
DROP TABLE IF EXISTS gold_indicadores_viagem;

CREATE TABLE gold_indicadores_viagem (
    nome_orgao_solicitante VARCHAR(255),
    quantidade_viagens INT,
    custo_total_viagens DECIMAL(14,2),
    quantidade_pagamentos INT,
    total_pago DECIMAL(14,2),
    quantidade_trechos INT,
    duracao_media DECIMAL(10,2)
);

DROP VIEW IF EXISTS vw_gold_indicadores_viagem;

CREATE VIEW vw_gold_indicadores_viagem AS
SELECT *
FROM gold_indicadores_viagem;