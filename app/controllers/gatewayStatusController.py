# Get Datasources gateway status
# Documentation: https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/get-datasource-status

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
from datetime import datetime

import Manage_Token.index as tkn
import database.postgres.main as database

try:
    # Cria conexao com o banco
    conn = database.PgConnect()

    # Cria cursor para fazer a query
    cur = conn.cursor()

    # Definindo a query
    query = """SELECT
                dataset_name,
                datasource_name,
                datasource_id,
                gateway_name,
                gateway_id
               FROM datasources
               """

    # Aplicando a consulta no banco
    cur.execute(query)

    db_return = cur.fetchall()

    # Encerando o cursor e conexao
    cur.close()
    conn.close()

    connected = True
except Exception as err:
    print(f'gatewayStatusController :: query database => ERROR => {err}')
    connected = False

if connected == True:

    # Definindo API request
    access_list = tkn.Token_Manager()

    token_type = access_list["token_type"]
    token = access_list["access_token"]

    header = { 
            "Authorization": f"{token_type} {token}"
            }

    # Percorendo a lista de retorno do banco e fazendo o request da API
    for datasetName, datasourceName, datasourceId, gatewayName, gatewayId in db_return:

        url = f'https://api.powerbi.com/v1.0/myorg/gateways/{gatewayId}/datasources/{datasourceId}/status'

        response = requests.request("GET", url, headers= header)

        is_active = response.status_code

        if is_active == 400:
            status = 'inativo'
        elif is_active == 200:
            status = 'ativo'
        else:
            stauts = 'undefined'

        inserted_at = datetime.now()

        # Definindo dict para inserir no banco
        insert = {
                "datasetName": f'{datasetName}',
                "datasourceName": f'{datasourceName}',
                "datasourceId": f'{datasourceId}',
                "gatewayId": f'{gatewayId}',
                "gatewayName": f'{gatewayName}',
                "datasourceStatus": f'{status}',
                "insertedAt": f'{inserted_at}'
                }

        print(f'{insert}\n')


