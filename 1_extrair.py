# FASE 1 - EXTRAÇÃO DE DADOS

import pandas as pd
from pathlib import Path

from config import (
    PASTA_DADOS,
    ARQUIVOS,
    CSV_SEPARADOR,
    CSV_ENCODING,
    TAMANHO_BLOCO
)

from banco import conectar

# Caminho CSV
PASTA_CSV = PASTA_DADOS / "raw"

# Conexão
print("Conectando ao MySQL...")

conexao = conectar()

print("Conexão realizada!")

# Limpar tabelas RAW antes da carga
def limpar_raw(conexao):
    print("\nLimpando tabelas RAW...")

    tabelas = [
        "raw_viagem",
        "raw_pagamento",
        "raw_passagem",
        "raw_trecho"
    ]

    cursor = conexao.cursor()

    for tabela in tabelas:
        cursor.execute(
            f"TRUNCATE TABLE {tabela}"
        )
        print(f"Tabela limpa: {tabela}")

    conexao.commit()
    cursor.close()

    print("Limpeza RAW concluída!")

# Função de carga RAW
def carregar_csv(nome_arquivo, tabela):
    caminho = PASTA_CSV / nome_arquivo

    print("\nArquivo:")
    print(caminho)

    print("Lendo CSV...")

    df = pd.read_csv(
        caminho,
        sep=CSV_SEPARADOR,
        encoding=CSV_ENCODING,
        dtype=str
    )

    print("Registros encontrados:", len(df))

    # transforma NaN em vazio
    df = df.fillna("")

    colunas = list(df.columns)

    placeholders = ", ".join(
        ["%s"] * len(colunas)
    )

    sql = f"""
        INSERT INTO {tabela}
        VALUES ({placeholders})
    """

    linhas = list(
        df.itertuples(
            index=False,
            name=None
        )
    )

    print("Inserindo no banco...")

    cursor = conexao.cursor()

    for inicio in range(
        0,
        len(linhas),
        TAMANHO_BLOCO
    ):

        lote = linhas[
            inicio:
            inicio + TAMANHO_BLOCO
        ]

        cursor.executemany(
            sql,
            lote
        )

        conexao.commit()

    cursor.close()

    print("Carga concluída:", tabela)

# Execução da extração dos arquivos
for nome, configuracao in ARQUIVOS.items():

    carregar_csv(
        configuracao["csv"],
        configuracao["tabela_raw"]
    )

conexao.close()

print("\nExtração finalizada com sucesso!")