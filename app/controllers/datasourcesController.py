# API: GET Datasources 
# Documentation: https://docs.microsoft.com/en-us/rest/api/power-bi/datasets/get-datasources

# ----------------------- ADD RAIZ DO PROJETO AO ARQUIVO  ----------------------- #
# Adicionando o path para a Raiz do projeto dinamicamente para fazer a importação de arquivos.py
import sys
import os

def Resolve_Path():
    # Recupera o diretorio atual e separa o ultimo iten
    current_path = os.getcwd() # --> retorna diretorio atual: ex: (main/path/to/folder)
    split_path = os.path.split(current_path) # --> retorna: (main/path/to, folder)
    head, tail = split_path # --> recupera os dois itens um para cada variavel (em ordem)

    # Encontra o path até a raiz do projeto (raiz = InfoCargas)
    while not head.endswith('InfoCargas'):
        split_path = os.path.split(head)
        head, tail = split_path

    return head

path = Resolve_Path()
sys.path.append(os.path.abspath(f"{path}"))
# ---------------------------------------------------------------------------------- #

import requests

import Manage_Token.index as tkn
import database.postgres.main as pgconnection


# Criando conexão com o Postgres
conn = pgconnection.PgConnect()

# definindo o cursor 
cur = conn.cursor()

# Fazendo consulta no postgres
query = 'Select id, name from datasets'

cur.execute(query)

db_return = cur.fetchall()

cur.close()
conn.close()

print(f'Data retrived from db:\n {db_return}')

filter_return = db_return[0]
dataset_id, dataset_name = filter_return

print(f'The dataset {dataset_name} has the id: {dataset_id}')

