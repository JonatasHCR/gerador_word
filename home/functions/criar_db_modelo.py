import sqlite3
from pathlib import Path
import json

ROOT_DIR = Path(__file__).parent
DB_NAME = 'modelos.sqlite3'
DB_FILE = ROOT_DIR / DB_NAME


def criar_banco():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    # SQL
    cursor.execute(
        f'CREATE TABLE IF NOT EXISTS modelos'
        '('
        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'name TEXT UNIQUE NOT NULL,'
        'variaveis TEXT,'
        'ref_variaveis TEXT'
        ')'
    )
    connection.commit()
    cursor.close()
    connection.close()

def inserir(nome,dados,ref_dados):
    criar_banco()
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    lista_convert_dados = json.dumps(dados)
    lista_convert_ref = json.dumps(ref_dados) 

    cursor.execute('''
    INSERT INTO modelos (name,variaveis,ref_variaveis) VALUES (?,?,?)
''', (nome, lista_convert_dados,lista_convert_ref)
    )
    connection.commit()
    cursor.close()
    connection.close()

def retirar(nome_modelo):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    cursor.execute('SELECT variaveis,ref_variaveis FROM modelos WHERE name = ?',(nome_modelo,))
    resultado = cursor.fetchall()
    for var in resultado:
        variavel = json.loads(var[0])
        ref_variavel = json.loads(var[1])
    return (variavel,ref_variavel)
