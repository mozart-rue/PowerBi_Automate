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
import app.models.refreshHistoryModel as dataModel

# Recuperando dados do banco para usar como parametro
try:
    conn = database.PgConnect()

    # Criando cursor
    cur = conn.cursor()

    # Executando query no banco
    cur.execute("SELECT dataset_id, name FROM datasets")
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

            # Apaga os dados antes de inserir para não duplicar
            total_itens = len(data) -1
            
            # recupera a data do item mais antigo a ser inserido
            delete_from = data[total_itens]["startTime"]

            # transforma para o tipo de dado certo => de string para date
            delete_from = delete_from.replace("T", " ")
            delete_from = delete_from.replace("Z", "")
            delete_from = datetime.strptime(delete_from, '%Y-%m-%d %H:%M:%S.%f')

            dataModel.Delete_RefreshHistory(delete_from, name, datasetId)

            for i in data:

                # Recupera valores para inserir no banco
                refresh_type = i["refreshType"]
                status = i["status"]
                start_time = i["startTime"]
                request_id = i["requestId"]
                history_id = i["id"]

                created_at = datetime.now()
                
                # limpando strings da data de retorno
                start_time = start_time.replace("T", " ")
                start_time = start_time.replace("Z", "")

                # alterando formato de campo de data de string para date
                try:
                    startTime = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
                except:
                    startTime = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

                # end time, tem condição especial, Caso status esteja em progresso, não possui data de finalização
                if i["status"] == "Unknown":
                    endTime = ""
                    total_time = ""
                    status = "InProgress"
                else:
                    end_time = i['endTime']
                    end_time = end_time.replace("T", " ")
                    end_time = end_time.replace("Z", "")

                    # alterando formato de campo de data de string para date
                    try:
                        endTime = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
                    except:
                        endTime = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                    
                    # Calcula tempo total de atualização
                    total_time = endTime - startTime

                # Criando dict para inserir no banco
                insert = {
                        "dataset_name": f"{name}",
                        "dataset_id": f"{datasetId}",
                        "status": f"{status}",
                        "refresh_type": f"{refresh_type}",
                        "start_time": f"{startTime}",
                        "end_time": f"{endTime}",
                        "total_time": f"{total_time}",
                        "request_id": f"{request_id}",
                        "history_id": f"{history_id}",
                        "inserted_at": f"{created_at}"
                        }
                try:
                    dataModel.Insert_RefreshHistory(insert) 
                except Exception as err:
                    print(f'refreshHistoryController :: Insert dados no banco :: ERROR => {err}')

        else:
            print(f"{datasetId} Name: {name} não posui historico de atualizações ainda")

else:
    print('getRefreshHistoryController :: Erro => Não foi possivel executar a query no banco de dados')

