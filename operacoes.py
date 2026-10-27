import database
from datetime import datetime
import hashlib


def gerar_hash(texto):
    return hashlib.sha256(texto.encode()).hexdigest()

def cadastrar_inspetor(nome, matricula):
    conexao = database.conectar()
    cursor = conexao.cursor()
    # To check the names of the inspectors, open the terminal and view the list..    
    #python
    #import database
    #conexion = database.conectar()
    #cursor = conectar.cursor()
    #cursor.execute("SELECT * FROM inspetores") ou cursor.execute("SELECT nome, matricula_hash FROM inspetores")
    #Result = cursor.fetchall()
    #[print(dict(linha)) for linha in resultado]
    #This should retrieve the names registered in the database. 

    matricula_hash = gerar_hash(matricula)

    cursor.execute("""
        INSERT INTO inspetores(nome, matricula_hash)
        VALUES(?, ?)
        """, (nome, matricula_hash))

    conexao.commit()
    conexao.close()


def hoje():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def registrar_inspecao(tipo_maquina, numero_equipamento, inspetor_manutencao, resultado_final, itens_checklist):
    conexao = database.conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO inspecoes
            (tipo_maquina, numero_equipamento, inspetor_manutencao, data_hora, resultado_final)
        VALUES (?, ?, ?, ?, ?)
    """, (tipo_maquina, numero_equipamento, inspetor_manutencao, hoje(), resultado_final))

    # Get the inspection Id
    id_inspecao = cursor.lastrowid

    # Entered each item from the checklist
    for item in itens_checklist:
        cursor.execute("""
            INSERT INTO itens_inspecao
                (inspecao_id, nome_item, status, observacao)
            VALUES (?, ?, ?, ?)
        """, (id_inspecao, item["nome_item"], item["status"], item["observacao"]))

    conexao.commit()
    conexao.close()

    return id_inspecao



itens_checklist = [
    {"nome_item": "Pneus", "status": "OK", "observacao": ""},
    {"nome_item": "Cabos", "status": "Pendência", "observacao": ""},
    {"nome_item": "Sinalização sonora", "status": "OK", "observacao": ""},
    {"nome_item": "Câmeras", "status": "Pendência", "observacao": ""},
    {"nome_item": "Botões de emergência", "status": "OK", "observacao": ""},
    {"nome_item": "Vidros", "status": "OK", "observacao": ""},
    {"nome_item": "Óleo", "status": "OK", "observacao": ""},
    {"nome_item": "Água", "status": "OK", "observacao": ""},
]



def listar_inspecoes(numero_equipamento=None):
    conexao = database.conectar()
    cursor = conexao.cursor()

    query = "SELECT * FROM inspecoes WHERE 1=1"
    parametros = []

    if numero_equipamento:
        query += " AND numero_equipamento = ?"
        parametros.append(numero_equipamento)

    query += " ORDER BY data_hora DESC"

    cursor.execute(query, parametros)
    resultados = cursor.fetchall()
    conexao.close()
    return resultados



def fazer_login(nome, matricula):
    conexao = database.conectar()
    cursor = conexao.cursor()

    matricula = gerar_hash(matricula)

    cursor.execute("""SELECT * FROM inspetores WHERE nome = ? AND matricula_hash = ? """, (nome, matricula))
    
    resultado = cursor.fetchone()
    conexao.close()
    return resultado




