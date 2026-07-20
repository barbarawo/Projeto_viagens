# FASE 2 - TRANSFORMAR DADOS

import pandas as pd
from banco import criar_engine, conectar

# CONEXÃO MYSQL
print("Conectando ao MySQL...")

conexao = conectar()
engine = criar_engine()

print("Conexão realizada!")

# LEITURA RAW
def ler_raw(tabela):
    print(f"\nLendo RAW: {tabela}")

    df = pd.read_sql(
        f"SELECT * FROM {tabela}",
        engine
    )

    print("Registros encontrados:", len(df))

    return df

# FUNÇÃO PARA GRAVAR NA CAMADA SILVER
def gravar_silver(df, tabela):
    print(f"Gravando SILVER: {tabela}")

    # Corrige valores decimais brasileiros
    colunas_decimal = [
        "valor_passagem",
        "taxa_servico",
        "numero_diarias"
    ]

    for coluna in colunas_decimal:
        if coluna in df.columns:
            df[coluna] = (
                df[coluna]
                .astype(str)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
            )

            df[coluna] = pd.to_numeric(
                df[coluna],
                errors="coerce"
            )

    # Corrige todas as datas
    colunas_data = [
        "data_emissao_compra",
        "origem_data",
        "destino_data"
    ]

    for coluna in colunas_data:
        if coluna in df.columns:
            df[coluna] = pd.to_datetime(
                df[coluna],
                format="%d/%m/%Y",
                errors="coerce"
            )

    # Converte datas para formato aceito pelo MySQL
    for coluna in colunas_data:
        if coluna in df.columns:
            df[coluna] = (
                df[coluna]
                .dt.strftime("%Y-%m-%d")
            )

    df.to_sql(
        tabela,
        con=engine,
        if_exists="append",
        index=False,
        chunksize=5000
    )

    print(f"{tabela} gravada com sucesso!")

# LIMPEZA SILVER
def limpar_silver():
    print("\nLimpando camada Silver...")

    cursor = conexao.cursor()

    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

    cursor.execute("TRUNCATE TABLE silver_trecho")

    cursor.execute("TRUNCATE TABLE silver_passagem")

    cursor.execute("TRUNCATE TABLE silver_pagamento")

    cursor.execute("TRUNCATE TABLE silver_viagem")

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

    conexao.commit()

    cursor.close()

    print("Camada Silver limpa!")

# SILVER - VIAGEM
def transformar_viagem():
    print("\nTransformando raw_viagem...")

    df = ler_raw("raw_viagem")

    print("Tratando dados de viagem...")

     # Identificador como TEXTO - preserva zeros à esquerda
    df["identificador_processo_viagem"] = (
        df["identificador_processo_viagem"]
        .astype(str)
        .str.zfill(19)
    )

    # Conversão de datas
    df["data_inicio"] = pd.to_datetime(
        df["data_inicio"],
        dayfirst=True,
        errors="coerce"
    )

    df["data_fim"] = pd.to_datetime(
        df["data_fim"],
        dayfirst=True,
        errors="coerce"
    )

    # Códigos numéricos
    colunas_codigo = [
        "codigo_orgao_superior",
        "codigo_orgao_solicitante"
    ]

    for coluna in colunas_codigo:
        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

    # Valores financeiros
    colunas_valor = [
        "valor_diarias",
        "valor_passagens",
        "valor_devolucao",
        "valor_outros_gastos"
    ]

    for coluna in colunas_valor:
        df[coluna] = (
            df[coluna]
            .astype(str)
            .str.replace(",", ".", regex=False)
        )

        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

    # Duração
    df["duracao_dias"] = (
        df["data_fim"]
        -
        df["data_inicio"]
    ).dt.days

    # Valor total
    df["valor_total"] = (
        df["valor_diarias"].fillna(0)
        +
        df["valor_passagens"].fillna(0)
        +
        df["valor_devolucao"].fillna(0)
        +
        df["valor_outros_gastos"].fillna(0)

    )

    gravar_silver(
        df,
        "silver_viagem"
    )

    print(
        "silver_viagem:",
        len(df),
        "registros"
    )

# SILVER - PAGAMENTO
def transformar_pagamento():
    print("\nTransformando raw_pagamento...")

    df = ler_raw("raw_pagamento")

    print("Tratando pagamentos...")

     # Identificador como TEXTO
    df["identificador_processo_viagem"] = (
        df["identificador_processo_viagem"]
        .astype(str)
        .str.zfill(19)
    )

    # Códigos numéricos
    colunas_codigo = [
        "codigo_orgao_superior",
        "codigo_orgao_pagador",
        "codigo_unidade_gestora_pagadora"
    ]

    for coluna in colunas_codigo:

        df[coluna] = (
            df[coluna]
            .replace("", None)
        )

        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

    # Valor
    df["valor"] = (
        df["valor"]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )

    df["valor"] = pd.to_numeric(
        df["valor"],
        errors="coerce"
    )

    # remove sem vínculo
    df = df[
        df["identificador_processo_viagem"]
        .notna()
    ]

    gravar_silver(
        df,
        "silver_pagamento"
    )

    print(
        "silver_pagamento:",
        len(df),
        "registros"
    )

# SILVER - PASSAGEM
def transformar_passagem():
    print("\nTransformando raw_passagem...")

    df = ler_raw("raw_passagem")

    print("Tratando passagens...")

    df["identificador_processo_viagem"] = (
        df["identificador_processo_viagem"]
        .astype(str)
        .str.zfill(19)
    )

# Valores monetários
    colunas_valor = [
        "valor_passagem",
        "taxa_servico"
    ]

    for coluna in colunas_valor:
        df[coluna] = (
            df[coluna]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )

        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

    # Datas
    df["data_emissao_compra"] = pd.to_datetime(
        df["data_emissao_compra"],
        dayfirst=True,
        errors="coerce"
    )

    # Hora
    df["hora_emissao_compra"] = (
        df["hora_emissao_compra"]
        .astype(str)
    )

    # Remove registros sem viagem
    df = df[
        df["identificador_processo_viagem"].notna()
    ]

    print(
        "Passagens tratadas:",
        len(df)
    )

    gravar_silver(
        df,
        "silver_passagem"
    )

    print(
        "silver_passagem:",
        len(df),
        "registros"
    )

# SILVER - TRECHO
def transformar_trecho():
    print("\nTransformando raw_trecho...")

    df = ler_raw("raw_trecho")

    print("Tratando trechos...")

    df["identificador_processo_viagem"] = (
        df["identificador_processo_viagem"]
        .astype(str)
        .str.zfill(19)
    )

    gravar_silver(
        df,
        "silver_trecho"
    )

    print(
        "silver_trecho:",
        len(df),
        "registros"
    )

# EXECUÇÃO
limpar_silver()

transformar_viagem()

transformar_pagamento()

transformar_passagem()

transformar_trecho()

print("\nTransformação finalizada com sucesso!")

conexao.close()

print("Conexão encerrada.")