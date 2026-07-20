# CONEXÃO E OPERAÇÕES BÁSICAS DO MYSQL

import mysql.connector
from mysql.connector import Error

from sqlalchemy import create_engine

from config import MYSQL_CONFIG

# Abre uma conexao com o MySQL e a retorna. Em caso de falha, lanca um erro.
def conectar():
    try:
        return mysql.connector.connect(**MYSQL_CONFIG)

    except Error as erro:
        raise RuntimeError(
            f"Erro ao conectar no MySQL: {erro}"
        )

# Engine SQLAlchemy.
def criar_engine():
    return create_engine(
        f"mysql+mysqlconnector://"
        f"{MYSQL_CONFIG['user']}:"
        f"{MYSQL_CONFIG['password']}@"
        f"{MYSQL_CONFIG['host']}:"
        f"{MYSQL_CONFIG['port']}/"
        f"{MYSQL_CONFIG['database']}"
    )

# Executa um comando SQL simples
def executar(conexao, sql):
    cursor = conexao.cursor()
    cursor.execute(sql)
    conexao.commit()
    cursor.close()

# Insere varias linhas de uma vez.
def inserir_em_lote(conexao, sql_insert, linhas):
    if not linhas:
        return

    cursor = conexao.cursor()
    cursor.executemany(sql_insert, linhas)
    conexao.commit()
    cursor.close()

# Teste de conexão
if __name__ == "__main__":
    try:
        conexao = conectar()
        print("Conexão realizada com sucesso!")
        conexao.close()

    except Exception as erro:
        print("Erro na conexão:")
        print(erro)