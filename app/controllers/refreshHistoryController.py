# API GET Refresh History
# Documentation: https://docs.microsoft.com/en-us/rest/api/power-bi/datasets/get-refresh-history


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

import database.postgres.main as database
import Manage_Token.index as tkn

# Recuperando dados do banco para usar como parametro
try:
    conn = database.PgConnect()

    # Criando cursor
    cur = conn.cursor()

    # Executando query no banco
    cur.execute("SELECT id, name FROM datasets")
    db_return = cur.fetchall()

    # Encera a conexão com o banco de dados
    cur.close()
    conn.close()
    
    connected = True

except Exception as err:
    print(f'getRefreshHistoryController :: query select na base de dados :: ERRO => {err}')
    connected = False

if connected == True:
   
    # Defininindo parametros para fazer o request da API
    access_list = tkn.Token_Manager()

    token_type = access_list["token_type"]
    token = access_list["access_token"]

    header = {
            "Authorization": f"{token_type} {token}"
            }

    # Percore a lista de itens retornados do DB e faz o request na API
    for datasetId, name in db_return:

        url = f'https://api.powerbi.com/v1.0/myorg/datasets/{datasetId}/refreshes?$top=10'

        response = requests.request("GET", url, headers= header)

        res = response.json()
        data = res["value"]

        # Se a lista não estiver vazia continua para inserir
        if data:
        
            for i in data:

                # Recupera valores para inserir no banco
                refresh_type = i["refreshType"]
                status = i["status"]
                start_time = i["startTime"]
                end_time = i["endTime"]
                request_id = i["requestId"]
                history_id = i["id"]

                created_at = datetime.now()

                # Criando dict para inserir no banco
                insert = {
                        "dataset_name": f"{name}",
                        "dataset_id": f"{datasetId}",
                        "status": f"{status}",
                        "refresh_type": f"{refresh_type}",
                        "start_time": f"{start_time}",
                        "end_time": f"{end_time}",
                        "request_id": f"{request_id}",
                        "history_id": f"{history_id}",
                        "inserted_at": f"{created_at}"
                        }

                print(f'{insert}\n')
                        
        else:
            print(f"{datasetId} Name: {name} não posui historico de atualizações ainda")

else:
    print('getRefreshHistoryController :: Erro => Não foi possivel executar a query no banco de dados')

