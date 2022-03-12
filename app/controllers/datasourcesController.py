# API: GET Datasources 
# Documentation: https://docs.microsoft.com/en-us/rest/api/power-bi/datasets/get-datasources
# Documentatio 2: https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/get-datasource

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


try:
    # Criando conexão com o Postgres
    conn = pgconnection.PgConnect()

    # definindo o cursor 
    cur = conn.cursor()

    # Fazendo consulta no postgres
    query = 'Select id, name from datasets'

    cur.execute(query)

    db_return = cur.fetchall()

    # Fechando o cursor e conexão 
    cur.close()
    conn.close()

    connected = True
except Exception as error: 
    print(f'datasetsController : PG Connection: ERROR :: {error}')
    connected = False



# Se a teve resultado do banco de dados continua para consumir as API's
if connected == True:
    
    # Definindo parametros para consumir as API's
    access_list = tkn.Token_Manager()

    token_type = access_list["token_type"]
    token = access_list["access_token"]
    
    header = {
            "Authorization": f"{token_type} {token}"
            }

    datasources_dict = {}

    total_itens = len(db_return)

    for datasetId, name in db_return:
        url = f"https://api.powerbi.com/v1.0/myorg/datasets/{datasetId}/datasources"

        datasource = requests.request("GET", url, headers= header )

        values = datasource.json()
        value = values["value"]

        datasourceId = value[0]["datasourceId"]
        gatewayId = value[0]["gatewayId"]
        
        url_gw = f'https://api.powerbi.com/v1.0/myorg/gateways/{gatewayId}/datasources/{datasourceId}'

        datasource_detailed = requests.request("GET", url_gw, headers= header )

        # Recuperando dados do datasource detailed

        data = datasource_detailed.json()

        datasource_type = data["datasourceType"]
        credential_type = data["credentialType"]
        
        try:
            datasource_name = data["datasourceName"]
        except:
            datasource_name = "undefined"
        
        print(f"""
                    dataset_name: {name},
                    dataset_id: {datasetId},
                    datasource_name: {datasource_name},
                    conn_type: {datasource_type},
                    cred_type: {credential_type},
                    gateway_id: {gatewayId},
                    datasource_id: {datasourceId}
                \n""")


