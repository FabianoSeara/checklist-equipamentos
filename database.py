import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "inspecoes.db")

def conectar():
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    return conexao

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inspecoes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_maquina TEXT NOT NULL,
    numero_equipamento TEXT NOT NULL,
    inspetor_manutencao TEXT NOT NULL,
    data_hora TEXT NOT NULL,
    resultado_final TEXT)
    """)

    conexao.commit()
    conexao.close()


def criar_tabela_itens():
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_inspecao(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        inspecao_id INTEGER NOT NULL,
        nome_item TEXT NOT NULL,
        status TEXT NOT NULL,
        observacao TEXT,
        FOREIGN KEY (inspecao_id) REFERENCES inspecoes (id)
            )
        """)

        conexao.commit()
        conexao.close()


def criar_tabela_inspetores():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inspetores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        matricula_hash TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()