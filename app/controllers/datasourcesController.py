# API: GET Datasources 
# Documentation: https://docs.microsoft.com/en-us/rest/api/power-bi/datasets/get-datasources
# Documentatio 2: https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/get-datasource
# Documentation Gateway details: https://docs.microsoft.com/en-us/rest/api/power-bi/gateways/get-gateway#code-try-0

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
import database.postgres.main as pgconnection
import app.models.datasourceModel as dataModel

try:
    # Criando conexão com o Postgres
    conn = pgconnection.PgConnect()

    # definindo o cursor 
    cur = conn.cursor()

    # Fazendo consulta no postgres
    query = 'Select dataset_id, name from datasets'

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


    # Fazendo o delete antes de prosseguir
    try:
        conn = pgconnection.PgConnect()

        cur = conn.cursor()
        cur.execute("DELETE FROM datasources")
        conn.commit()

        cur.close()
        conn.close()
    except Exception as err:
        print(f"datasouceController :: Deletando base de dados :: ERROR => {err}")

    for datasetId, name in db_return:
        url = f"https://api.powerbi.com/v1.0/myorg/datasets/{datasetId}/datasources"

        datasource = requests.request("GET", url, headers= header )

        values = datasource.json()
        value = values["value"]

        datasourceId = value[0]["datasourceId"]
        gatewayId = value[0]["gatewayId"]
        
        url_gw = f'https://api.powerbi.com/v1.0/myorg/gateways/{gatewayId}/datasources/{datasourceId}'

        datasource_detailed = requests.request("GET", url_gw, headers= header )
        
        # Chamando API que retorna detalhes sobre o gateway
        url_gw_detail = f'https://api.powerbi.com/v1.0/myorg/gateways/{gatewayId}'

        
        gateway_detailed = requests.request("GET", url_gw_detail, headers= header)
        try:
            # Recuperando dados detalhados do gateway
            gw_data = gateway_detailed.json()
        
            gateway_name = gw_data["name"]
            gateway_status = gw_data["gatewayStatus"]
        except:
            gateway_name = "undefined"
            gateway_status = "undefined"

        # Recuperando dados do datasource detailed

        data = datasource_detailed.json()

        datasource_type = data["datasourceType"]
        credential_type = data["credentialType"]
        
        try:
            datasource_name = data["datasourceName"]
        except:
            datasource_name = "undefined"
        
        inserted_at = datetime.now()

        # Definindo dict para inserir no banco
        insert = {
                "dataset_name": f'{name}',
                "dataset_id": f'{datasetId}',
                "datasource_name": f'{datasource_name}',
                "datasource_id": f'{datasourceId}',
                "gateway_id": f'{gatewayId}',
                "gateway_name": f'{gateway_name}',
                "gateway_status": f'{gateway_status}',
                "conn_type": f'{datasource_type}',
                "cred_type": f'{credential_type}',
                "inserted_at": f'{inserted_at}'
                }
        
        # Inserindo no banco
        try:
            dataModel.Insert_Datasources(insert)
        except Exception as err:
            print(f'datasourceController: Insert to database: ERROR :: {err}')

else:
    print('Não foi possivel fazer a consulta no banco de dados')

